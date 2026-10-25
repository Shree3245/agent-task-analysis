import re

from agent_task_analysis.privacy import IDENTITY_HASH, SafeError, label, task_digest
from agent_task_analysis.storage import connect, load, require_current

DEFAULT_RULES = [
    {"type": "code", "tool_pattern": r"shell|bash|python|edit|patch|file|terminal"},
    {"type": "research", "tool_pattern": r"search|browse|fetch|web"},
    {"type": "email", "tool_pattern": r"email|mail"},
    {"type": "calendar", "tool_pattern": r"calendar|schedule"},
]


def classify_task(task, rules=None):
    if task.task_type != "unknown":
        return task.task_type
    names = [c.tool_name for c in task.calls if c.tool_name]
    for rule in DEFAULT_RULES if rules is None else rules:
        if set(rule) - {"type", "tool_pattern", "min_calls", "max_calls", "min_output_input_ratio"}:
            raise SafeError("invalid_classification_rule")
        if not rule.get("min_calls", 0) <= task.n_calls <= rule.get("max_calls", float("inf")):
            continue
        if "tool_pattern" in rule and not any(
            re.search(rule["tool_pattern"], name, re.I) for name in names
        ):
            continue
        if "min_output_input_ratio" in rule:
            inp = sum(c.input_tokens or 0 for c in task.calls)
            out = sum(c.output_tokens or 0 for c in task.calls)
            if not inp or out / inp < rule["min_output_input_ratio"]:
                continue
        task.task_type = label(rule["type"])
        break
    return task.task_type


def apply_map(db, config):
    if not isinstance(config, dict) or set(config) - {"tasks", "types", "rules"}:
        raise SafeError("invalid_type_mapping")
    count = 0
    # Overrides name source IDs ("otel:trace-001"); stored IDs are their keyed digest.
    overrides = {k if IDENTITY_HASH.fullmatch(str(k)) else task_digest(k): v
                 for k, v in config.get("tasks", {}).items()}
    with connect(db) as conn:
        require_current(conn)
        tasks = load(conn)
        conn.execute("BEGIN TRANSACTION")
        try:
            for task in tasks:
                before = task.task_type
                direct = overrides.get(task.task_id)
                if direct is not None:
                    task.task_type = label(direct)
                elif before in config.get("types", {}):
                    task.task_type = label(config["types"][before])
                elif before == "unknown":
                    classify_task(task, config.get("rules"))
                if before != task.task_type:
                    conn.execute(
                        "UPDATE tasks SET task_type=? WHERE task_id=?",
                        [task.task_type, task.task_id],
                    )
                    count += 1
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
    return count

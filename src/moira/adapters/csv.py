from moira.adapters.base import model_call, tool_call
from moira.privacy import SafeError

ALLOWED = {
    "task_id",
    "task_type",
    "provider",
    "model",
    "ts_start",
    "ts_end",
    "outcome",
    "capped",
    "cap_reason",
    "recorded_cost",
    "tool_name",
    "tool_args",
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_tokens",
}


def extract(row, ctx, fallback):
    columns = ctx.options.get("columns", {})
    if not columns or set(columns) - ALLOWED:
        raise SafeError("invalid_csv_columns")
    values = {}
    for canonical, column in columns.items():
        if column in row:
            values[canonical] = row[column] if row[column] != "" else None
            # Record canonical names only: configured column names may be sensitive.
            ctx.fields.add("csv." + canonical)
    task = ctx.task(
        values.get("task_id"),
        fallback,
        values.get("task_type"),
        outcome=values.get("outcome"),
        capped=values.get("capped"),
        reason=values.get("cap_reason"),
    )
    call = model_call(
        ctx,
        task,
        {},
        model=values.get("model"),
        provider=values.get("provider"),
        usage=values,
        recorded=values.get("recorded_cost"),
        start=values.get("ts_start"),
        end=values.get("ts_end"),
    )
    if values.get("tool_name"):
        tool_call(task, values["tool_name"], values.get("tool_args"), parent=call.call_idx)
    yield task

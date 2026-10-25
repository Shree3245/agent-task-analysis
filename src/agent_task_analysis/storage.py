import json
from pathlib import Path

import duckdb
import pyarrow as pa

from agent_task_analysis.privacy import IDENTITY_HASH, SafeError, key_id, task_digest
from agent_task_analysis.schema import Call, Task

SCHEMA_VERSION = 4
CALL_SQL = """CREATE TABLE IF NOT EXISTS calls (
 task_id VARCHAR NOT NULL, call_idx BIGINT NOT NULL,
 ts_start VARCHAR, ts_end VARCHAR, provider VARCHAR, model VARCHAR,
 input_tokens BIGINT, cached_input_tokens BIGINT, cache_write_input_tokens BIGINT,
 output_tokens BIGINT, reasoning_tokens BIGINT, tool_name VARCHAR, tool_args_hash VARCHAR,
 recorded_cost DOUBLE, capped BOOLEAN, event_kind VARCHAR, parent_call_idx BIGINT,
 PRIMARY KEY(task_id, call_idx))"""
TASK_SQL = """CREATE TABLE IF NOT EXISTS tasks (
 task_id VARCHAR PRIMARY KEY, task_type VARCHAR, source VARCHAR, started_at VARCHAR,
 ended_at VARCHAR, n_calls BIGINT, outcome VARCHAR, capped BOOLEAN, cap_reason VARCHAR,
 task_group VARCHAR)"""
# Version 1 databases predate task_group; it is added as an empty column on write.
MIGRATIONS = ["ALTER TABLE tasks ADD COLUMN IF NOT EXISTS task_group VARCHAR"]


def connect(path, read_only=False):
    path = Path(path)
    if read_only and not path.exists():
        raise SafeError("database_not_found_run_ingest_first")
    if not read_only:
        path.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(
        str(path),
        read_only=read_only,
        config={
            "enable_external_access": "false",
            "autoinstall_known_extensions": "false",
            "autoload_known_extensions": "false",
        },
    )
    if not read_only:
        conn.execute(TASK_SQL)
        conn.execute(CALL_SQL)
        for sql in MIGRATIONS:
            conn.execute(sql)
    return conn


def manifest(conn):
    row = conn.execute("SELECT comment FROM duckdb_tables() WHERE table_name='tasks'").fetchone()
    return (
        json.loads(row[0]) if row and row[0] else {"schema_version": SCHEMA_VERSION, "imports": []}
    )


def require_current(conn):
    """Refuse writes that would mix raw IDs, or digests keyed by another install."""
    sql = "SELECT count(*) FROM tasks WHERE NOT regexp_full_match(task_id, '[0-9a-f]{64}')"
    if conn.execute(sql).fetchone()[0]:
        raise SafeError("database_has_raw_task_ids_use_a_fresh_database")
    existing = conn.execute("SELECT count(*) FROM tasks").fetchone()[0]
    if existing and manifest(conn).get("hash_key") != key_id():
        raise SafeError("database_hashed_with_a_different_key_use_a_fresh_database")


def save(conn, tasks, evidence):
    """Import whole tasks atomically; a repeated import is a no-op, a conflict an error."""
    if any(not IDENTITY_HASH.fullmatch(t.task_id) for t in tasks):
        raise SafeError("task_ids_must_be_sha256")
    require_current(conn)
    existing = {t.task_id: t for t in load(conn)}
    fresh = []
    duplicate = 0
    for task in tasks:
        old = existing.get(task.task_id)
        if old:
            # Classification can be changed independently; don't undo an override on reimport.
            comparable = old.row() | {"task_type": task.task_type}
            if comparable != task.row() or [c.row() for c in old.calls] != [
                c.row() for c in task.calls
            ]:
                raise SafeError("conflicting_task_reimport_use_a_distinct_namespace")
            duplicate += 1
        else:
            fresh.append(task)
    if not fresh:
        return {"inserted_tasks": 0, "duplicate_tasks": duplicate, "inserted_calls": 0}
    conn.execute("BEGIN TRANSACTION")
    try:
        for table, rows in (
            ("tasks", [t.row() for t in fresh]),
            ("calls", [c.row() for t in fresh for c in t.calls]),
        ):
            if rows:
                conn.register("safe_batch", pa.Table.from_pylist(rows))
                conn.execute(f"INSERT INTO {table} BY NAME SELECT * FROM safe_batch")
                conn.unregister("safe_batch")
        m = manifest(conn)
        m["imports"].append(evidence)
        m["hash_key"] = key_id()
        serialized = json.dumps(m, sort_keys=True).replace("'", "''")
        conn.execute(f"COMMENT ON TABLE tasks IS '{serialized}'")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {
        "inserted_tasks": len(fresh),
        "duplicate_tasks": duplicate,
        "inserted_calls": sum(t.n_calls for t in fresh),
    }


def load(conn):
    def dictionaries(sql):
        result = conn.execute(sql)
        columns = [d[0] for d in result.description]
        return [dict(zip(columns, row)) for row in result.fetchall()]

    def hashed(task_id):
        # Databases written before schema 3 hold raw IDs; hash them before any use.
        return task_id if IDENTITY_HASH.fullmatch(task_id) else task_digest(task_id)

    tasks = {}
    for row in dictionaries("SELECT * FROM tasks ORDER BY task_id"):
        row["task_id"] = hashed(row["task_id"])
        tasks[row["task_id"]] = Task(**row)
    for row in dictionaries("SELECT * FROM calls ORDER BY task_id, call_idx"):
        row["task_id"] = hashed(row["task_id"])
        tasks[row["task_id"]].calls.append(Call(**row))
    return list(tasks.values())

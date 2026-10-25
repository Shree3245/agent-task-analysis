import csv
import hashlib
import json
from pathlib import Path

import ijson
import pyarrow.parquet as pq

from agent_task_analysis.adapters import SOURCES, adapter
from agent_task_analysis.adapters.base import Context
from agent_task_analysis.classify import classify_task
from agent_task_analysis.privacy import SafeError
from agent_task_analysis.storage import connect, save

MAX_RECORD = 128 * 1024 * 1024


def records(path, source):
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        for batch in pq.ParquetFile(path).iter_batches(batch_size=1):
            yield from batch.to_pylist()
    elif source == "csv":
        csv.field_size_limit(MAX_RECORD)
        with path.open(newline="", encoding="utf-8-sig") as handle:
            yield from csv.DictReader(handle)
    elif suffix in {".jsonl", ".ndjson"}:
        with path.open("rb") as handle:
            while line := handle.readline(MAX_RECORD + 1):
                if len(line) > MAX_RECORD:
                    raise SafeError("record_size_limit")
                if line.strip():
                    yield json.loads(line)
    else:
        with path.open("rb") as handle:
            first = handle.read(4096).lstrip()[:1]
            handle.seek(0)
            if first == b"[":
                yield from ijson.items(handle, "item", use_float=True)
            else:
                if path.stat().st_size > MAX_RECORD:
                    raise SafeError("record_size_limit_use_jsonl_or_parquet")
                yield json.load(handle)


def merge_task(target, piece):
    offset = len(target.calls)
    for call in piece.calls:
        call.call_idx += offset
        if call.parent_call_idx is not None:
            call.parent_call_idx += offset
        target.calls.append(call)
    if target.task_type == "unknown":
        target.task_type = piece.task_type
    elif piece.task_type != "unknown" and target.task_type != piece.task_type:
        raise SafeError("conflicting_task_types")
    for key, fn in (("started_at", min), ("ended_at", max)):
        present = [v for v in (getattr(target, key), getattr(piece, key)) if v]
        setattr(target, key, fn(present) if present else None)
    if piece.task_group and target.task_group and piece.task_group != target.task_group:
        raise SafeError("conflicting_task_groups")
    target.task_group = target.task_group or piece.task_group
    if piece.outcome != "unknown":
        target.outcome = piece.outcome
    if piece.capped:
        target.capped, target.cap_reason = True, piece.cap_reason


def ingest(source, path, db, *, namespace="", options=None, benchmark=False):
    if source not in SOURCES:
        raise SafeError("unknown_source")
    path = Path(path)
    if not path.exists():
        raise SafeError("input_not_found")
    extensions = (
        {".csv"} if source == "csv" else {".json", ".jsonl", ".ndjson", ".traj", ".parquet"}
    )
    files = (
        sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in extensions)
        if path.is_dir()
        else [path]
    )
    if not files:
        raise SafeError("no_supported_input_files")

    def stream():
        for file in files:
            # Filenames/paths never persist; a stable digest supplies identity when exports omit IDs.
            local_key = file.relative_to(path).as_posix() if path.is_dir() else file.name
            file_key = hashlib.sha256(local_key.encode()).hexdigest()[:24]
            for index, root in enumerate(records(file, source)):
                yield f"{file_key}:{index}", root

    return ingest_records(source, stream(), db, namespace=namespace, options=options,
                          benchmark=benchmark, files=len(files))


def ingest_records(source, stream, db, *, namespace="", options=None, benchmark=False, files=0,
                   extra_evidence=None):
    """stream yields (fallback identity, raw record); records are parsed in memory only."""
    ctx = Context(source, namespace, options=options or {})
    grouped = {}
    count = 0
    for fallback, root in stream:
        count += 1
        for piece in adapter(source)(root, ctx, fallback):
            if piece.task_id in grouped:
                merge_task(grouped[piece.task_id], piece)
            else:
                grouped[piece.task_id] = piece
    if ctx.options.get("drop_tasks_without_model_calls"):
        for key in [k for k, t in grouped.items() if not any(c.event_kind == "model" for c in t.calls)]:
            del grouped[key]
            ctx.warn("task_without_model_calls_dropped")
    if not grouped:
        raise SafeError("no_tasks_in_supported_records")
    for task in grouped.values():
        task.finalize()
        classify_task(task, (options or {}).get("rules"))
    evidence = {
        "source": source,
        "adapter_version": 1,
        "files": files,
        "records": count,
        "tasks": len(grouped),
        "fields_read": sorted(ctx.fields),
        "warnings": ctx.warnings,
        "benchmark": bool(benchmark),
        "token_semantics": ctx.options.get("token_semantics", "native"),
        "content_retained": False,
    } | (extra_evidence or {})
    with connect(db) as conn:
        result = save(conn, list(grouped.values()), evidence)
    return result | {"warnings": ctx.warnings}

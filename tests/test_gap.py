import copy
import csv
import hashlib
import json
import uuid

from conftest import CSV_OPTIONS
from agent_task_analysis.ingest import ingest
from agent_task_analysis.report.dashboard import tagging
from agent_task_analysis.storage import connect, load, manifest


def write_calls(path, calls):
    """calls: (task_id, task_type, session, iso start); one model call per row."""
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["task_id", "task_type", "session", "model", "ts_start", "input_tokens",
                    "output_tokens"])
        for task_id, task_type, session, start in calls:
            w.writerow([task_id, task_type, session, "gpt-4o-mini", start, 100, 10])


def options(session=True):
    o = copy.deepcopy(CSV_OPTIONS)
    o["columns"]["ts_start"] = "ts_start"
    if session:
        o["columns"]["session"] = "session"
    return o | {"gap_seconds": 60}


def runs(db):
    with connect(db, read_only=True) as conn:
        return sorted((t.task_type, t.n_calls) for t in load(conn))


def test_gap_groups_calls_per_session_and_type(tmp_path):
    canary = "user-" + uuid.uuid4().hex
    t = "2026-10-01T10:00:"
    write_calls(tmp_path / "calls.csv", [
        # Two users interleaved: each is one run of three calls 20 s apart.
        ("c1", "triage", canary, t + "00"), ("c2", "triage", "user-b", t + "05"),
        ("c3", "triage", canary, t + "20"), ("c4", "triage", "user-b", t + "25"),
        ("c5", "triage", canary, t + "40"), ("c6", "triage", "user-b", t + "45"),
        # Same user, another type at the same time: its own run.
        ("c7", "brief", canary, t + "30"),
        # Same user and type after 5 quiet minutes: a new run.
        ("c8", "triage", canary, "2026-10-01T10:05:41"),
    ])
    db = tmp_path / "a.duckdb"
    result = ingest("csv", tmp_path / "calls.csv", db, options=options())
    assert result["warnings"]["runs_merged_by_gap"] == 4
    assert "gap_grouping_without_session" not in result["warnings"]
    assert runs(db) == [("brief", 1), ("triage", 1), ("triage", 3), ("triage", 3)]
    with connect(db, read_only=True) as conn:
        assert manifest(conn)["imports"][0]["gap_seconds"] == 60
    # Neither the session ID nor its hash is stored.
    hashed = hashlib.sha256(canary.encode()).hexdigest()
    for value in (canary, hashed):
        assert value.encode() not in db.read_bytes()
        with connect(db, read_only=True) as conn:
            assert value not in json.dumps([t.row() for t in load(conn)])
            assert value not in json.dumps(manifest(conn))


def test_gap_without_session_warns(tmp_path):
    write_calls(tmp_path / "calls.csv", [
        ("c1", "triage", "", "2026-10-01T10:00:00"), ("c2", "triage", "", "2026-10-01T10:00:30"),
    ])
    db = tmp_path / "a.duckdb"
    result = ingest("csv", tmp_path / "calls.csv", db, options=options(session=False))
    assert result["warnings"]["gap_grouping_without_session"] == 1
    assert runs(db) == [("triage", 2)]


def test_without_gap_each_trace_stays_a_run(tmp_path):
    write_calls(tmp_path / "calls.csv", [
        ("c1", "triage", "u", "2026-10-01T10:00:00"), ("c2", "triage", "u", "2026-10-01T10:00:30"),
    ])
    db = tmp_path / "a.duckdb"
    o = options()
    del o["gap_seconds"]
    ingest("csv", tmp_path / "calls.csv", db, options=o)
    assert runs(db) == [("triage", 1), ("triage", 1)]


def report(groups, imports=None):
    return {"evidence": {"imports": imports or [{}]}, "groups": groups, "min_samples": 30,
            "n_tasks": sum(g["n_total"] for g in groups)}


def test_tagging_notes():
    single = {"name": "triage", "n_total": 100, "single_call_share": 0.9}
    multi = {"name": "brief", "n_total": 100, "single_call_share": 0.1}
    few = {"name": "rare", "n_total": 10, "single_call_share": 1.0}
    assert tagging(report([multi, few])) == []
    [note] = tagging(report([single, multi]))
    assert note.startswith("Most runs of triage are a single model call.") and "--gap 60" in note
    gap = tagging(report([single], [{"gap_seconds": 60, "warnings": {"gap_grouping_without_session": 1}}]))
    assert len(gap) == 2 and "quiet gap of 60 seconds" in gap[0] and "no session or user ID" in gap[1]
    unknown = {"name": "unknown", "n_total": 50, "single_call_share": 0.1}
    [note] = tagging(report([multi, unknown]))
    assert note.startswith("50 runs (33%) have no task type")

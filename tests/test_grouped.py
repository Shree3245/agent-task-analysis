import json
from pathlib import Path
import re
import uuid

import duckdb
import numpy as np
import pytest

from synthetic import grouped, run_assignments, ungrouped
from agent_task_analysis.analysis.backtest import time_split
from agent_task_analysis.analysis.fixed_price import simulations
from agent_task_analysis.analysis.grouped import (FOLDS, SCENARIOS, Arrays, check_disjoint, cross_validate,
                                    group_key, partitions, ratios, repeated_groups)
from agent_task_analysis.analysis.history import build_history
from agent_task_analysis.cli import main
from agent_task_analysis.ingest import merge_task
from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.privacy import SafeError, group_digest, task_digest
from agent_task_analysis.report.model import make_report
from agent_task_analysis.report.render import render
from agent_task_analysis.schema import Task
from agent_task_analysis.storage import CALL_SQL, connect, load, save

GOLDEN = Path(__file__).parent / "fixtures/golden/no-groups.md"


def history(tasks):
    return build_history(tasks, load_catalog())


def row(rows, scope, mode="exclude", capped=True, target=0.7):
    return next(r for r in rows if r["scope"] == scope and r["censoring"] == mode
                and r["capped"] == capped and abs(r["target"] - target) < 1e-9)


def test_grouped_interval_is_wider_than_leaky_time_split_and_groups_never_cross():
    h = history(grouped())
    _, train, test, _ = time_split(h)
    # The time split scores the same 50 groups it was fit on: that is the leak.
    assert {group_key(t) for t in train} == {group_key(t) for t in test}
    split = row(simulations(train, test, [0.7], scope="holdout"), "holdout")
    cv = row(cross_validate(h, [0.7], scope="grouped_cv"), "grouped_cv")
    assert cv["ci"][1] - cv["ci"][0] > split["ci"][1] - split["ci"][0]
    assert cv["ci"][1] > split["ci"][1]
    for _, train, test in partitions(h, "grouped_cv"):
        assert not {group_key(t) for t in train} & {group_key(t) for t in test}
    assert sorted(f["test_groups"] for f in cv["folds"]) == [10] * FOLDS


def test_overlapping_groups_are_rejected_in_code():
    h = history(grouped())
    with pytest.raises(AssertionError):
        check_disjoint(h[:60], h[40:100])
    a = Arrays(h)
    leaky = np.arange(len(a.total)) // 50 % FOLDS  # one fold per run: groups span folds
    with pytest.raises(AssertionError):
        ratios(a, np.ones(len(a.total), dtype=int), leaky, FOLDS)


def test_vectorized_refit_matches_scalar_point_estimate():
    # Unit weights on the point-estimate folds must reproduce the scalar replay exactly,
    # including mid-task cap crossings and the inflated censoring tail.
    h = history(grouped(capped_every=9))
    rows = cross_validate(h, [0.7], scope="grouped_cv", draws=5)
    fold = {t.task.task_id: f - 1 for f, _, test in partitions(h, "grouped_cv") for t in test}
    complete = [t for t in h if t.complete]
    pooled, _ = ratios(Arrays(h), np.ones(len(complete), dtype=int),
                       np.array([fold[t.task.task_id] for t in complete]), FOLDS)
    assert len(rows) == len(SCENARIOS)
    for r in rows:
        assert 0.7 * pooled[(r["censoring"], r["capped"])] == pytest.approx(r["loss_ratio"], rel=1e-9)
    assert row(rows, "grouped_cv", "inflate")["n_test"] > row(rows, "grouped_cv")["n_test"]


def test_leave_one_run_out_fits_three_runs_and_scores_the_fourth():
    tasks = grouped()
    runs = {k: v["run_id"] for k, v in run_assignments(tasks).items()}
    rows = cross_validate(history(tasks), [0.7], scope="leave_one_run_out", runs=runs, draws=50)
    r = row(rows, "leave_one_run_out")
    assert [(f["n_train"], f["n_test"]) for f in r["folds"]] == [(150, 50)] * 4
    assert cross_validate(history(tasks), [0.7], scope="leave_one_run_out", runs={}) == []


def test_report_verdict_uses_grouped_cv_and_shows_leaky_time_split(tmp_path):
    tasks = grouped()
    report = make_report(tasks, {"imports": [], "benchmark_assignments": run_assignments(tasks)},
                         load_catalog(), redact=True)
    g = report["groups"][0]
    assert g["grouped"] and g["verdict"]["reason"].startswith(("grouped_cv", "exclude"))
    assert {r["scope"] for r in g["simulations"]} >= {"grouped_cv", "leave_one_run_out", "holdout"}
    render(report, tmp_path / "r.html")
    md = (tmp_path / "r.md").read_text()
    assert "Time split (leaks repeated tasks) loss ratio" in md
    assert "Difference: time split − grouped CV" in md
    assert "task_group" in md.split("## Summary verdicts")[0]


def test_without_task_groups_the_time_split_report_is_unchanged(tmp_path):
    tasks = ungrouped()
    assert not repeated_groups(history(tasks))
    report = make_report(tasks, {"imports": []}, load_catalog(), redact=True)
    assert all(g["verdict"]["reason"].startswith(("holdout", "exclude"))
               for g in report["groups"])
    assert not any(r["scope"] == "grouped_cv" for g in report["groups"] for r in g["simulations"])
    render(report, tmp_path / "r.html")
    md = re.sub(r"Report generated: \S+\.", "Report generated: <time>.",
                (tmp_path / "r.md").read_text())
    # Golden = the pre-grouping report plus only the task_group field, the split table,
    # the drift and recency section, and the review pool's backdated cutoff.
    assert md == GOLDEN.read_text()
    assert "| code | synthetic | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group" in md


def test_unrepeated_groups_keep_the_time_split():
    tasks = [t for t in grouped() if t.task_id.startswith("run0:")]
    assert all(t.task_group for t in tasks) and not repeated_groups(history(tasks))


def test_same_seed_same_results():
    h = history(grouped(capped_every=9))

    def run(seed):
        rows = cross_validate(h, [0.6, 0.7], scope="grouped_cv", seed=seed, draws=200)
        return json.dumps([{k: v for k, v in r.items() if k != "_samples"} for r in rows]), \
            [r["_samples"] for r in rows]

    (a, sa), (b, sb) = run(4), run(4)
    assert a == b and all(np.array_equal(x, y, equal_nan=True) for x, y in zip(sa, sb))
    assert run(5)[0] != a


@pytest.mark.parametrize("source", ["openhands", "swe-agent", "mini-swe-agent"])
def test_adapters_hash_instance_ids_and_reports_never_show_them(source, tmp_path, monkeypatch):
    instance = "PRIVATE_" + uuid.uuid4().hex
    usage = {"input_tokens": 150, "output_tokens": 20}
    record = {
        "openhands": {"instance_id": instance, "model": "gpt-4o-mini",
                      "events": [{"type": "llm", "usage": usage,
                                  "timestamp": "2025-01-01T00:00:00Z"}]},
        "swe-agent": {"instance_id": instance, "model": "gpt-4o-mini",
                      "trajectory": [{"usage": usage, "timestamp": "2025-01-01T00:00:00Z"}]},
        "mini-swe-agent": {"instance_id": instance, "info": {"model_name": "gpt-4o-mini"},
                           "messages": [{"role": "assistant", "usage": usage,
                                         "timestamp": "2025-01-01T00:00:00Z"}]},
    }[source]
    monkeypatch.chdir(tmp_path)
    Path("in.json").write_text(json.dumps(record))
    for run in ("run-1", "run-2"):
        assert main(["ingest", source, "in.json", "--namespace", run]) == 0
    with connect(".agent-task-analysis/agent-task-analysis.duckdb", read_only=True) as conn:
        groups = {t.task_group for t in load(conn)}
    assert groups == {group_digest(instance)}
    assert main(["report", "--out", "report.html", "--redact-task-ids"]) == 0
    for out in ("report.html", "report.md"):
        assert instance not in Path(out).read_text()


def test_other_adapters_leave_task_group_empty(tmp_path):
    from conftest import FIXTURES
    from agent_task_analysis.ingest import ingest
    ingest("otel", FIXTURES / "otel/sample.json", tmp_path / "db.duckdb")
    with connect(tmp_path / "db.duckdb", read_only=True) as conn:
        assert [t.task_group for t in load(conn)] == [None]


def test_task_group_must_be_a_hash_and_cannot_conflict():
    with pytest.raises(SafeError):
        Task("a", task_group="django__django-11099").finalize()
    a, b = Task("a", task_group="0" * 64), Task("a", task_group="1" * 64)
    with pytest.raises(SafeError):
        merge_task(a, b)


def version_one(db, task_id):
    with duckdb.connect(str(db)) as conn:
        conn.execute("""CREATE TABLE tasks (task_id VARCHAR PRIMARY KEY, task_type VARCHAR,
            source VARCHAR, started_at VARCHAR, ended_at VARCHAR, n_calls BIGINT,
            outcome VARCHAR, capped BOOLEAN, cap_reason VARCHAR)""")
        conn.execute(CALL_SQL)
        conn.execute("INSERT INTO tasks VALUES (?, 'code', 'csv', NULL, NULL, 0, 'unknown', false, NULL)",
                     [task_id])


def test_version_one_database_gains_empty_task_group(tmp_path):
    db, old, new = tmp_path / "old.duckdb", "b" * 64, "c" * 64
    version_one(db, old)
    with connect(db, read_only=True) as conn:
        assert load(conn)[0].task_group is None
    with connect(db) as conn:
        # The column is added on open; digests from before keyed hashing cannot be mixed in.
        assert "task_group" in [c[0] for c in conn.execute("DESCRIBE tasks").fetchall()]
        with pytest.raises(SafeError, match="different_key"):
            save(conn, [Task(new, task_group="a" * 64).finalize()], {"source": "test"})


def test_raw_task_ids_never_leave_storage(tmp_path):
    db = tmp_path / "old.duckdb"
    version_one(db, "csv:customer-4471")
    with connect(db, read_only=True) as conn:
        assert load(conn)[0].task_id == task_digest("csv:customer-4471")
    with connect(db) as conn, pytest.raises(SafeError, match="raw_task_ids"):
        save(conn, [Task("d" * 64).finalize()], {"source": "test"})
    with connect(tmp_path / "new.duckdb") as conn, pytest.raises(SafeError, match="sha256"):
        save(conn, [Task("csv:customer-4471").finalize()], {"source": "test"})

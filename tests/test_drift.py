from datetime import timedelta
from importlib.resources import files

import numpy as np
import pytest
import yaml

from synthetic import START, grouped, task
from agent_task_analysis.analysis.backtest import time_split
from agent_task_analysis.analysis.drift import data_end, drift, weekly
from agent_task_analysis.analysis.fixed_price import simulations
from agent_task_analysis.analysis.grouped import Arrays, cross_validate, partitions, ratios
from agent_task_analysis.analysis.history import build_history
from agent_task_analysis.cli import main, select_window
from agent_task_analysis.pricing.catalog import load_catalog, rates_at
from agent_task_analysis.pricing.reprice import call_cost
from agent_task_analysis.privacy import SafeError, task_digest
from agent_task_analysis.report.model import make_report
from agent_task_analysis.report.render import render
from agent_task_analysis.schema import Call
from agent_task_analysis.storage import connect, save


def history(tasks, catalog=None):
    return build_history(tasks, catalog or load_catalog())


def stepped(n=120, factor=3.0, outcomes=None):
    """One pool, one task every 12 hours; costs jump by `factor` halfway through."""
    rng = np.random.default_rng(7)
    result = []
    for i in range(n):
        level = 1.0 if i < n // 2 else factor
        tokens = rng.lognormal(10, 0.3, 3) * level
        outcome = outcomes[i % len(outcomes)] if outcomes else "success"
        result.append(task(f"s{i}", tokens, START + timedelta(hours=12 * i), outcome=outcome))
    return result


def catalog_file(tmp_path, changes, name="prices.yaml"):
    data = yaml.safe_load(files("agent_task_analysis.pricing").joinpath("data/prices.v1.yaml").read_text())
    data["version"] = "test"
    data["models"]["openai/gpt-4o-mini"]["changes"] = changes
    path = tmp_path / name
    path.write_text(yaml.safe_dump(data))
    return path


def holdout(rows, target=0.7, billing=None):
    return next(r for r in rows if r["scope"] == "holdout" and r["censoring"] == "exclude"
                and r["capped"] and abs(r["target"] - target) < 1e-9
                and (billing is None or r.get("billing") == billing))


def test_rate_changes_apply_from_their_date_and_validate(tmp_path):
    catalog = load_catalog(catalog_file(tmp_path, [{"effective": "2025-03-01", "input": 0.3},
                                                   {"effective": "2025-02-01", "output": 1.2}]))
    rates = catalog["models"]["openai/gpt-4o-mini"]
    assert [c["effective"] for c in rates["changes"]] == ["2025-02-01", "2025-03-01"]
    assert rates_at(rates, None)["input"] == 0.15
    assert rates_at(rates, "2025-02-15T00:00:00+00:00") | {} == rates_at(rates, "2025-02-01T00:00:00+00:00")
    assert (rates_at(rates, "2025-02-15T00:00:00+00:00")["output"],
            rates_at(rates, "2025-02-15T00:00:00+00:00")["input"]) == (1.2, 0.15)
    assert rates_at(rates, "2025-03-01T00:00:00+00:00")["input"] == 0.3
    before = Call("a", 0, "2025-01-31T23:59:00+00:00", None, "openai", "gpt-4o-mini",
                  input_tokens=1_000_000, cached_input_tokens=0, cache_write_input_tokens=0,
                  output_tokens=1_000_000, reasoning_tokens=0)
    after = Call("a", 1, "2025-03-02T00:00:00+00:00", None, "openai", "gpt-4o-mini",
                 input_tokens=1_000_000, cached_input_tokens=0, cache_write_input_tokens=0,
                 output_tokens=1_000_000, reasoning_tokens=0)
    assert call_cost(before, catalog)[0] == pytest.approx(0.75)
    assert call_cost(after, catalog)[0] == pytest.approx(1.5)
    # A projection prices an old call at the rates in force on the projection date.
    assert call_cost(before, catalog, as_of="2025-03-01")[0] == pytest.approx(1.5)
    with pytest.raises(SafeError):
        load_catalog(catalog_file(tmp_path, [{"effective": "2025-03-01", "input": 1},
                                             {"effective": "2025-03-01", "input": 2}], "dup.yaml"))
    with pytest.raises(SafeError):
        load_catalog(catalog_file(tmp_path, [{"effective": "soon", "input": 1}], "bad.yaml"))
    with pytest.raises(SafeError):
        load_catalog(catalog_file(tmp_path, [{"effective": "2025-03-01", "input": -1}], "neg.yaml"))


def test_projection_doubling_every_rate_doubles_spend_price_and_kept_loss_ratio(tmp_path):
    tasks = stepped(factor=1.0)
    end = data_end(history(tasks)).date()
    date = (end + timedelta(days=10)).isoformat()
    catalog = load_catalog(catalog_file(tmp_path, [{"effective": date, "input": 0.3,
                                                    "cached_input": 0.15, "output": 1.2}]))
    report = make_report(tasks, {"imports": []}, catalog)
    assert report["future_rate_changes"] == [date]
    (p,) = report["projections"]
    base = holdout(report["groups"][0]["simulations"])
    assert p["models"] == ["openai/gpt-4o-mini"]
    assert p["spend_change"] == pytest.approx(1.0)
    assert p["price"] == pytest.approx(2 * base["price"])
    assert p["kept"]["loss_ratio"] == pytest.approx(2 * base["loss_ratio"])
    assert p["kept"]["ci"][1] == pytest.approx(2 * base["ci"][1], rel=1e-6)


def test_overrides_price_unlisted_models_and_are_labeled(tmp_path):
    tasks = stepped(factor=1.0)
    for t in tasks[::2]:
        t.calls[0].model = "house-model"
        t.calls[0].provider = "acme"
    (tmp_path / "rates.yaml").write_text(yaml.safe_dump({
        "description": "Contract rates, 2025",
        "models": {"acme/house-model": {"input": 1, "output": 2},
                   "openai/gpt-4o-mini": {"input": 0.1, "cached_input": 0.05, "output": 0.5}}}))
    plain = make_report(tasks, {"imports": []}, load_catalog())
    assert plain["groups"][0]["n_unpriced"] == 60 and plain["overrides"] is None
    catalog = load_catalog(overrides=tmp_path / "rates.yaml")
    assert catalog["overrides"]["added"] == ["acme/house-model"]
    assert catalog["overrides"]["replaced"] == ["openai/gpt-4o-mini"]
    report = make_report(tasks, {"imports": []}, catalog)
    g = report["groups"][0]
    assert g["n_unpriced"] == 0 and g["override_share"] == pytest.approx(1.0)
    render(report, tmp_path / "r.html")
    md = (tmp_path / "r.md").read_text()
    assert "RATE OVERRIDES APPLIED" in md and "Contract rates, 2025" in md
    assert "Spend priced at override rates" in md
    assert "override rates priced 100.0% of spend" in md
    (tmp_path / "bad.yaml").write_text(yaml.safe_dump({"models": {"nomodelslash": {"input": 1, "output": 1}}}))
    with pytest.raises(SafeError):
        load_catalog(overrides=tmp_path / "bad.yaml")


def test_drift_flags_a_cost_step_and_reports_weekly_means():
    h = history(stepped(factor=3.0))
    _, train, _, _ = time_split(h)
    d = drift(train, h, data_end(h), 15, 30)
    # Training holds 60 tasks at 1x and 20 at 3x (mean 1.5); the recent window is all 3x.
    assert d["ratio"] == pytest.approx(2.0, rel=0.1) and d["reprice"]
    assert d["recent_n"] == 30 and d["fit_n"] == len(train)
    flat = history(stepped(factor=1.0))
    _, flat_train, _, _ = time_split(flat)
    assert not drift(flat_train, flat, data_end(flat), 15, 30)["reprice"]
    weeks = weekly(h)
    assert sum(w["n"] for w in weeks) == len(h)
    assert weeks[0]["mean"] < weeks[-1]["mean"]


def test_recency_fit_tracks_the_new_cost_level():
    report = make_report(stepped(factor=3.0), {"imports": []}, load_catalog(), recent_days=10)
    r = report["groups"][0]["recency"]
    # The full-period fit underprices the costlier holdout; the last-10-day fit does not.
    assert r["full"]["loss_ratio"] > 1 and r["recent"]["price"] > r["full"]["price"]
    assert r["recent"]["loss_ratio"] < r["full"]["loss_ratio"]
    assert r["current"]["n_train"] == 20
    assert report["groups"][0]["drift"]["reprice"]


def test_refund_adjusted_price_and_loss_ratio_follow_billable_tasks():
    h = history(stepped(factor=1.0, outcomes=["success", "fail", "success", "unknown"]))
    _, train, test, _ = time_split(h)
    per_task = holdout(simulations(train, test, [0.7], scope="holdout"))
    rows = simulations(train, test, [0.7], scope="holdout", billing="refund_failed")
    r = holdout(rows, billing="refund_failed")
    fit = [t for t in train if not t.task.capped]
    assert r["train_billable"] == sum(t.task.outcome != "fail" for t in fit)
    assert r["price"] == pytest.approx(per_task["price"] * len(fit) / r["train_billable"])
    strict = holdout(simulations(train, test, [0.7], scope="holdout",
                                 billing="refund_unconfirmed"), billing="refund_unconfirmed")
    assert strict["train_billable"] == sum(t.task.outcome == "success" for t in fit)
    assert strict["price"] > r["price"] > per_task["price"]
    # Same seed, all tasks billed: the paired bootstrap reproduces the per-task interval.
    everyone = history(stepped(factor=1.0))
    _, tr, te, _ = time_split(everyone)
    paired = holdout(simulations(tr, te, [0.7], scope="holdout", billing="refund_failed"))
    plain = holdout(simulations(tr, te, [0.7], scope="holdout"))
    assert paired["ci"] == pytest.approx(plain["ci"]) and paired["price"] == pytest.approx(plain["price"])


def test_grouped_refund_billing_matches_the_vectorized_point_estimate():
    h = history(grouped())
    rows = cross_validate(h, [0.7], scope="grouped_cv", billing="refund_failed", draws=5)
    assert {r["billing"] for r in rows} == {"refund_failed"}
    fold = {t.task.task_id: f - 1 for f, _, test in partitions(h, "grouped_cv") for t in test}
    complete = [t for t in h if t.complete]
    pooled, _ = ratios(Arrays(h), np.ones(len(complete), dtype=int),
                       np.array([fold[t.task.task_id] for t in complete]), 5,
                       billing="refund_failed")
    for r in rows:
        assert 0.7 * pooled[(r["censoring"], r["capped"])] == pytest.approx(r["loss_ratio"])
    per_task = cross_validate(h, [0.7], scope="grouped_cv", draws=5)
    # A third of groups fail: refunding them raises the price per billed task.
    assert rows[0]["price"] > next(r for r in per_task if r["censoring"] == rows[0]["censoring"]
                                   and r["capped"] == rows[0]["capped"])["price"]


def test_since_until_select_by_start_time(tmp_path):
    tasks = stepped(n=10)  # starts every 12h from 2025-01-01T00:00
    kept, window = select_window(tasks, "2025-01-02", "2025-01-03")
    assert [t.task_id for t in kept] == ["s2", "s3", "s4", "s5"]  # until includes the whole day
    assert window == {"since": "2025-01-02", "until": "2025-01-03", "outside": 6, "untimed": 0}
    kept, _ = select_window(tasks, None, "2025-01-02T12:00:00Z")
    assert [t.task_id for t in kept] == ["s0", "s1", "s2", "s3"]
    assert select_window(tasks) == (tasks, None)
    with pytest.raises(SafeError):
        select_window(tasks, "2025-01-03", "2025-01-02")
    with pytest.raises(SafeError):
        select_window(tasks, "yesterday")
    db = tmp_path / "db.duckdb"
    stored = stepped(n=120)
    for t in stored:
        t.task_id = task_digest(t.task_id)
        for c in t.calls:
            c.task_id = t.task_id
    with connect(db) as conn:
        save(conn, stored, {"source": "synthetic", "files": 1, "records": 120, "fields_read": []})
    out = tmp_path / "r.html"
    assert main(["report", "--db", str(db), "--out", str(out), "--since", "2025-01-20",
                 "--recent-days", "7"]) == 0
    md = out.with_suffix(".md").read_text()
    assert "Report window: tasks that started from 2025-01-20 through the last task (UTC). 38 tasks outside" in md
    assert "Recent window (last 7 days)" in md and "## Drift and recency" in md
    assert main(["report", "--db", str(db), "--out", str(out), "--since", "2026-01-01"]) == 2
    assert main(["report", "--db", str(db), "--out", str(out), "--recent-days", "0"]) == 2

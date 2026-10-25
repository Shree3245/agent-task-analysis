import numpy as np
import pytest

from synthetic import grouped, unprice
from agent_task_analysis.analysis.grouped import FOLDS, Arrays, cross_validate, partitions, ratios
from agent_task_analysis.analysis.history import build_history
from agent_task_analysis.analysis.verdicts import verdict
from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.report.model import make_report


def history(tasks):
    return build_history(tasks, load_catalog())


def row(upper, mode="exclude", unpriced="excluded"):
    return {"scope": "grouped_cv", "capped": True, "target": 0.7, "censoring": mode,
            "unpriced": unpriced, "train_uncapped": 60, "test_uncapped": 30, "ci": [0.6, upper]}


def test_under_two_percent_unpriced_needs_both_verdicts():
    h = history(unprice(grouped(), 100))  # 2 of 200 tasks: 1%
    assert sum(not t.complete for t in h) == 2
    passing = verdict([row(0.8)], h, scope="grouped_cv", imputed=[row(0.85, unpriced="p99")])
    assert passing["label"] == "VIABLE" and passing["unpriced_at_p99"] == "VIABLE"
    assert "also with 2 unpriced tasks (1.0%) at the training p99 cost" in passing["reason"]
    failing = verdict([row(0.8)], h, scope="grouped_cv", imputed=[row(0.95, unpriced="p99")])
    assert failing["label"] == "NOT VIABLE"
    assert (failing["unpriced_excluded"], failing["unpriced_at_p99"]) == ("VIABLE", "NOT VIABLE")
    assert "with unpriced tasks at training p99" in failing["reason"]


def test_two_percent_or_more_unpriced_is_not_viable():
    h = history(unprice(grouped(), 50))  # 4 of 200: exactly 2%
    v = verdict([row(0.5)], h, scope="grouped_cv", imputed=[row(0.5, unpriced="p99")])
    assert v["label"] == "NOT VIABLE" and v["unpriced_at_p99"] is None
    assert v["reason"].startswith("4 tasks (2.0%) have unknown costs; the limit is under 2%")


def test_imputation_scores_unpriced_at_training_p99_and_never_fits_on_them():
    h = history(unprice(grouped(capped_every=9), 100))
    base = cross_validate(h, [0.7], scope="grouped_cv", draws=5)
    stressed = cross_validate(h, [0.7], scope="grouped_cv", draws=5, impute=True)
    for b, s in zip(base, stressed):
        assert s["unpriced"] == "p99" and b["unpriced"] == "excluded"
        assert [f["price"] for f in s["folds"]] == [f["price"] for f in b["folds"]]
    # Vectorized refit matches the scalar point estimate with imputation too.
    fold = {t.task.task_id: f - 1 for f, _, test in partitions(h, "grouped_cv") for t in test}
    a = Arrays(h, impute=True)
    tasks = [t for t in h]  # impute keeps every task, in history order
    pooled, _ = ratios(a, np.ones(len(tasks), dtype=int),
                       np.array([fold[t.task.task_id] for t in tasks]), FOLDS)
    for r in stressed:
        assert 0.7 * pooled[(r["censoring"], r["capped"])] == pytest.approx(r["loss_ratio"], rel=1e-9)
    excluded = next(r for r in base if r["censoring"] == "exclude" and r["capped"])
    imputed = next(r for r in stressed if r["censoring"] == "exclude" and r["capped"])
    # Capped unpriced tasks follow censoring like any other: dropped when capped runs are excluded.
    assert imputed["n_test"] == excluded["n_test"] + sum(not t.complete and not t.task.capped for t in h)


def test_report_shows_both_verdicts_and_highest_success_target(tmp_path):
    from agent_task_analysis.report.render import render
    tasks = unprice(grouped(), 100)
    report = make_report(tasks, {"imports": [{"benchmark": True, "source": "synthetic", "files": 1, "records": 200, "fields_read": []}]}, load_catalog(), redact=True)
    g = report["groups"][0]
    assert g["verdict"]["unpriced_at_p99"] in {"VIABLE", "NOT VIABLE"} and g["imputed"]
    best = g["success_viable"]
    assert best["per_task_price_70"] > 0
    if best["target"]:
        assert best["target"] in {0.6, 0.65, 0.7} and best["price_per_resolved"] > best["per_task_price_70"] * 0.6
    render(report, tmp_path / "r.html")
    md = (tmp_path / "r.md").read_text()
    assert "Unpriced tasks · verdict both ways" in md
    assert "Success-only billing · highest viable target" in md


def test_highest_success_target_is_the_highest_that_passes():
    from agent_task_analysis.report.model import SUCCESS_TARGETS
    h = history(grouped())
    success = cross_validate(h, list(SUCCESS_TARGETS), scope="grouped_cv", success_only=True, draws=200)
    labels = {t: verdict(success, h, scope="grouped_cv", target=t)["label"] for t in SUCCESS_TARGETS}
    from agent_task_analysis.report.model import highest_success_target
    best = highest_success_target([], success, [], h, 30)["target"]
    passing = [t for t in SUCCESS_TARGETS if labels[t] == "VIABLE"]
    assert best == (max(passing) if passing else None)

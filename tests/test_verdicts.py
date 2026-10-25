from agent_task_analysis.analysis.verdicts import verdict
from agent_task_analysis.analysis.history import PricedTask
from agent_task_analysis.schema import Task


def row(mode, upper):
    return {
        "scope": "holdout",
        "capped": True,
        "target": 0.7,
        "censoring": mode,
        "train_uncapped": 60,
        "test_uncapped": 30,
        "ci": [0.6, upper],
    }


def test_strict_threshold_and_censor_disagreement():
    history = [PricedTask(Task("a", capped=True), [1], True, {})]
    result = verdict([row("exclude", 0.89), row("inflate", 0.91)], history)
    assert result["label"] == "NOT VIABLE" and result["censoring_disagreement"]
    assert verdict([row("exclude", 0.9)], [])["label"] == "NOT VIABLE"
    assert verdict([row("exclude", 0.89)], [])["label"] == "VIABLE"


def test_missing_costs_and_missing_time_cannot_pass():
    history = [PricedTask(Task("a"), [], False, {})]
    assert verdict([row("exclude", 0.7)], history)["label"] == "NOT VIABLE"
    assert verdict([], [])["label"] == "NOT VIABLE"

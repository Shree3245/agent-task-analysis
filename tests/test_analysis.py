from datetime import datetime, timedelta, timezone
import numpy as np
import pytest
from agent_task_analysis.schema import Task
from agent_task_analysis.analysis.history import PricedTask
from agent_task_analysis.analysis.shape import cost_shape
from agent_task_analysis.analysis.caps import replay
from agent_task_analysis.analysis.bootstrap import bootstrap_means, interval
from agent_task_analysis.analysis.backtest import time_split
from agent_task_analysis.analysis.fixed_price import simulations, macro_simulations
from agent_task_analysis.analysis.censoring import tail_increment


def tasks(costs, kind="code", offset=0, capped=False):
    result = []
    for i, cost in enumerate(costs):
        dt = (datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(days=i + offset)).isoformat()
        task = Task(f"{kind}-{i}", task_type=kind, started_at=dt, ended_at=dt, capped=capped)
        result.append(PricedTask(task, [cost], True, {0: cost}))
    return result


def test_equal_type_weights_and_top_spend():
    shape = cost_shape([1] * 100 + [100], [1 / 100] * 100 + [1])
    assert shape["mean"] == pytest.approx(50.5)
    assert shape["p90"] == 100
    assert cost_shape([1, 1, 1, 97])["top_1_share"] == 0.97


def test_replay_pays_crossing_call_no_future_knowledge():
    assert replay([2, 10, 4], 5) == (12, True)
    assert replay([2, 10], 5) == (12, False)


def test_bootstrap_seed_draws_and_constant_cost():
    a = bootstrap_means([1, 2, 100], seed=7)
    assert len(a) == 2000
    assert np.array_equal(a, bootstrap_means([1, 2, 100], seed=7))
    assert interval(bootstrap_means([4] * 30)) == [4, 4]


def test_backtest_is_elapsed_time_and_prices_do_not_see_future():
    data = tasks([1] * 80 + [10] * 40)
    cutoff, train, test, skipped = time_split(data)
    assert len(train) == 80 and len(test) == 40 and skipped == 0
    rows = simulations(train, test, [0.7], scope="holdout")
    plain = next(r for r in rows if not r["capped"] and r["censoring"] == "exclude")
    assert plain["price"] == pytest.approx(1 / 0.7)
    assert plain["loss_ratio"] == pytest.approx(7)
    # A huge later task must not change the training tail.
    assert tail_increment(train) == 1


def test_censoring_is_sensitivity_not_observed_cost():
    train = tasks([1] * 99 + [10])
    test = tasks([1] * 30) + tasks([5], offset=200, capped=True)
    rows = simulations(train, test, [0.7], scope="holdout")
    excluded = next(r for r in rows if not r["capped"] and r["censoring"] == "exclude")
    inflated = next(r for r in rows if not r["capped"] and r["censoring"] == "inflate")
    assert excluded["n_test"] == 30 and inflated["n_test"] == 31
    assert inflated["loss_ratio"] > excluded["loss_ratio"]


def test_macro_loss_ratio_does_not_pool_counts():
    a = simulations(tasks([1] * 100), tasks([1] * 100), [0.7], scope="holdout")
    b = simulations(tasks([1] * 2), tasks([10] * 2), [0.7], scope="holdout")
    row = next(
        r for r in macro_simulations([a, b]) if not r["capped"] and r["censoring"] == "exclude"
    )
    assert row["loss_ratio"] == pytest.approx((0.7 + 7) / 2)

"""Cost drift over time, recency-window pricing and scheduled rate-change projections.

Windows are defined on task start times and anchored at the latest start in the report,
never the wall clock, so a report is reproducible from its data.
"""

from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np

from agent_task_analysis.analysis.bootstrap import interval
from agent_task_analysis.analysis.fixed_price import simulations

DRIFT_LIMIT = 0.25


def started(t):
    return datetime.fromisoformat(t.task.started_at) if t.task.started_at else None


def data_end(history):
    return max((s for t in history if (s := started(t))), default=None)


def usable(tasks):
    return [t for t in tasks if t.complete and not t.task.capped]


def recent(tasks, end, days):
    """Tasks that started within `days` before `end` (inclusive of end)."""
    return [t for t in tasks if (s := started(t)) and s > end - timedelta(days=days)]


def span(tasks):
    times = [s for t in tasks if (s := started(t))]
    return [min(times).date().isoformat(), max(times).date().isoformat()] if times else None


def weekly(history):
    weeks = defaultdict(list)
    for t in usable(history):
        if s := started(t):
            weeks[(s - timedelta(days=s.weekday())).date().isoformat()].append(t.cost)
    return [{"week": w, "n": len(v), "mean": float(np.mean(v)), "total": float(sum(v))}
            for w, v in sorted(weeks.items())]


def drift(fit, history, end, days, min_samples):
    """Mean cost of the last `days` against the window the verdict price was fit on."""
    fitted, latest = usable(fit), usable(recent(history, end, days)) if end else []
    fit_mean = float(np.mean([t.cost for t in fitted])) if fitted else None
    recent_mean = float(np.mean([t.cost for t in latest])) if latest else None
    ratio = recent_mean / fit_mean if fit_mean and recent_mean is not None else None
    return {"fit_window": span(fitted), "fit_n": len(fitted), "fit_mean": fit_mean,
            "recent_window": span(latest), "recent_n": len(latest), "recent_mean": recent_mean,
            "ratio": ratio, "reprice": ratio is not None and abs(ratio - 1) > DRIFT_LIMIT,
            "small": min(len(fitted), len(latest)) < min_samples}


def pick(rows, scope, target):
    return next((r for r in rows if r["scope"] == scope and r["censoring"] == "exclude"
                 and r["capped"] and abs(r["target"] - target) < 1e-9), None)


def recency(history, train, test, cutoff, end, days, target, seed, min_samples):
    """Full-period vs last-`days` fits, scored on the same holdout, plus the price a
    last-`days` fit gives today (in-sample, not validated)."""
    result = {"days": days, "full": None, "recent": None, "current": None}
    if cutoff:
        result["full"] = pick(simulations(train, test, [target], scope="holdout", seed=seed),
                              "holdout", target)
        start = datetime.fromisoformat(cutoff) - timedelta(days=days)
        window = [t for t in train if (s := started(t)) and s >= start]
        result["recent"] = pick(simulations(window, test, [target], scope="recent_holdout",
                                            seed=seed), "recent_holdout", target)
        result["recent_window"] = span(window)
    if end:
        current = recent(history, end, days)
        result["current"] = pick(simulations(current, current, [target], scope="recent_in_sample",
                                             seed=seed), "recent_in_sample", target)
        result["current_window"] = span(current)
    for key in ("full", "recent"):
        row = result[key]
        result[key + "_passes"] = bool(row and row["ci"][1] < 0.9 and min(
            row["train_uncapped"], row["test_uncapped"]) >= min_samples)
    return result


def projection(history_at, train_ids, test_ids, current_price, base_spend, end, days, target,
               seed):
    """One pool at one future rate date: refit price, and the loss ratio if the current
    price is kept. Same tasks and time split as the verdict; only rates change."""
    train = [t for t in history_at if t.task.task_id in train_ids]
    test = [t for t in history_at if t.task.task_id in test_ids]
    row = pick(simulations(train, test, [target], scope="holdout", seed=seed), "holdout", target)
    current = recent(history_at, end, days) if end else []
    now = pick(simulations(current, current, [target], scope="recent_in_sample", seed=seed),
               "recent_in_sample", target)
    spend = sum(t.cost for t in history_at if t.complete)
    kept = None
    if row and current_price:
        mean_cost = row["loss_ratio"] * row["price"]
        kept = {"loss_ratio": mean_cost / current_price,
                "ci": interval(row["_means"] / current_price)}
    return {"price": row["price"] if row else None, "kept": kept,
            "current_price": now["price"] if now else None,
            "spend_change": spend / base_spend - 1 if base_spend else None}

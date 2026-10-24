"""Grouped cross-validation: prices are only ever scored on task groups they were not fit on.

Each fold fits its own mean price, p99 cap and censoring tail on training groups only.
Intervals resample whole groups (all runs of a drawn group together) and rerun the
entire cross-validation, refitting every price, in each draw.
"""

from collections import Counter
import hashlib
import json

import numpy as np

from moira.analysis.bootstrap import interval
from moira.analysis.caps import replay
from moira.analysis.censoring import imputed_tasks, scenario_tasks, tail_increment
from moira.analysis.fixed_price import billable
from moira.analysis.shape import quantile

DRAWS = 1000
FOLDS = 5
SCENARIOS = [(mode, capped) for mode in ("exclude", "inflate") for capped in (False, True)]


def group_key(t):
    # A task without a group is its own group: unrepeated work cannot leak.
    return t.task.task_group or "task:" + t.task.task_id


def repeated_groups(history):
    counts = Counter(t.task.task_group for t in history if t.task.task_group)
    return any(n > 1 for n in counts.values())


def signature(tasks):
    return json.dumps(sorted([t.task.n_calls, t.complete, t.task.capped, t.task.outcome, t.costs]
                             for t in tasks))


def group_order(history, seed=0):
    """Order groups by their own data, not their keyed IDs, so folds and bootstrap draws
    are the same on every install; the keyed ID only breaks exact ties."""
    members = {}
    for t in history:
        members.setdefault(group_key(t), []).append(t)
    return sorted(members, key=lambda g: (
        hashlib.sha256(f"{seed}:{signature(members[g])}".encode()).hexdigest(), g))


def run_order(history, runs):
    members = {}
    for t in history:
        members.setdefault(runs[t.task.task_id], []).append(t)
    return sorted(members, key=lambda r: (hashlib.sha256(signature(members[r]).encode()).hexdigest(), r))


def validation_basis(history):
    """Which split the verdict uses for one pricing pool, and why."""
    counts = Counter(t.task.task_group for t in history if t.task.task_group)
    repeated = sum(n > 1 for n in counts.values())
    sources = ", ".join(sorted({t.task.source for t in history}))
    if repeated:
        split = "grouped_cv"
        why = (f"{repeated} of {len(counts)} task groups repeat (up to {max(counts.values())} tasks"
               " each), so a time split would score tasks it was fit on")
    elif counts:
        split, why = "holdout", "task_group is set but no group repeats, so tasks cannot leak"
    else:
        split, why = "holdout", "no source in this pool sets task_group, so repeats cannot be detected"
    return {"sources": sources, "grouped_tasks": sum(counts.values()), "groups": len(counts),
            "repeated_groups": repeated, "max_per_group": max(counts.values(), default=0),
            "split": split, "why": why}


def check_disjoint(train, test):
    if {group_key(t) for t in train} & {group_key(t) for t in test}:
        raise AssertionError("a task group appears in both training and scoring")


def partitions(history, scope, seed=0, runs=None):
    if scope == "grouped_cv":
        groups = group_order(history, seed)
        if len(groups) < FOLDS:
            return []
        folds = {g: i % FOLDS for i, g in enumerate(groups)}
        part = lambda t: folds[group_key(t)]  # noqa: E731
        keys = list(range(FOLDS))
    else:
        if not runs or any(t.task.task_id not in runs for t in history):
            return []
        part = lambda t: runs[t.task.task_id]  # noqa: E731
        keys = run_order(history, runs)
        if len(keys) < 2:
            return []
    result = []
    for i, key in enumerate(keys):
        train = [t for t in history if part(t) != key]
        test = [t for t in history if part(t) == key]
        if scope == "grouped_cv":
            check_disjoint(train, test)
        result.append((i + 1, train, test))
    return result


def groups(values, uncapped=False):
    return len({group_key(t) for t, _, _ in values if not uncapped or not t.task.capped})


def cross_validate(history, targets, *, scope, seed=0, runs=None, success_only=False,
                   draws=DRAWS, impute=False, billing="all_tasks"):
    """impute: score each unpriced held-out task at the training p99 (never fit on them).

    success_only bills confirmed successes and drops unknown outcomes; the refund rules
    keep every task and refund fail/aborted (refund_failed) or all but confirmed
    successes (refund_unconfirmed)."""
    billing = "success_only" if success_only else billing
    parts = partitions(history, scope, seed, runs)
    if success_only:
        # Fit and score only known outcomes; fold assignments stay unchanged.
        parts = [(f, [t for t in tr if t.task.outcome != "unknown"],
                  [t for t in te if t.task.outcome != "unknown"]) for f, tr, te in parts]
    if not parts:
        return []
    pooled_draws, fold_draws = refit_draws(history, scope, seed, runs, billing, draws, impute)
    result = []
    for mode, capped in SCENARIOS:
        fitted = []
        for fold, training, evaluation in parts:
            tail = tail_increment(training)
            p99 = quantile([t.cost for t in training if t.complete and not t.task.capped], 0.99)
            cap = p99 if capped else None
            train = scenario_tasks(training, mode, tail)
            test = scenario_tasks(evaluation, mode, tail)
            if not train or not test or p99 is None:
                break
            if impute:
                test += imputed_tasks(evaluation, mode, tail, p99)
            train = [(t, *replay(costs, cap)) for t, costs in train]
            test = [(t, *replay(costs, cap)) for t, costs in test]
            n_billable = sum(billable(t, stopped, billing) for t, _, stopped in train)
            spend = sum(cost for _, cost, _ in train)
            if not n_billable or spend <= 0:
                break
            fitted.append((fold, train, test, cap, tail, spend / n_billable))
        if len(fitted) != len(parts):
            continue
        pooled_ratio = pooled_draws[(mode, capped)]
        fold_ratio = fold_draws[(mode, capped)].ravel()
        for target in targets:
            records, folds = [], []
            for fold, train, test, cap, tail, mean in fitted:
                price = mean / target
                paid = [price if billable(t, stopped, billing) else 0.0
                        for t, _, stopped in test]
                records += [(cost, p, stopped) for (_, cost, stopped), p in zip(test, paid)]
                folds.append({"fold": fold, "price": price, "cap": cap, "tail_increment": tail,
                              "train_groups": groups(train), "test_groups": groups(test),
                              "train_uncapped_groups": groups(train, True),
                              "test_uncapped_groups": groups(test, True),
                              "n_train": len(train), "n_test": len(test),
                              "train_billable": sum(billable(t, s, billing)
                                                    for t, _, s in train),
                              "loss_ratio": sum(c for _, c, _ in test) / sum(paid)
                              if sum(paid) else None})
            revenue = sum(r[1] for r in records)
            if revenue <= 0:
                continue
            # Verdict interval: loss ratio of one held-out fold, a price fit on the other
            # groups. The pooled ratio nearly cancels to the target, so its band is narrow.
            samples = target * fold_ratio
            pooled = target * pooled_ratio
            result.append({
                "scope": scope, "billing": billing,
                "unpriced": "p99" if impute else "excluded",
                "censoring": mode, "capped": capped, "target": target,
                "price": float(np.mean([f["price"] for f in folds])),
                "price_basis": "mean of separately fitted fold prices",
                "cap": None, "tail_increment": None,
                "loss_ratio": sum(r[0] for r in records) / revenue,
                "ci": interval(samples[np.isfinite(samples)]),
                "pooled_ci": interval(pooled[np.isfinite(pooled)]),
                "tasks_lost": sum(r[0] > r[1] for r in records) / len(records),
                "worst_loss": max(0.0, max(r[0] - r[1] for r in records)),
                "stopped": sum(r[2] for r in records) / len(records),
                "n_train": min(f["n_train"] for f in folds), "n_test": len(records),
                "train_uncapped": min(f["train_uncapped_groups"] for f in folds),
                "test_uncapped": min(f["test_uncapped_groups"] for f in folds),
                "folds": folds, "draws": draws,
                "draws_valid": int(np.isfinite(pooled).sum()),
                "_samples": samples,
            })
    return result


class Arrays:
    """Complete tasks as padded cumulative-cost rows, for vectorized cap replay.

    With impute, unpriced tasks are added as one-call rows whose cost is set per fold;
    their total holds the known partial spend until then.
    """

    def __init__(self, history, runs=None, impute=False):
        self.groups = group_order(history)
        index = {g: i for i, g in enumerate(self.groups)}
        tasks = [t for t in history if t.complete or impute]
        width = max((len(t.costs) for t in tasks), default=1)
        self.cumulative = np.full((len(tasks), width), np.inf)
        self.unpriced = np.array([not t.complete for t in tasks], dtype=bool)
        for i, t in enumerate(tasks):
            if t.complete:
                self.cumulative[i, : len(t.costs)] = np.cumsum(t.costs)
        self.n_calls = np.array([len(t.costs) if t.complete else 1 for t in tasks], dtype=int)
        self.total = np.where(self.unpriced, [t.cost for t in tasks],
                              self.cumulative[np.arange(len(tasks)), self.n_calls - 1])
        self.capped = np.array([t.task.capped for t in tasks], dtype=bool)
        self.success = np.array([t.task.outcome == "success" for t in tasks], dtype=bool)
        self.known = np.array([t.task.outcome != "unknown" for t in tasks], dtype=bool)
        self.refunded = np.array([t.task.outcome in ("fail", "aborted") for t in tasks],
                                 dtype=bool)
        self.group = np.array([index[group_key(t)] for t in tasks], dtype=int)
        run_names = run_order(history, runs) if runs else []
        self.run = np.array([run_names.index(runs[t.task.task_id]) for t in tasks]
                            if runs else [], dtype=int)
        self.n_runs = len(run_names)


def ratios(a, weight, fold, n_folds, billing="all_tasks", grouped=True):
    """Out-of-fold cost / (price × target) per scenario, pooled and per held-out fold.

    Loss ratio = target × ratio. Returns ({scenario: pooled}, {scenario: [per fold]}).
    """
    totals = {s: [0.0, 0.0] for s in SCENARIOS}
    per_fold = {s: [] for s in SCENARIOS}
    failed = ({s: np.nan for s in SCENARIOS}, {s: [np.nan] * n_folds for s in SCENARIOS})
    base = weight > 0
    if billing == "success_only":
        base &= a.known
    rows = np.arange(len(a.total))
    for f in range(n_folds):
        # Unpriced tasks are never fit on; they are only present to be scored.
        train, test = base & (fold != f) & ~a.unpriced, base & (fold == f)
        if grouped and np.intersect1d(a.group[train], a.group[test]).size:
            raise AssertionError("a task group appears in both training and scoring")
        uncapped = train & ~a.capped
        if not uncapped.any():
            return failed
        values = np.repeat(a.total[uncapped], weight[uncapped])
        threshold, cap = np.quantile(values, [0.95, 0.99])
        tail = values[values >= threshold].mean()
        # Cumulative costs are nondecreasing, so the first crossing is a prefix count.
        crossing = (a.cumulative <= cap).sum(axis=1)
        crossed_cost = a.cumulative[rows, np.minimum(crossing, a.n_calls - 1)]
        total = a.total
        if a.unpriced.any():
            imputed = np.maximum(a.total, cap)  # cap is this fold's training p99
            total = np.where(a.unpriced, imputed, a.total)
            crossing = np.where(a.unpriced, (imputed <= cap).astype(int), crossing)
            crossed_cost = np.where(a.unpriced, imputed, crossed_cost)
        crossed = crossing < a.n_calls
        for mode in ("exclude", "inflate"):
            inflated = a.capped if mode == "inflate" else np.zeros_like(a.capped)
            include = np.ones_like(a.capped) if mode == "inflate" else ~a.capped
            raw = total + inflated * tail
            # An inflated tail is one more indivisible call, so crossing earlier stops work.
            stop = crossed & ((crossing < a.n_calls - 1) | inflated)
            for capped in (False, True):
                key = (mode, capped)
                cost = np.where(crossed, crossed_cost, raw) if capped else raw
                stopped = stop if capped else np.zeros_like(stop)
                if billing == "all_tasks":
                    bill = np.ones_like(stopped)
                elif billing == "refund_failed":
                    bill = ~a.refunded & ~stopped
                else:
                    bill = a.success & ~stopped
                tr, te = train & include, test & include
                spend = (weight * cost)[tr].sum()
                n_billable = (weight * bill)[tr].sum()
                if not tr.any() or not te.any() or not n_billable or spend <= 0:
                    totals[key] = None
                    per_fold[key].append(np.nan)
                    continue
                cost_te = (weight * cost)[te].sum()
                revenue = spend / n_billable * (weight * bill)[te].sum()
                per_fold[key].append(cost_te / revenue if revenue > 0 else np.nan)
                if totals[key] is not None:
                    totals[key][0] += cost_te
                    totals[key][1] += revenue
    pooled = {s: v[0] / v[1] if v and v[1] > 0 else np.nan for s, v in totals.items()}
    return pooled, per_fold


def refit_draws(history, scope, seed=0, runs=None, billing="all_tasks", draws=DRAWS,
                impute=False):
    """Cluster bootstrap: whole groups with replacement, full CV refit in every draw."""
    a = Arrays(history, runs if scope == "leave_one_run_out" else None, impute)
    rng = np.random.default_rng(seed)
    n = len(a.groups)
    n_folds = FOLDS if scope == "grouped_cv" else a.n_runs
    pooled = {s: np.full(draws, np.nan) for s in SCENARIOS}
    held_out = {s: np.full((draws, n_folds), np.nan) for s in SCENARIOS}
    if not len(a.total):
        return pooled, held_out
    for d in range(draws):
        counts = np.bincount(rng.integers(0, n, n), minlength=n)
        if scope == "grouped_cv":
            # Every copy of a drawn group joins the same fold.
            drawn = rng.permutation(np.flatnonzero(counts))
            fold_of = np.full(n, -1)
            fold_of[drawn] = np.arange(len(drawn)) % FOLDS
            fold = fold_of[a.group]
        else:
            fold = a.run
        values, folds = ratios(a, counts[a.group], fold, n_folds, billing,
                               grouped=scope == "grouped_cv")
        for s in SCENARIOS:
            pooled[s][d] = values[s]
            held_out[s][d] = folds[s]
    return pooled, held_out

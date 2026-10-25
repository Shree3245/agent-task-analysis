import numpy as np
from agent_task_analysis.analysis.bootstrap import bootstrap_means, bootstrap_ratios, interval
from agent_task_analysis.analysis.caps import replay
from agent_task_analysis.analysis.censoring import imputed_tasks, scenario_tasks, tail_increment
from agent_task_analysis.analysis.shape import quantile


def billable(task, stopped, billing):
    """Whether a task pays the price. A cap-stopped task is refunded under every refund rule."""
    if billing == "all_tasks":
        return True
    if stopped:
        return False
    if billing == "refund_failed":
        return task.task.outcome not in ("fail", "aborted")
    return task.task.outcome == "success"  # success_only, refund_unconfirmed


def simulations(training, evaluation, targets, *, scope, seed=0, impute=False,
                billing="all_tasks"):
    """billing other than all_tasks: price = training spend / (target × billable training
    tasks); revenue is that price times billable held-out tasks."""
    if billing != "all_tasks":
        return billed_simulations(training, evaluation, targets, scope=scope, seed=seed,
                                  impute=impute, billing=billing)
    results = []
    tail = tail_increment(training)
    uncapped = [t.cost for t in training if t.complete and not t.task.capped]
    recommended = quantile(uncapped, 0.99)
    for mode in ("exclude", "inflate"):
        train = scenario_tasks(training, mode, tail)
        test = scenario_tasks(evaluation, mode, tail)
        if impute:
            if recommended is None or test is None:
                continue
            test = test + imputed_tasks(evaluation, mode, tail, recommended)
        for capped in (False, True):
            if not train or not test or (capped and recommended is None):
                continue
            cap = recommended if capped else None
            train_costs = [replay(costs, cap)[0] for _, costs in train]
            eval_costs = np.array([replay(costs, cap)[0] for _, costs in test])
            mean = float(np.mean(train_costs))
            # Resample a canonical order: storage order follows keyed IDs, which differ
            # per install, and seeded draws must not depend on them.
            means = bootstrap_means(np.sort(eval_costs), seed=seed)
            for target in targets:
                price = mean / target
                if price <= 0:
                    continue
                lr_samples = means / price
                results.append(
                    {
                        "scope": scope,
                        "unpriced": "p99" if impute else "excluded",
                        "censoring": mode,
                        "capped": capped,
                        "cap": cap,
                        "tail_increment": tail,
                        "target": target,
                        "price": price,
                        "loss_ratio": float(eval_costs.mean() / price),
                        "ci": interval(lr_samples),
                        "tasks_lost": float(np.mean(eval_costs > price)),
                        "worst_loss": max(0.0, float(eval_costs.max() - price)),
                        "n_train": len(train),
                        "n_test": len(test),
                        "train_uncapped": sum(not t.task.capped for t, _ in train),
                        "test_uncapped": sum(not t.task.capped for t, _ in test),
                        "stopped": sum(replay(costs, cap)[1] for _, costs in test) / len(test),
                        "_samples": lr_samples,
                        "_means": means,
                    }
                )
    return results


def macro_simulations(groups):
    """Equal type contributions; never pool costs/revenue by task count."""
    if not groups:
        return []
    indexed = [
        {(r["scope"], r["censoring"], r["capped"], r["target"]): r for r in g} for g in groups
    ]
    common = set.intersection(*(set(g) for g in indexed))
    result = []
    for key in sorted(common):
        rs = [g[key] for g in indexed]
        if len({len(r["_samples"]) for r in rs}) > 1:
            continue
        samples = np.mean([r["_samples"] for r in rs], axis=0)
        row = {k: rs[0][k] for k in ("scope", "censoring", "capped", "target")}
        for name in ("price", "loss_ratio", "tasks_lost", "stopped"):
            row[name] = float(np.mean([r[name] for r in rs]))
        row.update(
            ci=interval(samples),
            worst_loss=max(r["worst_loss"] for r in rs),
            n_train=sum(r["n_train"] for r in rs),
            n_test=sum(r["n_test"] for r in rs),
            cap=None,
            tail_increment=None,
            _samples=samples,
        )
        result.append(row)
    return result


def billed_simulations(training, evaluation, targets, *, scope, seed, impute, billing):
    results = []
    tail = tail_increment(training)
    uncapped = [t.cost for t in training if t.complete and not t.task.capped]
    recommended = quantile(uncapped, 0.99)
    for mode in ("exclude", "inflate"):
        train = scenario_tasks(training, mode, tail)
        test = scenario_tasks(evaluation, mode, tail)
        if impute:
            if recommended is None or test is None:
                continue
            test = test + imputed_tasks(evaluation, mode, tail, recommended)
        for capped in (False, True):
            if not train or not test or (capped and recommended is None):
                continue
            cap = recommended if capped else None
            fit = [(t, *replay(costs, cap)) for t, costs in train]
            scored = [(t, *replay(costs, cap)) for t, costs in test]
            spend = sum(cost for _, cost, _ in fit)
            n_billable = sum(billable(t, stopped, billing) for t, _, stopped in fit)
            costs = np.array([cost for _, cost, _ in scored])
            bills = np.array([billable(t, stopped, billing) for t, _, stopped in scored], dtype=float)
            if spend <= 0 or not n_billable or not bills.sum():
                continue
            # Canonical order for seeded resampling, as in the all-tasks path.
            order = np.lexsort((bills, costs))
            ratios = bootstrap_ratios(costs[order], bills[order], seed=seed)
            for target in targets:
                price = spend / n_billable / target
                revenue = price * bills
                samples = ratios[np.isfinite(ratios)] / price
                results.append({
                    "scope": scope, "billing": billing,
                    "unpriced": "p99" if impute else "excluded",
                    "censoring": mode, "capped": capped, "cap": cap, "tail_increment": tail,
                    "target": target, "price": price,
                    "loss_ratio": float(costs.sum() / revenue.sum()),
                    "ci": interval(samples),
                    "tasks_lost": float(np.mean(costs > revenue)),
                    "worst_loss": max(0.0, float((costs - revenue).max())),
                    "n_train": len(train), "n_test": len(test),
                    "train_uncapped": sum(not t.task.capped for t, _ in train),
                    "test_uncapped": sum(not t.task.capped for t, _ in test),
                    "train_billable": n_billable, "test_billable": int(bills.sum()),
                    "stopped": sum(s for _, _, s in scored) / len(scored),
                    "draws": len(ratios), "draws_valid": int(np.isfinite(ratios).sum()),
                    "_samples": samples,
                })
    return results

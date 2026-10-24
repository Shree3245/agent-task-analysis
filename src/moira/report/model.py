from collections import defaultdict
from dataclasses import fields
from datetime import datetime, timezone
import hashlib
import numpy as np

from moira.analysis.audit import audit
from moira.analysis.backtest import time_split
from moira.analysis.benchmark import outcome_summary
from moira.analysis.grouped import cross_validate, validation_basis
from moira.analysis.caps import cap_table
from moira.analysis.drift import data_end, drift, projection, recency, weekly
from moira.analysis.fixed_price import macro_simulations, simulations
from moira.analysis.history import build_history
from moira.analysis.shape import cost_shape
from moira.analysis.verdicts import UNPRICED_LIMIT, verdict
from moira.pricing.catalog import change_dates
from moira.pricing.reprice import reconcile
from moira.privacy import redacted_id
from moira.report.charts import distribution, loss_curve
from moira.schema import Call, Task


def receipts(history, rows, target, scope="holdout"):
    selected = next(
        (
            r
            for r in rows
            if r["scope"] == scope
            and r["censoring"] == "exclude"
            and r["capped"]
            and r["target"] == target
        ),
        None,
    )
    selected = selected or next(
        (
            r
            for r in rows
            if r["scope"] == "in_sample"
            and r["censoring"] == "exclude"
            and r["capped"]
            and r["target"] == target
        ),
        None,
    )
    ordered = sorted(history, key=lambda t: t.cost)
    indices = sorted(
        set(int(round(i)) for i in np.linspace(0, max(0, len(ordered) - 1), min(5, len(ordered))))
    )
    result = []
    for index in indices:
        task = ordered[index]
        tool_groups = defaultdict(list)
        unlinked = defaultdict(int)
        for c in task.task.calls:
            if c.event_kind == "tool":
                if c.parent_call_idx is None:
                    unlinked[c.tool_name] += 1
                else:
                    tool_groups[c.parent_call_idx].append(c.tool_name)
        groups = {}
        for c in task.task.calls:
            if c.event_kind != "model":
                continue
            names = sorted(set(tool_groups[c.call_idx]))
            name = (
                names[0]
                if len(names) == 1
                else "Shared tools: " + ", ".join(names)
                if names
                else "Model-only calls"
            )
            group = groups.setdefault(
                name, {"tool": name, "calls": 0, "cost": 0.0, "unknown": False}
            )
            group["calls"] += 1
            cost = task.per_call[c.call_idx]
            group["unknown"] |= cost is None
            group["cost"] += cost or 0
        for name, count in unlinked.items():
            groups["unlinked:" + name] = {
                "tool": name + " (unlinked tool events)",
                "calls": count,
                "cost": None,
                "unknown": True,
            }
        result.append(
            {
                "task_id": task.task.task_id,
                "task_type": task.task.task_type,
                "fixed_price": selected["price"] if selected else None,
                "price_basis": selected["scope"] if selected else "unavailable",
                "known_cost": task.cost,
                "complete": task.complete,
                "outcome": task.task.outcome,
                "capped": task.task.capped,
                "groups": list(groups.values()),
            }
        )
    return result


SUCCESS_TARGETS = (0.6, 0.65, 0.7)


def highest_success_target(rows, success, imputed, history, min_samples):
    """Highest success-only target that passes the same VIABLE rule, with its price."""
    def price(table, billing, target):
        row = next((r for r in table if r["scope"] == "grouped_cv" and r["billing"] == billing
                    and r["censoring"] == "exclude" and r["capped"]
                    and abs(r["target"] - target) < 1e-9), None)
        return row["price"] if row else None

    result = {"per_task_price_70": price(rows, "all_tasks", 0.7), "target": None,
              "price_per_resolved": None}
    for target in sorted(SUCCESS_TARGETS, reverse=True):
        v = verdict(success, history, min_samples, "grouped_cv", target=target, imputed=imputed)
        if v["label"] == "VIABLE":
            result.update(target=target, price_per_resolved=price(success, "success_only", target))
            break
    result["reason"] = None if result["target"] else v["reason"]
    return result


REFUND_RULES = ("refund_failed", "refund_unconfirmed")


def refunds(typed, train, test, grouped, target, seed, min_samples, stress):
    """Refund-adjusted prices on the verdict split: failed/aborted tasks are refunded
    (unknown outcomes still pay), and the bound where only confirmed successes pay."""
    result = {}
    scope = "grouped_cv" if grouped else "holdout"
    for rule in REFUND_RULES:
        if grouped:
            rows = cross_validate(typed, [target], scope=scope, seed=seed, billing=rule)
            imputed = cross_validate(typed, [target], scope=scope, seed=seed, billing=rule,
                                     impute=True) if stress else []
        else:
            rows = simulations(train, test, [target], scope=scope, seed=seed, billing=rule)
            imputed = simulations(train, test, [target], scope=scope, seed=seed, billing=rule,
                                  impute=True) if stress else []
        row = next((r for r in rows if r["censoring"] == "exclude" and r["capped"]), None)
        result[rule] = {"row": row, "verdict": verdict(rows, typed, min_samples, scope,
                                                       target=target, imputed=imputed)}
    return result


def make_report(
    tasks, evidence, catalog, *, target=0.7, redact=False, seed=0, min_samples=30, repeat=3,
    recent_days=30, window=None,
):
    history = build_history(tasks, catalog)
    end = data_end(history)
    overrides = catalog.get("overrides")
    benchmark = any(x.get("benchmark") for x in evidence.get("imports", []))
    runs = {k: v["run_id"] for k, v in evidence.get("benchmark_assignments", {}).items()
            if v.get("run_id")}
    cutoff, train, test, dropped = time_split(history)
    names = sorted({t.task.task_type for t in history})
    targets = sorted(set([0.6, 0.7, 0.8, target]))
    success_targets = sorted(set(targets) | set(SUCCESS_TARGETS))
    groups, all_values, weights = [], [], []
    for name in names:
        typed = [t for t in history if t.task.task_type == name]
        values = [t.cost for t in typed if t.complete and not t.task.capped]
        local_seed = (seed + int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)) % 2**32
        rows = simulations(typed, typed, targets, scope="in_sample", seed=local_seed)
        typed_train = [t for t in train if t.task.task_type == name]
        typed_test = [t for t in test if t.task.task_type == name]
        rows += simulations(typed_train, typed_test, targets, scope="holdout", seed=local_seed)
        # Under the unpriced limit, the verdict must also hold with each unpriced task
        # scored at the training p99; these rows are that stress test.
        unpriced = sum(not t.complete for t in typed)
        stress = 0 < unpriced < UNPRICED_LIMIT * len(typed)
        imputed, success_imputed = [], []
        chart_row = next(
            (
                r
                for r in rows
                if r["scope"] == "holdout"
                and r["capped"]
                and r["censoring"] == "exclude"
                and r["target"] == 0.7
            ),
            None,
        )
        chart_row = chart_row or next(
            (r for r in rows if r["capped"] and r["censoring"] == "exclude" and r["target"] == 0.7),
            None,
        )
        success_billing = []
        basis = validation_basis(typed)
        grouped = basis["split"] == "grouped_cv"
        if grouped:
            # Repeated groups leak across a time split; it stays as a diagnostic column only.
            for scope in ("grouped_cv", "leave_one_run_out"):
                rows += cross_validate(typed, targets, scope=scope, seed=local_seed, runs=runs)
                if benchmark:
                    success_billing += cross_validate(typed, success_targets, scope=scope,
                                                      seed=local_seed, runs=runs,
                                                      success_only=True)
            if stress:
                imputed = cross_validate(typed, targets, scope="grouped_cv", seed=local_seed,
                                         impute=True)
                if benchmark:
                    success_imputed = cross_validate(typed, success_targets, scope="grouped_cv",
                                                     seed=local_seed, success_only=True,
                                                     impute=True)
        elif stress:
            imputed = simulations(typed_train, typed_test, targets, scope="holdout",
                                  seed=local_seed, impute=True)
            chart_row = next((r for r in rows if r["scope"] == "in_sample" and r["capped"]
                              and r["censoring"] == "exclude" and r["target"] == .7), None)
        fit = typed if grouped else typed_train
        # Refunds change nothing unless some known outcome exists and some task is not a
        # confirmed success.
        outcomes_known = (any(t.task.outcome != "unknown" for t in typed)
                          and any(t.task.outcome != "success" for t in typed))
        spend = sum(t.cost for t in typed)
        groups.append(
            {
                "complete_spend": sum(t.cost for t in typed if t.complete),
                "drift": drift(fit, typed, end, recent_days, min_samples),
                "weekly": weekly(typed),
                "recency": recency(typed, typed_train, typed_test, cutoff, end, recent_days,
                                   target, local_seed, min_samples),
                "refunds": refunds(typed, typed_train, typed_test, grouped, target, local_seed,
                                   min_samples, stress) if outcomes_known else None,
                "override_share": sum(t.override_cost for t in typed) / spend
                if overrides and spend else None,
                "name": name,
                "n_total": len(typed),
                "n_capped": sum(t.task.capped for t in typed),
                "n_unpriced": sum(not t.complete for t in typed),
                "shape": cost_shape(values),
                "audit": audit(typed, repeat=repeat),
                "caps": cap_table(typed),
                "simulations": rows,
                "grouped": grouped,
                "validation": basis,
                "verdict": verdict(rows, typed, min_samples, "grouped_cv" if grouped else "holdout",
                                   imputed=imputed),
                "imputed": imputed,
                "success_viable": highest_success_target(rows, success_billing, success_imputed,
                                                         typed, min_samples)
                if success_billing else None,
                "outcomes": outcome_summary(typed),
                "success_billing": success_billing,
                "receipts": receipts(typed, rows, target, "in_sample" if grouped else "holdout"),
                "distribution": distribution(values, name),
                "loss_curve": loss_curve(chart_row, name) if chart_row else None,
            }
        )
        if values:
            all_values.extend(values)
            weights.extend([1 / len(values)] * len(values))
    projections = []
    future = [d for d in change_dates(catalog) if end and d > end.date().isoformat()]
    split_ids = ({t.task.task_id for t in train}, {t.task.task_id for t in test})
    for date in future:
        at = build_history(tasks, catalog, as_of=date)
        changing = sorted(key for key, rates in catalog["models"].items()
                          if any(c["effective"] == date for c in rates.get("changes", [])))
        for g in groups:
            typed = [t for t in at if t.task.task_type == g["name"]]
            base = next((r for r in g["simulations"] if r["scope"] == "holdout"
                         and r["censoring"] == "exclude" and r["capped"]
                         and abs(r["target"] - target) < 1e-9), None)
            local_seed = (seed + int(hashlib.sha256(g["name"].encode()).hexdigest()[:8], 16)) % 2**32
            projections.append({"type": g["name"], "date": date, "models": changing,
                                "price_now": base["price"] if base else None,
                                **projection(typed, *split_ids, base["price"] if base else None,
                                             g["complete_spend"], end, recent_days,
                                             target, local_seed)})
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window": window,
        "data_end": end.isoformat() if end else None,
        "recent_days": recent_days,
        "drift_limit": 0.25,
        "rate_changes": change_dates(catalog),
        "future_rate_changes": future,
        "projections": projections,
        "overrides": overrides,
        "groups": groups,
        "overall_shape": cost_shape(all_values, weights) if weights else {"n": 0},
        "overall_simulations": macro_simulations([g["simulations"] for g in groups]),
        "evidence": evidence,
        "catalog": {k: catalog[k] for k in ("version", "sha256", "description")},
        "retained_call_fields": [f.name for f in fields(Call)],
        "retained_task_fields": [f.name for f in fields(Task) if f.name != "calls"],
        "reconciliation": reconcile(tasks, catalog),
        "verdict_scope": "grouped_cv" if any(g["grouped"] for g in groups) else "holdout",
        "grouped": any(g["grouped"] for g in groups),
        "run_ids": bool(runs),
        "task_groups": sum(bool(t.task_group) for t in tasks),
        "cutoff": cutoff,
        "split_excluded": dropped,
        "n_tasks": len(tasks),
        "known_spend": sum(t.cost for t in history),
        "target": target,
        "min_samples": min_samples,
        "seed": seed,
        "redacted": redact,
        "benchmark": benchmark,
        "priced_types": sum(bool(g["shape"]["n"]) for g in groups),
    }
    result["source_formula_verification"] = None
    if evidence.get("source_formula") == "bai-sonnet-3.7":
        from moira.pricing.reprice import call_cost
        n = matches = 0
        for task in tasks:
            for call in task.calls:
                if call.event_kind != "model" or call.recorded_cost is None:
                    continue
                n += 1
                cost, _ = call_cost(call, catalog)
                if cost is not None:
                    matches += abs(cost + call.cache_write_input_tokens * 3 / 1e6
                                   - call.recorded_cost) <= max(1e-12, call.recorded_cost * .01)
        result["source_formula_verification"] = {"calls": n, "matches": matches,
                                                "verified": n > 0 and matches == n}
    result["overall_caps"] = []
    for index in range(3):
        present = [g["caps"][index] for g in groups if len(g["caps"]) == 3]
        if present:
            result["overall_caps"].append(
                {
                    "quantile": present[0]["quantile"],
                    "types": len(present),
                    "stopped": float(np.mean([r["stopped"] for r in present])),
                    "saved_per_task": float(np.mean([r["saved"] / r["n"] for r in present])),
                    "saved_share": float(
                        np.mean([r["saved_share"] for r in present if r["saved_share"] is not None])
                    )
                    if any(r["saved_share"] is not None for r in present)
                    else None,
                }
            )
    result["overall_audit"] = (
        {
            k: float(np.mean([g["audit"][k] for g in groups]))
            for k in ("failed_aborted_fraction", "failed_aborted_spend_per_task", "loop_fraction")
        }
        if groups
        else {}
    )
    if redact:

        def walk(value):
            if isinstance(value, dict):
                return {k: redacted_id(v) if k == "task_id" else walk(v) for k, v in value.items()}
            if isinstance(value, list):
                return [walk(v) for v in value]
            return value

        result = walk(result)
    return result

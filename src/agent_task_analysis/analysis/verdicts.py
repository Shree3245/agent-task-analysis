UNPRICED_LIMIT = 0.02


def checks(rows, history, min_samples, scope, target):
    selected = {
        r["censoring"]: r
        for r in rows
        if r["scope"] == scope and r["capped"] and abs(r["target"] - target) < 1e-9
    }
    scenarios = ["exclude", "inflate"] if any(t.task.capped for t in history) else ["exclude"]
    reasons = []
    for scenario in scenarios:
        row = selected.get(scenario)
        if not row:
            reasons.append(f"{scenario}: no usable {scope} or positive fitted price")
            continue
        if min(row["train_uncapped"], row["test_uncapped"]) < min_samples:
            reasons.append(
                f"{scenario}: fewer than {min_samples} uncapped tasks in training or holdout"
            )
        if row.get("draws_valid", 0) < row.get("draws", 0):
            reasons.append(
                f"{scenario}: {row['draws'] - row['draws_valid']} of {row['draws']} refit draws unusable"
            )
        if row["ci"][1] >= 0.9:
            reasons.append(
                f"{scenario}: upper loss-ratio interval is {row['ci'][1]:.1%}, needs <90%"
            )
    disagreement = len(selected) == 2 and (
        (selected["exclude"]["ci"][1] < 0.9) != (selected["inflate"]["ci"][1] < 0.9)
    )
    if disagreement:
        reasons.append("Censoring scenarios disagree")
    return reasons, disagreement


def verdict(rows, history, min_samples=30, scope="holdout", target=0.7, imputed=None):
    """VIABLE needs the upper interval below 90% with the p99 cap under both censoring
    scenarios. Unpriced tasks must be under 2% of the pool, and the rule must also hold
    when each unpriced held-out task costs the training p99 (the imputed rows)."""
    unpriced = sum(not t.complete for t in history)
    share = unpriced / len(history) if history else 0.0
    reasons, disagreement = checks(rows, history, min_samples, scope, target)
    base = "NOT VIABLE" if reasons else "VIABLE"
    stressed = None
    if unpriced and share >= UNPRICED_LIMIT:
        reasons.insert(0, f"{unpriced} tasks ({share:.1%}) have unknown costs; the limit is under 2%")
    elif unpriced:
        extra, _ = checks(imputed or [], history, min_samples, scope, target)
        stressed = "NOT VIABLE" if extra else "VIABLE"
        reasons += [f"with unpriced tasks at training p99, {r}" for r in extra]
    viable = not reasons
    reason = "; ".join(reasons) if reasons else (
        f"{scope}: upper loss-ratio interval stays below 90% at the {target:.0%} target with p99 cap")
    if viable and unpriced:
        reason += f"; also with {unpriced} unpriced tasks ({share:.1%}) at the training p99 cost"
    return {
        "label": "VIABLE" if viable else "NOT VIABLE",
        "reason": reason,
        "censoring_disagreement": disagreement,
        "unpriced": unpriced,
        "unpriced_share": share,
        "unpriced_excluded": base,
        "unpriced_at_p99": stressed,
    }

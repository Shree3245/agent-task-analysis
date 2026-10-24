from moira.analysis.shape import quantile

CAP_QUANTILES = (0.95, 0.99, 0.995)


def replay(costs, cap):
    """Stop AFTER a completed call crosses the ceiling; retain that call's overshoot."""
    if cap is None:
        return sum(costs), False
    spent = 0.0
    for index, cost in enumerate(costs):
        spent += cost
        if spent > cap:
            return spent, index < len(costs) - 1
    return spent, False


def cap_table(history):
    usable = [t for t in history if t.complete and not t.task.capped]
    values = [t.cost for t in usable]
    if not values:
        return []
    rows = []
    for q in CAP_QUANTILES:
        cap = quantile(values, q)
        runs = [replay(t.costs, cap) for t in usable]
        total = sum(values)
        saved = total - sum(r[0] for r in runs)
        rows.append(
            {
                "quantile": q,
                "cap": cap,
                "n": len(usable),
                "stopped": sum(r[1] for r in runs) / len(runs),
                "saved": saved,
                "saved_share": saved / total if total else None,
                "ideal_stopped": sum(v > cap for v in values) / len(values),
                "ideal_saved": sum(max(0, v - cap) for v in values),
            }
        )
    return rows

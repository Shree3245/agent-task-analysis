from collections import Counter
from agent_task_analysis.pricing.catalog import rates_at
from agent_task_analysis.schema import TOKEN_FIELDS


def rate_key(call, catalog):
    key = f"{call.provider}/{call.model}"
    return catalog.get("aliases", {}).get(key, key)


def call_cost(call, catalog, as_of=None):
    """Rates in effect when the call started, or on `as_of` for a projection."""
    if call.event_kind == "tool":
        return 0.0, None
    rates = catalog["models"].get(rate_key(call, catalog))
    if rates is None:
        return None, "unknown_model"
    rates = rates_at(rates, as_of or call.ts_start)
    if any(getattr(call, k) is None for k in TOKEN_FIELDS):
        return None, "missing_usage"
    context = call.input_tokens + call.cached_input_tokens + call.cache_write_input_tokens
    tier = rates.get("long_context")
    if tier and context > tier["threshold"]:
        rates = rates | tier
    total = 0.0
    for field, name in zip(
        TOKEN_FIELDS, ("input", "cached_input", "cache_write", "output", "output")
    ):
        n = getattr(call, field)
        if n and rates.get(name) is None:
            return None, "missing_rate_class"
        total += n * (rates.get(name) or 0)
    return total / 1_000_000, None


def reconcile(tasks, catalog):
    counts = Counter()
    unknown = Counter()
    mismatches = []
    totals = {"recorded": 0.0, "repriced_comparable": 0.0, "recorded_comparable": 0.0}
    cache_write_diagnostic = Counter()
    for task in tasks:
        for call in task.calls:
            if call.event_kind != "model":
                continue
            counts["model_calls"] += 1
            cost, reason = call_cost(call, catalog)
            if reason:
                counts[reason] += 1
                if reason == "unknown_model":
                    unknown[f"{call.provider}/{call.model}"] += 1
            if call.recorded_cost is not None:
                counts["recorded_calls"] += 1
                totals["recorded"] += call.recorded_cost
                if cost is not None:
                    counts["comparable_calls"] += 1
                    totals["repriced_comparable"] += cost
                    totals["recorded_comparable"] += call.recorded_cost
                    tolerance = max(1e-12, call.recorded_cost * 0.01)
                    if call.cache_write_input_tokens:
                        rates = rates_at(catalog["models"][rate_key(call, catalog)], call.ts_start)
                        tier = rates.get("long_context", {})
                        if (
                            tier
                            and call.input_tokens
                            + call.cached_input_tokens
                            + call.cache_write_input_tokens
                            > tier["threshold"]
                        ):
                            rates = rates | tier
                        cache_write_diagnostic["calls"] += 1
                        if (
                            abs(
                                cost
                                + call.cache_write_input_tokens * rates["input"] / 1e6
                                - call.recorded_cost
                            )
                            <= tolerance
                        ):
                            cache_write_diagnostic["matches"] += 1
                    if abs(cost - call.recorded_cost) <= tolerance:
                        counts["within_one_percent"] += 1
                    elif len(mismatches) < 20:
                        mismatches.append(
                            {
                                "task_id": task.task_id,
                                "call_idx": call.call_idx,
                                "recorded": call.recorded_cost,
                                "repriced": cost,
                            }
                        )
    n, comparable = counts["recorded_calls"], counts["comparable_calls"]
    return dict(counts) | {
        "agreement": counts["within_one_percent"] / n if n else None,
        "comparable_agreement": counts["within_one_percent"] / comparable if comparable else None,
        "acceptance": "UNAVAILABLE"
        if not n
        else "PASS"
        if counts["within_one_percent"] / n >= 0.99
        else "FAIL",
        "unknown_models": dict(unknown),
        "mismatches": mismatches,
        "totals": totals,
        "extra_cache_write_input_charge_diagnostic": dict(cache_write_diagnostic),
    }

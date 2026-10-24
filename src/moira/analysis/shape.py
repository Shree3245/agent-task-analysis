import math
import numpy as np


def quantile(values, q):
    return float(np.quantile(values, q, method="linear")) if len(values) else None


def weighted_quantile(values, weights, q):
    pairs = sorted(zip(values, weights))
    threshold = q * sum(weights)
    cumulative = 0
    for value, weight in pairs:
        cumulative += weight
        if cumulative >= threshold - 1e-14:
            return float(value)
    return float(pairs[-1][0]) if pairs else None


def cost_shape(values, weights=None):
    if not len(values):
        return {"n": 0}
    values = np.asarray(values, dtype=float)
    weighted = weights is not None
    weights = np.asarray(weights if weighted else np.ones(len(values)) / len(values), dtype=float)
    weights /= weights.sum()

    def q(p):
        return weighted_quantile(values, weights, p) if weighted else quantile(values, p)

    p50, p90 = q(0.5), q(0.9)
    spend = float(np.dot(values, weights))

    def tail_share(fraction):
        if spend == 0:
            return None
        if not weighted:
            return float(
                np.sort(values)[-max(1, math.ceil(len(values) * fraction)) :].sum() / values.sum()
            )
        remaining, total = fraction, 0.0
        for i in np.argsort(values)[::-1]:
            take = min(remaining, weights[i])
            total += take * values[i]
            remaining -= take
            if remaining < 1e-14:
                break
        return total / spend

    return {
        "n": len(values),
        "mean": spend,
        "median": p50,
        "p90": p90,
        "p99": q(0.99),
        "max": float(values.max()),
        "p90_p50": p90 / p50 if p50 else None,
        "top_1_share": tail_share(0.01),
        "top_5_share": tail_share(0.05),
    }

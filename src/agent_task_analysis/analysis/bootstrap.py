import numpy as np

DRAWS = 2000


def bootstrap_means(costs, seed=0, draws=DRAWS):
    """Bounded batches: no O(draws * all_dataset_tasks) allocation."""
    if not len(costs):
        return np.array([])
    costs = np.asarray(costs, dtype=float)
    rng = np.random.default_rng(seed)
    result = []
    batch = max(1, min(64, 1_000_000 // len(costs)))
    for start in range(0, draws, batch):
        ix = rng.integers(0, len(costs), size=(min(batch, draws - start), len(costs)))
        result.extend(costs[ix].mean(axis=1))
    return np.asarray(result)


def interval(samples):
    return [float(v) for v in np.quantile(samples, [0.05, 0.95])] if len(samples) else None


def bootstrap_ratios(costs, bills, seed=0, draws=DRAWS):
    """Paired task resamples of total cost / billable tasks; nan when a draw bills nothing."""
    if not len(costs):
        return np.array([])
    costs, bills = np.asarray(costs, dtype=float), np.asarray(bills, dtype=float)
    rng = np.random.default_rng(seed)
    result = []
    batch = max(1, min(64, 1_000_000 // len(costs)))
    for start in range(0, draws, batch):
        ix = rng.integers(0, len(costs), size=(min(batch, draws - start), len(costs)))
        billed = bills[ix].sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            result.extend(np.where(billed > 0, costs[ix].sum(axis=1) / billed, np.nan))
    return np.asarray(result)

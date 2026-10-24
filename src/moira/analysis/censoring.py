from moira.analysis.shape import quantile


def tail_increment(training):
    values = [t.cost for t in training if t.complete and not t.task.capped]
    if not values:
        return None
    threshold = quantile(values, 0.95)
    tail = [x for x in values if x >= threshold]
    return sum(tail) / len(tail)


def scenario_tasks(tasks, mode, increment):
    result = []
    for task in tasks:
        if not task.complete:
            continue
        if task.task.capped:
            if mode == "exclude":
                continue
            if increment is None:
                return None
            # An unresolved future tail is modeled as one additional indivisible call.
            # This is conservative relative to clipping the cost to the cap for free.
            result.append((task, [*task.costs, increment]))
        else:
            result.append((task, task.costs))
    return result


def imputed_tasks(tasks, mode, increment, p99):
    """Stress test for unpriced tasks: each costs the training p99 (or its known partial
    spend, if higher), charged as one indivisible call; censoring applies as usual."""
    result = []
    for task in tasks:
        if task.complete or (task.task.capped and mode == "exclude"):
            continue
        cost = max(task.cost, p99)
        result.append((task, [cost, increment] if task.task.capped else [cost]))
    return result

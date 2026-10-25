import math
from datetime import datetime


def time_split(tasks):
    starts = [datetime.fromisoformat(t.task.started_at) for t in tasks if t.task.started_at]
    ends = [datetime.fromisoformat(t.task.ended_at) for t in tasks if t.task.ended_at]
    if not starts or not ends or max(ends) <= min(starts):
        return None, [], [], len(tasks)
    cutoff = min(starts) + (max(ends) - min(starts)) * (2 / 3)
    training, evaluation = [], []
    for task in tasks:
        if not task.task.started_at or not task.task.ended_at:
            continue
        if datetime.fromisoformat(task.task.ended_at) < cutoff:
            training.append(task)
        elif datetime.fromisoformat(task.task.started_at) >= cutoff:
            evaluation.append(task)
    return cutoff.isoformat(), training, evaluation, len(tasks) - len(training) - len(evaluation)


def split_at(tasks, cutoff):
    """Training tasks end before the cutoff; held-out tasks start at or after it."""
    training, evaluation = [], []
    for task in tasks:
        if not task.task.started_at or not task.task.ended_at:
            continue
        if datetime.fromisoformat(task.task.ended_at) < cutoff:
            training.append(task)
        elif datetime.fromisoformat(task.task.started_at) >= cutoff:
            evaluation.append(task)
    return training, evaluation


def backdated_split(tasks, min_samples):
    """A cutoff for one pool whose share of the report-wide split is too small to test.

    The newest third of the pool's uncapped runs, and never fewer than `min_samples`, are
    held out; the cutoff moves back to the first of them. Training still ends before the
    cutoff, so the price is only tested on runs that came after everything it was fit on.
    Returns None when the pool cannot fill both sides.
    """
    timed = sorted((datetime.fromisoformat(t.task.started_at) for t in tasks
                    if t.task.started_at and t.task.ended_at and not t.task.capped))
    held = max(min_samples, math.ceil(len(timed) / 3))
    if len(timed) - held < min_samples:
        return None
    cutoff = timed[len(timed) - held]
    training, evaluation = split_at(tasks, cutoff)
    if min(sum(not t.task.capped for t in part) for part in (training, evaluation)) < min_samples:
        return None
    return cutoff.isoformat(), training, evaluation

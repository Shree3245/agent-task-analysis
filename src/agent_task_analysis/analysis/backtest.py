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

"""Deterministic synthetic histories for grouped-validation tests."""

from datetime import datetime, timedelta, timezone
import hashlib

import numpy as np

from moira.schema import Call, Task

START = datetime(2025, 1, 1, tzinfo=timezone.utc)


def task(task_id, tokens, start, *, group=None, capped=False, outcome="success", kind="code"):
    extra = {"task_group": hashlib.sha256(group.encode()).hexdigest()} if group else {}
    t = Task(task_id, kind, "synthetic", outcome=outcome, capped=capped,
             cap_reason="turn_limit" if capped else None, **extra)
    for i, n in enumerate(tokens):
        ts = (start + timedelta(seconds=i)).isoformat()
        t.calls.append(Call(task_id, i, ts, ts, "openai", "gpt-4o-mini",
                            input_tokens=int(n), cached_input_tokens=0, cache_write_input_tokens=0,
                            output_tokens=int(n // 10), reasoning_tokens=0))
    return t.finalize()


def ungrouped(n=240, seed=3):
    """Two task types, capped tail, timestamps spread evenly; no task_group."""
    rng = np.random.default_rng(seed)
    result = []
    for i in range(n):
        calls = rng.integers(1, 6)
        tokens = rng.lognormal(10, 0.8, calls)
        result.append(task(f"t{i}", tokens, START + timedelta(hours=i),
                           capped=i % 37 == 0, kind="code" if i % 3 else "review"))
    return result


def grouped(groups=50, runs=4, seed=5, capped_every=0):
    """Each group has its own cost level; runs are sequential in time."""
    rng = np.random.default_rng(seed)
    levels = rng.lognormal(10, 1.0, groups)
    result = []
    for r in range(runs):
        for g in range(groups):
            tokens = levels[g] * rng.lognormal(0, 0.05, 3)
            start = START + timedelta(days=30 * r, minutes=10 * g)
            capped = bool(capped_every) and (g * runs + r) % capped_every == 0
            result.append(task(f"run{r}:g{g}", tokens, start, group=f"instance-{g}",
                               capped=capped, outcome="fail" if g % 3 == 0 else "success"))
    return result


def run_assignments(tasks):
    return {t.task_id: {"run_id": hashlib.sha256(t.task_id.split(":")[0].encode()).hexdigest()}
            for t in tasks}


def unprice(tasks, every):
    """Give every n-th task one call with an unknown model: its cost becomes a lower bound."""
    for i, t in enumerate(tasks):
        if i % every == 0:
            ts = t.calls[-1].ts_end
            t.calls.append(Call(t.task_id, len(t.calls), ts, ts, "unknown", "unknown-model",
                                input_tokens=10, cached_input_tokens=0, cache_write_input_tokens=0,
                                output_tokens=1, reasoning_tokens=0))
            t.finalize()
    return tasks

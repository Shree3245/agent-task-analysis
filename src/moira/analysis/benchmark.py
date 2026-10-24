"""Benchmark outcome summaries."""


def outcome_summary(history):
    n = len(history)
    known = [t for t in history if t.task.outcome != "unknown"]
    successes = [t for t in history if t.task.outcome == "success"]
    priced = [t for t in history if t.complete]
    priced_successes = [t for t in priced if t.task.outcome == "success"]
    return {"tasks": n, "known_outcomes": len(known), "successes": len(successes),
            "success_rate": len(successes) / len(known) if known else None,
            "priced_tasks": len(priced), "priced_successes": len(priced_successes),
            "cost_per_success": sum(t.cost for t in priced) / len(priced_successes)
            if priced_successes else None,
            "iteration_limited": sum(t.task.cap_reason == "turn_limit" for t in history),
            "iteration_limit_share": sum(t.task.cap_reason == "turn_limit" for t in history) / n if n else None}

from collections import Counter
from agent_task_analysis.analysis.shape import quantile


def audit(history, repeat=3, call_multiple=2):
    p99 = quantile([t.task.n_calls for t in history], 0.99)
    loops = []
    for t in history:
        counts = Counter(
            (c.tool_name, c.tool_args_hash)
            for c in t.task.calls
            if c.event_kind == "tool" and c.tool_args_hash
        )
        repeated = [
            {"tool": name, "repeats": count}
            for (name, _), count in counts.items()
            if count >= repeat
        ]
        too_many = p99 is not None and t.task.n_calls > call_multiple * p99
        if repeated or too_many:
            loops.append(
                {
                    "task_id": t.task.task_id,
                    "repeated": repeated,
                    "calls": t.task.n_calls,
                    "above_call_threshold": too_many,
                    "known_cost": t.cost,
                }
            )
    return {
        "runaways": [
            {
                "task_id": t.task.task_id,
                "cost": t.cost,
                "complete": t.complete,
                "capped": t.task.capped,
                "outcome": t.task.outcome,
            }
            for t in sorted(history, key=lambda t: t.cost, reverse=True)[:10]
        ],
        "loops": loops[:50],
        "loop_tasks": len(loops),
        "repeat_threshold": repeat,
        "call_p99": p99,
        "call_threshold_multiple": call_multiple,
        "failed_aborted_spend": sum(
            t.cost for t in history if t.task.outcome in {"fail", "aborted"}
        ),
        "failed_aborted_fraction": sum(t.task.outcome in {"fail", "aborted"} for t in history)
        / len(history)
        if history
        else None,
        "failed_aborted_spend_per_task": sum(
            t.cost for t in history if t.task.outcome in {"fail", "aborted"}
        )
        / len(history)
        if history
        else None,
        "loop_fraction": len(loops) / len(history) if history else None,
        "known_spend": sum(t.cost for t in history),
        "censored_spend": sum(t.cost for t in history if t.task.capped),
    }

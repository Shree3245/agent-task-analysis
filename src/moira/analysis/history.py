from dataclasses import dataclass
from moira.pricing.reprice import call_cost, rate_key
from moira.schema import Task


@dataclass
class PricedTask:
    task: Task
    costs: list[float]
    complete: bool
    per_call: dict
    override_cost: float = 0.0

    @property
    def cost(self):
        return sum(self.costs)


def build_history(tasks, catalog, as_of=None):
    """as_of prices every call at the rates in effect on that date (a projection);
    otherwise each call uses the rates in effect when it started."""
    overridden = set((catalog.get("overrides") or {}).get("models", []))
    result = []
    for task in tasks:
        costs, per_call, override = [], {}, 0.0
        complete = task.n_calls > 0
        for call in task.calls:
            if call.event_kind != "model":
                continue
            cost, _ = call_cost(call, catalog, as_of)
            per_call[call.call_idx] = cost
            if cost is None:
                complete = False
            else:
                costs.append(cost)
                if rate_key(call, catalog) in overridden:
                    override += cost
        result.append(PricedTask(task, costs, complete, per_call, override))
    return result

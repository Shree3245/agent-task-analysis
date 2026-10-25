from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import math

from agent_task_analysis.privacy import IDENTITY_HASH, SafeError, label

TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_tokens",
)
CAP_REASONS = {"turn_limit", "dollar_limit", "time_limit", "other_limit"}


def number(value, integer=False):
    if value is None or value == "":
        return None
    try:
        n = float(value)
        if isinstance(value, bool) or not math.isfinite(n) or n < 0:
            raise ValueError
        if integer and (n != int(n) or n > 2**53):
            raise ValueError
        return int(n) if integer else n
    except (TypeError, ValueError, OverflowError):
        raise SafeError("invalid_nonnegative_number") from None


def timestamp(value):
    if value is None or value == "":
        return None
    try:
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, (float, int)) or str(value).isdigit():
            n = float(value)
            if n > 1e17:
                n /= 1e9
            elif n > 1e14:
                n /= 1e6
            elif n > 1e11:
                n /= 1e3
            dt = datetime.fromtimestamp(n, timezone.utc)
        else:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (ValueError, TypeError, OverflowError, OSError):
        raise SafeError("invalid_timestamp") from None


def status(value=None, capped=False, reason=None):
    """Inspect status metadata in memory; retain enums only."""
    s = str(value or "").lower()
    r = str(reason or "").lower()
    if reason in CAP_REASONS:
        cap = reason
    elif any(
        x in s + r for x in ("cost_limit", "budget", "dollar_limit", "costlimit", "exit_cost")
    ):
        cap = "dollar_limit"
    elif any(
        x in s + r
        for x in (
            "max_step",
            "max_turn",
            "iteration_limit",
            "turn_limit",
            "step_limit",
            "max_iter",
            "exit_round",
        )
    ) or ("iteration" in s + r and any(x in s + r for x in ("maximum", "limit", "exceed"))):
        cap = "turn_limit"
    elif any(x in s + r for x in ("timeout", "time_limit", "deadline")):
        cap = "time_limit"
    else:
        cap = "other_limit" if capped is True or str(capped).lower() == "true" else None
    if s in {"success", "successful", "completed", "resolved", "submitted", "ok", "true"}:
        outcome = "success"
    elif s in {"fail", "failed", "failure", "error", "false", "unresolved"} or s.startswith(
        "exit_error"
    ):
        outcome = "fail"
    elif cap or s in {"aborted", "cancelled", "canceled", "stopped", "interrupted"}:
        outcome = "aborted"
    else:
        outcome = "unknown"
    return outcome, bool(cap), cap


@dataclass
class Call:
    task_id: str
    call_idx: int
    ts_start: str | None = None
    ts_end: str | None = None
    provider: str = "unknown"
    model: str = "unknown"
    input_tokens: int | None = None
    cached_input_tokens: int | None = None
    cache_write_input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    tool_name: str | None = None
    tool_args_hash: str | None = None
    recorded_cost: float | None = None
    capped: bool = False
    event_kind: str = "model"
    parent_call_idx: int | None = None

    def row(self):
        return asdict(self)


@dataclass
class Task:
    task_id: str
    task_type: str = "unknown"
    source: str = "unknown"
    started_at: str | None = None
    ended_at: str | None = None
    n_calls: int = 0
    outcome: str = "unknown"
    capped: bool = False
    cap_reason: str | None = None
    # Hash of what makes two tasks the same work (e.g. a benchmark instance ID).
    task_group: str | None = None
    calls: list[Call] = field(default_factory=list, repr=False)

    def row(self):
        return {k: v for k, v in asdict(self).items() if k != "calls"}

    def finalize(self):
        self.task_id = label(self.task_id, limit=1024)
        self.task_type = label(self.task_type)
        if self.task_group is not None and not IDENTITY_HASH.fullmatch(self.task_group):
            raise SafeError("task_group_must_be_sha256")
        by_index = {c.call_idx: c for c in self.calls}

        def order(call):
            parent = by_index.get(call.parent_call_idx)
            return (call.ts_start or (parent.ts_start if parent else None) or "", call.call_idx)

        self.calls.sort(key=order)
        renumber = {call.call_idx: i for i, call in enumerate(self.calls)}
        for i, call in enumerate(self.calls):
            if call.ts_start and call.ts_end and call.ts_start > call.ts_end:
                raise SafeError("reversed_call_timestamps")
            call.call_idx = i
            if call.parent_call_idx is not None:
                call.parent_call_idx = renumber[call.parent_call_idx]
        self.n_calls = sum(c.event_kind == "model" for c in self.calls)
        starts = [c.ts_start for c in self.calls if c.ts_start]
        ends = [c.ts_end or c.ts_start for c in self.calls if c.ts_end or c.ts_start]
        self.started_at = self.started_at or (min(starts) if starts else None)
        self.ended_at = self.ended_at or (max(ends) if ends else None)
        if self.started_at and self.ended_at and self.started_at > self.ended_at:
            raise SafeError("reversed_task_timestamps")
        for call in self.calls:
            call.capped = self.capped
        return self

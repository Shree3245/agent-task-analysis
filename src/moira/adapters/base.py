"""Small explicit extractors. Raw records must never reach the store."""

from dataclasses import dataclass, field
import json

from moira.privacy import SafeError, digest, group_digest, label, task_digest
from moira.schema import Call, Task, number, status, timestamp


@dataclass
class Context:
    source: str
    namespace: str = ""
    fields: set = field(default_factory=set)
    warnings: dict = field(default_factory=dict)
    options: dict = field(default_factory=dict)
    seen: dict = field(default_factory=dict, repr=False)

    def warn(self, code):
        self.warnings[code] = self.warnings.get(code, 0) + 1

    def unique(self, task, event_id):
        if not event_id:
            return True
        key = (task.task_id, str(event_id))
        signature = (task.row(), [c.row() for c in task.calls])
        if key in self.seen:
            if self.seen[key] != signature:
                raise SafeError("conflicting_source_event")
            self.warn("duplicate_source_event_skipped")
            return False
        self.seen[key] = signature
        return True

    def get(self, row, *paths, default=None):
        for path in paths:
            value = row
            if isinstance(value, dict) and path in value:
                value = value[path]
            else:
                for part in path.split("."):
                    if not isinstance(value, dict) or part not in value:
                        value = None
                        break
                    value = value[part]
            if value is not None:
                self.fields.add(path)
                return value
        return default

    def task(
        self,
        raw_id,
        fallback,
        task_type=None,
        outcome=None,
        start=None,
        end=None,
        capped=False,
        reason=None,
        group=None,
    ):
        if raw_id is None:
            self.warn("inferred_task_identity")
        key = label(raw_id if raw_id is not None else fallback, limit=768)
        prefix = self.source + (":" + label(self.namespace) if self.namespace else "")
        result, cap, cap_reason = status(outcome, capped, reason)
        return Task(
            task_digest(f"{prefix}:{key}"),
            label(task_type),
            self.source,
            timestamp(start),
            timestamp(end),
            outcome=result,
            capped=cap,
            cap_reason=cap_reason,
            task_group=group_digest(group),
        )


def mapping(value):
    return value if isinstance(value, dict) else {}


def json_value(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return None
    return value


def model_call(
    ctx,
    task,
    row,
    *,
    model=None,
    provider=None,
    usage=None,
    recorded=None,
    start=None,
    end=None,
    tools=None,
    token_semantics=None,
):
    from moira.pricing.normalize import normalize, provider_for

    model = label(model)
    provider = provider_for(model, provider)
    try:
        quantities = normalize(
            mapping(usage), provider, token_semantics or ctx.options.get("token_semantics", "native")
        )
    except SafeError as error:
        if str(error) != "inconsistent_token_classes" or not ctx.options.get("inconsistent_usage_as_unknown"):
            raise
        quantities = normalize(mapping(usage), provider, "exclusive")
        quantities["input_tokens"] = None
        quantities["output_tokens"] = None
        ctx.warn("inconsistent_usage_unpriced")
    idx = len(task.calls)
    call = Call(
        task.task_id,
        idx,
        timestamp(start),
        timestamp(end),
        provider,
        model,
        **quantities,
        recorded_cost=number(recorded),
    )
    task.calls.append(call)
    for tool in tools or []:
        if isinstance(tool, dict):
            function = mapping(tool.get("function")) or tool
            name = function.get("name") or function.get("tool_name")
            if name:
                args = function.get("arguments", function.get("input", function.get("args")))
                tool_call(task, name, args, parent=idx, start=start, end=end)
    return call


def tool_call(task, name, args, *, parent=None, start=None, end=None):
    task.calls.append(
        Call(
            task.task_id,
            len(task.calls),
            timestamp(start),
            timestamp(end),
            tool_name=label(name),
            tool_args_hash=digest(args) if args is not None else None,
            event_kind="tool",
            parent_call_idx=parent,
        )
    )


def response_tools(value):
    """Only tool envelopes are extracted; message text is never returned."""
    value = json_value(value)
    if isinstance(value, dict):
        if value.get("tool_calls"):
            return value["tool_calls"]
        if value.get("choices"):
            return response_tools(value["choices"][0].get("message", {}))
        value = value.get("content", value.get("parts", []))
    tools = []
    if isinstance(value, list):
        for part in value:
            if not isinstance(part, dict):
                continue
            if part.get("type") in {"tool_use", "tool_call", "function_call"}:
                tools.append(part)
            elif "functionCall" in part:
                tools.append(part["functionCall"])
            elif part.get("role") == "assistant":
                tools.extend(response_tools(part))
    return tools


def rows(value, keys):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in keys:
            if isinstance(value.get(key), list):
                return value[key]
        return [value]
    raise SafeError("unsupported_record_shape")

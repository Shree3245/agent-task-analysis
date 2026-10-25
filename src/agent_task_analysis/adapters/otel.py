from agent_task_analysis.adapters.base import mapping, model_call, response_tools, rows, tool_call
from agent_task_analysis.schema import number


def attributes(value):
    def unwrap(v):
        if not isinstance(v, dict):
            return v
        for k in (
            "stringValue",
            "intValue",
            "doubleValue",
            "boolValue",
            "string_value",
            "int_value",
            "double_value",
            "bool_value",
        ):
            if k in v:
                return v[k]
        if "arrayValue" in v:
            return [unwrap(x) for x in v["arrayValue"].get("values", [])]
        return None

    if isinstance(value, list):
        return {
            x["key"]: unwrap(x.get("value")) for x in value if isinstance(x, dict) and "key" in x
        }
    return mapping(value)


def spans(root):
    if isinstance(root, dict) and ("resourceSpans" in root or "resource_spans" in root):
        for resource in root.get("resourceSpans", root.get("resource_spans", [])):
            for scope in resource.get(
                "scopeSpans",
                resource.get("scope_spans", resource.get("instrumentationLibrarySpans", [])),
            ):
                yield from scope.get("spans", [])
    elif isinstance(root, dict) and "spans" in root:
        yield from root["spans"]
    else:
        yield from rows(root, ())


def extract(root, ctx, fallback):
    meta = mapping(root)
    for index, span in enumerate(spans(root)):
        if not isinstance(span, dict):
            continue
        a = attributes(span.get("attributes"))

        def get(*paths, default=None):
            return ctx.get(a, *paths, default=default)

        op = get("gen_ai.operation.name")
        task_id = (
            get("task.id", "task_id", "gen_ai.conversation.id")
            or ctx.get(meta, "task_id", "session_id", "trace_id")
            or ctx.get(span, "traceId", "trace_id")
        )
        task_type = get("task.type", "task_type") or ctx.get(
            meta, "task_type", "benchmark", "benchmark_name"
        )
        task = ctx.task(
            task_id,
            fallback,
            task_type,
            outcome=get("task.outcome") or ctx.get(meta, "outcome", "status"),
            capped=get("task.capped", default=False),
            reason=get("task.cap_reason"),
            session=get("session.id", "user.id", "enduser.id")
            or ctx.get(meta, "session_id", "user_id"),
        )
        start = ctx.get(span, "startTimeUnixNano", "start_time", "start_time_unix_nano")
        end = ctx.get(span, "endTimeUnixNano", "end_time", "end_time_unix_nano")
        if op == "execute_tool":
            tool_call(
                task,
                get("gen_ai.tool.name", default="unknown"),
                get("gen_ai.tool.call.arguments", "tool.arguments"),
                start=start,
                end=end,
            )
        elif op in {"chat", "generate_content", "generate", "text_completion", "embeddings"} or any(
            k.startswith("gen_ai.usage.") for k in a
        ):
            usage = {}
            keys = {
                "input_tokens": ("gen_ai.usage.input_tokens", "gen_ai.usage.prompt_tokens"),
                "output_tokens": ("gen_ai.usage.output_tokens", "gen_ai.usage.completion_tokens"),
                "cached_input_tokens": (
                    "gen_ai.usage.cache_read.input_tokens",
                    "gen_ai.usage.cached_input_tokens",
                ),
                "cache_write_input_tokens": (
                    "gen_ai.usage.cache_creation.input_tokens",
                    "gen_ai.usage.cache_write.input_tokens",
                ),
                "reasoning_tokens": (
                    "gen_ai.usage.reasoning.output_tokens",
                    "gen_ai.usage.reasoning_tokens",
                ),
            }
            for key, names in keys.items():
                value = get(*names)
                if value is not None:
                    usage[key] = value
            # OTel input/output totals include their cache/reasoning subclasses across providers.
            usage = {key: number(value, integer=True) for key, value in usage.items()}
            provider = get("gen_ai.provider.name", "gen_ai.system")
            if "input_tokens" in usage:
                usage["input_tokens"] = (
                    usage["input_tokens"]
                    - usage.get("cached_input_tokens", 0)
                    - usage.get("cache_write_input_tokens", 0)
                )
            if "output_tokens" in usage:
                usage["output_tokens"] -= usage.get("reasoning_tokens", 0)
            model_call(
                ctx,
                task,
                span,
                model=get("gen_ai.response.model", "gen_ai.request.model"),
                provider=provider,
                usage=usage,
                start=start,
                end=end,
                recorded=get("gen_ai.usage.cost", "gen_ai.cost.total", "llm.cost.total"),
                tools=response_tools(get("gen_ai.output.messages")),
                token_semantics="exclusive",
            )
        else:
            ctx.warn("non_model_span_skipped")
            continue
        if ctx.unique(task, ctx.get(span, "spanId", "span_id")):
            yield task

from agent_task_analysis.adapters.base import mapping, model_call, response_tools, rows


def extract(root, ctx, fallback):
    for row in rows(root, ("data", "logs")):
        meta = mapping(row.get("metadata"))
        task_id = ctx.get(meta, "task_id", "session_id") or ctx.get(row, "session_id", "request_id")
        if not ctx.get(meta, "task_id", "session_id") and not row.get("session_id"):
            ctx.warn("one_request_per_task_fallback")
        task = ctx.task(
            task_id,
            fallback,
            ctx.get(meta, "task_type"),
            outcome=ctx.get(meta, "outcome") or ctx.get(row, "status"),
            capped=ctx.get(meta, "capped", default=False),
            reason=ctx.get(meta, "cap_reason"),
        )
        usage = mapping(ctx.get(row, "usage", default={})) or {
            k: ctx.get(row, k)
            for k in (
                "prompt_tokens",
                "completion_tokens",
                "cache_read_input_tokens",
                "cache_creation_input_tokens",
                "cached_input_tokens",
                "reasoning_tokens",
                "prompt_tokens_details",
                "completion_tokens_details",
            )
        }
        model_call(
            ctx,
            task,
            row,
            model=ctx.get(row, "model"),
            provider=ctx.get(row, "custom_llm_provider", "metadata.provider"),
            usage=usage,
            recorded=ctx.get(row, "spend"),
            start=ctx.get(row, "startTime", "start_time"),
            end=ctx.get(row, "endTime", "end_time"),
            tools=response_tools(ctx.get(row, "response")),
        )
        if ctx.unique(task, ctx.get(row, "request_id")):
            yield task

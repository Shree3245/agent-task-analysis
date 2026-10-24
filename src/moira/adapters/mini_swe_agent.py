from moira.adapters.base import mapping, model_call, response_tools


def extract(root, ctx, fallback):
    if "detailed_predictions" in root:
        # ASSERT-KTH stores messages plus one aggregate token total: never apportion it.
        detail = mapping(root["detailed_predictions"])
        ctx.fields.add("detailed_predictions.completion.tool_calls")
        ctx.warn("aggregate_usage_without_call_breakdown")
        instance = ctx.get(root, "instance_id")
        task = ctx.task(instance, fallback, "code", group=instance)
        for message in detail.get("completion", []):
            if message.get("role") == "assistant":
                model_call(
                    ctx,
                    task,
                    message,
                    model=ctx.options.get("model"),
                    usage=ctx.get(message, "usage", default={}),
                    tools=response_tools(message),
                )
        yield task
        return
    info = mapping(root.get("info"))
    task = ctx.task(
        ctx.get(root, "task_id", "instance_id") or ctx.get(info, "instance_id"),
        fallback,
        ctx.get(root, "task_type", default="code"),
        outcome=ctx.get(info, "exit_status") or ctx.get(root, "outcome"),
        start=ctx.get(root, "started_at"),
        end=ctx.get(root, "ended_at"),
        capped=ctx.get(root, "capped", default=False),
        reason=ctx.get(root, "cap_reason"),
        group=ctx.get(root, "instance_id") or ctx.get(info, "instance_id"),
    )
    model = ctx.get(info, "model_name", "config.model.model_name") or ctx.get(root, "model")
    for message in root.get("messages", []):
        if message.get("role") != "assistant":
            continue
        extra = mapping(message.get("extra"))
        model_call(
            ctx,
            task,
            message,
            model=ctx.get(message, "model", default=model),
            usage=ctx.get(message, "usage", "extra.usage", default={}),
            recorded=ctx.get(extra, "cost"),
            start=ctx.get(message, "timestamp"),
            tools=response_tools(message),
        )
    if not task.calls and info.get("model_stats"):
        ctx.warn("aggregate_usage_without_calls")
        model_call(ctx, task, {}, model=model)
    yield task

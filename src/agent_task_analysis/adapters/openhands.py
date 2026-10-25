from agent_task_analysis.adapters.base import mapping, model_call, response_tools, rows, tool_call


def extract(root, ctx, fallback):
    meta = mapping(root)
    task = ctx.task(
        ctx.get(meta, "instance_id", "task_id"),
        fallback,
        ctx.get(meta, "task_type", default="code"),
        outcome=ctx.get(meta, "outcome", "test_result.resolved", "resolved", "exit_status"),
        start=ctx.get(meta, "started_at"),
        end=ctx.get(meta, "ended_at"),
        capped=ctx.get(meta, "capped", default=False),
        reason=ctx.get(meta, "cap_reason", "stop_reason"),
        group=ctx.get(meta, "instance_id"),
    )
    if ctx.options.get("task_id"):
        task = ctx.task(
            ctx.options["task_id"],
            fallback,
            task.task_type,
            outcome=task.outcome,
            capped=task.capped,
            reason=task.cap_reason,
            group=ctx.get(meta, "instance_id"),
        )
    model = ctx.get(meta, "model", "metadata.llm_config.model", "metadata.model")
    metrics = mapping(meta.get("metrics"))
    if isinstance(metrics.get("token_usages"), list):
        usages = metrics["token_usages"]
        costs = metrics.get("costs", [])
        ctx.fields.update({"metrics.token_usages", "metrics.costs"})
        matched = len(usages) == len(costs)
        if not matched:
            ctx.warn("per_call_cost_list_mismatch")
        parents = {}
        for index, usage in enumerate(usages):
            cost = costs[index] if matched else {}
            call = model_call(
                ctx,
                task,
                {},
                model=usage.get("model", model),
                usage=usage,
                recorded=cost.get("cost"),
                start=cost.get("timestamp"),
            )
            if usage.get("response_id"):
                parents[usage["response_id"]] = call.call_idx
        for e in meta.get("history", []):
            if not isinstance(e, dict) or not e.get("action"):
                continue
            response_id = ctx.get(e, "tool_call_metadata.model_response.id")
            tool_call(
                task,
                ctx.get(e, "action"),
                ctx.get(e, "args"),
                parent=parents.get(response_id),
                start=ctx.get(e, "timestamp"),
            )
        from agent_task_analysis.schema import status

        error = ctx.get(meta, "error")
        outcome, capped, reason = status("error" if error else None, reason=error)
        if capped:
            task.outcome, task.capped, task.cap_reason = outcome, capped, reason
        elif error and task.outcome == "unknown":
            task.outcome = "fail"
        yield task
        return
    events = rows(root, ("events", "history", "trajectory", "llm_calls"))
    for event in events:
        if isinstance(event, list):
            events2 = event
        else:
            events2 = [event]
        for e in events2:
            if not isinstance(e, dict):
                continue
            response = mapping(e.get("response"))
            usage = ctx.get(e, "usage", "response.usage", "llm_response.usage")
            if usage is not None or e.get("type") in {"llm", "model"}:
                model_call(
                    ctx,
                    task,
                    e,
                    model=ctx.get(e, "model", "response.model", default=model),
                    usage=usage,
                    recorded=ctx.get(e, "cost", "response_cost"),
                    start=ctx.get(e, "timestamp", "start_time"),
                    end=ctx.get(e, "end_time"),
                    tools=response_tools(response),
                )
            if e.get("action"):
                # action is an enum in OpenHands, args may contain source code.
                tool_call(
                    task, ctx.get(e, "action"), ctx.get(e, "args"), start=ctx.get(e, "timestamp")
                )
    if not any(c.event_kind == "model" for c in task.calls):
        # Keep a visible unknown-cost task rather than pricing aggregate tokens as calls.
        ctx.warn("aggregate_usage_without_calls")
        model_call(ctx, task, {}, model=model)
    yield task

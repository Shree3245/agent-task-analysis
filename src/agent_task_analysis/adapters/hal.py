from agent_task_analysis.adapters.base import mapping, model_call, response_tools, rows


def extract(root, ctx, fallback):
    envelope = mapping(root)
    config = mapping(envelope.get("config"))
    results = mapping(envelope.get("results"))
    success = set(str(x) for x in results.get("successful_tasks", []))
    failures = set(str(x) for x in results.get("failed_tasks", []))
    if results:
        ctx.fields.update({"results.successful_tasks", "results.failed_tasks"})
    records = rows(root, ("raw_logging_results", "calls", "data", "traces"))
    parent_ids = {r.get("parent_id") for r in records if isinstance(r, dict) and r.get("parent_id")}
    for record in records:
        if record.get("id") in parent_ids and not mapping(record.get("output")).get("usage"):
            ctx.warn("aggregate_parent_span_skipped")
            continue
        summary = mapping(record.get("summary"))
        usage_by_model = mapping(summary.get("usage"))
        output = mapping(record.get("output"))
        usage = ctx.get(record, "output.usage", "usage")
        model = ctx.get(record, "output.model", "inputs.model", "model")
        if usage is None and len(usage_by_model) == 1:
            model, usage = next(iter(usage_by_model.items()))
            ctx.fields.add("summary.usage")
        # Weave parent/agent summaries can include all child usage: only leaf model calls.
        if not usage and not model:
            ctx.warn("non_model_span_skipped")
            continue
        task_id = ctx.get(
            record,
            "task_id",
            "weave_task_id",
            "attributes.weave_task_id",
            "attributes.task_id",
            "trace_id",
        )
        outcome = (
            "success"
            if str(task_id) in success
            else "fail"
            if str(task_id) in failures
            else ctx.get(record, "outcome", "attributes.outcome")
        )
        task = ctx.task(
            task_id,
            fallback,
            ctx.get(record, "task_type", "attributes.task_type", "attributes.benchmark")
            or ctx.get(config, "benchmark_name"),
            outcome=outcome,
            capped=ctx.get(record, "capped", default=False),
            reason=ctx.get(record, "cap_reason"),
        )
        model_call(
            ctx,
            task,
            record,
            model=model,
            usage=usage,
            recorded=ctx.get(record, "cost", "summary.cost"),
            start=ctx.get(record, "started_at", "start_time"),
            end=ctx.get(record, "ended_at", "end_time"),
            tools=response_tools(output),
        )
        if ctx.unique(task, ctx.get(record, "id")):
            yield task

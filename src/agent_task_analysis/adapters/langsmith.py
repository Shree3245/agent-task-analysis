from agent_task_analysis.adapters.base import mapping, model_call, response_tools, rows, tool_call


def extract(root, ctx, fallback):
    def walk(run, root_id=None, inherited=None, parent_status=None):
        metadata = mapping(run.get("extra", {}).get("metadata"))
        task_id = root_id or ctx.get(run, "trace_id", "id")
        task = ctx.task(
            task_id,
            fallback,
            ctx.get(metadata, "task_type") or inherited,
            outcome=ctx.get(metadata, "outcome", "status"),
            capped=ctx.get(metadata, "capped", default=False),
            reason=ctx.get(metadata, "cap_reason"),
        )
        if parent_status:
            if task.outcome == "unknown":
                task.outcome = parent_status[0]
            if parent_status[1]:
                task.capped, task.cap_reason = parent_status[1:]
        start, end = ctx.get(run, "start_time"), ctx.get(run, "end_time")
        kind = run.get("run_type", "llm")
        if kind == "llm":
            usage = ctx.get(
                run, "usage_metadata", "outputs.llm_output.token_usage", "outputs.usage", default={}
            )
            # Some exports keep usage at run level.
            if not usage:
                usage = {k: ctx.get(run, k) for k in ("prompt_tokens", "completion_tokens")}
            model_call(
                ctx,
                task,
                run,
                model=ctx.get(metadata, "ls_model_name", "model_name")
                or ctx.get(run, "extra.invocation_params.model", "name"),
                provider=ctx.get(metadata, "ls_provider"),
                usage=usage,
                start=start,
                end=end,
                recorded=ctx.get(run, "total_cost"),
                tools=response_tools(ctx.get(run, "outputs")),
            )
            if ctx.unique(task, ctx.get(run, "id")):
                yield task
        elif kind == "tool":
            tool_call(
                task,
                ctx.get(run, "name", default="unknown"),
                ctx.get(run, "inputs"),
                start=start,
                end=end,
            )
            if ctx.unique(task, ctx.get(run, "id")):
                yield task
        for child in run.get("child_runs", []):
            yield from walk(
                child, task_id, task.task_type, (task.outcome, task.capped, task.cap_reason)
            )

    for run in rows(root, ("runs", "data")):
        yield from walk(run)

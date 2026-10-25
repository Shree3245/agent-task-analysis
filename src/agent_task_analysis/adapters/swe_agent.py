from agent_task_analysis.adapters.base import mapping, model_call, response_tools, tool_call


def extract(root, ctx, fallback):
    if "trajectory_steps" in root:
        # ASSERT-KTH R2E-Gym variant: step-level tokens but no absolute clock.
        reward = ctx.get(root, "reward")
        task = ctx.task(
            ctx.get(root, "ds.instance_id"),
            fallback,
            "code",
            outcome=("success" if reward > 0 else "fail")
            if isinstance(reward, (int, float))
            else None,
            reason=ctx.get(root, "exit_reason"),
            group=ctx.get(root, "ds.instance_id"),
        )
        model = ctx.get(root, "agent_args.llm_name")
        for step in root["trajectory_steps"]:
            usage = {
                "prompt_tokens": ctx.get(step, "token_usage_prompt"),
                "completion_tokens": ctx.get(step, "token_usage_completion"),
            }
            call = model_call(ctx, task, step, model=model, usage=usage)
            action = ctx.get(step, "action")
            if action is not None:
                tool_call(task, "shell", action, parent=call.call_idx)
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
    model = ctx.get(root, "model") or ctx.get(info, "model_name", "config.agent.model.name")
    for step in root.get("trajectory", []):
        call = model_call(
            ctx,
            task,
            step,
            model=ctx.get(step, "model", default=model),
            usage=ctx.get(step, "usage", "model_usage", default={}),
            recorded=ctx.get(step, "cost"),
            start=ctx.get(step, "timestamp"),
            tools=response_tools(step.get("response")),
        )
        action = ctx.get(step, "action")
        if isinstance(action, dict):
            tool_call(
                task, action.get("name", "action"), action.get("arguments"), parent=call.call_idx
            )
        elif isinstance(action, str):
            # The command may contain code. Hash it, never classify or retain it.
            tool_call(task, "shell", action, parent=call.call_idx)
    if not task.calls:
        ctx.warn("aggregate_usage_without_calls")
    yield task

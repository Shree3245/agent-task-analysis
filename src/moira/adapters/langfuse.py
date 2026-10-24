from moira.adapters.base import mapping, model_call, response_tools, rows, tool_call


def extract(root, ctx, fallback):
    for trace in rows(root, ("data", "traces")):
        observations = trace.get("observations", [trace])
        for obs in observations:
            kind = str(obs.get("type", "GENERATION")).upper()
            task = ctx.task(
                ctx.get(obs, "traceId", "trace_id") or ctx.get(trace, "id"),
                fallback,
                ctx.get(trace, "metadata.task_type") or ctx.get(obs, "metadata.task_type"),
                outcome=ctx.get(trace, "metadata.outcome", "metadata.status"),
                capped=ctx.get(trace, "metadata.capped", default=False),
                reason=ctx.get(trace, "metadata.cap_reason"),
            )
            start = ctx.get(obs, "startTime", "start_time", "timestamp")
            end = ctx.get(obs, "endTime", "end_time")
            if kind in {"GENERATION", "EMBEDDING"}:
                u = dict(mapping(ctx.get(obs, "usageDetails", "usage", default={})))
                for old, new in (
                    ("cacheReadInput", "cached_input_tokens"),
                    ("cacheCreationInput", "cache_write_input_tokens"),
                ):
                    if old in u:
                        u[new] = u[old]
                model_call(
                    ctx,
                    task,
                    obs,
                    model=ctx.get(obs, "model"),
                    provider=ctx.get(obs, "metadata.provider"),
                    usage=u,
                    start=start,
                    end=end,
                    recorded=ctx.get(obs, "calculatedTotalCost", "costDetails.total", "totalCost"),
                    tools=response_tools(ctx.get(obs, "output")),
                )
            elif kind == "TOOL":
                tool_call(
                    task,
                    ctx.get(obs, "name", default="unknown"),
                    ctx.get(obs, "input"),
                    start=start,
                    end=end,
                )
            else:
                ctx.warn("non_model_span_skipped")
                continue
            if ctx.unique(task, ctx.get(obs, "id")):
                yield task

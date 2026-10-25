"""Braintrust project-log events (API fetch or JSON/JSONL export), one span per record.

A trace (root_span_id) is one task. LLM spans are model calls; tool spans and tool calls in
an LLM span's output are tool events. The root span supplies the task type and outcome.
Braintrust metrics are inclusive: prompt_tokens counts cache reads and cache writes, and
completion_tokens counts reasoning tokens.
"""

from agent_task_analysis.adapters.base import mapping, model_call, response_tools, tool_call
from agent_task_analysis.pricing.normalize import provider_for
from agent_task_analysis.privacy import label
from agent_task_analysis.schema import number

CACHE_WRITES = ("prompt_cache_creation_5m_tokens", "prompt_cache_creation_1h_tokens")


def usage(ctx, metrics):
    def count(name):
        value = ctx.get(metrics, name)
        return None if value is None else number(value, integer=True)

    prompt, completion = count("prompt_tokens"), count("completion_tokens")
    cached = count("prompt_cached_tokens") or 0
    split = [count(k) for k in CACHE_WRITES]
    if any(v is not None for v in split):
        writes = sum(v or 0 for v in split)
        if split[1]:
            # agent-task-analysis's catalog has one (5-minute) cache-write rate; 1-hour writes cost more.
            ctx.warn("cache_write_1h_priced_at_5m_rate")
    else:
        writes = count("prompt_cache_creation_tokens") or count("prompt_cache_write_tokens") or 0
    reasoning = count("completion_reasoning_tokens") or 0
    result = {"cached_input_tokens": cached, "cache_write_input_tokens": writes,
              "reasoning_tokens": reasoning}
    if prompt is not None:
        if prompt >= cached + writes:
            result["input_tokens"] = prompt - cached - writes
        else:
            # Older SDKs reported Anthropic prompt_tokens without the cache classes.
            ctx.warn("prompt_tokens_exclusive_of_cache")
            result["input_tokens"] = prompt
    if completion is not None:
        if completion >= reasoning:
            result["output_tokens"] = completion - reasoning
        else:
            ctx.warn("completion_tokens_exclusive_of_reasoning")
            result["output_tokens"] = completion
    return result


def extract(root, ctx, fallback):
    # A saved fetch response ({"events": [...]}) or a JSON array holds many spans.
    events = root.get("events") if isinstance(root, dict) and "events" in root else root
    if isinstance(events, list):
        for index, event in enumerate(events):
            yield from span(event, ctx, f"{fallback}:{index}")
    else:
        yield from span(root, ctx, fallback)


def output_tools(value):
    # Chat-completion wrappers log `output` as the list of choices.
    if isinstance(value, list) and value and all(isinstance(v, dict) and "message" in v for v in value):
        value = {"choices": value}
    return response_tools(value)


def span(root, ctx, fallback):
    if not isinstance(root, dict):
        return
    attributes = mapping(root.get("span_attributes"))
    metadata = mapping(root.get("metadata"))
    metrics = mapping(root.get("metrics"))
    kind = ctx.get(attributes, "type")
    if ctx.get(attributes, "purpose") == "scorer":
        ctx.warn("scorer_span_skipped")
        return
    trace = ctx.get(root, "root_span_id") or ctx.get(root, "span_id", "id")
    is_root = bool(root.get("is_root")) or (trace is not None and root.get("span_id") == trace)
    outcome = None
    task_type = None
    if is_root:
        task_type = ctx.get(metadata, "task_type", "task.type") or ctx.get(attributes, "name")
        outcome = ctx.get(metadata, "outcome", "task.outcome")
        if outcome is None and root.get("error") not in (None, "", {}):
            # Presence only: the error text is never read.
            outcome = "fail"
    task = ctx.task(trace, fallback, task_type, outcome=outcome,
                    capped=ctx.get(metadata, "capped", default=False),
                    reason=ctx.get(metadata, "cap_reason"))
    start = ctx.get(metrics, "start") or ctx.get(root, "created")
    end = ctx.get(metrics, "end")
    tokens = any(k in metrics for k in ("prompt_tokens", "completion_tokens"))
    if kind == "llm" or tokens:
        model = ctx.get(metadata, "model")
        provider = provider_for(label(model)) if model else "unknown"
        if provider == "unknown":
            provider = ctx.get(metadata, "provider")
        model_call(ctx, task, root, model=model, provider=provider, usage=usage(ctx, metrics),
                   start=start, end=end, tools=output_tools(root.get("output")),
                   token_semantics="exclusive")
    elif kind == "tool":
        tool_call(task, ctx.get(attributes, "name", default="unknown"), root.get("input"),
                  start=start, end=end)
    elif not is_root:
        ctx.warn("non_model_span_skipped")
        return
    if ctx.unique(task, ctx.get(root, "id", "span_id")):
        yield task

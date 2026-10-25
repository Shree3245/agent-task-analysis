import copy
import json

import pytest
from conftest import FIXTURES, CSV_OPTIONS
from agent_task_analysis.adapters import adapter, SOURCES
from agent_task_analysis.adapters.base import Context
from agent_task_analysis.analysis.history import build_history
from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.privacy import SafeError
from agent_task_analysis.schema import status
from agent_task_analysis.ingest import ingest
from agent_task_analysis.storage import connect, load


@pytest.mark.parametrize("source", SOURCES)
def test_explicit_caps_survive_each_adapter(source):
    if source == "csv":
        data = {
            "task_id": "a",
            "model": "gpt-4o-mini",
            "input_tokens": "1",
            "output_tokens": "1",
            "capped": "true",
            "cap_reason": "time_limit",
        }
        options = copy.deepcopy(CSV_OPTIONS)
        options["columns"].update(capped="capped", cap_reason="cap_reason")
    else:
        data = json.loads((FIXTURES / source / "sample.json").read_text())
        options = {}
        if source == "otel":
            attrs = data["resourceSpans"][0]["scopeSpans"][0]["spans"][0]["attributes"]
            attrs.extend(
                [
                    {"key": "task.capped", "value": {"boolValue": True}},
                    {"key": "task.cap_reason", "value": {"stringValue": "time_limit"}},
                ]
            )
        elif source == "langfuse":
            data["metadata"].update(capped=True, cap_reason="time_limit")
        elif source == "langsmith":
            data["extra"]["metadata"].update(capped=True, cap_reason="time_limit")
        elif source == "litellm":
            data["metadata"].update(capped=True, cap_reason="time_limit")
        elif source == "braintrust":
            for event in data["events"]:
                event["metadata"].update(capped=True, cap_reason="time_limit")
        else:
            data.update(capped=True, cap_reason="time_limit")
    tasks = list(adapter(source)(data, Context(source, options=options), "fallback"))
    assert tasks and all(t.capped and t.cap_reason == "time_limit" for t in tasks)


@pytest.mark.parametrize(
    "reason,expected",
    [
        ("exit_cost", "dollar_limit"),
        ("Agent reached maximum number of iterations", "turn_limit"),
        ("deadline exceeded", "time_limit"),
        ("failed", None),
        ("cancelled", None),
    ],
)
def test_caps_are_not_all_failures(reason, expected):
    _, capped, actual = status(reason)
    assert actual == expected and capped == bool(expected)


def test_otlp_deduplicates_and_multiple_tools_do_not_duplicate_tokens(tmp_path):
    span = {
        "span_id": "s",
        "trace_id": "t",
        "attributes": {
            "gen_ai.operation.name": "chat",
            "gen_ai.request.model": "gpt-4o-mini",
            "gen_ai.usage.input_tokens": 100,
            "gen_ai.usage.output_tokens": 10,
            "gen_ai.output.messages": [
                {
                    "role": "assistant",
                    "parts": [
                        {"type": "tool_call", "name": "a", "arguments": {"x": 1}},
                        {"type": "tool_call", "name": "b", "arguments": {"x": 2}},
                    ],
                }
            ],
        },
    }
    p = tmp_path / "input.json"
    p.write_text(json.dumps([span, span]))
    db = tmp_path / "db.duckdb"
    result = ingest("otel", p, db)
    assert result["warnings"]["duplicate_source_event_skipped"] == 1
    with connect(db, True) as conn:
        tasks = load(conn)
    assert tasks[0].n_calls == 1 and len(tasks[0].calls) == 3
    assert build_history(tasks, load_catalog())[0].cost == pytest.approx(0.000021)


def test_hal_parent_aggregate_not_billed_again():
    data = {
        "raw_logging_results": [
            {
                "id": "parent",
                "trace_id": "t",
                "summary": {
                    "usage": {"gpt-4o-mini": {"prompt_tokens": 100, "completion_tokens": 10}}
                },
            },
            {
                "id": "child",
                "parent_id": "parent",
                "trace_id": "t",
                "output": {
                    "model": "gpt-4o-mini",
                    "usage": {"prompt_tokens": 100, "completion_tokens": 10},
                },
            },
        ]
    }
    tasks = list(adapter("hal")(data, Context("hal"), "fallback"))
    assert len(tasks) == 1 and len(tasks[0].calls) == 1


def test_real_openhands_metrics_shape_keeps_billing_discrepancy():
    data = {
        "instance_id": "issue",
        "metrics": {
            "token_usages": [
                {
                    "model": "litellm_proxy/anthropic/claude-3-7-sonnet-20250219",
                    "prompt_tokens": 4869,
                    "completion_tokens": 544,
                    "cache_read_tokens": 3398,
                    "cache_write_tokens": 1468,
                    "response_id": "r",
                }
            ],
            "costs": [{"cost": 0.0190974, "timestamp": 1744226712.513}],
        },
        "error": "Agent reached maximum number of iterations",
    }
    task = list(adapter("openhands")(data, Context("openhands"), "fallback"))[0].finalize()
    assert task.capped and task.cap_reason == "turn_limit"
    call = task.calls[0]
    assert call.input_tokens == 3 and call.cache_write_input_tokens == 1468
    assert build_history([task], load_catalog())[0].cost == pytest.approx(0.0146934)
    assert call.recorded_cost == 0.0190974


def test_missing_usage_is_unknown_not_zero():
    data = {"request_id": "a", "model": "gpt-4o-mini"}
    task = list(adapter("litellm")(data, Context("litellm"), "fallback"))[0].finalize()
    assert task.calls[0].input_tokens is None
    assert not build_history([task], load_catalog())[0].complete


def test_invalid_metadata_counts_fail_safely():
    data = {
        "request_id": "a",
        "model": "gpt-4o-mini",
        "prompt_tokens": "secret-content",
        "completion_tokens": 1,
    }
    with pytest.raises(SafeError, match="invalid_nonnegative_number"):
        list(adapter("litellm")(data, Context("litellm"), "fallback"))


def test_r2e_gym_step_tokens_and_capped_reward():
    data = {
        "ds": {"instance_id": "issue"},
        "agent_args": {"llm_name": "hosted_vllm/Qwen/Qwen3-32B"},
        "reward": 0,
        "exit_reason": "max_steps",
        "trajectory_steps": [
            {
                "token_usage_prompt": 300,
                "token_usage_completion": 50,
                "action": "secret code",
                "thought": "private thought",
            }
        ],
    }
    task = list(adapter("swe-agent")(data, Context("swe-agent"), "fallback"))[0].finalize()
    assert task.capped and task.cap_reason == "turn_limit"
    assert task.calls[0].input_tokens == 300 and task.calls[0].output_tokens == 50
    assert task.started_at is None
    assert "secret code" not in str([c.row() for c in task.calls])


def test_otel_cache_subclasses_are_exclusive_even_without_provider_attribute():
    data = {
        "trace_id": "t",
        "attributes": {
            "gen_ai.operation.name": "chat",
            "gen_ai.request.model": "claude-sonnet-4-5",
            "gen_ai.usage.input_tokens": 1000,
            "gen_ai.usage.cache_read.input_tokens": 600,
            "gen_ai.usage.cache_creation.input_tokens": 300,
            "gen_ai.usage.output_tokens": 200,
            "gen_ai.usage.reasoning.output_tokens": 150,
        },
    }
    task = list(adapter("otel")(data, Context("otel"), "fallback"))[0]
    call = task.calls[0]
    assert call.input_tokens == 100 and call.output_tokens == 50
    assert call.reasoning_tokens == 150 and call.cache_write_input_tokens == 300

"""Regression evidence: a source-formula fit must not manufacture validation."""

import importlib.util
import json
from pathlib import Path
import pytest

from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.pricing.normalize import normalize
from agent_task_analysis.pricing.reprice import call_cost, reconcile
from agent_task_analysis.schema import Call, Task
from agent_task_analysis.privacy import SafeError


spec = importlib.util.spec_from_file_location(
    "bai_audit", Path(__file__).resolve().parents[1] / "benchmarks/audit_bai_costs.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_sonnet37_source_fit_does_not_override_default_or_prove_native_identity():
    # First retained completion in the pinned public Sonnet 3.7 mini archive.
    usage = {
        "prompt_tokens": 73916,
        "completion_tokens": 822,
        "cache_creation_input_tokens": 725,
        "cache_read_input_tokens": 73191,
    }
    row = audit.inspect_call(
        usage, 0.03918105, "litellm_proxy/claude-3-7-sonnet-20250219", load_catalog()
    )
    assert row["source_eq12_match"] is True
    assert row["provider_match"] is False
    assert row["provider_cost"] == pytest.approx(0.03700605)
    assert row["native_identity"] is None  # Never infer an independent observation.
    c = Call(
        "example",
        0,
        provider="anthropic",
        model="claude-3-7-sonnet-20250219",
        recorded_cost=0.03918105,
        **normalize(usage, "anthropic"),
    )
    assert call_cost(c, load_catalog())[0] == pytest.approx(0.03700605)
    assert (
        reconcile([Task("example", calls=[c]).finalize()], load_catalog())["acceptance"] == "FAIL"
    )


def test_sonnet45_source_formula_would_break_correct_recorded_agreement():
    row = audit.inspect_call(
        {
            "prompt_tokens": 126900,
            "completion_tokens": 839,
            "cache_creation_input_tokens": 526,
            "cache_read_input_tokens": 126374,
        },
        0.0524697,
        "claude-sonnet-4-5-20250929",
        load_catalog(),
    )
    assert row["provider_match"] is True
    assert row["source_eq12_match"] is False


def test_sonnet4_inconsistent_counts_are_not_clamped_to_pass():
    usage = {
        "prompt_tokens": 87616,
        "completion_tokens": 1097,
        "cache_creation_input_tokens": 575,
        "cache_read_input_tokens": 87616,
    }
    row = audit.inspect_call(
        usage, 0.04489605, "litellm_proxy/claude-sonnet-4-20250514", load_catalog()
    )
    assert row["source_eq12_match"] is True
    assert row["provider_cost"] is None
    assert row["inferred_input_residual"] == -575
    with pytest.raises(SafeError, match="inconsistent_token_classes"):
        normalize(usage, "anthropic")


def test_native_identity_requires_independent_input_and_audit_drops_content():
    usage = {
        "prompt_tokens": 1000,
        "input_tokens": 100,
        "completion_tokens": 10,
        "cache_creation_input_tokens": 200,
        "cache_read_input_tokens": 700,
        "prompt": "CANARY_BAI",
        "tool_args": {"x": "CANARY_BAI"},
        "completion_tokens_details": {"reasoning_tokens": 0, "output": "CANARY_BAI"},
    }
    row = audit.inspect_call(usage, 1, "unknown", load_catalog())
    assert row["native_identity"] is True
    assert "CANARY_BAI" not in json.dumps(row)
    usage["input_tokens"] = 101
    assert audit.inspect_call(usage, 1, "unknown", load_catalog())["native_identity"] is False


def test_zero_recorded_unknown_tariff_is_not_a_validated_free_call():
    row = audit.inspect_call(
        {
            "prompt_tokens": 72765,
            "completion_tokens": 817,
            "prompt_tokens_details": {"cached_tokens": 72368},
        },
        0,
        "Qwen3-Coder-480B-A35B-Instruct-FP8",
        load_catalog(),
    )
    assert row["provider_match"] is None
    assert row["provider_reason"] == "unknown_model"
    assert row["source_eq12_match"] is None

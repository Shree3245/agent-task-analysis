import pytest
from moira.pricing.normalize import normalize
from moira.pricing.catalog import load_catalog
from moira.pricing.reprice import call_cost, reconcile
from moira.schema import Call, Task
from moira.privacy import SafeError


def test_cache_and_reasoning_are_not_double_counted():
    q = normalize(
        {
            "prompt_tokens": 1000,
            "prompt_tokens_details": {"cached_tokens": 400},
            "completion_tokens": 100,
            "completion_tokens_details": {"reasoning_tokens": 60},
        },
        "openai",
    )
    call = Call("a", 0, provider="openai", model="gpt-4o-mini", **q)
    assert call_cost(call, load_catalog())[0] == pytest.approx(
        (600 * 0.15 + 400 * 0.075 + 100 * 0.6) / 1e6
    )
    assert q["output_tokens"] == 40 and q["reasoning_tokens"] == 60


def test_anthropic_additive_cache_and_google_additive_thoughts():
    q = normalize(
        {
            "input_tokens": 100,
            "cache_read_input_tokens": 500,
            "cache_creation_input_tokens": 200,
            "output_tokens": 20,
        },
        "anthropic",
    )
    c = Call("a", 0, provider="anthropic", model="claude-sonnet-4-5", **q)
    assert call_cost(c, load_catalog())[0] == pytest.approx(
        (100 * 3 + 500 * 0.3 + 200 * 3.75 + 20 * 15) / 1e6
    )
    q = normalize(
        {
            "promptTokenCount": 250000,
            "cachedContentTokenCount": 240000,
            "candidatesTokenCount": 50,
            "thoughtsTokenCount": 100,
        },
        "google",
    )
    c = Call("b", 0, provider="google", model="gemini-2.5-pro", **q)
    assert call_cost(c, load_catalog())[0] == pytest.approx(
        (10000 * 2.5 + 240000 * 0.25 + 150 * 15) / 1e6
    )


def test_unknown_model_missing_usage_and_zero_recorded():
    q = normalize({"input_tokens": 0, "output_tokens": 0}, "openai")
    c = Call("a", 0, provider="openai", model="gpt-4o-mini", recorded_cost=0, **q)
    task = Task("a", calls=[c]).finalize()
    assert reconcile([task], load_catalog())["agreement"] == 1
    c.input_tokens = 1
    assert reconcile([task], load_catalog())["agreement"] == 0
    c.model = "invented"
    assert call_cost(c, load_catalog()) == (None, "unknown_model")
    assert reconcile([task], load_catalog())["agreement"] == 0
    c.model, c.input_tokens = "gpt-4o-mini", None
    assert call_cost(c, load_catalog()) == (None, "missing_usage")


def test_inconsistent_counts_rejected():
    with pytest.raises(SafeError):
        normalize({"input_tokens": 5, "cached_input_tokens": 10}, "openai")

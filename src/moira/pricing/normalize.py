from moira.privacy import SafeError, label
from moira.schema import TOKEN_FIELDS, number


def provider_for(model, provider=None):
    if provider and provider != "unknown":
        aliases = {"google_genai": "google", "gemini": "google", "gcp": "google"}
        return aliases.get(str(provider), label(provider))
    # Explicit model-family identifiers only; no fuzzy model price matching.
    name = model.lower().split("/")[-1]
    for prefixes, result in [
        (("claude-",), "anthropic"),
        (("gpt-", "o1", "o3", "o4"), "openai"),
        (("gemini-",), "google"),
        (("deepseek-",), "deepseek"),
    ]:
        if name.startswith(prefixes):
            return result
    return "unknown"


def normalize(usage, provider, semantics="native"):
    def read(*names):
        for name in names:
            value = usage
            if name in usage:
                value = usage[name]
            else:
                for part in name.split("."):
                    value = value.get(part) if isinstance(value, dict) else None
            if value is not None:
                return number(value, integer=True)
        return None

    inp = read("input_tokens", "prompt_tokens", "promptTokenCount", "input")
    out = read("output_tokens", "completion_tokens", "candidatesTokenCount", "output")
    cached = read(
        "cached_input_tokens",
        "cache_read_input_tokens",
        "cache_read_tokens",
        "cachedContentTokenCount",
        "prompt_tokens_details.cached_tokens",
        "input_tokens_details.cached_tokens",
        "input_token_details.cache_read",
    )
    write = read(
        "cache_write_input_tokens",
        "cache_creation_input_tokens",
        "cache_write_tokens",
        "cacheWriteInputTokenCount",
        "input_token_details.cache_creation",
    )
    reasoning = read(
        "reasoning_tokens",
        "thinking_tokens",
        "thoughtsTokenCount",
        "completion_tokens_details.reasoning_tokens",
        "output_tokens_details.reasoning_tokens",
        "output_token_details.reasoning",
    )
    if semantics not in {"native", "exclusive"}:
        raise SafeError("invalid_token_semantics")
    if semantics != "exclusive":
        if inp is not None and (
            provider != "anthropic" or "prompt_tokens" in usage or "input_token_details" in usage
        ):
            inp -= (cached or 0) + (write or 0)
        # OpenAI reasoning is a subset of completion_tokens; Gemini thoughts are additive.
        if out is not None and (provider != "google" or "completion_tokens" in usage):
            out -= reasoning or 0
    if (inp is not None and inp < 0) or (out is not None and out < 0):
        raise SafeError("inconsistent_token_classes")
    # Missing main usage stays unknown. Optional classes absent from a usage record are zero.
    return dict(zip(TOKEN_FIELDS, (inp, cached or 0, write or 0, out, reasoning or 0)))

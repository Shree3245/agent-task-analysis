"""Offline Bai accounting investigation; emits allowlisted usage metadata only.

Mini archives are valid for call reconciliation, never for whole-task costs.
Full archives use final output.jsonl summaries, excluding critic attempts.
This diagnostic does not change moira's pricing or acceptance criteria.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tarfile

from moira.pricing.catalog import load_catalog
from moira.pricing.normalize import normalize, provider_for
from moira.pricing.reprice import call_cost
from moira.privacy import SafeError, label
from moira.schema import Call


# Explicit routes observed in these pinned public archives; no fuzzy tariff matching.
ROUTES = {
    "litellm_proxy/claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
    "litellm_proxy/anthropic/claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
    "litellm_proxy/claude-sonnet-4-20250514": "claude-sonnet-4-20250514",
}
FIELDS = (
    "prompt_tokens",
    "input_tokens",
    "completion_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
)


def metadata(usage):
    """Never copy arbitrary usage keys, nested payloads, or source content."""
    result = {
        k: usage[k]
        for k in FIELDS
        if isinstance(usage.get(k), (int, float)) and not isinstance(usage[k], bool)
    }
    for key, names in (
        ("prompt_tokens_details", ("cached_tokens", "cache_creation_tokens")),
        ("completion_tokens_details", ("reasoning_tokens",)),
    ):
        details = usage.get(key) or {}
        result[key] = {
            k: details[k]
            for k in names
            if isinstance(details.get(k), (int, float)) and not isinstance(details[k], bool)
        }
    return result


def inspect_call(usage, recorded, model, catalog):
    usage = metadata(usage)
    prompt = usage.get("prompt_tokens")
    output = usage.get("completion_tokens", usage.get("output_tokens"))
    read = usage.get(
        "cache_read_input_tokens",
        usage.get("cache_read_tokens", usage["prompt_tokens_details"].get("cached_tokens", 0)),
    )
    write = usage.get("cache_creation_input_tokens", usage.get("cache_write_tokens", 0))
    native = usage.get("input_tokens")
    identity = None if native is None or prompt is None else prompt == native + read + write
    model = ROUTES.get(model, model)
    provider = provider_for(model)
    reason = None
    try:
        cost, reason = call_cost(
            Call("audit", 0, provider=provider, model=model, **normalize(usage, provider)), catalog
        )
    except SafeError as error:
        cost, reason = None, str(error)
    source = None
    # Appendix B Eq. 1–2, explicitly restricted to the three Sonnet families
    # audited here with published rates 3 / .3 / 3.75 / 15 USD per million.
    if (
        model
        in {
            "claude-3-7-sonnet-20250219",
            "claude-sonnet-4-20250514",
            "claude-sonnet-4-5-20250929",
        }
        and prompt is not None
        and output is not None
    ):
        source = ((prompt - read) * 3 + read * 0.3 + write * 3.75 + output * 15) / 1e6
    tolerance = max(1e-12, recorded * 0.01) if recorded is not None else None
    return {
        "model": label(model),
        "usage": usage,
        "recorded_cost": recorded,
        "provider_cost": cost,
        "provider_reason": reason,
        "source_eq12_cost": source,
        "native_identity": identity,
        "inferred_input_residual": None if prompt is None else prompt - read - write,
        "provider_match": None
        if tolerance is None or cost is None
        else abs(cost - recorded) <= tolerance,
        "source_eq12_match": None
        if tolerance is None or source is None
        else abs(source - recorded) <= tolerance,
    }


def observations(path):
    mini = "_mini" in path.name
    with tarfile.open(path, "r|gz") as archive:
        for member in archive:
            if not member.isfile():
                continue
            if mini and member.name.endswith(".json"):
                root = json.load(archive.extractfile(member))
                response = root.get("response") or {}
                yield (
                    member.name,
                    response.get("usage") or {},
                    root.get("cost"),
                    response.get("model", "unknown"),
                )
            elif not mini and Path(member.name).name == "output.jsonl":
                with archive.extractfile(member) as stream:
                    for row_idx, line in enumerate(stream):
                        root = json.loads(line)
                        metrics = root.get("metrics") or {}
                        usages, costs = metrics.get("token_usages", []), metrics.get("costs", [])
                        if len(usages) != len(costs):
                            raise ValueError("Unaligned summary usage/cost arrays")
                        for idx, (usage, cost) in enumerate(zip(usages, costs)):
                            yield (
                                f"{member.name}:{row_idx}:{idx}",
                                usage,
                                cost.get("cost"),
                                usage.get("model", "unknown"),
                            )


def raw_examples(path, catalog, limit=5):
    """Inspect actual responses as well as summaries, without retaining payloads."""
    rows = []
    with tarfile.open(path, "r|gz") as archive:
        for member in archive:
            if (
                not member.isfile()
                or "/llm_completions/" not in member.name
                or not member.name.endswith(".json")
            ):
                continue
            root = json.load(archive.extractfile(member))
            response = root.get("response") or {}
            usage = response.get("usage") or {}
            row = inspect_call(usage, root.get("cost"), response.get("model", "unknown"), catalog)
            details = usage.get("cost_details") or {}
            # Numeric billing components only; never copy arbitrary cost_details fields.
            row["recorded_components"] = {
                name: details[name]
                for name in (
                    "upstream_inference_prompt_cost",
                    "upstream_inference_completions_cost",
                )
                if isinstance(details.get(name), (int, float))
                and not isinstance(details[name], bool)
            }
            row["record_hash"] = hashlib.sha256(member.name.encode()).hexdigest()
            rows.append(row)
            if len(rows) == limit:
                break
    return rows


def audit(path, catalog):
    counts = Counter()
    models = Counter()
    examples = []
    for identifier, usage, recorded, model in observations(path):
        counts["records"] += 1
        models[label(model)] += 1
        if not usage:
            counts["missing_usage"] += 1
        row = inspect_call(usage, recorded, model, catalog)
        counts["recorded_calls"] += recorded is not None
        counts["zero_recorded_cost"] += recorded == 0
        counts["native_identity_testable"] += row["native_identity"] is not None
        counts["native_identity_pass"] += row["native_identity"] is True
        counts["negative_input_residual"] += (row["inferred_input_residual"] or 0) < 0
        for basis in ("provider", "source_eq12"):
            counts[basis + "_comparable"] += row[basis + "_match"] is not None
            counts[basis + "_within_1pct"] += row[basis + "_match"] is True
        if row["provider_reason"]:
            counts[row["provider_reason"]] += 1
        if len(examples) < 5:
            examples.append({"record_hash": hashlib.sha256(identifier.encode()).hexdigest(), **row})
    n = counts["recorded_calls"]
    return {
        "archive": path.name,
        "scope": "final completion samples only"
        if "_mini" in path.name
        else "all final output.jsonl per-call summaries; critic attempts excluded",
        "counts": dict(counts),
        "models": dict(models),
        "provider_agreement_all_recorded": counts["provider_within_1pct"] / n if n else None,
        "source_eq12_agreement_all_recorded": counts["source_eq12_within_1pct"] / n
        if counts["source_eq12_comparable"] and n
        else None,
        "examples": examples,
        "raw_response_examples": raw_examples(path, catalog) if "_mini" not in path.name else [],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    catalog = load_catalog()
    results = []
    for path in args.archives:
        results.append(audit(path, catalog))
        print(path.name, results[-1]["counts"], flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "paper": "https://arxiv.org/html/2604.22750v3#A2",
                "source_code_revision": "335ecf2a29607bbfe8b13708f10b7b9091bcba45",
                "dataset_revision": "fa9cbb063f770df596da95af24f7af3b8f595778",
                "catalog_sha256": catalog["sha256"],
                "content_retained": False,
                "identity_limit": "Native input_tokens must be present independently; a reconstructed residual is not proof.",
                "results": results,
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()

# Bai accounting investigation

These are **benchmark tasks, not production workloads**. The report still uses
provider-correct pricing. No source-formula CLI mode was enabled: the requested
cross-model and independent native-token checks did not both hold.

## What the source formula establishes

[Appendix B, equations 1–2](https://arxiv.org/html/2604.22750v3#A2) computes
`(prompt_tokens - cache_read) * input_rate + cache_read * read_rate
+ cache_creation * write_rate + completion_tokens * output_rate`.
The [authors' implementation](https://github.com/LongjuBai/agent_token_consumption_analysis/blob/335ecf2a29607bbfe8b13708f10b7b9091bcba45/analysis/phase_level_analysis/token_cost_ratio_analysis.py#L80)
uses the same computation, with a zero floor on non-cached input. The audited
Sonnet rates are $3 / $0.30 / $3.75 / $15 per million tokens. None of the inspected
Sonnet samples needs that floor for `prompt_tokens - cache_read`.

If `prompt_tokens` includes writes, this formula charges those tokens at both the
base-input and cache-write rates. Provider-correct exclusive accounting charges
each token class once. Their difference is therefore exactly
`cache_creation * $3 / 1,000,000` for these Sonnet rates.

For the report's full Sonnet 3.7 selection:

- 2,000 final task trajectories; 88,439 model calls; 27 censored tasks.
- Recorded total: **$1,728.20700585**.
- Provider-correct token reprice: **$1,474.99911885**.
- Difference: **$253.20788700**.
- Standard-rate reconciliation: **83 / 88,439 (0.09385%)** within 1%.
- Adding the base-input charge on writes reproduces the recorded costs within 1%.
  This fits the source formula; it does not independently establish native input
  counts or authenticate a provider invoice.

## Cross-model check

The five compact archives retain final completions, not full task histories. They
are useful for checking call accounting but are not used to calculate task costs
or extend the report's verdict population.

| Model and scope | Calls | Provider-rate agreement within 1% | Appendix B Eq. 1–2 agreement |
| --- | ---: | --- | --- |
| Sonnet 3.7, compact final completions | 2,000 | 3 / 2,000 | 2,000 / 2,000 |
| Sonnet 4.5, compact final completions | 2,000 | 2,000 / 2,000 | 0 / 2,000 |
| Sonnet 4, compact final completions | 2,000 | Unavailable: every record has reads + writes greater than prompt tokens | 2,000 / 2,000 |
| GPT-5, compact final completions | 1,998 | 1,998 / 1,998 | Not applicable: Claude-specific equation |
| Qwen3-Coder-480B, compact final completions | 2,000 | Unavailable: all costs recorded as zero; no verified hosted tariff | Not applicable |
| Kimi-K2, all final summary calls in full archive | 152,054 | Unavailable: OpenRouter route has no verified historical tariff in Moira | Not applicable |

The GPT-5 comparison uses $1.25 input, $0.125 cached input, and $10 output per
million. It is a provider-rate check, not a reproduction of Appendix B Eq. 4:
that printed equation uses `0.2 * input_rate`, inconsistent with the $0.125 cached
rate quoted immediately above it.

Kimi has 15 zero-cost records among 152,054 summary calls. In five separately
inspected raw responses, the recorded output component divided by output tokens
implies $2.50, $2.50, $3.00, $3.00, and $2.50 per million. One response charges
all prompt tokens at $0.60 despite reporting cached tokens; another fits a
$0.15 cache-read rate. These are observed billing components, not tariffs fitted
into Moira to force agreement. The [OpenRouter model page](https://openrouter.ai/moonshotai/kimi-k2-0905)
identifies the route and currently lists $0.60/$2.50 input/output; a current list
price cannot establish the route used by every historical request.

Thus GPT-5 matching does not establish that GPT, Qwen and Kimi all match. Nor does
the Sonnet 3.7 result generalize to all Claude exports: applying its extra charge
would break the already-matching Sonnet 4.5 sample.

## Five raw Sonnet 3.7 records

These are the first five completion records encountered in the pinned compact
Sonnet 3.7 archive. Only numeric usage and cost metadata was saved.

| Record | prompt_tokens | cache_creation | cache_read | Native input_tokens | Inferred residual |
| --- | ---: | ---: | ---: | --- | ---: |
| 1 | 73,916 | 725 | 73,191 | Absent | 0 |
| 2 | 89,395 | 655 | 88,740 | Absent | 0 |
| 3 | 62,365 | 238 | 62,127 | Absent | 0 |
| 4 | 40,691 | 356 | 40,335 | Absent | 0 |
| 5 | 31,463 | 446 | 31,017 | Absent | 0 |

All five satisfy `prompt_tokens = cache_creation + cache_read`. But they omit
native `input_tokens`, so the requested three-way identity cannot be verified
independently. Setting input to the inferred residual would make the test circular.
[Anthropic's API documentation](https://platform.claude.com/docs/en/api/typescript/messages)
defines native total input as the sum of the three classes; it does not prove
which historical normalization a proxy applied to a particular export.

## Verdict rerun

The regenerated [HTML report](openhands-bai.html) and [Markdown report](openhands-bai.md)
use the same default exclusive token accounting as before. No rates or tokens were
changed to make recorded costs match. The `code` verdict remains **VIABLE** under
the specified simulation rule; recorded-cost acceptance remains **FAIL**.

| Censoring scenario | Fitted price at 70% target | Holdout loss ratio | 90% bootstrap interval |
| --- | ---: | ---: | --- |
| Exclude censored runs | $1.0271/task | 68.62% | 66.44%–70.92% |
| Inflate censored costs by the training tail | $1.0817/task | 68.93% | 66.24%–71.66% |

Both use the training p99 cap of **$2.3406**, stop after the crossing call, and
include overshoot. Both interval upper bounds are below 90%; censoring scenarios
agree. Caps represent unfinished work. The result remains conditional on the
export's token semantics, public rates, and the other report limits.

## Evidence and reproduction

- [Compact-archive audit](bai-mini-cost-audit.json): per-model counts and five
  metadata-only raw examples per archive.
- [Kimi audit](bai-kimi-cost-audit.json): full final-summary counts and five raw
  response examples with numeric recorded billing components.
- [Corrected-cost verdict rerun](bai-corrected-verdicts.json): reconciliation and
  both capped holdout scenarios, including the 2,000-draw intervals.

Dataset revision: `fa9cbb063f770df596da95af24f7af3b8f595778` of
`loong0814/openhands_trajectories`. Author code revision:
`335ecf2a29607bbfe8b13708f10b7b9091bcba45`. Public archives remain outside this repo.
The download script verifies SHA-256 against the published LFS hashes.

```sh
uv run python benchmarks/download_openhands_bai.py \
  --out "$DATA_DIR/bai-mini" --include '*_mini.tar.gz'
uv run python benchmarks/download_openhands_bai.py \
  --out "$DATA_DIR/bai-kimi" --include 'kimi-k2_4runs.tar.gz'
uv run python benchmarks/audit_bai_costs.py "$DATA_DIR/bai-mini/"*_mini.tar.gz \
  --out benchmarks/results/bai-mini-cost-audit.json
uv run python benchmarks/audit_bai_costs.py "$DATA_DIR/bai-kimi/kimi-k2_4runs.tar.gz" \
  --out benchmarks/results/bai-kimi-cost-audit.json
moira report --db "$DATA_DIR/bai.duckdb" --redact-task-ids \
  --out benchmarks/results/openhands-bai.html
```

The report database comes from the full Sonnet 3.7 ingestion command in
[the benchmark instructions](../README.md). The audit is offline and does not
extract archive contents. It reproduces Eq. 1–2 as a diagnostic only, never as a
replacement for default pricing or an automatic acceptance override.

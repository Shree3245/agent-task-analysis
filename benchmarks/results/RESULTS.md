# Measured results

Generated locally with moira 0.1.0 on 2026-10-23. **Benchmark tasks, not production
workloads.** All reports use the shipped `2026-10-23.1` catalog and hashed task IDs.
Each HTML has an equivalent Markdown file and a source/checksum provenance manifest.

| Collection | Selected scope | Tasks | Model calls | Capped | Fully priceable tasks |
| --- | --- | ---: | ---: | ---: | ---: |
| [Bai OpenHands](openhands-bai.html) | Full Sonnet 3.7 archive; four final-trajectory runs | 2,000 | 88,439 | 27 | 2,000 |
| [ASSERT-KTH](assert-kth.html) | Qwen3-32B: one nano-agent run + one R2E-Gym run | 1,000 | 20,879 | 169 | 0 |
| [Exgentic v1](exgentic.html) | All 39 published Parquet shards | 1,781 | 38,052 | 0 detected | 111 |
| [HAL](hal.html) | One GPT-4.1 SciCode evaluation, officially decrypted | 65 | 288 | 0 detected | 65 |

“Fully priceable” means all observed model calls have rates and usage. It does not
mean uncensored: the 27 Bai capped runs remain censored. Zero detected caps in other
exports does not establish that no run was limited; source signals may be absent.

## Recorded-cost agreement: an unresolved acceptance gate

The independent standard-rate fixture tests reconcile at 100%. **The actual Bai
export fails the requested >=99% agreement gate:** only 83/88,439 calls (0.09385%)
are within 1% of recorded cost under standard public rates.

- Recorded comparable cost: **$1,728.20700585**.
- Standard token reprice: **$1,474.99911885**.
- Difference: **$253.20788700**.
- All 88,439 recorded costs match, within 1%, the formula
  `standard_reprice + cache_write_tokens × $3 / 1,000,000`.

The [Appendix B investigation](BAI_ACCOUNTING.md) now confirms that the paper and
authors' code use a formula that adds this charge when prompt tokens include cache
writes. Cross-model evidence does not establish a universal correction: Sonnet 4.5
already matches standard rates, Sonnet 4 has inconsistent inclusive counts, Qwen
records zero costs, and Kimi lacks a verified historical route tariff. Five raw
Sonnet 3.7 records also omit native input counts, preventing an independent identity
check. Moira keeps standard prices unchanged and reports **FAIL**. The conditional
source-formula mode was not enabled; the formula is reproduced only in the offline
audit. Arithmetic agreement is not independent validation of native token parsing.

The other selected datasets lack per-call recorded dollar costs, so reconciliation
is **UNAVAILABLE**, not PASS. Aggregate dataset costs are not assigned to calls to
manufacture a comparison.

## Reading the verdicts

Bai's `code` type passes the specified capped interval rule **under the
standard-rate scenario**. The same 500 SWE-bench instances appear in all four runs, so
the verdict now uses grouped cross-validation by instance. Held-out-fold capped
intervals are 61.7–79.1% excluding censored runs and 60.1–81.0% with tail inflation,
at a mean fold price of $1.0171. The time split, which leaks repeated instances, gave
66.3–70.9% and 66.1–71.7%: its upper bound was about 8–9 points too optimistic.
Success-only billing stays VIABLE up to a 65% target, at $1.8030 per resolved task.
The six-model comparison is in [bai-models/COMPARISON.md](bai-models/COMPARISON.md). The recorded-billing discrepancy is prominently
flagged before that verdict. It is not a claim about actual production margins or
the value of unfinished work.

ASSERT-KTH has no supplied hosted-vLLM tariff. Nano-agent also lacks per-call token
classes; R2E-Gym supplies step tokens but no absolute timestamps. Its NOT VIABLE
verdict means insufficient cost/time evidence, not proven poor economics.

Exgentic v1 omits cache breakdowns and recorded dollars. Most model IDs refer to
cloud-specific routes without matching catalog entries; these stay unknown. The
known-spend lower bound is $205.41913775, not the dataset's actual total cost. Only
111 sessions have all calls priceable. All six type verdicts are NOT VIABLE because
cost coverage and/or temporal sample evidence are insufficient.

HAL's selected evaluation has complete token usage and a standard-rate total of
$2.522736, but insufficient uncapped holdout sample size for the default verdict
threshold. Its task outcomes come from the evaluation's success/failure lists.

## Verification performed

- 66 tests pass with network sockets disabled, including a canary test for all nine
  adapters, malformed-input redaction, cap signals, duplicate events, multi-tool
  accounting, token-class normalization, time-split leakage, equal-type weighting,
  bootstrap determinism, and censoring disagreement.
- Ruff checks pass. Source distribution and wheel build successfully.
- The wheel installs in a separate environment outside the repo; its public-data
  demo passes with sockets and DNS blocked and imports from isolated site-packages.
- The Bai HTML was opened by an isolated headless Chrome context in offline mode:
  all seven sections, two SVG charts, zero external requests, zero JavaScript errors,
  and no document overflow at 1,440px or 390px width. Screenshots were visually
  inspected; see [browser verification](qa/verification.json).
- Raw/decrypted data and local databases remain outside this repository. No public
  dataset uploads or private-log network calls were made.

These runs do not claim complete coverage of all models/evaluations in the much
larger Bai, ASSERT-KTH, or HAL collections. Exact selection and revisions are in the
companion provenance manifests and [reproduction instructions](../README.md).

# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

65 tasks. Price catalog 2026-10-23.1 · SHA-256 74182d05619a62951c47e44eb2c2222f86f1bf516325820588970e093abe012b.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

HAL subset: 1 explicitly downloaded and decrypted evaluations. Decryption used HAL&#x27;s published script outside this repository.

Import 1: hal · 1 files · 1 records. Fields read: benchmark_name, ended_at, id, output.model, output.usage, results.failed_tasks, results.successful_tasks, started_at, weave_task_id

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2025-04-21T20:12:50.239691+00:00; 5 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $2.5227. Overall distribution weights each of 1 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| scicode | 65 | 0 | 0 | NOT VIABLE | exclude: fewer than 30 uncapped tasks in training or holdout; exclude: upper loss-ratio interval is 219.6%, needs &lt;90% |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| scicode | hal | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scicode | 65 | $0.0388 | $0.0280 | $0.0731 | $0.2270 | $0.3429 | 2.61 | 13.6% | 30.1% |
| Overall · equal type weight | 65 | $0.0388 | $0.0280 | $0.0800 | $0.3429 | $0.3429 | 2.86 | 8.8% | 26.7% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| scicode | 65 | 0 | 0.0% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 93.8%; their spend per task $0.0380; tasks with loop signals 0.0%. Raw dollar totals below are accounting totals.

Repricing acceptance: UNAVAILABLE. 0 of 0 recorded-cost calls within 1% (—); 0 comparable calls (— agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.0000; standard-rate reprice $0.0000; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| scicode | 4 | 65/65 | 6.2% | 65/4 | $0.6307 |

### Unknown models

| Provider/model | Calls |
| --- | --- |

No available observations for this table.

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |

No available observations for this table.

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| scicode | $2.5227 | $2.4717 | $0.0000 | 0 | 14.00 |

### scicode · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-2bd64796dd6fe35c702f1562d42b05146b2a0a59d2d2af2f610eb1d48bfd2303 | $0.3429 | complete | fail | False |
| task-f2f32dbd46edc562cae263a2ab5e140f983733ca3bd552b58d8af58c3acc7766 | $0.1618 | complete | fail | False |
| task-7c3d984439718f9bc1b8546547bd31d0e5527b40c87438ca7b9e1eacc01c74a8 | $0.1393 | complete | fail | False |
| task-e21f1204a3966473813dbd254f22cfbf05f8ba16ff538d9e1d15e02b27de26ad | $0.1155 | complete | fail | False |
| task-d6b164fbb9532fcd6879b1dbdf508a94e96d742693ef7f62f4230e291ddc8c68 | $0.0973 | complete | fail | False |
| task-47c51fd7b56ed56e792c5bc63107dd246031cd0d41d4b44a0b8d24f971362738 | $0.0868 | complete | fail | False |
| task-a5afb000bdd5891944c5444dbaa4fc205d6cdf89a2874d10f2ac3cfcb2d92c37 | $0.0800 | complete | fail | False |
| task-f855f2768853f4049fe8293630a057a1f2c884920f28af09530f5e4eb2edbf8c | $0.0628 | complete | fail | False |
| task-91580790f32b0e3f5121d7fcef097212458d550cdb0155b41ab0230c659bd66c | $0.0625 | complete | fail | False |
| task-fb860c063b4dd54db0c70d02986e347537dd56e2201287f1fd19dab98d4912ec | $0.0553 | complete | fail | False |

### scicode · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |

No available observations for this table.

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| scicode | p95 | $0.1118 | 4.6% | $0.2808 | 11.1% | 6.2% | $0.3121 |
| scicode | p99 | $0.2270 | 1.5% | $0.0849 | 3.4% | 1.5% | $0.1159 |
| scicode | p99.5 | $0.2849 | 0.0% | $0.0000 | 0.0% | 1.5% | $0.0580 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 1 | 4.6% | $0.0043 | 11.1% |
| p99 | 1 | 1.5% | $0.0013 | 3.4% |
| p99.5 | 1 | 0.0% | $0.0000 | 0.0% |

## Fixed-price simulation with confidence intervals

Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.

In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.

Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type&#x27;s mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the &lt;90% upper-CI decision is flagged in the verdict.

Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.

### scicode

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $0.0647 | 60.0% | 46.3% – 76.3% | 10.8% | $0.2782 | 65/65 |
| in_sample | exclude | none | 70.0% | $0.0554 | 70.0% | 54.0% – 89.0% | 13.8% | $0.2875 | 65/65 |
| in_sample | exclude | none | 80.0% | $0.0485 | 80.0% | 61.7% – 101.8% | 18.5% | $0.2944 | 65/65 |
| in_sample | exclude | p99 | 60.0% | $0.0625 | 60.0% | 47.8% – 73.7% | 12.3% | $0.1955 | 65/65 |
| in_sample | exclude | p99 | 70.0% | $0.0536 | 70.0% | 55.8% – 86.0% | 15.4% | $0.2045 | 65/65 |
| in_sample | exclude | p99 | 80.0% | $0.0469 | 80.0% | 63.8% – 98.3% | 20.0% | $0.2111 | 65/65 |
| in_sample | inflate | none | 60.0% | $0.0647 | 60.0% | 46.3% – 76.3% | 10.8% | $0.2782 | 65/65 |
| in_sample | inflate | none | 70.0% | $0.0554 | 70.0% | 54.0% – 89.0% | 13.8% | $0.2875 | 65/65 |
| in_sample | inflate | none | 80.0% | $0.0485 | 80.0% | 61.7% – 101.8% | 18.5% | $0.2944 | 65/65 |
| in_sample | inflate | p99 | 60.0% | $0.0625 | 60.0% | 47.8% – 73.7% | 12.3% | $0.1955 | 65/65 |
| in_sample | inflate | p99 | 70.0% | $0.0536 | 70.0% | 55.8% – 86.0% | 15.4% | $0.2045 | 65/65 |
| in_sample | inflate | p99 | 80.0% | $0.0469 | 80.0% | 63.8% – 98.3% | 20.0% | $0.2111 | 65/65 |
| holdout | exclude | none | 60.0% | $0.0542 | 134.1% | 94.9% – 178.8% | 50.0% | $0.1076 | 52/8 |
| holdout | exclude | none | 70.0% | $0.0464 | 156.5% | 110.7% – 208.6% | 75.0% | $0.1153 | 52/8 |
| holdout | exclude | none | 80.0% | $0.0406 | 178.8% | 126.5% – 238.4% | 87.5% | $0.1211 | 52/8 |
| holdout | exclude | p99 | 60.0% | $0.0515 | 141.2% | 99.9% – 188.2% | 50.0% | $0.1103 | 52/8 |
| holdout | exclude | p99 | 70.0% | $0.0441 | 164.8% | 116.6% – 219.6% | 87.5% | $0.1176 | 52/8 |
| holdout | exclude | p99 | 80.0% | $0.0386 | 188.3% | 133.2% – 251.0% | 87.5% | $0.1232 | 52/8 |
| holdout | inflate | none | 60.0% | $0.0542 | 134.1% | 94.9% – 178.8% | 50.0% | $0.1076 | 52/8 |
| holdout | inflate | none | 70.0% | $0.0464 | 156.5% | 110.7% – 208.6% | 75.0% | $0.1153 | 52/8 |
| holdout | inflate | none | 80.0% | $0.0406 | 178.8% | 126.5% – 238.4% | 87.5% | $0.1211 | 52/8 |
| holdout | inflate | p99 | 60.0% | $0.0515 | 141.2% | 99.9% – 188.2% | 50.0% | $0.1103 | 52/8 |
| holdout | inflate | p99 | 70.0% | $0.0441 | 164.8% | 116.6% – 219.6% | 87.5% | $0.1176 | 52/8 |
| holdout | inflate | p99 | 80.0% | $0.0386 | 188.3% | 133.2% – 251.0% | 87.5% | $0.1232 | 52/8 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | exclude | none | 60.0% | $0.0542 | 134.1% | 94.9% – 178.8% | 50.0% | $0.1076 | 52/8 |
| holdout | exclude | none | 70.0% | $0.0464 | 156.5% | 110.7% – 208.6% | 75.0% | $0.1153 | 52/8 |
| holdout | exclude | none | 80.0% | $0.0406 | 178.8% | 126.5% – 238.4% | 87.5% | $0.1211 | 52/8 |
| holdout | exclude | p99 | 60.0% | $0.0515 | 141.2% | 99.9% – 188.2% | 50.0% | $0.1103 | 52/8 |
| holdout | exclude | p99 | 70.0% | $0.0441 | 164.8% | 116.6% – 219.6% | 87.5% | $0.1176 | 52/8 |
| holdout | exclude | p99 | 80.0% | $0.0386 | 188.3% | 133.2% – 251.0% | 87.5% | $0.1232 | 52/8 |
| holdout | inflate | none | 60.0% | $0.0542 | 134.1% | 94.9% – 178.8% | 50.0% | $0.1076 | 52/8 |
| holdout | inflate | none | 70.0% | $0.0464 | 156.5% | 110.7% – 208.6% | 75.0% | $0.1153 | 52/8 |
| holdout | inflate | none | 80.0% | $0.0406 | 178.8% | 126.5% – 238.4% | 87.5% | $0.1211 | 52/8 |
| holdout | inflate | p99 | 60.0% | $0.0515 | 141.2% | 99.9% – 188.2% | 50.0% | $0.1103 | 52/8 |
| holdout | inflate | p99 | 70.0% | $0.0441 | 164.8% | 116.6% – 219.6% | 87.5% | $0.1176 | 52/8 |
| holdout | inflate | p99 | 80.0% | $0.0386 | 188.3% | 133.2% – 251.0% | 87.5% | $0.1232 | 52/8 |
| in_sample | exclude | none | 60.0% | $0.0647 | 60.0% | 46.3% – 76.3% | 10.8% | $0.2782 | 65/65 |
| in_sample | exclude | none | 70.0% | $0.0554 | 70.0% | 54.0% – 89.0% | 13.8% | $0.2875 | 65/65 |
| in_sample | exclude | none | 80.0% | $0.0485 | 80.0% | 61.7% – 101.8% | 18.5% | $0.2944 | 65/65 |
| in_sample | exclude | p99 | 60.0% | $0.0625 | 60.0% | 47.8% – 73.7% | 12.3% | $0.1955 | 65/65 |
| in_sample | exclude | p99 | 70.0% | $0.0536 | 70.0% | 55.8% – 86.0% | 15.4% | $0.2045 | 65/65 |
| in_sample | exclude | p99 | 80.0% | $0.0469 | 80.0% | 63.8% – 98.3% | 20.0% | $0.2111 | 65/65 |
| in_sample | inflate | none | 60.0% | $0.0647 | 60.0% | 46.3% – 76.3% | 10.8% | $0.2782 | 65/65 |
| in_sample | inflate | none | 70.0% | $0.0554 | 70.0% | 54.0% – 89.0% | 13.8% | $0.2875 | 65/65 |
| in_sample | inflate | none | 80.0% | $0.0485 | 80.0% | 61.7% – 101.8% | 18.5% | $0.2944 | 65/65 |
| in_sample | inflate | p99 | 60.0% | $0.0625 | 60.0% | 47.8% – 73.7% | 12.3% | $0.1955 | 65/65 |
| in_sample | inflate | p99 | 70.0% | $0.0536 | 70.0% | 55.8% – 86.0% | 15.4% | $0.2045 | 65/65 |
| in_sample | inflate | p99 | 80.0% | $0.0469 | 80.0% | 63.8% – 98.3% | 20.0% | $0.2111 | 65/65 |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### scicode · task-37190ba3a66c747c1e7c6fd2d1f4af73efdd46e9b10f84d11e760e3228515c01 · fixed $0.0441 (holdout) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | $0.0023 |

### scicode · task-21dc205beb8c0fe22173db5914f751733875dc27cd4b64315c193c45b43715ba · fixed $0.0441 (holdout) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 3 | $0.0142 |

### scicode · task-ff6fb5b42f07cd9320854392121b264648a93d6e3df9bb0b6df76083b6d1c990 · fixed $0.0441 (holdout) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 5 | $0.0280 |

### scicode · task-1edad649b38d445baaf55ee1d43b1dab2f0f0fa0872d3d1085a971e4d08e0586 · fixed $0.0441 (holdout) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 3 | $0.0400 |

### scicode · task-2bd64796dd6fe35c702f1562d42b05146b2a0a59d2d2af2f610eb1d48bfd2303 · fixed $0.0441 (holdout) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 14 | $0.3429 |

## Limits

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:33:29.196910+00:00. No network requests are required to view this file.

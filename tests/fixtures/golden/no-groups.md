# What this report saw

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

240 tasks. Price catalog 2026-10-23.1 · SHA-256 74182d05619a62951c47e44eb2c2222f86f1bf516325820588970e093abe012b.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2025-01-07T15:20:01.333333+00:00; 0 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $4.5534. Overall distribution weights each of 2 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 160 | 4 | 0 | VIABLE | holdout: upper loss-ratio interval stays below 90% at the 70% target with p99 cap |
| review | 80 | 3 | 0 | NOT VIABLE | exclude: fewer than 30 uncapped tasks in training or holdout; inflate: fewer than 30 uncapped tasks in training or holdout |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | synthetic | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| review | synthetic | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 156 | $0.0182 | $0.0159 | $0.0384 | $0.0567 | $0.0683 | 2.41 | 4.5% | 14.9% |
| review | 77 | $0.0203 | $0.0179 | $0.0389 | $0.0660 | $0.0789 | 2.18 | 5.0% | 15.3% |
| Overall · equal type weight | 233 | $0.0193 | $0.0166 | $0.0387 | $0.0619 | $0.0789 | 2.34 | 3.9% | 14.7% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Drift and recency

Windows use task start times and end at the latest start in this report (2025-01-10T23:00:00+00:00), not today&#x27;s date. Recent window: the last 30 days. Fit window: the tasks the verdict price is fit on (the time-split training period, or the whole pool under grouped CV). Means use complete, uncapped tasks.

Reprice recommended when the recent mean differs from the fit-window mean by more than 25%. With fewer than 30 tasks in either window the ratio is noisy; it is flagged but still shown.

Recency-window pricing at the 70% target, p99 cap, capped runs excluded. The full-period price is fit on the whole time-split training period; the recent-fit price on its last 30 days only. Both are scored on the same holdout. The current price is fit in-sample on the last 30 days of all data: it is what a recent fit charges now, and it has no holdout yet.

### Drift per pool

| Type | Fit window | Fit tasks | Fit mean | Recent window (last 30 days) | Recent tasks | Recent mean | Recent ÷ fit | Reprice recommended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 2025-01-01 – 2025-01-07 | 103 | $0.0180 | 2025-01-01 – 2025-01-10 | 156 | $0.0182 | 1.01 | no |
| review | 2025-01-01 – 2025-01-07 | 52 | $0.0206 | 2025-01-01 – 2025-01-10 | 77 | $0.0203 | 0.98 | no |

### Recency-window pricing

| Type | Full-period price | Train/test uncapped | Holdout loss ratio | 90% CI | Recent-fit window | Recent-fit price | Train/test uncapped | Holdout loss ratio | 90% CI | Current price (last 30 days, not validated) | Current window tasks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | $0.0257 | 103/53 | 72.6% | 61.8% – 84.2% | 2025-01-01 – 2025-01-07 | $0.0257 | 103/53 | 72.6% | 61.8% – 84.2% | $0.0261 | 156 |
| review | $0.0295 | 52/25 | 66.7% | 52.2% – 83.2% | 2025-01-01 – 2025-01-07 | $0.0295 | 52/25 | 66.7% | 52.2% – 83.2% | $0.0290 | 77 |

### Weekly mean cost · complete, uncapped tasks

| Type | Week of | Tasks | Mean | Total |
| --- | --- | --- | --- | --- |
| code | 2024-12-30 | 78 | $0.0183 | $1.4291 |
| code | 2025-01-06 | 78 | $0.0182 | $1.4167 |
| review | 2024-12-30 | 38 | $0.0226 | $0.8586 |
| review | 2025-01-06 | 39 | $0.0181 | $0.7050 |

## Cost audit

Equal-type overall: failed/aborted tasks 0.0%; their spend per task $0.0000; tasks with loop signals 0.0%. Raw dollar totals below are accounting totals.

Repricing acceptance: UNAVAILABLE. 0 of 0 recorded-cost calls within 1% (—); 0 comparable calls (— agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per successful task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.0000; standard-rate reprice $0.0000; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per successful task

| Type | Resolved | Known outcomes / tasks | Success rate | Priced tasks / priced successes | Priced spend / confirmed success |
| --- | --- | --- | --- | --- | --- |
| code | 160 | 160/160 | 100.0% | 160/160 | $0.0184 |
| review | 80 | 80/80 | 100.0% | 80/80 | $0.0201 |

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
| code | $2.9417 | $0.0000 | $0.0959 | 0 | 5.00 |
| review | $1.6117 | $0.0000 | $0.0481 | 0 | 5.00 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-c44474038d459e40e4714afefa7bf8dae9f9834b22f5e8ec1dd434ecb62b512e | $0.0683 | complete | success | False |
| task-0e9897794250e4d04bf0f641193ac4aa60a0f7eb398adbc85c7e81fb338e14ac | $0.0586 | complete | success | False |
| task-e7777240b9496c5c378ce775374b3435698527f2798f749ab9ceba486869cba6 | $0.0552 | complete | success | False |
| task-8949c3180c9357efa6ffa5673c5fc103fc4a9c79b8f612544298ffa66beca554 | $0.0527 | complete | success | False |
| task-851a67139d558236d5be6ae4a1e7547cf316f18070a4514d2a4c819b61eb1a3c | $0.0488 | complete | success | False |
| task-a4c799aad93e60004381edb70b426d3d02a3d2daaada56632c72ba9a149c7cce | $0.0487 | complete | success | False |
| task-356b9af4e8a7ab58bc06d84b037bdb7b1b4936d97a1ea0f0fbbcacb9ba1a94cb | $0.0483 | complete | success | False |
| task-1dfbdd3a71e6a47ee2061227744f279c0b02fc5e41ed42e2887e5c517f1fd8cc | $0.0446 | complete | success | False |
| task-b233c090327b1b9dd34c4a07112b770a3d1040c49839af760a78f7eeeb9e5846 | $0.0445 | complete | success | False |
| task-100805c88b9c8a47e825a45a3d5ccda8bce131bc41c2eb333de78e40d827af5a | $0.0443 | complete | success | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |

No available observations for this table.

### review · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-e8816c740eb9b470ce55839b91e1070a22ca77e225278ad0fc2866bd542fa337 | $0.0789 | complete | success | False |
| task-564679730e0aff0edb037eafe69017a15eb22dad17c3bbe80d8109aa5c54d49d | $0.0619 | complete | success | False |
| task-e24e11787de370252be17ade26ac788a0adf4790bcd187e398a0fd283db73ad5 | $0.0498 | complete | success | False |
| task-a5db1805cfa292a9c3d00ef5b932266a7f70ad2e52358217ebde8ff05514e77d | $0.0483 | complete | success | False |
| task-2f2b1afc0a29221249251fcd318abd8b14abc41a0d4088e581b9585c3cba4da2 | $0.0429 | complete | success | False |
| task-11d30b65f715c67e217c706a5bd1d43418b15a5e095ac0fea1dc9a6beeb69254 | $0.0411 | complete | success | False |
| task-b6cc17ffca0e52d65fac77537baffef3fc4bc3326d18b3ad5d91340bc2c6a529 | $0.0410 | complete | success | False |
| task-771cb6925b236b5d10ee3450cf3d4e9594aaabc3adf7873e291ad2231a8f8d38 | $0.0405 | complete | success | False |
| task-e12867583c08b185409d301a17f658959be57eea7451a9f3634bb4c2f6526965 | $0.0377 | complete | success | False |
| task-8a37b83c96f1aa17d63d5db633defe9edaca1d3958f2eae81c94b48be948e4f6 | $0.0373 | complete | success | False |

### review · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |

No available observations for this table.

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | p95 | $0.0445 | 0.6% | $0.0020 | 0.1% | 5.1% | $0.0689 |
| code | p99 | $0.0567 | 0.0% | $0.0000 | 0.0% | 1.3% | $0.0135 |
| code | p99.5 | $0.0608 | 0.0% | $0.0000 | 0.0% | 0.6% | $0.0076 |
| review | p95 | $0.0440 | 3.9% | $0.0529 | 3.4% | 5.2% | $0.0629 |
| review | p99 | $0.0660 | 0.0% | $0.0000 | 0.0% | 1.3% | $0.0129 |
| review | p99.5 | $0.0724 | 0.0% | $0.0000 | 0.0% | 1.3% | $0.0065 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 2 | 2.3% | $0.0003 | 1.7% |
| p99 | 2 | 0.0% | $0.0000 | 0.0% |
| p99.5 | 2 | 0.0% | $0.0000 | 0.0% |

## Fixed-price simulation with confidence intervals

Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.

In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.

Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type&#x27;s mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the &lt;90% upper-CI decision is flagged in the verdict.

Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.

### code

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $0.0304 | 60.0% | 54.2% – 66.1% | 16.7% | $0.0379 | 156/156 |
| in_sample | exclude | none | 70.0% | $0.0261 | 70.0% | 63.2% – 77.1% | 24.4% | $0.0423 | 156/156 |
| in_sample | exclude | none | 80.0% | $0.0228 | 80.0% | 72.2% – 88.2% | 30.8% | $0.0455 | 156/156 |
| in_sample | exclude | p99 | 60.0% | $0.0304 | 60.0% | 54.2% – 66.1% | 16.7% | $0.0379 | 156/156 |
| in_sample | exclude | p99 | 70.0% | $0.0261 | 70.0% | 63.2% – 77.1% | 24.4% | $0.0423 | 156/156 |
| in_sample | exclude | p99 | 80.0% | $0.0228 | 80.0% | 72.2% – 88.2% | 30.8% | $0.0455 | 156/156 |
| in_sample | inflate | none | 60.0% | $0.0329 | 60.0% | 53.6% – 66.9% | 17.5% | $0.0625 | 160/160 |
| in_sample | inflate | none | 70.0% | $0.0282 | 70.0% | 62.6% – 78.1% | 21.2% | $0.0672 | 160/160 |
| in_sample | inflate | none | 80.0% | $0.0246 | 80.0% | 71.5% – 89.2% | 30.0% | $0.0707 | 160/160 |
| in_sample | inflate | p99 | 60.0% | $0.0329 | 60.0% | 53.6% – 66.9% | 17.5% | $0.0625 | 160/160 |
| in_sample | inflate | p99 | 70.0% | $0.0282 | 70.0% | 62.6% – 78.1% | 21.2% | $0.0672 | 160/160 |
| in_sample | inflate | p99 | 80.0% | $0.0246 | 80.0% | 71.5% – 89.2% | 30.0% | $0.0707 | 160/160 |
| holdout | exclude | none | 60.0% | $0.0300 | 62.2% | 53.0% – 72.1% | 22.6% | $0.0286 | 103/53 |
| holdout | exclude | none | 70.0% | $0.0257 | 72.6% | 61.8% – 84.2% | 26.4% | $0.0328 | 103/53 |
| holdout | exclude | none | 80.0% | $0.0225 | 82.9% | 70.6% – 96.2% | 28.3% | $0.0361 | 103/53 |
| holdout | exclude | p99 | 60.0% | $0.0300 | 62.2% | 53.0% – 72.1% | 22.6% | $0.0286 | 103/53 |
| holdout | exclude | p99 | 70.0% | $0.0257 | 72.6% | 61.8% – 84.2% | 26.4% | $0.0328 | 103/53 |
| holdout | exclude | p99 | 80.0% | $0.0225 | 82.9% | 70.6% – 96.2% | 28.3% | $0.0361 | 103/53 |
| holdout | inflate | none | 60.0% | $0.0325 | 61.8% | 51.2% – 73.5% | 22.2% | $0.0627 | 106/54 |
| holdout | inflate | none | 70.0% | $0.0279 | 72.1% | 59.8% – 85.8% | 24.1% | $0.0673 | 106/54 |
| holdout | inflate | none | 80.0% | $0.0244 | 82.4% | 68.3% – 98.1% | 29.6% | $0.0708 | 106/54 |
| holdout | inflate | p99 | 60.0% | $0.0325 | 61.8% | 51.2% – 73.5% | 22.2% | $0.0627 | 106/54 |
| holdout | inflate | p99 | 70.0% | $0.0279 | 72.1% | 59.8% – 85.8% | 24.1% | $0.0673 | 106/54 |
| holdout | inflate | p99 | 80.0% | $0.0244 | 82.4% | 68.3% – 98.1% | 29.6% | $0.0708 | 106/54 |

### review

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $0.0338 | 60.0% | 52.2% – 68.5% | 15.6% | $0.0451 | 77/77 |
| in_sample | exclude | none | 70.0% | $0.0290 | 70.0% | 60.8% – 79.9% | 23.4% | $0.0499 | 77/77 |
| in_sample | exclude | none | 80.0% | $0.0254 | 80.0% | 69.5% – 91.4% | 36.4% | $0.0535 | 77/77 |
| in_sample | exclude | p99 | 60.0% | $0.0338 | 60.0% | 52.2% – 68.5% | 15.6% | $0.0451 | 77/77 |
| in_sample | exclude | p99 | 70.0% | $0.0290 | 70.0% | 60.8% – 79.9% | 23.4% | $0.0499 | 77/77 |
| in_sample | exclude | p99 | 80.0% | $0.0254 | 80.0% | 69.5% – 91.4% | 36.4% | $0.0535 | 77/77 |
| in_sample | inflate | none | 60.0% | $0.0373 | 60.0% | 51.4% – 69.5% | 15.0% | $0.0477 | 80/80 |
| in_sample | inflate | none | 70.0% | $0.0320 | 70.0% | 59.9% – 81.1% | 23.8% | $0.0530 | 80/80 |
| in_sample | inflate | none | 80.0% | $0.0280 | 80.0% | 68.5% – 92.7% | 31.2% | $0.0570 | 80/80 |
| in_sample | inflate | p99 | 60.0% | $0.0373 | 60.0% | 51.4% – 69.5% | 15.0% | $0.0477 | 80/80 |
| in_sample | inflate | p99 | 70.0% | $0.0320 | 70.0% | 59.9% – 81.1% | 23.8% | $0.0530 | 80/80 |
| in_sample | inflate | p99 | 80.0% | $0.0280 | 80.0% | 68.5% – 92.7% | 31.2% | $0.0570 | 80/80 |
| holdout | exclude | none | 60.0% | $0.0344 | 57.2% | 44.8% – 71.3% | 16.0% | $0.0275 | 52/25 |
| holdout | exclude | none | 70.0% | $0.0295 | 66.7% | 52.2% – 83.2% | 24.0% | $0.0324 | 52/25 |
| holdout | exclude | none | 80.0% | $0.0258 | 76.2% | 59.7% – 95.0% | 28.0% | $0.0361 | 52/25 |
| holdout | exclude | p99 | 60.0% | $0.0344 | 57.2% | 44.8% – 71.3% | 16.0% | $0.0275 | 52/25 |
| holdout | exclude | p99 | 70.0% | $0.0295 | 66.7% | 52.2% – 83.2% | 24.0% | $0.0324 | 52/25 |
| holdout | exclude | p99 | 80.0% | $0.0258 | 76.2% | 59.7% – 95.0% | 28.0% | $0.0361 | 52/25 |
| holdout | inflate | none | 60.0% | $0.0380 | 56.2% | 42.8% – 70.8% | 11.5% | $0.0267 | 54/26 |
| holdout | inflate | none | 70.0% | $0.0326 | 65.6% | 50.0% – 82.7% | 19.2% | $0.0321 | 54/26 |
| holdout | inflate | none | 80.0% | $0.0285 | 74.9% | 57.1% – 94.5% | 26.9% | $0.0362 | 54/26 |
| holdout | inflate | p99 | 60.0% | $0.0380 | 56.2% | 42.8% – 70.8% | 11.5% | $0.0267 | 54/26 |
| holdout | inflate | p99 | 70.0% | $0.0326 | 65.6% | 50.0% – 82.7% | 19.2% | $0.0321 | 54/26 |
| holdout | inflate | p99 | 80.0% | $0.0285 | 74.9% | 57.1% – 94.5% | 26.9% | $0.0362 | 54/26 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | exclude | none | 60.0% | $0.0322 | 59.7% | 51.6% – 68.4% | 19.3% | $0.0286 | 155/78 |
| holdout | exclude | none | 70.0% | $0.0276 | 69.6% | 60.2% – 79.8% | 25.2% | $0.0328 | 155/78 |
| holdout | exclude | none | 80.0% | $0.0242 | 79.6% | 68.8% – 91.2% | 28.2% | $0.0361 | 155/78 |
| holdout | exclude | p99 | 60.0% | $0.0322 | 59.7% | 51.6% – 68.4% | 19.3% | $0.0286 | 155/78 |
| holdout | exclude | p99 | 70.0% | $0.0276 | 69.6% | 60.2% – 79.8% | 25.2% | $0.0328 | 155/78 |
| holdout | exclude | p99 | 80.0% | $0.0242 | 79.6% | 68.8% – 91.2% | 28.2% | $0.0361 | 155/78 |
| holdout | inflate | none | 60.0% | $0.0353 | 59.0% | 50.4% – 68.1% | 16.9% | $0.0627 | 160/80 |
| holdout | inflate | none | 70.0% | $0.0302 | 68.8% | 58.8% – 79.5% | 21.7% | $0.0673 | 160/80 |
| holdout | inflate | none | 80.0% | $0.0265 | 78.7% | 67.2% – 90.8% | 28.3% | $0.0708 | 160/80 |
| holdout | inflate | p99 | 60.0% | $0.0353 | 59.0% | 50.4% – 68.1% | 16.9% | $0.0627 | 160/80 |
| holdout | inflate | p99 | 70.0% | $0.0302 | 68.8% | 58.8% – 79.5% | 21.7% | $0.0673 | 160/80 |
| holdout | inflate | p99 | 80.0% | $0.0265 | 78.7% | 67.2% – 90.8% | 28.3% | $0.0708 | 160/80 |
| in_sample | exclude | none | 60.0% | $0.0321 | 60.0% | 55.0% – 65.2% | 16.1% | $0.0451 | 233/233 |
| in_sample | exclude | none | 70.0% | $0.0275 | 70.0% | 64.2% – 76.0% | 23.9% | $0.0499 | 233/233 |
| in_sample | exclude | none | 80.0% | $0.0241 | 80.0% | 73.3% – 86.9% | 33.6% | $0.0535 | 233/233 |
| in_sample | exclude | p99 | 60.0% | $0.0321 | 60.0% | 55.0% – 65.2% | 16.1% | $0.0451 | 233/233 |
| in_sample | exclude | p99 | 70.0% | $0.0275 | 70.0% | 64.2% – 76.0% | 23.9% | $0.0499 | 233/233 |
| in_sample | exclude | p99 | 80.0% | $0.0241 | 80.0% | 73.3% – 86.9% | 33.6% | $0.0535 | 233/233 |
| in_sample | inflate | none | 60.0% | $0.0351 | 60.0% | 54.6% – 65.8% | 16.2% | $0.0625 | 240/240 |
| in_sample | inflate | none | 70.0% | $0.0301 | 70.0% | 63.7% – 76.7% | 22.5% | $0.0672 | 240/240 |
| in_sample | inflate | none | 80.0% | $0.0263 | 80.0% | 72.8% – 87.7% | 30.6% | $0.0707 | 240/240 |
| in_sample | inflate | p99 | 60.0% | $0.0351 | 60.0% | 54.6% – 65.8% | 16.2% | $0.0625 | 240/240 |
| in_sample | inflate | p99 | 70.0% | $0.0301 | 70.0% | 63.7% – 76.7% | 22.5% | $0.0672 | 240/240 |
| in_sample | inflate | p99 | 80.0% | $0.0263 | 80.0% | 72.8% – 87.7% | 30.6% | $0.0707 | 240/240 |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-628b49d96dcde97a430dd4f597705899e09a968f793491e4b704cae33a40dc02 · fixed $0.0257 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | $0.0009 |

### code · task-ef4a63ba1ff87e2e913979439e4effe27fb674a3cd5088f12f29a52e774c3aa0 · fixed $0.0257 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | $0.0070 |

### code · task-b55cec66dec0e2383a2e66dbb34fed98ef575c77e35193ad643484a7a6959e56 · fixed $0.0257 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 3 | $0.0159 |

### code · task-fda9f04c2ded017607d60770485b3f2eb5872e0f48340f2c55c5bdfcffe93602 · fixed $0.0257 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 5 | $0.0260 |

### code · task-c44474038d459e40e4714afefa7bf8dae9f9834b22f5e8ec1dd434ecb62b512e · fixed $0.0257 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 2 | $0.0683 |

### review · task-f228962502c7ff37c2965f1d2633c745cef8658ec873eac4ea771275038599a9 · fixed $0.0295 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | $0.0008 |

### review · task-8c23bb247251de35f3d8fce8df28c1863000659bcd97dc66845be73d6abc19de · fixed $0.0295 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 3 | $0.0088 |

### review · task-f6b6d0d62eb661c6d3fd7e35e972a8ed44b4aa2fd6c87b449b82b1b7b1a2319f · fixed $0.0295 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 2 | $0.0179 |

### review · task-1cd09acac02b19bc982d23f6b858b3784a06bf11040ad7e25a280e92eb911dae · fixed $0.0295 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 4 | $0.0284 |

### review · task-e8816c740eb9b470ce55839b91e1070a22ca77e225278ad0fc2866bd542fa337 · fixed $0.0295 (holdout) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 5 | $0.0789 |

## Limits

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Drift ratios and recency prices describe the observed period. A recent window is smaller than the full period, so its prices and intervals are noisier; the current last-window price is in-sample. Rate-change projections hold usage fixed and change only rates.

Seed: 0. Bootstrap draws: 2,000. Report generated: <time>. No network requests are required to view this file.

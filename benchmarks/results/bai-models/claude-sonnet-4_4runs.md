# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

1999 tasks. Price catalog 2026-10-23.1-bai-routes.1 · SHA-256 50395bc63c7d0dcd458b5e074bbc5b2883fbe4985bba4ee58f1fec65493f9069.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ. Bai analysis adds exact observed provider/proxy route aliases; dollar rates are unchanged. Qwen hosted and Kimi OpenRouter tariffs remain unknown.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Bai SWE-bench Verified: claude-sonnet-4_4runs.tar.gz. Benchmark tasks, not production.

Task groups: 1999 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 1999 records. Fields read: action, args, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Import limitations: inconsistent_usage_unpriced: 139097

Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded.

## Summary verdicts

REPRICING CHECK FAILED. Verdicts below describe standard-rate token costs, not validated recorded billing. Review the reconciliation discrepancy in Cost audit before using these prices.

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2025-06-03T04:21:51.376433+00:00; 20 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $0.4463. Overall distribution weights each of 0 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 500 iterations for 1999 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 1999 | 0 | 1999 | NOT VIABLE | 1999 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable grouped_cv or positive fitted price |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| code | 1999 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 1999 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

### code · grouped CV vs time split

| Censoring | Cap | Target | Grouped CV loss ratio | Held-out fold 90% CI (verdict) | Pooled 90% CI | Tasks losing | Worst loss | Leave-one-run-out loss ratio | Leave-one-run-out held-out 90% CI | Time split (leaks repeated tasks) loss ratio | Time split 90% CI | Difference: time split − grouped CV | Difference: upper CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 0 | — | — | — | — | — | — | — | — |
| Overall · equal type weight | 0 | — | — | — | — | — | — | — | — |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| code | 1999 | 0 | 0.0% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 31.1%; their spend per task $0.0001; tasks with loop signals 37.7%. Raw dollar totals below are accounting totals.

Repricing acceptance: FAIL. 41 of 139138 recorded-cost calls within 1% (0.0%); 41 comparable calls (100.0% agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.4463; standard-rate reprice $0.4463; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1373 | 1994/1999 | 68.9% | 0/0 | — |

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
| code | $0.4463 | $0.1988 | $0.0000 | 754 | 165.00 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-8ae7e28dafd5a79103afa737a5af0b2c73941bfc0e02dcf7b4776133e602b7d8 | $0.0391 | lower bound | success | False |
| task-12a31d33d062c6cde7a212488f19006c6fa7ae1c2244b9982fa64882928e3c8d | $0.0295 | lower bound | fail | False |
| task-5a434c44fe8c5fffb27d84a5f49ebab607fb75a169013089eeeea9ad203aa961 | $0.0257 | lower bound | fail | False |
| task-38ebcb03a2293a01e56aa26b97e9eabd613e99253c465adac979015d6f83d41b | $0.0217 | lower bound | success | False |
| task-e8374c67f87b06d903c2c7802a62fcd6ea24c609e4f8eb55782e80c40cc3e59a | $0.0194 | lower bound | fail | False |
| task-cb5bc6bc2c41ec01f65e2f9781c7147e23da9df3ab3ddde6686eba322d7ef161 | $0.0192 | lower bound | success | False |
| task-8576efa9c9cf77d15739b907803f208e164ad530065aeb8d54e60f5c17723e24 | $0.0189 | lower bound | success | False |
| task-a6bcaf22eb0e2ea250c9e5ec74ce2a0d4f97f0fadc8f5eae016bef53ffc91f44 | $0.0170 | lower bound | success | False |
| task-eae1785b56ddc4f04d6894ac301b450ff63ae9b43f94eed97c7ea5367bd124ab | $0.0162 | lower bound | fail | False |
| task-f62f15c423236bc2f3f9317c1d9589e829178f51c987035dac82442c87807383 | $0.0142 | lower bound | fail | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-a6b4b3af1b6f897b9ff06442f1b623d7b60ebace13efaa5b4a5d557ce544485e | run × 3 | 58 | False | $0.0000 |
| task-bbe5b48601cb7442906a29c8e9d99455d23efe2f2c53d23106b1546f432032a2 | run × 3; run × 6 | 106 | False | $0.0000 |
| task-89bdcbf193736532c76b7edfddd3197c7f3aa358b7e3a3b80590dab079fbff26 | run × 3 | 118 | False | $0.0000 |
| task-86901cb8797041279380170db7b8abbaa2f1d4fa05ddbff44967306e85a069ae | run × 3 | 57 | False | $0.0000 |
| task-51936fe061d99b54d433d830504cea16d6699c606b834f194add8901d5eed2d5 | run × 3 | 50 | False | $0.0000 |
| task-3b13744945dd7297931fc37f71d4dd03e0d31f22edcaf43953c3e978db52ce52 | run × 3; run × 3 | 56 | False | $0.0000 |
| task-89a267795c26d0519f7baf49bc3e5f8f2ebcc0b867c27450077d56c6be35642d | run × 3 | 58 | False | $0.0000 |
| task-f6f69433b52fa2414050d1152e7a4b650978f7813cdd68e8226db8071145a800 | run × 4 | 56 | False | $0.0000 |
| task-d9c6096271422ad40df0bfdbd239fdac76ec97a2f2bb7b214f21c8548ab7aa95 | run × 3 | 48 | False | $0.0000 |
| task-25f804c0c78b266179f87f08f4c6b19bb8187dc6d00914b58b04a7c9408ec388 | run × 3; run × 6 | 146 | False | $0.0000 |
| task-bf0d2bedec3e3fd15f90adda0901f6fada0df891ec5cdbd544f6b897df6ba39f | run × 3 | 91 | False | $0.0000 |
| task-cc2e1bf25c5da25d6768d10ecaa0d9ac55191da53ed0166ead24d96c87010443 | run × 5; run × 3; run × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4; condensation × 4 | 111 | False | $0.0000 |
| task-41ebec0e8227136afb2346d5c7de944a06d80106e04e249e6f2431869b227db4 | run × 3; run × 6 | 132 | False | $0.0000 |
| task-6e13bc1a6c50b48766168dd930e9053ec6837c815a37475b19e9be4b53ceb804 | run × 4 | 52 | False | $0.0000 |
| task-a94099571757b277cc709fb346b8f542bb957836bc34c4a6c0dfe871aeed40d2 | run × 5 | 70 | False | $0.0000 |
| task-a7a4397bcca04a93f12c0b9346d51a74b88f83c80b1ddb33cee68ad5439ac086 | run × 3 | 91 | False | $0.0000 |
| task-86a8ec0867b88dbc7ee1b97ea16a673bf083534af730e3beaea9bfcf0728b31c | run × 3 | 80 | False | $0.0000 |
| task-0f86e6e94c2aac0422d0ab8932c17c32f73c08f946b4adb6c5c6033ee249bd60 | run × 3 | 92 | False | $0.0000 |
| task-303c7e43fa58a5398f7330a2c60fe22ae05484b976692d939a4dd884a89748d0 | run × 4 | 73 | False | $0.0000 |
| task-7a4dd5c803fafb7c9abaff63d62a1004248bd817bd62263d169d49f85afe2ce2 | run × 3 | 58 | False | $0.0000 |
| task-8acbb60a75274cf8256cd0c45fedbf307017921cb8721e306d6fb87f3de8d947 | run × 3 | 46 | False | $0.0000 |
| task-3521c8aea4128d9434c0645acec32d7e5626ea7f54453bf5d0dff6866637e96d | run × 11; run × 4 | 136 | False | $0.0000 |
| task-36043dfd24bb0d42154d0e6612a4ede284d8d2ff5b94bfdfb5096c697c19e8e4 | run × 13; run × 6; run × 7 | 171 | False | $0.0000 |
| task-4e418e3a2c7d8857a5fea3f6fcced06e8611226d9ef0301262f9fc55d11c08f3 | run × 4 | 85 | False | $0.0000 |
| task-6f26a8cc64e3030ea0307ee0cd4fb566fd046d386684ef6df01b930beba09c53 | run × 5 | 91 | False | $0.0000 |
| task-a6f4952f9b6af8b9989ada7b9a05d06a0ed960031af6f6be2f8032f0b5bd3d70 | run × 3 | 75 | False | $0.0000 |
| task-b65aa5e6d9e8d7854a8a3d3053f58b97929bcdd13f0c392797bffd1cd8a91152 | run × 6 | 136 | False | $0.0000 |
| task-41ccf9e027132c1b84057c8e215e422fc429c32011911346fd15cc5dd0dc4123 | run × 3 | 67 | False | $0.0000 |
| task-e55b4d9f34507adf545277d8ddaab5ec14947fd84b083df4b4f15d83bad6ae46 | run × 3 | 48 | False | $0.0000 |
| task-73682958dc6c738979e007d366e8b6ab4681d7d2e47154899b8aca44a2d0884f | run × 3; run × 8; run × 4 | 256 | False | $0.0000 |
| task-98bd73519f46365c54961601085854b66557dcfe0d505d61ed4116efdc0c78eb | run × 4 | 100 | False | $0.0000 |
| task-71e309e0d4a785241f8c8167fc0f83728bac369a1bf9f63befb9d7e2295566dd | run × 3 | 60 | False | $0.0000 |
| task-a959ea5094215e9c6315b1090fe06dfed5eb4845118cfdfa9cb4acd2c145cee7 | run × 3; run × 3 | 95 | False | $0.0000 |
| task-e8ae0f0e698999996c8f3a7cd5336e3428166307825b3db540202412b4aaa1c1 | run × 4; run × 5 | 109 | False | $0.0000 |
| task-46ec5cc821408ed1527f0c51801ed7cca95cfb2c21c643fe13f473a7010d8851 | run × 7; run × 3 | 109 | False | $0.0000 |
| task-8c7ad098323779b83f961704c1da4e00dd277323467280a0c60339c5e0ba001b | run × 5 | 60 | False | $0.0000 |
| task-0e4b271fa40def8175e3ae5ee22c5c8987c90ba426aca9f7a71bbb30da3d8222 | run × 3; run × 3 | 70 | False | $0.0078 |
| task-a0feb6bea7497f14e233f27290beb63ee9fb7037e6284a7205965bf6bf6ec3d3 | run × 5 | 66 | False | $0.0000 |
| task-2ad965381e411608b2c6fc87412f7907370e9325003a084724e9783c3ee3fe6d | run × 3 | 72 | False | $0.0000 |
| task-9d73bcddd1b3c9037251ec70ace7a899f803a538984d2a025c2ca2f027022cdd | run × 4; run × 3; run × 4; run × 8 | 142 | False | $0.0000 |
| task-df47544be9adbb46ac80f8084fee0c13b47f08b7c818065dd88c50c5ab9e8fe3 | run × 3 | 106 | False | $0.0000 |
| task-8e24e1ec64d1720076a4625ee417508a5d609dc67900c66dba1301776063fd67 | run × 3 | 63 | False | $0.0000 |
| task-74dfbd25cc23db3efaeb63cc13809febc522e38285ad937f6a9d4888e9e987ef | run × 4; run × 3; run × 4 | 98 | False | $0.0000 |
| task-7a45c1b9c1ca04558d70228f597dff9c9ad47cd69e4cd1506ff09bd67ecac159 | run × 3 | 47 | False | $0.0000 |
| task-4bc54022ff8f93b85b4f6fedf836854b2d11095443378520148decebcb78c7db | run × 3 | 39 | False | $0.0000 |
| task-b315f4e654c268ecd04cd75fef1a8e07a493af51ed5d921845ef81229b46004a | run × 3 | 54 | False | $0.0000 |
| task-92635cb8af1c3d80122e1b5f47307ac793ede8c725fb7fdda516e5413bbdc168 | run × 7 | 119 | False | $0.0000 |
| task-b6af2f0cff5ed2c224f6ce1ae030bf0793455faca26c2aeb884002ad2cc0cccf | run × 4 | 72 | False | $0.0000 |
| task-bd91e7c1a2cc6ebf40195d666a32a7c6245725fcc40f9f566a363058101f234c | run × 3 | 59 | False | $0.0000 |
| task-462a6bdfc507caa881bf68757ed63c04db71affde6b5e47ef8b269ddc83ea8bc | run × 3 | 113 | False | $0.0000 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |

No available observations for this table.

## Fixed-price simulation with confidence intervals

Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.

In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.

Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type&#x27;s mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the &lt;90% upper-CI decision is flagged in the verdict.

Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.

Grouped CV and leave-one-run-out rows pool out-of-fold costs and revenues into the loss ratio, tasks-losing share and worst loss. Each fold fits its own price, p99 cap and censoring tail using training data only. Displayed price is the mean fitted fold price, not a single price used for every held-out task. Their 90% CI is the held-out fold loss ratio across 1,000 group-bootstrap draws that refit every price. Leave-one-run-out fits on the other runs and scores one run: same tasks, new run, so it shares groups across training and scoring by design. Charts and sample receipts use descriptive in-sample prices; time-split rows do not drive grouped verdicts.

### code

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### code · fold fits at 70% target with cap

| Scope | Billing | Censoring | Fold | Train/test groups | Price | Cap | Score loss ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-a6b4b3af1b6f897b9ff06442f1b623d7b60ebace13efaa5b4a5d557ce544485e · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 3 | ≥ $0.0000 |
| read | 9 | ≥ $0.0000 |
| run | 28 | ≥ $0.0000 |
| edit | 17 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-e295ce3cc0754e83b8bd6bab57ad40e7fd2a9cbba63306bfc3b77e6bd0adcf4f · fixed — (unavailable) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 3 | ≥ $0.0000 |
| read | 37 | ≥ $0.0000 |
| run | 96 | ≥ $0.0000 |
| edit | 36 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-9e34e00a17e9661ff1c3d3fa9ed1bcbc4c00f629f4126fcf9d9bc178a86507e8 · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 3 | ≥ $0.0000 |
| read | 5 | ≥ $0.0000 |
| run | 26 | ≥ $0.0000 |
| edit | 7 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-85f50341290ba3856338f43b6e087018924537c804615c691919ea199eea03b5 · fixed — (unavailable) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 3 | ≥ $0.0000 |
| read | 13 | ≥ $0.0000 |
| run | 32 | ≥ $0.0000 |
| edit | 10 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-8ae7e28dafd5a79103afa737a5af0b2c73941bfc0e02dcf7b4776133e602b7d8 · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 2 | ≥ $0.0065 |
| read | 17 | ≥ $0.0000 |
| run | 42 | ≥ $0.0000 |
| edit | 13 | ≥ $0.0326 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

## Limits

Resolution is joined within each run by instance_id using SWE-bench report.json results. Empty patches are unresolved; missing/error-only results remain unknown. Instance IDs are retained only as the hashed task_group; run IDs only as hashes for leave-one-run-out.

Five grouped folds keep all repeats of an instance together. Leave-one-run-out can still share instances with its training runs. Group-bootstrap draws refit every fold price; model-selection uncertainty is not captured.

Costs use the supplied token classes and provider-correct exclusive pricing. Unresolvable token conventions and unsupported route tariffs remain unpriced. Cost per success includes failed attempts and is a lower bound where harness-censored costs remain. See BAI_ACCOUNTING.md for source accounting differences.

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by moira. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one moira install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:38:11.561110+00:00. No network requests are required to view this file.

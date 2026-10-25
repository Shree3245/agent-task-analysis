# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

2000 tasks. Price catalog 2026-10-23.1-bai-routes.1 · SHA-256 50395bc63c7d0dcd458b5e074bbc5b2883fbe4985bba4ee58f1fec65493f9069.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ. Bai analysis adds exact observed provider/proxy route aliases; dollar rates are unchanged. Qwen hosted and Kimi OpenRouter tariffs remain unknown.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Bai SWE-bench Verified: gpt_5.2_4runs.tar.gz. Benchmark tasks, not production.

Task groups: 2000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 2000 records. Fields read: action, args, error, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Import limitations: aggregate_usage_without_calls: 25

Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded.

## Summary verdicts

REPRICING CHECK FAILED. Verdicts below describe standard-rate token costs, not validated recorded billing. Review the reconciliation discrepancy in Cost audit before using these prices.

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2026-01-24T22:30:49.165665+00:00; 25 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $1,511.3111. Overall distribution weights each of 1 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 500 iterations for 1975 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 2000 | 0 | 28 | VIABLE | grouped_cv: upper loss-ratio interval stays below 90% at the 70% target with p99 cap; also with 28 unpriced tasks (1.4%) at the training p99 cost |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| code | 28 | 1.4% | VIABLE | VIABLE | 81.3% → 85.1% | 81.3% → 85.1% |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 2000 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

### code · grouped CV vs time split

| Censoring | Cap | Target | Grouped CV loss ratio | Held-out fold 90% CI (verdict) | Pooled 90% CI | Tasks losing | Worst loss | Leave-one-run-out loss ratio | Leave-one-run-out held-out 90% CI | Time split (leaks repeated tasks) loss ratio | Time split 90% CI | Difference: time split − grouped CV | Difference: upper CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exclude | none | 60.0% | 60.0% | 50.6% – 70.8% | 59.9% – 60.1% | 12.6% | $5.4831 | 60.0% | 55.4% – 68.1% | 57.7% | 54.6% – 60.7% | -2.3% | -10.0% |
| exclude | none | 70.0% | 70.0% | 59.0% – 82.6% | 69.9% – 70.1% | 17.8% | $5.6628 | 70.0% | 64.6% – 79.4% | 67.3% | 63.7% – 70.9% | -2.7% | -11.7% |
| exclude | none | 80.0% | 80.0% | 67.4% – 94.4% | 79.9% – 80.1% | 23.8% | $5.7976 | 80.0% | 73.9% – 90.8% | 76.9% | 72.8% – 81.0% | -3.1% | -13.4% |
| exclude | p99 | 60.0% | 60.0% | 51.0% – 69.7% | 59.7% – 60.0% | 13.1% | $2.1925 | 59.9% | 56.1% – 65.6% | 58.7% | 55.6% – 61.8% | -1.3% | -7.9% |
| exclude | p99 | 70.0% | 70.0% | 59.5% – 81.3% | 69.6% – 70.0% | 18.5% | $2.3702 | 69.9% | 65.4% – 76.6% | 68.5% | 64.9% – 72.1% | -1.5% | -9.2% |
| exclude | p99 | 80.0% | 80.0% | 68.0% – 92.9% | 79.5% – 80.0% | 24.6% | $2.5036 | 79.9% | 74.7% – 87.5% | 78.3% | 74.1% – 82.4% | -1.7% | -10.5% |
| inflate | none | 60.0% | 60.0% | 50.6% – 70.8% | 59.9% – 60.1% | 12.6% | $5.4831 | 60.0% | 55.4% – 68.1% | 57.7% | 54.6% – 60.7% | -2.3% | -10.0% |
| inflate | none | 70.0% | 70.0% | 59.0% – 82.6% | 69.9% – 70.1% | 17.8% | $5.6628 | 70.0% | 64.6% – 79.4% | 67.3% | 63.7% – 70.9% | -2.7% | -11.7% |
| inflate | none | 80.0% | 80.0% | 67.4% – 94.4% | 79.9% – 80.1% | 23.8% | $5.7976 | 80.0% | 73.9% – 90.8% | 76.9% | 72.8% – 81.0% | -3.1% | -13.4% |
| inflate | p99 | 60.0% | 60.0% | 51.0% – 69.7% | 59.7% – 60.0% | 13.1% | $2.1925 | 59.9% | 56.1% – 65.6% | 58.7% | 55.6% – 61.8% | -1.3% | -7.9% |
| inflate | p99 | 70.0% | 70.0% | 59.5% – 81.3% | 69.6% – 70.0% | 18.5% | $2.3702 | 69.9% | 65.4% – 76.6% | 68.5% | 64.9% – 72.1% | -1.5% | -9.2% |
| inflate | p99 | 80.0% | 80.0% | 68.0% – 92.9% | 79.5% – 80.0% | 24.6% | $2.5036 | 79.9% | 74.7% – 87.5% | 78.3% | 74.1% – 82.4% | -1.7% | -10.5% |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 1972 | $0.7664 | $0.5763 | $1.4279 | $3.2951 | $6.7411 | 2.48 | 6.0% | 18.5% |
| Overall · equal type weight | 1972 | $0.7664 | $0.5762 | $1.4285 | $3.3094 | $6.7411 | 2.48 | 5.9% | 18.4% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| code | 2000 | 0 | 0.0% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 36.7%; their spend per task $0.3382; tasks with loop signals 18.4%. Raw dollar totals below are accounting totals.

Repricing acceptance: FAIL. 844 of 91826 recorded-cost calls within 1% (0.9%); 91826 comparable calls (0.9% agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $5,072.4757; standard-rate reprice $1,511.3111; difference $3,561.1646.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1257 | 1991/2000 | 63.1% | 1972/1257 | $1.2023 |

### Unknown models

| Provider/model | Calls |
| --- | --- |
| unknown/unknown | 25 |

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 3 | $0.0160 | $0.0073 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 5 | $0.0173 | $0.0086 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 7 | $0.0144 | $0.0041 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 9 | $0.0193 | $0.0090 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 11 | $0.0123 | $0.0064 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 14 | $0.0195 | $0.0076 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 16 | $0.0251 | $0.0164 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 20 | $0.0217 | $0.0060 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 22 | $0.0270 | $0.0082 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 24 | $0.0256 | $0.0041 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 26 | $0.0351 | $0.0129 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 28 | $0.0289 | $0.0057 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 30 | $0.0524 | $0.0373 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 32 | $0.0506 | $0.0258 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 34 | $0.0560 | $0.0308 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 36 | $0.0695 | $0.0431 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 38 | $0.0585 | $0.0289 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 40 | $0.0405 | $0.0125 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 42 | $0.0504 | $0.0207 |
| task-caeeae94cb4cbfa4dcea3a13f186b3361403097b263f4997038f40bbb3a74303 | 44 | $0.0433 | $0.0121 |

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| code | $1,511.3111 | $676.3758 | $0.0000 | 369 | 129.05 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-51bf8a6772c54d63621a5b7e6aca7b26b25211ede0029b194fea4b2c79ff6200 | $6.7411 | complete | fail | False |
| task-cd2c0e3248eb65e7b89dee53beaa4b85060bcffcc4dac096b4b3c9adb4bba4be | $6.5807 | complete | fail | False |
| task-6a304e144fa1a44cabc226ce5dcfcf8d416f761f1dbedd13f3eebdd20078fbcb | $6.1451 | complete | fail | False |
| task-ac5866d490cd5ecb13d43f9f217403e7128a778fb89c2400cc04e7d20f8f4e41 | $5.9182 | complete | fail | False |
| task-09c0055973a784b4daf0951b05a477488d8f71ed7e29ac32c55781018f3c7821 | $5.6147 | complete | success | False |
| task-aaaefb6280339fd4563c13ee12d612be0040bdce3683f14588c86b54eb158e4b | $4.8198 | complete | success | False |
| task-41dfd668e540967c5ced940111b50b169d11930bee2e4aadb621e26ed75bd1fb | $4.6991 | complete | fail | False |
| task-f40642806d3071ff18e5a7272514e23062278ac9d825cd2524080b33a6fcccc3 | $4.3808 | complete | success | False |
| task-9863477589a4076450a94a83efc80341934ba8b6b8914c72147abe5e2ede2962 | $4.3735 | complete | fail | False |
| task-9f363f77e42d61fa2f7fe89c8b88492cb6fb260baaef3720cdd5795c0309911a | $4.3572 | complete | unknown | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-a57437886d36d2df2144095b03e493e6b4f8b2a975df5467140e0e9725b706a5 | run × 4 | 60 | False | $0.7275 |
| task-3544cbd55cc24915e59a1a8b90cb7d4330552e266173e0e675d300dda2ca4739 | run × 3 | 38 | False | $0.5201 |
| task-53d75bad56c18ed35cbea742415af5b7930a2373f39b317b325a506113e9fb86 | run × 4 | 62 | False | $0.6943 |
| task-9eebb1a6b6d15a843bb87e7967c87622ed3e3e53d4253c535152d486a293d9c0 | run × 3 | 34 | False | $0.3845 |
| task-abd795d57be684a1dbac51d6dca04ffbf25c31dd909148b3ee6b27dce6737870 | run × 3 | 30 | False | $0.4457 |
| task-8978fa5a7b349eaea47b8b964a111fa456a19464a7bc3a755ad1ec9c06894509 | run × 4 | 46 | False | $0.7801 |
| task-b3821ba975535020a4053c7275849b51431a73cece433a4b3388b14b3f25f1a3 | run × 4 | 74 | False | $1.2990 |
| task-14543580a30bf9af963b074eda0b6f04756fd729f6c7af984731eef698205f7b | run × 5 | 49 | False | $0.5307 |
| task-be0b04a62dd36ff8ef79d0315fbb639e0f3d9d6a69ea6692550fc52eeaa88023 | run × 3 | 36 | False | $0.4705 |
| task-df175d73c83520180a474eca0f1a7c5ba6efb6cdb890e88b1717abf4a6dcc40d | run × 3 | 54 | False | $0.7275 |
| task-917acaad18647956a3620c84ed6421b5a2defed0188f1f585bbe3a3e8a8b8bae | run × 3; run × 3 | 70 | False | $1.2050 |
| task-c48876af3097e34171459e6b9e73cd374de6b590d1375715b5c3a7b0b2cdf041 | run × 4 | 56 | False | $0.9967 |
| task-775ef60b9364fd6790c25224b2cc189291769186086c6f5a256458b3056f044b | run × 4 | 63 | False | $0.7528 |
| task-53c9fb0475cb06a6da8f36fc4265140ef385deb27ce6e35bff9a51a59c959696 | run × 6 | 53 | False | $0.7567 |
| task-72e70cad39d67af33f6ac88335b0417593e0720d880a8669333203fc62598a31 | run × 3 | 40 | False | $0.4217 |
| task-0c52dc1a0a7d6eee3e895367829a1e5546d1447532e8a15e990cbd627fbda722 | run × 3 | 66 | False | $0.9525 |
| task-2b18b91c4d7b52dc2e09d49aab71f3e7d98c7e73d09916feb6ace4a6e2c72ff5 | run × 4 | 28 | False | $0.3834 |
| task-f714ad3d3f0f13d5a55926e41ef058f0b7665438924822cb9dce7453a3ce9e21 | run × 3 | 55 | False | $0.9421 |
| task-10caaf800b889df4ca7822be0ec5a58e7245b8baf6b21d723570bbbb0557343b | run × 3 | 73 | False | $0.9150 |
| task-39d19f944b9af2c85d830ae25a8c7acdf8cac9e2ce060bc0eeafc63d9d0bd05d | run × 5 | 148 | False | $4.0522 |
| task-51bf8a6772c54d63621a5b7e6aca7b26b25211ede0029b194fea4b2c79ff6200 | edit × 4; edit × 5; edit × 6; edit × 4; edit × 10; run × 3; edit × 9; edit × 4; run × 7; run × 3 | 176 | False | $6.7411 |
| task-6a304e144fa1a44cabc226ce5dcfcf8d416f761f1dbedd13f3eebdd20078fbcb | run × 3; run × 5; run × 3; run × 3 | 162 | False | $6.1451 |
| task-abe968d286515ad71c38a986c5b7d12025e0eb5d2ad8c691801f43b6b0399434 | run × 3 | 32 | False | $0.3670 |
| task-e243647ceb61929a27b49bf50bb608d9bcdf77584e31a10e3d8cad3ef98e94b8 | run × 3 | 34 | False | $0.3939 |
| task-c302bafa3ae731fc9210d18b1af5b4fa4f08cfb52e3b2d8dfe00327991550838 | run × 4 | 46 | False | $0.5560 |
| task-cab184eeefdb7c71ea4af5913f516f0b3ba0899a6b9a45e4176b244f484ac9e1 | run × 3 | 53 | False | $0.7396 |
| task-0eeba4c56301d599df966745a251b1c2050f640057d907d9775040a3afd278a2 | run × 3 | 86 | False | $1.6069 |
| task-f8bd3c1ce0367f2c6b9e4b7a57fd7bfe3e6296d5235fe6b04663e46c92efd8dd | run × 3 | 47 | False | $0.5787 |
| task-bf5fb387f60e71476208dee9ba232a22adeae7348753240500cb7b0beb7b9f05 | run × 6 | 67 | False | $1.3077 |
| task-ae5e4a6fd26c345b015597da252f79b5d78faec2e1eca7b3d5e55eae420a2340 | run × 4 | 50 | False | $0.9985 |
| task-6d33b3ac79b00f7004d8739fe4cf5d705cc688ea0f5d4752438ee839e777b5b0 | run × 4 | 27 | False | $0.1889 |
| task-d6375b4ed73a82317ed68948bc1aa22e7c2ab511bd940a9fdf74e9a5071104a3 | run × 3; run × 3 | 107 | False | $2.5865 |
| task-6baa5163fa4968fba4471c9588f893fdec475cdb02779411e4a6e8b7d4da6338 | run × 4 | 77 | False | $1.5523 |
| task-a271761a1b7d786e055258ba8eab6275c9ed496020ecfc29827f53f1742f5fe2 | run × 3 | 55 | False | $0.8237 |
| task-05498ba690ef2b1ff822207d8798f073469aaed5961cb133b35f62f4e4a358cc | run × 3; run × 3 | 93 | False | $1.4426 |
| task-a0d4bc1cb5ce665209e22a2fbf2c8f1b2a5b6889781b650d2a592d8d692d66a8 | run × 5 | 46 | False | $0.4827 |
| task-9bf4920eda3f7a52dadf45d73fa35bcbf289704bf165b70ea93ff22ae532a398 | run × 4; run × 7 | 51 | False | $0.5227 |
| task-35bafc498dc417183f101dae596a66b4df08c534f7620b337097f7bd923a2b2b | run × 3 | 50 | False | $0.7579 |
| task-13739b633652a26835180bd884be5a4701732be4628182ec54168623af789611 | run × 3 | 76 | False | $2.1304 |
| task-3dd2e6ff6b23cfd49abaec0020239b23467bdda07344a84f51d5c6eae36bfcee | run × 3 | 35 | False | $0.4628 |
| task-86962a7b13e461f8f3c088dd7c678e055d5b8707d58485cd8d77cf1c07c6364b | run × 3 | 53 | False | $0.8284 |
| task-153a3d65c60fa0d4baa2d882eae64aae8c614ea8eea8e4a97f356bed8936dca7 | run × 6 | 52 | False | $0.8193 |
| task-86db77d4c473511dee60984ebf1f56c257a9dd629811448cfd6c4fd2a6b35ae6 | run × 3 | 34 | False | $0.5278 |
| task-c36e58209f5204ebe2b09c676a28c46dd4309897de61bbfeb9240a5ac936726f | run × 4 | 56 | False | $0.7684 |
| task-226767fbe90ead25bf9235db003cf6894aad2a97abd0e46ba8dc34e0f75c0192 | run × 3; run × 3 | 40 | False | $0.4759 |
| task-2d42656138b3b5e92c4f15dfcc4bc246529f2ba8d93024f448eb69c8a06ae9a0 | run × 4 | 77 | False | $1.2293 |
| task-46600d6b5b034e582b288105331df8f6abf232d746bbe24da9bcac29eaaeb8dd | run × 4; run × 5; run × 11; run × 3 | 167 | False | $4.0231 |
| task-d2dab4b8316813b527c2382fbccf46add428478ff1d4156be1d7c21b850125c8 | run × 3 | 51 | False | $0.7163 |
| task-935002306b8493360ae8190647f5882ffcb608e9d455b0b3f4793cd9d8a2b1a0 | run × 3 | 32 | False | $0.6595 |
| task-1a721da251eb43f1255827b8041f5d948b0701295a3924a9c51739e4da165a83 | run × 3 | 69 | False | $1.3177 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | p95 | $1.8753 | 4.8% | $89.9028 | 5.9% | 5.0% | $93.7925 |
| code | p99 | $3.2951 | 1.0% | $24.0333 | 1.6% | 1.0% | $24.6089 |
| code | p99.5 | $4.2494 | 0.5% | $10.6390 | 0.7% | 0.5% | $11.1360 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 1 | 4.8% | $0.0456 | 5.9% |
| p99 | 1 | 1.0% | $0.0122 | 1.6% |
| p99.5 | 1 | 0.5% | $0.0054 | 0.7% |

## Fixed-price simulation with confidence intervals

Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.

In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.

Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type&#x27;s mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the &lt;90% upper-CI decision is flagged in the verdict.

Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.

Grouped CV and leave-one-run-out rows pool out-of-fold costs and revenues into the loss ratio, tasks-losing share and worst loss. Each fold fits its own price, p99 cap and censoring tail using training data only. Displayed price is the mean fitted fold price, not a single price used for every held-out task. Their 90% CI is the held-out fold loss ratio across 1,000 group-bootstrap draws that refit every price. Leave-one-run-out fits on the other runs and scores one run: same tasks, new run, so it shares groups across training and scoring by design. Charts and sample receipts use descriptive in-sample prices; time-split rows do not drive grouped verdicts.

Success-only billing: price = all training costs / (target loss ratio × billable training successes). Failed attempts still incur costs but generate no revenue. A replay cap that stops a previously successful task makes it unbillable; earlier completion outcomes are not invented. This scenario uses fully priced tasks with known outcomes only; excluded outcomes and cost coverage are shown above. Its fold assignments are unchanged. Censored completion costs remain a sensitivity assumption.

### code

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $1.2773 | 60.0% | 58.2% – 62.0% | 12.5% | $5.4638 | 1972/1972 |
| in_sample | exclude | none | 70.0% | $1.0948 | 70.0% | 67.9% – 72.3% | 17.7% | $5.6463 | 1972/1972 |
| in_sample | exclude | none | 80.0% | $0.9580 | 80.0% | 77.5% – 82.6% | 23.4% | $5.7831 | 1972/1972 |
| in_sample | exclude | p99 | 60.0% | $1.2570 | 60.0% | 58.4% – 61.8% | 13.1% | $2.1797 | 1972/1972 |
| in_sample | exclude | p99 | 70.0% | $1.0774 | 70.0% | 68.1% – 72.0% | 18.5% | $2.3593 | 1972/1972 |
| in_sample | exclude | p99 | 80.0% | $0.9427 | 80.0% | 77.8% – 82.3% | 24.3% | $2.4940 | 1972/1972 |
| in_sample | inflate | none | 60.0% | $1.2773 | 60.0% | 58.2% – 62.0% | 12.5% | $5.4638 | 1972/1972 |
| in_sample | inflate | none | 70.0% | $1.0948 | 70.0% | 67.9% – 72.3% | 17.7% | $5.6463 | 1972/1972 |
| in_sample | inflate | none | 80.0% | $0.9580 | 80.0% | 77.5% – 82.6% | 23.4% | $5.7831 | 1972/1972 |
| in_sample | inflate | p99 | 60.0% | $1.2570 | 60.0% | 58.4% – 61.8% | 13.1% | $2.1797 | 1972/1972 |
| in_sample | inflate | p99 | 70.0% | $1.0774 | 70.0% | 68.1% – 72.0% | 18.5% | $2.3593 | 1972/1972 |
| in_sample | inflate | p99 | 80.0% | $0.9427 | 80.0% | 77.8% – 82.3% | 24.3% | $2.4940 | 1972/1972 |
| holdout | exclude | none | 60.0% | $1.2891 | 57.7% | 54.6% – 60.7% | 11.0% | $2.5664 | 1501/471 |
| holdout | exclude | none | 70.0% | $1.1049 | 67.3% | 63.7% – 70.9% | 15.9% | $2.7506 | 1501/471 |
| holdout | exclude | none | 80.0% | $0.9668 | 76.9% | 72.8% – 81.0% | 21.9% | $2.8887 | 1501/471 |
| holdout | exclude | p99 | 60.0% | $1.2651 | 58.7% | 55.6% – 61.8% | 11.7% | $2.2959 | 1501/471 |
| holdout | exclude | p99 | 70.0% | $1.0844 | 68.5% | 64.9% – 72.1% | 16.8% | $2.4767 | 1501/471 |
| holdout | exclude | p99 | 80.0% | $0.9488 | 78.3% | 74.1% – 82.4% | 22.9% | $2.6122 | 1501/471 |
| holdout | inflate | none | 60.0% | $1.2891 | 57.7% | 54.6% – 60.7% | 11.0% | $2.5664 | 1501/471 |
| holdout | inflate | none | 70.0% | $1.1049 | 67.3% | 63.7% – 70.9% | 15.9% | $2.7506 | 1501/471 |
| holdout | inflate | none | 80.0% | $0.9668 | 76.9% | 72.8% – 81.0% | 21.9% | $2.8887 | 1501/471 |
| holdout | inflate | p99 | 60.0% | $1.2651 | 58.7% | 55.6% – 61.8% | 11.7% | $2.2959 | 1501/471 |
| holdout | inflate | p99 | 70.0% | $1.0844 | 68.5% | 64.9% – 72.1% | 16.8% | $2.4767 | 1501/471 |
| holdout | inflate | p99 | 80.0% | $0.9488 | 78.3% | 74.1% – 82.4% | 22.9% | $2.6122 | 1501/471 |
| grouped_cv | exclude | none | 60.0% | $1.2773 | 60.0% | 50.6% – 70.8% | 12.6% | $5.4831 | 1574/1972 |
| grouped_cv | exclude | none | 70.0% | $1.0948 | 70.0% | 59.0% – 82.6% | 17.8% | $5.6628 | 1574/1972 |
| grouped_cv | exclude | none | 80.0% | $0.9580 | 80.0% | 67.4% – 94.4% | 23.8% | $5.7976 | 1574/1972 |
| grouped_cv | exclude | p99 | 60.0% | $1.2573 | 60.0% | 51.0% – 69.7% | 13.1% | $2.1925 | 1574/1972 |
| grouped_cv | exclude | p99 | 70.0% | $1.0777 | 70.0% | 59.5% – 81.3% | 18.5% | $2.3702 | 1574/1972 |
| grouped_cv | exclude | p99 | 80.0% | $0.9430 | 80.0% | 68.0% – 92.9% | 24.6% | $2.5036 | 1574/1972 |
| grouped_cv | inflate | none | 60.0% | $1.2773 | 60.0% | 50.6% – 70.8% | 12.6% | $5.4831 | 1574/1972 |
| grouped_cv | inflate | none | 70.0% | $1.0948 | 70.0% | 59.0% – 82.6% | 17.8% | $5.6628 | 1574/1972 |
| grouped_cv | inflate | none | 80.0% | $0.9580 | 80.0% | 67.4% – 94.4% | 23.8% | $5.7976 | 1574/1972 |
| grouped_cv | inflate | p99 | 60.0% | $1.2573 | 60.0% | 51.0% – 69.7% | 13.1% | $2.1925 | 1574/1972 |
| grouped_cv | inflate | p99 | 70.0% | $1.0777 | 70.0% | 59.5% – 81.3% | 18.5% | $2.3702 | 1574/1972 |
| grouped_cv | inflate | p99 | 80.0% | $0.9430 | 80.0% | 68.0% – 92.9% | 24.6% | $2.5036 | 1574/1972 |
| leave_one_run_out | exclude | none | 60.0% | $1.2773 | 60.0% | 55.4% – 68.1% | 12.4% | $5.4961 | 1475/1972 |
| leave_one_run_out | exclude | none | 70.0% | $1.0949 | 70.0% | 64.6% – 79.4% | 18.0% | $5.6740 | 1475/1972 |
| leave_one_run_out | exclude | none | 80.0% | $0.9580 | 80.0% | 73.9% – 90.8% | 23.6% | $5.8073 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.2572 | 59.9% | 56.1% – 65.6% | 13.0% | $2.2916 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.0776 | 69.9% | 65.4% – 76.6% | 18.6% | $2.4729 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.9429 | 79.9% | 74.7% – 87.5% | 24.1% | $2.6089 | 1475/1972 |
| leave_one_run_out | inflate | none | 60.0% | $1.2773 | 60.0% | 55.4% – 68.1% | 12.4% | $5.4961 | 1475/1972 |
| leave_one_run_out | inflate | none | 70.0% | $1.0949 | 70.0% | 64.6% – 79.4% | 18.0% | $5.6740 | 1475/1972 |
| leave_one_run_out | inflate | none | 80.0% | $0.9580 | 80.0% | 73.9% – 90.8% | 23.6% | $5.8073 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.2572 | 59.9% | 56.1% – 65.6% | 13.0% | $2.2916 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.0776 | 69.9% | 65.4% – 76.6% | 18.6% | $2.4729 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.9429 | 79.9% | 74.7% – 87.5% | 24.1% | $2.6089 | 1475/1972 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $1.2773 | 60.0% | 50.6% – 70.8% | 12.6% | $5.4831 | 1574/1972 |
| grouped_cv | exclude | none | 70.0% | $1.0948 | 70.0% | 59.0% – 82.6% | 17.8% | $5.6628 | 1574/1972 |
| grouped_cv | exclude | none | 80.0% | $0.9580 | 80.0% | 67.4% – 94.4% | 23.8% | $5.7976 | 1574/1972 |
| grouped_cv | exclude | p99 | 60.0% | $1.2573 | 60.0% | 51.0% – 69.7% | 13.1% | $2.1925 | 1574/1972 |
| grouped_cv | exclude | p99 | 70.0% | $1.0777 | 70.0% | 59.5% – 81.3% | 18.5% | $2.3702 | 1574/1972 |
| grouped_cv | exclude | p99 | 80.0% | $0.9430 | 80.0% | 68.0% – 92.9% | 24.6% | $2.5036 | 1574/1972 |
| grouped_cv | inflate | none | 60.0% | $1.2773 | 60.0% | 50.6% – 70.8% | 12.6% | $5.4831 | 1574/1972 |
| grouped_cv | inflate | none | 70.0% | $1.0948 | 70.0% | 59.0% – 82.6% | 17.8% | $5.6628 | 1574/1972 |
| grouped_cv | inflate | none | 80.0% | $0.9580 | 80.0% | 67.4% – 94.4% | 23.8% | $5.7976 | 1574/1972 |
| grouped_cv | inflate | p99 | 60.0% | $1.2573 | 60.0% | 51.0% – 69.7% | 13.1% | $2.1925 | 1574/1972 |
| grouped_cv | inflate | p99 | 70.0% | $1.0777 | 70.0% | 59.5% – 81.3% | 18.5% | $2.3702 | 1574/1972 |
| grouped_cv | inflate | p99 | 80.0% | $0.9430 | 80.0% | 68.0% – 92.9% | 24.6% | $2.5036 | 1574/1972 |
| holdout | exclude | none | 60.0% | $1.2891 | 57.7% | 54.6% – 60.7% | 11.0% | $2.5664 | 1501/471 |
| holdout | exclude | none | 70.0% | $1.1049 | 67.3% | 63.7% – 70.9% | 15.9% | $2.7506 | 1501/471 |
| holdout | exclude | none | 80.0% | $0.9668 | 76.9% | 72.8% – 81.0% | 21.9% | $2.8887 | 1501/471 |
| holdout | exclude | p99 | 60.0% | $1.2651 | 58.7% | 55.6% – 61.8% | 11.7% | $2.2959 | 1501/471 |
| holdout | exclude | p99 | 70.0% | $1.0844 | 68.5% | 64.9% – 72.1% | 16.8% | $2.4767 | 1501/471 |
| holdout | exclude | p99 | 80.0% | $0.9488 | 78.3% | 74.1% – 82.4% | 22.9% | $2.6122 | 1501/471 |
| holdout | inflate | none | 60.0% | $1.2891 | 57.7% | 54.6% – 60.7% | 11.0% | $2.5664 | 1501/471 |
| holdout | inflate | none | 70.0% | $1.1049 | 67.3% | 63.7% – 70.9% | 15.9% | $2.7506 | 1501/471 |
| holdout | inflate | none | 80.0% | $0.9668 | 76.9% | 72.8% – 81.0% | 21.9% | $2.8887 | 1501/471 |
| holdout | inflate | p99 | 60.0% | $1.2651 | 58.7% | 55.6% – 61.8% | 11.7% | $2.2959 | 1501/471 |
| holdout | inflate | p99 | 70.0% | $1.0844 | 68.5% | 64.9% – 72.1% | 16.8% | $2.4767 | 1501/471 |
| holdout | inflate | p99 | 80.0% | $0.9488 | 78.3% | 74.1% – 82.4% | 22.9% | $2.6122 | 1501/471 |
| in_sample | exclude | none | 60.0% | $1.2773 | 60.0% | 58.2% – 62.0% | 12.5% | $5.4638 | 1972/1972 |
| in_sample | exclude | none | 70.0% | $1.0948 | 70.0% | 67.9% – 72.3% | 17.7% | $5.6463 | 1972/1972 |
| in_sample | exclude | none | 80.0% | $0.9580 | 80.0% | 77.5% – 82.6% | 23.4% | $5.7831 | 1972/1972 |
| in_sample | exclude | p99 | 60.0% | $1.2570 | 60.0% | 58.4% – 61.8% | 13.1% | $2.1797 | 1972/1972 |
| in_sample | exclude | p99 | 70.0% | $1.0774 | 70.0% | 68.1% – 72.0% | 18.5% | $2.3593 | 1972/1972 |
| in_sample | exclude | p99 | 80.0% | $0.9427 | 80.0% | 77.8% – 82.3% | 24.3% | $2.4940 | 1972/1972 |
| in_sample | inflate | none | 60.0% | $1.2773 | 60.0% | 58.2% – 62.0% | 12.5% | $5.4638 | 1972/1972 |
| in_sample | inflate | none | 70.0% | $1.0948 | 70.0% | 67.9% – 72.3% | 17.7% | $5.6463 | 1972/1972 |
| in_sample | inflate | none | 80.0% | $0.9580 | 80.0% | 77.5% – 82.6% | 23.4% | $5.7831 | 1972/1972 |
| in_sample | inflate | p99 | 60.0% | $1.2570 | 60.0% | 58.4% – 61.8% | 13.1% | $2.1797 | 1972/1972 |
| in_sample | inflate | p99 | 70.0% | $1.0774 | 70.0% | 68.1% – 72.0% | 18.5% | $2.3593 | 1972/1972 |
| in_sample | inflate | p99 | 80.0% | $0.9427 | 80.0% | 77.8% – 82.3% | 24.3% | $2.4940 | 1972/1972 |
| leave_one_run_out | exclude | none | 60.0% | $1.2773 | 60.0% | 55.4% – 68.1% | 12.4% | $5.4961 | 1475/1972 |
| leave_one_run_out | exclude | none | 70.0% | $1.0949 | 70.0% | 64.6% – 79.4% | 18.0% | $5.6740 | 1475/1972 |
| leave_one_run_out | exclude | none | 80.0% | $0.9580 | 80.0% | 73.9% – 90.8% | 23.6% | $5.8073 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.2572 | 59.9% | 56.1% – 65.6% | 13.0% | $2.2916 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.0776 | 69.9% | 65.4% – 76.6% | 18.6% | $2.4729 | 1475/1972 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.9429 | 79.9% | 74.7% – 87.5% | 24.1% | $2.6089 | 1475/1972 |
| leave_one_run_out | inflate | none | 60.0% | $1.2773 | 60.0% | 55.4% – 68.1% | 12.4% | $5.4961 | 1475/1972 |
| leave_one_run_out | inflate | none | 70.0% | $1.0949 | 70.0% | 64.6% – 79.4% | 18.0% | $5.6740 | 1475/1972 |
| leave_one_run_out | inflate | none | 80.0% | $0.9580 | 80.0% | 73.9% – 90.8% | 23.6% | $5.8073 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.2572 | 59.9% | 56.1% – 65.6% | 13.0% | $2.2916 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.0776 | 69.9% | 65.4% – 76.6% | 18.6% | $2.4729 | 1475/1972 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.9429 | 79.9% | 74.7% – 87.5% | 24.1% | $2.6089 | 1475/1972 |

### code · success-only billing

| Scope | Censoring | Cap | Target | Mean fold price / success | Loss ratio | 90% CI | Tasks losing | Worst loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $1.9909 | 59.9% | 45.7% – 80.5% | 37.3% | $6.7411 |
| grouped_cv | exclude | none | 65.0% | $1.8378 | 64.9% | 49.5% – 87.2% | 37.7% | $6.7411 |
| grouped_cv | exclude | none | 70.0% | $1.7065 | 69.9% | 53.3% – 93.9% | 38.1% | $6.7411 |
| grouped_cv | exclude | none | 80.0% | $1.4932 | 79.9% | 60.9% – 107.4% | 39.2% | $6.7411 |
| grouped_cv | exclude | p99 | 60.0% | $1.9698 | 60.0% | 45.9% – 79.6% | 37.3% | $3.4367 |
| grouped_cv | exclude | p99 | 65.0% | $1.8183 | 65.0% | 49.7% – 86.2% | 37.7% | $3.4367 |
| grouped_cv | exclude | p99 | 70.0% | $1.6884 | 70.0% | 53.5% – 92.8% | 38.1% | $3.4367 |
| grouped_cv | exclude | p99 | 80.0% | $1.4773 | 80.0% | 61.1% – 106.1% | 39.3% | $3.4367 |
| grouped_cv | inflate | none | 60.0% | $1.9909 | 59.9% | 45.7% – 80.5% | 37.3% | $6.7411 |
| grouped_cv | inflate | none | 65.0% | $1.8378 | 64.9% | 49.5% – 87.2% | 37.7% | $6.7411 |
| grouped_cv | inflate | none | 70.0% | $1.7065 | 69.9% | 53.3% – 93.9% | 38.1% | $6.7411 |
| grouped_cv | inflate | none | 80.0% | $1.4932 | 79.9% | 60.9% – 107.4% | 39.2% | $6.7411 |
| grouped_cv | inflate | p99 | 60.0% | $1.9698 | 60.0% | 45.9% – 79.6% | 37.3% | $3.4367 |
| grouped_cv | inflate | p99 | 65.0% | $1.8183 | 65.0% | 49.7% – 86.2% | 37.7% | $3.4367 |
| grouped_cv | inflate | p99 | 70.0% | $1.6884 | 70.0% | 53.5% – 92.8% | 38.1% | $3.4367 |
| grouped_cv | inflate | p99 | 80.0% | $1.4773 | 80.0% | 61.1% – 106.1% | 39.3% | $3.4367 |
| leave_one_run_out | exclude | none | 60.0% | $1.9907 | 60.0% | 53.9% – 70.9% | 37.2% | $6.7411 |
| leave_one_run_out | exclude | none | 65.0% | $1.8376 | 65.0% | 58.4% – 76.8% | 37.6% | $6.7411 |
| leave_one_run_out | exclude | none | 70.0% | $1.7063 | 70.0% | 62.8% – 82.7% | 38.1% | $6.7411 |
| leave_one_run_out | exclude | none | 80.0% | $1.4930 | 80.0% | 71.8% – 94.5% | 39.0% | $6.7411 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.9693 | 59.9% | 54.5% – 69.0% | 37.3% | $3.3922 |
| leave_one_run_out | exclude | p99 | 65.0% | $1.8178 | 64.9% | 59.1% – 74.7% | 37.7% | $3.3922 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.6880 | 69.9% | 63.6% – 80.5% | 38.1% | $3.3922 |
| leave_one_run_out | exclude | p99 | 80.0% | $1.4770 | 79.9% | 72.7% – 92.0% | 39.2% | $3.3922 |
| leave_one_run_out | inflate | none | 60.0% | $1.9907 | 60.0% | 53.9% – 70.9% | 37.2% | $6.7411 |
| leave_one_run_out | inflate | none | 65.0% | $1.8376 | 65.0% | 58.4% – 76.8% | 37.6% | $6.7411 |
| leave_one_run_out | inflate | none | 70.0% | $1.7063 | 70.0% | 62.8% – 82.7% | 38.1% | $6.7411 |
| leave_one_run_out | inflate | none | 80.0% | $1.4930 | 80.0% | 71.8% – 94.5% | 39.0% | $6.7411 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.9693 | 59.9% | 54.5% – 69.0% | 37.3% | $3.3922 |
| leave_one_run_out | inflate | p99 | 65.0% | $1.8178 | 64.9% | 59.1% – 74.7% | 37.7% | $3.3922 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.6880 | 69.9% | 63.6% – 80.5% | 38.1% | $3.3922 |
| leave_one_run_out | inflate | p99 | 80.0% | $1.4770 | 79.9% | 72.7% – 92.0% | 39.2% | $3.3922 |

### Success-only billing · highest viable target

| Type | Per-task price at 70% (all tasks billed) | Highest viable success-only target | Price per resolved task at that target | Why none |
| --- | --- | --- | --- | --- |
| code | $1.0777 | 60.0% | $1.9698 | — |

### code · fold fits at 70% target with cap

| Scope | Billing | Censoring | Fold | Train/test groups | Price | Cap | Score loss ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | all_tasks | exclude | 1 | 400/100 | $1.0665 | $3.2836 | 73.6% |
| grouped_cv | all_tasks | exclude | 2 | 400/100 | $1.0776 | $3.2941 | 69.9% |
| grouped_cv | all_tasks | exclude | 3 | 400/100 | $1.0752 | $3.2275 | 70.4% |
| grouped_cv | all_tasks | exclude | 4 | 400/100 | $1.1043 | $3.4183 | 62.0% |
| grouped_cv | all_tasks | exclude | 5 | 400/100 | $1.0649 | $3.3202 | 74.3% |
| grouped_cv | all_tasks | inflate | 1 | 400/100 | $1.0665 | $3.2836 | 73.6% |
| grouped_cv | all_tasks | inflate | 2 | 400/100 | $1.0776 | $3.2941 | 69.9% |
| grouped_cv | all_tasks | inflate | 3 | 400/100 | $1.0752 | $3.2275 | 70.4% |
| grouped_cv | all_tasks | inflate | 4 | 400/100 | $1.1043 | $3.4183 | 62.0% |
| grouped_cv | all_tasks | inflate | 5 | 400/100 | $1.0649 | $3.3202 | 74.3% |
| leave_one_run_out | all_tasks | exclude | 1 | 500/491 | $1.0550 | $3.0796 | 75.0% |
| leave_one_run_out | all_tasks | exclude | 2 | 500/491 | $1.0815 | $3.3193 | 69.1% |
| leave_one_run_out | all_tasks | exclude | 3 | 500/493 | $1.0881 | $3.4037 | 67.7% |
| leave_one_run_out | all_tasks | exclude | 4 | 500/497 | $1.0858 | $3.3281 | 68.0% |
| leave_one_run_out | all_tasks | inflate | 1 | 500/491 | $1.0550 | $3.0796 | 75.0% |
| leave_one_run_out | all_tasks | inflate | 2 | 500/491 | $1.0815 | $3.3193 | 69.1% |
| leave_one_run_out | all_tasks | inflate | 3 | 500/493 | $1.0881 | $3.4037 | 67.7% |
| leave_one_run_out | all_tasks | inflate | 4 | 500/497 | $1.0858 | $3.3281 | 68.0% |
| grouped_cv | success_only | exclude | 1 | 399/100 | $1.6828 | $3.2465 | 71.2% |
| grouped_cv | success_only | exclude | 2 | 400/99 | $1.6668 | $3.2949 | 74.8% |
| grouped_cv | success_only | exclude | 3 | 399/100 | $1.7076 | $3.1682 | 66.0% |
| grouped_cv | success_only | exclude | 4 | 399/100 | $1.7414 | $3.3303 | 59.8% |
| grouped_cv | success_only | exclude | 5 | 399/100 | $1.6434 | $3.2955 | 80.1% |
| grouped_cv | success_only | inflate | 1 | 399/100 | $1.6828 | $3.2465 | 71.2% |
| grouped_cv | success_only | inflate | 2 | 400/99 | $1.6668 | $3.2949 | 74.8% |
| grouped_cv | success_only | inflate | 3 | 399/100 | $1.7076 | $3.1682 | 66.0% |
| grouped_cv | success_only | inflate | 4 | 399/100 | $1.7414 | $3.3303 | 59.8% |
| grouped_cv | success_only | inflate | 5 | 399/100 | $1.6434 | $3.2955 | 80.1% |
| leave_one_run_out | success_only | exclude | 1 | 499/489 | $1.6357 | $3.0417 | 78.4% |
| leave_one_run_out | success_only | exclude | 2 | 498/489 | $1.6995 | $3.3227 | 68.2% |
| leave_one_run_out | success_only | exclude | 3 | 499/491 | $1.7191 | $3.3653 | 65.3% |
| leave_one_run_out | success_only | exclude | 4 | 499/494 | $1.6976 | $3.2957 | 68.4% |
| leave_one_run_out | success_only | inflate | 1 | 499/489 | $1.6357 | $3.0417 | 78.4% |
| leave_one_run_out | success_only | inflate | 2 | 498/489 | $1.6995 | $3.3227 | 68.2% |
| leave_one_run_out | success_only | inflate | 3 | 499/491 | $1.7191 | $3.3653 | 65.3% |
| leave_one_run_out | success_only | inflate | 4 | 499/494 | $1.6976 | $3.2957 | 68.4% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-2c0a5f2144ff96520bba516f9c2a7f55ee324cb8a40de671330dd6b6fb554f66 · fixed $1.0774 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | ≥ $0.0000 |

### code · task-d20643e4d2163613d64fd7364af3626907e2246730cbf863fcb994f3c3922c84 · fixed $1.0774 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 7 | $0.0819 |
| run | 21 | $0.2416 |
| read | 2 | $0.0237 |
| edit | 1 | $0.0083 |
| Model-only calls | 1 | $0.0205 |
| finish | 1 | $0.0169 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

### code · task-48370ba34a0b56cd0fed76b19c7bf810149eb56cc5131797777e0b2584b94458 · fixed $1.0774 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 10 | $0.1524 |
| Model-only calls | 1 | $0.0089 |
| run | 16 | $0.2067 |
| read | 7 | $0.1252 |
| edit | 5 | $0.0628 |
| finish | 1 | $0.0138 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

### code · task-4fcb0cd1071d340b8dab8bfb0573265bbe9d9555adf307bc216d3ab60f1746f7 · fixed $1.0774 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 8 | $0.1530 |
| run | 39 | $0.6500 |
| read | 3 | $0.0209 |
| edit | 3 | $0.0521 |
| Model-only calls | 1 | $0.0250 |
| finish | 1 | $0.0161 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

### code · task-51bf8a6772c54d63621a5b7e6aca7b26b25211ede0029b194fea4b2c79ff6200 · fixed $1.0774 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 8 | $0.3160 |
| run | 86 | $3.7583 |
| read | 12 | $0.2402 |
| edit | 68 | $2.3279 |
| Model-only calls | 1 | $0.0332 |
| finish | 1 | $0.0655 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

## Limits

Resolution is joined within each run by instance_id using SWE-bench report.json results. Empty patches are unresolved; missing/error-only results remain unknown. Instance IDs are retained only as the hashed task_group; run IDs only as hashes for leave-one-run-out.

Five grouped folds keep all repeats of an instance together. Leave-one-run-out can still share instances with its training runs. Group-bootstrap draws refit every fold price; model-selection uncertainty is not captured.

Costs use the supplied token classes and provider-correct exclusive pricing. Unresolvable token conventions and unsupported route tariffs remain unpriced. Cost per success includes failed attempts and is a lower bound where harness-censored costs remain. See BAI_ACCOUNTING.md for source accounting differences.

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:38:45.987299+00:00. No network requests are required to view this file.

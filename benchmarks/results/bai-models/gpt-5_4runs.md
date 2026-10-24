# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

2000 tasks. Price catalog 2026-10-23.1-bai-routes.1 · SHA-256 50395bc63c7d0dcd458b5e074bbc5b2883fbe4985bba4ee58f1fec65493f9069.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ. Bai analysis adds exact observed provider/proxy route aliases; dollar rates are unchanged. Qwen hosted and Kimi OpenRouter tariffs remain unknown.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Bai SWE-bench Verified: gpt-5_4runs.tar.gz. Benchmark tasks, not production.

Task groups: 2000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 2000 records. Fields read: action, args, error, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Import limitations: aggregate_usage_without_calls: 1

Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded.

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2026-01-01T06:31:51.394402+00:00; 10 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $829.9134. Overall distribution weights each of 1 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 100 iterations for 1999 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 2000 | 9 | 3 | VIABLE | grouped_cv: upper loss-ratio interval stays below 90% at the 70% target with p99 cap; also with 3 unpriced tasks (0.1%) at the training p99 cost |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| code | 3 | 0.1% | VIABLE | VIABLE | 79.5% → 79.9% | 80.1% → 80.4% |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 2000 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

### code · grouped CV vs time split

| Censoring | Cap | Target | Grouped CV loss ratio | Held-out fold 90% CI (verdict) | Pooled 90% CI | Tasks losing | Worst loss | Leave-one-run-out loss ratio | Leave-one-run-out held-out 90% CI | Time split (leaks repeated tasks) loss ratio | Time split 90% CI | Difference: time split − grouped CV | Difference: upper CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exclude | none | 60.0% | 60.0% | 52.3% – 68.6% | 59.9% – 60.1% | 11.6% | $1.7214 | 60.0% | 57.3% – 62.9% | 63.1% | 60.7% – 65.6% | +3.1% | -3.0% |
| exclude | none | 70.0% | 70.0% | 61.0% – 80.0% | 69.9% – 70.1% | 17.9% | $1.8175 | 70.0% | 66.8% – 73.4% | 73.7% | 70.8% – 76.6% | +3.7% | -3.5% |
| exclude | none | 80.0% | 80.0% | 69.7% – 91.5% | 79.9% – 80.1% | 24.2% | $1.8895 | 80.0% | 76.4% – 83.9% | 84.2% | 80.9% – 87.5% | +4.2% | -4.0% |
| exclude | p99 | 60.0% | 59.9% | 52.5% – 68.1% | 59.8% – 60.0% | 11.8% | $0.8499 | 60.0% | 57.5% – 62.4% | 63.2% | 60.8% – 65.5% | +3.3% | -2.6% |
| exclude | p99 | 70.0% | 69.9% | 61.2% – 79.5% | 69.7% – 70.0% | 18.2% | $0.9468 | 70.0% | 67.1% – 72.8% | 73.7% | 71.0% – 76.4% | +3.8% | -3.0% |
| exclude | p99 | 80.0% | 79.9% | 70.0% – 90.8% | 79.7% – 80.0% | 24.7% | $1.0194 | 80.0% | 76.6% – 83.3% | 84.2% | 81.1% – 87.3% | +4.4% | -3.5% |
| inflate | none | 60.0% | 60.0% | 51.4% – 70.0% | 59.9% – 60.1% | 11.1% | $3.2091 | 60.0% | 57.1% – 63.2% | 62.9% | 60.1% – 65.7% | +2.9% | -4.3% |
| inflate | none | 70.0% | 70.0% | 60.0% – 81.7% | 69.9% – 70.1% | 16.7% | $3.3078 | 70.0% | 66.6% – 73.8% | 73.4% | 70.2% – 76.7% | +3.4% | -5.0% |
| inflate | none | 80.0% | 80.0% | 68.6% – 93.4% | 79.9% – 80.1% | 23.4% | $3.3818 | 80.0% | 76.1% – 84.3% | 83.8% | 80.2% – 87.6% | +3.8% | -5.7% |
| inflate | p99 | 60.0% | 59.8% | 52.0% – 68.7% | 59.7% – 60.1% | 11.8% | $1.8938 | 60.0% | 57.5% – 62.4% | 62.9% | 60.5% – 65.4% | +3.1% | -3.3% |
| inflate | p99 | 70.0% | 69.8% | 60.6% – 80.1% | 69.6% – 70.1% | 17.6% | $1.9910 | 70.0% | 67.1% – 72.8% | 73.4% | 70.6% – 76.3% | +3.6% | -3.8% |
| inflate | p99 | 80.0% | 79.8% | 69.3% – 91.6% | 79.5% – 80.1% | 24.2% | $2.0640 | 80.0% | 76.7% – 83.3% | 83.9% | 80.7% – 87.2% | +4.2% | -4.3% |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 1988 | $0.4096 | $0.3446 | $0.7125 | $1.4743 | $2.3939 | 2.07 | 4.4% | 15.1% |
| Overall · equal type weight | 1988 | $0.4096 | $0.3446 | $0.7135 | $1.4793 | $2.3939 | 2.07 | 4.4% | 15.0% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| code | 2000 | 9 | 0.4% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 40.1%; their spend per task $0.1876; tasks with loop signals 7.6%. Raw dollar totals below are accounting totals.

Repricing acceptance: PASS. 72187 of 72187 recorded-cost calls within 1% (100.0%); 72187 comparable calls (100.0% agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $829.9134; standard-rate reprice $829.9134; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1194 | 1996/2000 | 59.8% | 1997/1194 | $0.6951 |

### Unknown models

| Provider/model | Calls |
| --- | --- |
| unknown/unknown | 1 |

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |

No available observations for this table.

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| code | $829.9134 | $375.1019 | $15.5506 | 153 | 86.01 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-f9defda4a0384e34591d2a9afd73285b534a43f65b97bee2ade5a4e357438166 | $2.6771 | complete | fail | True |
| task-43e43969e309edf431b5b126c5b33e9add54916a4e643cb04fb7e096a5a1fc1e | $2.3939 | complete | fail | False |
| task-2736cc5a92d08e8f2729ffb1ccf4b87e0ac7b3af359ff2cac61f7b02dfdf72f0 | $2.1513 | complete | fail | False |
| task-d2bdc71b7bda7597a34013491275f52197af86dbffe93155d6473ae4c821005f | $2.1457 | complete | success | False |
| task-6e2648a7d6c85b36727277642bc04d403fb1b4229ae5ad16f1ca7e257afd347e | $2.0897 | complete | fail | True |
| task-49813e05cca5c8227c0f2d30cbf1dc723178fbef8d9090a1fcffd20ca4b7f6d1 | $2.0734 | complete | fail | False |
| task-e7af5643074341d43f3086b7d237b123a7b269f6dfe6c0811edc5c34277a1b96 | $2.0573 | complete | fail | True |
| task-5bcbe7a37a91e8a8e39c8b6d53647c0a1f9065ed75b907cd237b77539511c742 | $1.9774 | complete | fail | False |
| task-24000cb2fa0ea6e8643c463a590a061b489137a00dbfe5113f41207a589ba34f | $1.9600 | complete | fail | False |
| task-3d4d5f62e7da4861ffe3b4f57184d901b8f7fd7b16bc71226b615ccb00b7d8a7 | $1.9074 | complete | success | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-db6e0ba203f3252fcd76e69252218cd753840de2cd972736bddd13dbf9c432a4 | run × 5 | 41 | False | $0.6656 |
| task-5c51241668884f7a3beb1b190ad87bfa3f692cd81c09b922428eb05e431c972b | run × 3 | 40 | False | $0.6362 |
| task-5cad531a549512dd68cf6f67415adb9d77c1ae7704a78ad52a8fc6f271a219d6 | run × 3 | 79 | False | $0.7624 |
| task-6085f73a0345177dc8e018ba3ce2c0dd755683fd9b1f382bd79d90a9d3319979 | run × 3 | 56 | False | $0.9924 |
| task-f6171690d742d5687be126663243a63acbf245bb7612122ba1c90696242405f1 | run × 3 | 37 | False | $0.3857 |
| task-d11b5d644625b598bbb7452164a1bab192a46f103c51f9532f01c2c78037e59e | run × 3 | 81 | False | $1.5577 |
| task-aa40ea2c007150428a3c12866c4991d19eca2faf1ec69d4d80f9a507927fbdd9 | run × 3 | 53 | False | $0.5958 |
| task-d2bdc71b7bda7597a34013491275f52197af86dbffe93155d6473ae4c821005f | run × 4; run × 10 | 98 | False | $2.1457 |
| task-11ba3c32c33f854fe36a633848a857501e1c4b1196df00b457d55e4e47d67295 | run × 3 | 28 | False | $0.3291 |
| task-2f0460864225f8aea7e2e585c40c6d4f305f13c9a4d04427135b81f664f6396f | run × 3 | 32 | False | $0.3994 |
| task-fa461c06302954604a19277b46dadbef5f9630e87394f8cb18245ae573a16277 | run × 4 | 34 | False | $0.4186 |
| task-dc7dadf9e8576d241e111b245ba86c2d0f20cfd4efa4b200ea14c2bdf1f4d4e1 | run × 3 | 34 | False | $0.4272 |
| task-3ef67b2adb90ddbabefcf31e9a112c5aa27812040a88bcece116b2ec2dee471e | run × 4 | 47 | False | $0.8560 |
| task-790f05b62c1270f813ded26ef0dd5985d0928d81553c6cf4e80368dc51d5c041 | run × 3 | 44 | False | $0.4151 |
| task-ed44dc70aac8b7a0425809729a8ac8a43714a81944c84660b73dee20cdd91ca5 | run × 3 | 47 | False | $0.5925 |
| task-9e572c34dc0a16acf1acdaadceb9230cd67bdec1569abf3393d80932c33c34d1 | edit × 4 | 55 | False | $0.6878 |
| task-ce78e7062719c5e332252d157a0522cd7e33a27f10ce0090856b8f0d6a0e9b8c | run × 3 | 45 | False | $0.2853 |
| task-6a68462795ffd6916c6d2d5663182349cedad5f2ef53ca2ac2592603625f10b8 | run × 3 | 49 | False | $0.7208 |
| task-6776dc1ed9e09a7f2dfe68fc0dc3f9b48c6bca779459727a423d4a94065fc160 | run × 3; run × 3 | 50 | False | $0.5498 |
| task-7f856bb08ce99ca5f0605c73cb1ab050222518c318dfc8eda049c8352ffb70a7 | run × 3 | 40 | False | $0.4721 |
| task-3b7d81495e06a88e878b0d2345472a49f38deefe69f04c74cb469a7261ab2691 | run × 4; run × 4; run × 3 | 100 | False | $1.7400 |
| task-623528f60f0b8376ad54a71cffa7626d8c4e4667b4deb0c09aeaaec189714fff | run × 3 | 50 | False | $0.5701 |
| task-7cd906bb24e32098871119f609998746e04ae0faf6aa7ebf8c15418fb8afa0be | run × 4 | 63 | False | $0.6726 |
| task-df799c35114197fc8096f11102a6a33e4906c8c8924836838d7342b844c12e45 | run × 4 | 48 | False | $0.5403 |
| task-d1de51089be4899dda390b3846c43b131479f25b03c584f8600facfe3cd3f4fc | run × 8 | 100 | False | $1.7762 |
| task-f2844c39246506dad6eb0e2999f661f2adaec7c9d7a11fd2946ed9dea6a1d8ea | run × 4 | 92 | False | $1.4284 |
| task-d2f1254b816795555d496c0d5f05e2ec4c54e7361d766ead3657a08d8028d59e | run × 3 | 36 | False | $0.3649 |
| task-783ec042211f8f61b9f61ae1c85b7bc80d8a4e231f87ec635f4f3d2464efc611 | run × 3; run × 4 | 64 | False | $1.1492 |
| task-316a82b0f734f4cdcb668484fe9a58071b344f7a8a903dda5af25f1c51bfdfa6 | run × 3; run × 15 | 84 | False | $1.7318 |
| task-3971cea2dd5af76820279759ae8d30e52cd0207b772dde94ba5251e8909f0aa8 | run × 3 | 82 | False | $1.3862 |
| task-bab36dfcba5de8b43bb5dc3ce9702088758bfe82f86c8b8df0cc7fee9a2c550a | read × 3; edit × 4 | 47 | False | $0.3656 |
| task-a4b3e78e966b2cb388af8d9cd9f68ecb4dc81c6d84e4d3bf45c8dc0a3f832ed5 | read × 4 | 48 | False | $0.3915 |
| task-70ba77bc514b1bb8b57ac54d9b15fcdffeeab986320b113e752fce796f2688c4 | run × 4 | 34 | False | $0.5006 |
| task-7d9d8527e7aac9168a3571b5266c2c92b6a85e8a84004b4fd394ca2a63d895dc | run × 4 | 31 | False | $0.2838 |
| task-292cd450912e969e3307ba04f11238bf8be6279c1ec7e1758ded80ddcb78c2d5 | run × 4 | 43 | False | $0.3450 |
| task-5383d0005a396b6e2e5278a3c54c1dea5362db3e61dc13c4e8118b95e3a2a21d | task_tracking × 3 | 35 | False | $0.2105 |
| task-e7af5643074341d43f3086b7d237b123a7b269f6dfe6c0811edc5c34277a1b96 | run × 3; run × 3; run × 5 | 100 | False | $2.0573 |
| task-bb18a9202e9146b8fc14fe91d7148c7061d832ced130c6eab92d9044679621bf | run × 3 | 33 | False | $0.5006 |
| task-b2b7b12a5c01ac2e4a073a791355106170cee53768e1e76a96ed5741a1cf226e | run × 3 | 38 | False | $0.6094 |
| task-a4e1194ec39edc35c55e68047ab773f0eeddc0e2f5c9f560f07e3312ae61e514 | run × 3 | 42 | False | $0.6246 |
| task-be2bdd2ed2d46af5a310282346db89ccd8a4ec589012807f6170a4334712016a | run × 3 | 43 | False | $0.4146 |
| task-8a21427c23e2c7ae355ea02fa7873c1c47ec5f6e587a0e4e055559d6cd9e08a7 | run × 3 | 30 | False | $0.4031 |
| task-fb9462cde06bf54285a9cbbcfac9fd1a58079212b78f8de78287af261d2524b2 | run × 3 | 55 | False | $0.5123 |
| task-e170bfe9a491e1af31d3ba64f9cf0f66163ec09e47d1ab6caa58c8d23b178655 | run × 3 | 37 | False | $0.5049 |
| task-834d7a79f86a7a8cf0f2537557a92ae385cb382867b6093178f3819e4a024455 | run × 4 | 62 | False | $1.2380 |
| task-475023d681fe5a77f34fe2b61e902ea50d6112ec116bd8860d3b02f076726d33 | run × 5; run × 3; run × 3 | 47 | False | $0.6034 |
| task-6086dbd8d137b4a39b4edc62fb03db19661d86d4ae6734393a0274b27f83b1ec | run × 3 | 43 | False | $0.6672 |
| task-a024316cb3dfb7d0bc8bd5deeb8a70e4d35bca250678a06481fdae629a2b1aaa | run × 3 | 62 | False | $0.6699 |
| task-49813e05cca5c8227c0f2d30cbf1dc723178fbef8d9090a1fcffd20ca4b7f6d1 | run × 3; run × 6 | 75 | False | $2.0734 |
| task-285723800a3a10c9a4f9580952c8424ed5b12d3a5454f3bd8936f13e879c5a32 | run × 3 | 31 | False | $0.3693 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | p95 | $0.9066 | 4.7% | $30.7078 | 3.8% | 5.0% | $32.3139 |
| code | p99 | $1.4743 | 1.0% | $5.7991 | 0.7% | 1.0% | $6.2434 |
| code | p99.5 | $1.6522 | 0.5% | $3.4734 | 0.4% | 0.5% | $3.5747 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 1 | 4.7% | $0.0154 | 3.8% |
| p99 | 1 | 1.0% | $0.0029 | 0.7% |
| p99.5 | 1 | 0.5% | $0.0017 | 0.4% |

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
| in_sample | exclude | none | 60.0% | $0.6827 | 60.0% | 58.5% – 61.5% | 11.7% | $1.7112 | 1988/1988 |
| in_sample | exclude | none | 70.0% | $0.5852 | 70.0% | 68.3% – 71.7% | 17.7% | $1.8087 | 1988/1988 |
| in_sample | exclude | none | 80.0% | $0.5120 | 80.0% | 78.0% – 82.0% | 24.1% | $1.8819 | 1988/1988 |
| in_sample | exclude | p99 | 60.0% | $0.6779 | 60.0% | 58.6% – 61.4% | 12.2% | $0.8882 | 1988/1988 |
| in_sample | exclude | p99 | 70.0% | $0.5810 | 70.0% | 68.4% – 71.6% | 18.1% | $0.9850 | 1988/1988 |
| in_sample | exclude | p99 | 80.0% | $0.5084 | 80.0% | 78.1% – 81.9% | 24.5% | $1.0576 | 1988/1988 |
| in_sample | inflate | none | 60.0% | $0.7019 | 60.0% | 58.3% – 61.8% | 11.0% | $3.2050 | 1997/1997 |
| in_sample | inflate | none | 70.0% | $0.6016 | 70.0% | 68.0% – 72.0% | 16.9% | $3.3053 | 1997/1997 |
| in_sample | inflate | none | 80.0% | $0.5264 | 80.0% | 77.8% – 82.3% | 23.2% | $3.3805 | 1997/1997 |
| in_sample | inflate | p99 | 60.0% | $0.6885 | 60.0% | 58.5% – 61.5% | 11.7% | $1.8931 | 1997/1997 |
| in_sample | inflate | p99 | 70.0% | $0.5901 | 70.0% | 68.3% – 71.7% | 17.7% | $1.9915 | 1997/1997 |
| in_sample | inflate | p99 | 80.0% | $0.5164 | 80.0% | 78.0% – 82.0% | 24.1% | $2.0653 | 1997/1997 |
| holdout | exclude | none | 60.0% | $0.6667 | 63.1% | 60.7% – 65.6% | 13.8% | $1.2933 | 1227/752 |
| holdout | exclude | none | 70.0% | $0.5714 | 73.7% | 70.8% – 76.6% | 19.9% | $1.3886 | 1227/752 |
| holdout | exclude | none | 80.0% | $0.5000 | 84.2% | 80.9% – 87.5% | 26.3% | $1.4600 | 1227/752 |
| holdout | exclude | p99 | 60.0% | $0.6614 | 63.2% | 60.8% – 65.5% | 14.0% | $0.8146 | 1227/752 |
| holdout | exclude | p99 | 70.0% | $0.5669 | 73.7% | 71.0% – 76.4% | 20.3% | $0.9091 | 1227/752 |
| holdout | exclude | p99 | 80.0% | $0.4960 | 84.2% | 81.1% – 87.3% | 26.5% | $0.9800 | 1227/752 |
| holdout | inflate | none | 60.0% | $0.6863 | 62.9% | 60.1% – 65.7% | 13.1% | $3.1639 | 1233/755 |
| holdout | inflate | none | 70.0% | $0.5882 | 73.4% | 70.2% – 76.7% | 18.7% | $3.2620 | 1233/755 |
| holdout | inflate | none | 80.0% | $0.5147 | 83.8% | 80.2% – 87.6% | 25.3% | $3.3355 | 1233/755 |
| holdout | inflate | p99 | 60.0% | $0.6723 | 62.9% | 60.5% – 65.4% | 14.0% | $1.7746 | 1233/755 |
| holdout | inflate | p99 | 70.0% | $0.5762 | 73.4% | 70.6% – 76.3% | 19.7% | $1.8706 | 1233/755 |
| holdout | inflate | p99 | 80.0% | $0.5042 | 83.9% | 80.7% – 87.2% | 26.1% | $1.9426 | 1233/755 |
| grouped_cv | exclude | none | 60.0% | $0.6827 | 60.0% | 52.3% – 68.6% | 11.6% | $1.7214 | 1588/1988 |
| grouped_cv | exclude | none | 70.0% | $0.5852 | 70.0% | 61.0% – 80.0% | 17.9% | $1.8175 | 1588/1988 |
| grouped_cv | exclude | none | 80.0% | $0.5121 | 80.0% | 69.7% – 91.5% | 24.2% | $1.8895 | 1588/1988 |
| grouped_cv | exclude | p99 | 60.0% | $0.6778 | 59.9% | 52.5% – 68.1% | 11.8% | $0.8499 | 1588/1988 |
| grouped_cv | exclude | p99 | 70.0% | $0.5810 | 69.9% | 61.2% – 79.5% | 18.2% | $0.9468 | 1588/1988 |
| grouped_cv | exclude | p99 | 80.0% | $0.5084 | 79.9% | 70.0% – 90.8% | 24.7% | $1.0194 | 1588/1988 |
| grouped_cv | inflate | none | 60.0% | $0.7019 | 60.0% | 51.4% – 70.0% | 11.1% | $3.2091 | 1597/1997 |
| grouped_cv | inflate | none | 70.0% | $0.6016 | 70.0% | 60.0% – 81.7% | 16.7% | $3.3078 | 1597/1997 |
| grouped_cv | inflate | none | 80.0% | $0.5264 | 80.0% | 68.6% – 93.4% | 23.4% | $3.3818 | 1597/1997 |
| grouped_cv | inflate | p99 | 60.0% | $0.6892 | 59.8% | 52.0% – 68.7% | 11.8% | $1.8938 | 1597/1997 |
| grouped_cv | inflate | p99 | 70.0% | $0.5907 | 69.8% | 60.6% – 80.1% | 17.6% | $1.9910 | 1597/1997 |
| grouped_cv | inflate | p99 | 80.0% | $0.5169 | 79.8% | 69.3% – 91.6% | 24.2% | $2.0640 | 1597/1997 |
| leave_one_run_out | exclude | none | 60.0% | $0.6827 | 60.0% | 57.3% – 62.9% | 11.7% | $1.7104 | 1490/1988 |
| leave_one_run_out | exclude | none | 70.0% | $0.5852 | 70.0% | 66.8% – 73.4% | 17.6% | $1.8081 | 1490/1988 |
| leave_one_run_out | exclude | none | 80.0% | $0.5120 | 80.0% | 76.4% – 83.9% | 24.1% | $1.8813 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 60.0% | $0.6779 | 60.0% | 57.5% – 62.4% | 12.1% | $0.8627 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 70.0% | $0.5810 | 70.0% | 67.1% – 72.8% | 17.9% | $0.9597 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.5084 | 80.0% | 76.6% – 83.3% | 24.5% | $1.0324 | 1490/1988 |
| leave_one_run_out | inflate | none | 60.0% | $0.7019 | 60.0% | 57.1% – 63.2% | 11.1% | $3.2059 | 1497/1997 |
| leave_one_run_out | inflate | none | 70.0% | $0.6016 | 70.0% | 66.6% – 73.8% | 17.0% | $3.3060 | 1497/1997 |
| leave_one_run_out | inflate | none | 80.0% | $0.5264 | 80.0% | 76.1% – 84.3% | 23.2% | $3.3811 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 60.0% | $0.6889 | 60.0% | 57.5% – 62.4% | 11.7% | $2.0361 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 70.0% | $0.5905 | 70.0% | 67.1% – 72.8% | 17.7% | $2.1347 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.5167 | 80.0% | 76.7% – 83.3% | 24.1% | $2.2087 | 1497/1997 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $0.6827 | 60.0% | 52.3% – 68.6% | 11.6% | $1.7214 | 1588/1988 |
| grouped_cv | exclude | none | 70.0% | $0.5852 | 70.0% | 61.0% – 80.0% | 17.9% | $1.8175 | 1588/1988 |
| grouped_cv | exclude | none | 80.0% | $0.5121 | 80.0% | 69.7% – 91.5% | 24.2% | $1.8895 | 1588/1988 |
| grouped_cv | exclude | p99 | 60.0% | $0.6778 | 59.9% | 52.5% – 68.1% | 11.8% | $0.8499 | 1588/1988 |
| grouped_cv | exclude | p99 | 70.0% | $0.5810 | 69.9% | 61.2% – 79.5% | 18.2% | $0.9468 | 1588/1988 |
| grouped_cv | exclude | p99 | 80.0% | $0.5084 | 79.9% | 70.0% – 90.8% | 24.7% | $1.0194 | 1588/1988 |
| grouped_cv | inflate | none | 60.0% | $0.7019 | 60.0% | 51.4% – 70.0% | 11.1% | $3.2091 | 1597/1997 |
| grouped_cv | inflate | none | 70.0% | $0.6016 | 70.0% | 60.0% – 81.7% | 16.7% | $3.3078 | 1597/1997 |
| grouped_cv | inflate | none | 80.0% | $0.5264 | 80.0% | 68.6% – 93.4% | 23.4% | $3.3818 | 1597/1997 |
| grouped_cv | inflate | p99 | 60.0% | $0.6892 | 59.8% | 52.0% – 68.7% | 11.8% | $1.8938 | 1597/1997 |
| grouped_cv | inflate | p99 | 70.0% | $0.5907 | 69.8% | 60.6% – 80.1% | 17.6% | $1.9910 | 1597/1997 |
| grouped_cv | inflate | p99 | 80.0% | $0.5169 | 79.8% | 69.3% – 91.6% | 24.2% | $2.0640 | 1597/1997 |
| holdout | exclude | none | 60.0% | $0.6667 | 63.1% | 60.7% – 65.6% | 13.8% | $1.2933 | 1227/752 |
| holdout | exclude | none | 70.0% | $0.5714 | 73.7% | 70.8% – 76.6% | 19.9% | $1.3886 | 1227/752 |
| holdout | exclude | none | 80.0% | $0.5000 | 84.2% | 80.9% – 87.5% | 26.3% | $1.4600 | 1227/752 |
| holdout | exclude | p99 | 60.0% | $0.6614 | 63.2% | 60.8% – 65.5% | 14.0% | $0.8146 | 1227/752 |
| holdout | exclude | p99 | 70.0% | $0.5669 | 73.7% | 71.0% – 76.4% | 20.3% | $0.9091 | 1227/752 |
| holdout | exclude | p99 | 80.0% | $0.4960 | 84.2% | 81.1% – 87.3% | 26.5% | $0.9800 | 1227/752 |
| holdout | inflate | none | 60.0% | $0.6863 | 62.9% | 60.1% – 65.7% | 13.1% | $3.1639 | 1233/755 |
| holdout | inflate | none | 70.0% | $0.5882 | 73.4% | 70.2% – 76.7% | 18.7% | $3.2620 | 1233/755 |
| holdout | inflate | none | 80.0% | $0.5147 | 83.8% | 80.2% – 87.6% | 25.3% | $3.3355 | 1233/755 |
| holdout | inflate | p99 | 60.0% | $0.6723 | 62.9% | 60.5% – 65.4% | 14.0% | $1.7746 | 1233/755 |
| holdout | inflate | p99 | 70.0% | $0.5762 | 73.4% | 70.6% – 76.3% | 19.7% | $1.8706 | 1233/755 |
| holdout | inflate | p99 | 80.0% | $0.5042 | 83.9% | 80.7% – 87.2% | 26.1% | $1.9426 | 1233/755 |
| in_sample | exclude | none | 60.0% | $0.6827 | 60.0% | 58.5% – 61.5% | 11.7% | $1.7112 | 1988/1988 |
| in_sample | exclude | none | 70.0% | $0.5852 | 70.0% | 68.3% – 71.7% | 17.7% | $1.8087 | 1988/1988 |
| in_sample | exclude | none | 80.0% | $0.5120 | 80.0% | 78.0% – 82.0% | 24.1% | $1.8819 | 1988/1988 |
| in_sample | exclude | p99 | 60.0% | $0.6779 | 60.0% | 58.6% – 61.4% | 12.2% | $0.8882 | 1988/1988 |
| in_sample | exclude | p99 | 70.0% | $0.5810 | 70.0% | 68.4% – 71.6% | 18.1% | $0.9850 | 1988/1988 |
| in_sample | exclude | p99 | 80.0% | $0.5084 | 80.0% | 78.1% – 81.9% | 24.5% | $1.0576 | 1988/1988 |
| in_sample | inflate | none | 60.0% | $0.7019 | 60.0% | 58.3% – 61.8% | 11.0% | $3.2050 | 1997/1997 |
| in_sample | inflate | none | 70.0% | $0.6016 | 70.0% | 68.0% – 72.0% | 16.9% | $3.3053 | 1997/1997 |
| in_sample | inflate | none | 80.0% | $0.5264 | 80.0% | 77.8% – 82.3% | 23.2% | $3.3805 | 1997/1997 |
| in_sample | inflate | p99 | 60.0% | $0.6885 | 60.0% | 58.5% – 61.5% | 11.7% | $1.8931 | 1997/1997 |
| in_sample | inflate | p99 | 70.0% | $0.5901 | 70.0% | 68.3% – 71.7% | 17.7% | $1.9915 | 1997/1997 |
| in_sample | inflate | p99 | 80.0% | $0.5164 | 80.0% | 78.0% – 82.0% | 24.1% | $2.0653 | 1997/1997 |
| leave_one_run_out | exclude | none | 60.0% | $0.6827 | 60.0% | 57.3% – 62.9% | 11.7% | $1.7104 | 1490/1988 |
| leave_one_run_out | exclude | none | 70.0% | $0.5852 | 70.0% | 66.8% – 73.4% | 17.6% | $1.8081 | 1490/1988 |
| leave_one_run_out | exclude | none | 80.0% | $0.5120 | 80.0% | 76.4% – 83.9% | 24.1% | $1.8813 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 60.0% | $0.6779 | 60.0% | 57.5% – 62.4% | 12.1% | $0.8627 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 70.0% | $0.5810 | 70.0% | 67.1% – 72.8% | 17.9% | $0.9597 | 1490/1988 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.5084 | 80.0% | 76.6% – 83.3% | 24.5% | $1.0324 | 1490/1988 |
| leave_one_run_out | inflate | none | 60.0% | $0.7019 | 60.0% | 57.1% – 63.2% | 11.1% | $3.2059 | 1497/1997 |
| leave_one_run_out | inflate | none | 70.0% | $0.6016 | 70.0% | 66.6% – 73.8% | 17.0% | $3.3060 | 1497/1997 |
| leave_one_run_out | inflate | none | 80.0% | $0.5264 | 80.0% | 76.1% – 84.3% | 23.2% | $3.3811 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 60.0% | $0.6889 | 60.0% | 57.5% – 62.4% | 11.7% | $2.0361 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 70.0% | $0.5905 | 70.0% | 67.1% – 72.8% | 17.7% | $2.1347 | 1497/1997 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.5167 | 80.0% | 76.7% – 83.3% | 24.1% | $2.2087 | 1497/1997 |

### code · success-only billing

| Scope | Censoring | Cap | Target | Mean fold price / success | Loss ratio | 90% CI | Tasks losing | Worst loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $1.1373 | 59.9% | 46.4% – 78.6% | 40.8% | $2.3939 |
| grouped_cv | exclude | none | 65.0% | $1.0499 | 64.9% | 50.3% – 85.2% | 41.3% | $2.3939 |
| grouped_cv | exclude | none | 70.0% | $0.9749 | 69.9% | 54.2% – 91.7% | 41.5% | $2.3939 |
| grouped_cv | exclude | none | 80.0% | $0.8530 | 79.8% | 61.9% – 104.8% | 42.7% | $2.3939 |
| grouped_cv | exclude | p99 | 60.0% | $1.1343 | 59.8% | 46.5% – 78.4% | 40.8% | $1.5311 |
| grouped_cv | exclude | p99 | 65.0% | $1.0471 | 64.8% | 50.4% – 84.9% | 41.3% | $1.5311 |
| grouped_cv | exclude | p99 | 70.0% | $0.9723 | 69.8% | 54.3% – 91.5% | 41.5% | $1.5311 |
| grouped_cv | exclude | p99 | 80.0% | $0.8508 | 79.8% | 62.0% – 104.5% | 42.7% | $1.5311 |
| grouped_cv | inflate | none | 60.0% | $1.1726 | 59.9% | 45.9% – 80.0% | 41.0% | $3.8999 |
| grouped_cv | inflate | none | 65.0% | $1.0824 | 64.9% | 49.7% – 86.6% | 41.4% | $3.8999 |
| grouped_cv | inflate | none | 70.0% | $1.0051 | 69.9% | 53.5% – 93.3% | 41.7% | $3.8999 |
| grouped_cv | inflate | none | 80.0% | $0.8794 | 79.8% | 61.2% – 106.6% | 42.6% | $3.8999 |
| grouped_cv | inflate | p99 | 60.0% | $1.1576 | 59.8% | 46.2% – 79.0% | 41.0% | $2.5746 |
| grouped_cv | inflate | p99 | 65.0% | $1.0686 | 64.7% | 50.1% – 85.5% | 41.4% | $2.5746 |
| grouped_cv | inflate | p99 | 70.0% | $0.9922 | 69.7% | 53.9% – 92.1% | 41.8% | $2.5746 |
| grouped_cv | inflate | p99 | 80.0% | $0.8682 | 79.7% | 61.6% – 105.3% | 42.7% | $2.5746 |
| leave_one_run_out | exclude | none | 60.0% | $1.1369 | 60.0% | 56.7% – 63.7% | 40.8% | $2.3939 |
| leave_one_run_out | exclude | none | 65.0% | $1.0494 | 65.0% | 61.4% – 69.0% | 41.2% | $2.3939 |
| leave_one_run_out | exclude | none | 70.0% | $0.9745 | 70.0% | 66.1% – 74.3% | 41.5% | $2.3939 |
| leave_one_run_out | exclude | none | 80.0% | $0.8527 | 80.0% | 75.6% – 84.9% | 42.7% | $2.3939 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.1342 | 60.0% | 56.5% – 63.9% | 40.8% | $1.5416 |
| leave_one_run_out | exclude | p99 | 65.0% | $1.0470 | 65.0% | 61.3% – 69.2% | 41.2% | $1.5416 |
| leave_one_run_out | exclude | p99 | 70.0% | $0.9722 | 70.0% | 66.0% – 74.5% | 41.5% | $1.5416 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.8507 | 80.0% | 75.4% – 85.1% | 42.7% | $1.5416 |
| leave_one_run_out | inflate | none | 60.0% | $1.1721 | 60.0% | 56.3% – 64.0% | 41.0% | $3.9065 |
| leave_one_run_out | inflate | none | 65.0% | $1.0820 | 65.0% | 61.0% – 69.3% | 41.3% | $3.9065 |
| leave_one_run_out | inflate | none | 70.0% | $1.0047 | 70.0% | 65.7% – 74.7% | 41.7% | $3.9065 |
| leave_one_run_out | inflate | none | 80.0% | $0.8791 | 80.0% | 75.1% – 85.3% | 42.7% | $3.9065 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.1569 | 60.0% | 56.4% – 63.9% | 41.1% | $2.7267 |
| leave_one_run_out | inflate | p99 | 65.0% | $1.0679 | 65.1% | 61.1% – 69.2% | 41.4% | $2.7267 |
| leave_one_run_out | inflate | p99 | 70.0% | $0.9916 | 70.1% | 65.8% – 74.5% | 41.7% | $2.7267 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.8677 | 80.1% | 75.2% – 85.2% | 42.8% | $2.7267 |

### Success-only billing · highest viable target

| Type | Per-task price at 70% (all tasks billed) | Highest viable success-only target | Price per resolved task at that target | Why none |
| --- | --- | --- | --- | --- |
| code | $0.5810 | 65.0% | $1.0471 | — |

### code · fold fits at 70% target with cap

| Scope | Billing | Censoring | Fold | Train/test groups | Price | Cap | Score loss ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | all_tasks | exclude | 1 | 400/100 | $0.5768 | $1.4828 | 72.6% |
| grouped_cv | all_tasks | exclude | 2 | 400/100 | $0.5719 | $1.3688 | 74.6% |
| grouped_cv | all_tasks | exclude | 3 | 400/100 | $0.5921 | $1.5191 | 63.8% |
| grouped_cv | all_tasks | exclude | 4 | 400/100 | $0.5809 | $1.5192 | 70.4% |
| grouped_cv | all_tasks | exclude | 5 | 400/100 | $0.5831 | $1.4295 | 68.3% |
| grouped_cv | all_tasks | inflate | 1 | 400/100 | $0.5836 | $1.4828 | 74.5% |
| grouped_cv | all_tasks | inflate | 2 | 400/100 | $0.5800 | $1.3688 | 74.7% |
| grouped_cv | all_tasks | inflate | 3 | 400/100 | $0.6038 | $1.5191 | 63.1% |
| grouped_cv | all_tasks | inflate | 4 | 400/100 | $0.5938 | $1.5192 | 68.9% |
| grouped_cv | all_tasks | inflate | 5 | 400/100 | $0.5924 | $1.4295 | 68.2% |
| leave_one_run_out | all_tasks | exclude | 1 | 500/496 | $0.5785 | $1.4294 | 70.9% |
| leave_one_run_out | all_tasks | exclude | 2 | 500/498 | $0.5799 | $1.5111 | 70.8% |
| leave_one_run_out | all_tasks | exclude | 3 | 500/496 | $0.5838 | $1.4828 | 68.7% |
| leave_one_run_out | all_tasks | exclude | 4 | 500/498 | $0.5820 | $1.4741 | 69.6% |
| leave_one_run_out | all_tasks | inflate | 1 | 500/498 | $0.5884 | $1.4294 | 70.4% |
| leave_one_run_out | all_tasks | inflate | 2 | 500/500 | $0.5902 | $1.5111 | 70.6% |
| leave_one_run_out | all_tasks | inflate | 3 | 500/499 | $0.5919 | $1.4828 | 69.7% |
| leave_one_run_out | all_tasks | inflate | 4 | 500/500 | $0.5913 | $1.4741 | 69.5% |
| grouped_cv | success_only | exclude | 1 | 400/100 | $0.9751 | $1.4844 | 69.1% |
| grouped_cv | success_only | exclude | 2 | 400/100 | $0.9572 | $1.3694 | 74.5% |
| grouped_cv | success_only | exclude | 3 | 400/100 | $1.0120 | $1.5193 | 57.5% |
| grouped_cv | success_only | exclude | 4 | 400/100 | $0.9395 | $1.5195 | 84.1% |
| grouped_cv | success_only | exclude | 5 | 400/100 | $0.9777 | $1.4299 | 67.7% |
| grouped_cv | success_only | inflate | 1 | 400/100 | $0.9886 | $1.4844 | 71.5% |
| grouped_cv | success_only | inflate | 2 | 400/100 | $0.9751 | $1.3694 | 74.4% |
| grouped_cv | success_only | inflate | 3 | 400/100 | $1.0361 | $1.5193 | 56.7% |
| grouped_cv | success_only | inflate | 4 | 400/100 | $0.9648 | $1.5195 | 81.9% |
| grouped_cv | success_only | inflate | 5 | 400/100 | $0.9967 | $1.4299 | 67.6% |
| leave_one_run_out | success_only | exclude | 1 | 500/494 | $0.9633 | $1.4296 | 72.4% |
| leave_one_run_out | success_only | exclude | 2 | 500/498 | $0.9720 | $1.5114 | 70.1% |
| leave_one_run_out | success_only | exclude | 3 | 500/496 | $0.9745 | $1.4844 | 69.4% |
| leave_one_run_out | success_only | exclude | 4 | 500/496 | $0.9789 | $1.4743 | 68.2% |
| leave_one_run_out | success_only | inflate | 1 | 500/496 | $0.9832 | $1.4296 | 71.9% |
| leave_one_run_out | success_only | inflate | 2 | 500/500 | $0.9930 | $1.5114 | 70.0% |
| leave_one_run_out | success_only | inflate | 3 | 500/499 | $0.9910 | $1.4844 | 70.6% |
| leave_one_run_out | success_only | inflate | 4 | 500/498 | $0.9992 | $1.4743 | 67.8% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-a3aac58270ad41a447be2bff0673ff49c7d8fd127b0a61cfc6a99a4054a2fef7 · fixed $0.5810 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 1 | ≥ $0.0000 |

### code · task-ab7a25da9a7e8661d6eb9363520124a9f5c3a313e3b084ccac720d478e04ac51 · fixed $0.5810 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 6 | $0.0303 |
| run | 29 | $0.1772 |
| edit | 1 | $0.0120 |
| Model-only calls | 1 | $0.0120 |
| finish | 1 | $0.0085 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

### code · task-89cebcf1159ec781a54b4d0f94b7214ac1dbf6e6816d4e3d2bb229c01e872f2e · fixed $0.5810 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 6 | $0.0702 |
| run | 22 | $0.1955 |
| read | 2 | $0.0229 |
| edit | 4 | $0.0452 |
| finish | 1 | $0.0110 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-a3f8634f12a81e70a49e0210ce487d7cc132d0aeba1cf255370572ee932a9440 · fixed $0.5810 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 4 | $0.0263 |
| run | 31 | $0.3964 |
| read | 1 | $0.0045 |
| edit | 1 | $0.0331 |
| think | 1 | $0.0149 |
| Model-only calls | 1 | $0.0178 |
| finish | 1 | $0.0130 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 3 | — |
| recall (unlinked tool events) | 2 | — |

### code · task-f9defda4a0384e34591d2a9afd73285b534a43f65b97bee2ade5a4e357438166 · fixed $0.5810 (in_sample) · fail · capped=True

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 62 | $1.1276 |
| read | 4 | $0.1156 |
| think | 1 | $0.0471 |
| edit | 28 | $1.2619 |
| task_tracking | 5 | $0.1251 |
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

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:38:26.830910+00:00. No network requests are required to view this file.

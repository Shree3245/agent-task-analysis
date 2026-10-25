# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

2000 tasks. Price catalog 2026-10-23.1-bai-routes.1 · SHA-256 50395bc63c7d0dcd458b5e074bbc5b2883fbe4985bba4ee58f1fec65493f9069.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ. Bai analysis adds exact observed provider/proxy route aliases; dollar rates are unchanged. Qwen hosted and Kimi OpenRouter tariffs remain unknown.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Bai SWE-bench Verified: claude-sonnet-4.5_4runs.tar.gz. Benchmark tasks, not production.

Task groups: 2000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 2000 records. Fields read: action, args, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded.

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2025-12-22T12:00:30.347941+00:00; 4 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $3,680.9210. Overall distribution weights each of 1 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 500 iterations for 2000 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 2000 | 0 | 0 | VIABLE | grouped_cv: upper loss-ratio interval stays below 90% at the 70% target with p99 cap |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 2000 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

### code · grouped CV vs time split

| Censoring | Cap | Target | Grouped CV loss ratio | Held-out fold 90% CI (verdict) | Pooled 90% CI | Tasks losing | Worst loss | Leave-one-run-out loss ratio | Leave-one-run-out held-out 90% CI | Time split (leaks repeated tasks) loss ratio | Time split 90% CI | Difference: time split − grouped CV | Difference: upper CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exclude | none | 60.0% | 60.0% | 54.7% – 65.8% | 60.0% – 60.0% | 6.9% | $4.2166 | 60.0% | 57.4% – 62.1% | 60.0% | 59.0% – 61.1% | +0.0% | -4.7% |
| exclude | none | 70.0% | 70.0% | 63.9% – 76.7% | 70.0% – 70.0% | 12.5% | $4.6534 | 70.0% | 67.0% – 72.4% | 70.0% | 68.8% – 71.3% | +0.0% | -5.5% |
| exclude | none | 80.0% | 80.0% | 73.0% – 87.7% | 79.9% – 80.1% | 19.9% | $4.9811 | 80.0% | 76.6% – 82.8% | 80.0% | 78.7% – 81.4% | +0.0% | -6.3% |
| exclude | p99 | 60.0% | 60.0% | 54.8% – 65.4% | 59.9% – 60.0% | 7.0% | $1.6206 | 60.0% | 57.6% – 61.8% | 59.9% | 58.9% – 60.9% | -0.1% | -4.6% |
| exclude | p99 | 70.0% | 70.0% | 64.0% – 76.3% | 69.8% – 70.0% | 12.7% | $2.0555 | 70.0% | 67.2% – 72.1% | 69.9% | 68.7% – 71.0% | -0.1% | -5.3% |
| exclude | p99 | 80.0% | 80.0% | 73.1% – 87.2% | 79.8% – 80.0% | 20.2% | $2.3854 | 80.0% | 76.8% – 82.4% | 79.8% | 78.6% – 81.2% | -0.1% | -6.1% |
| inflate | none | 60.0% | 60.0% | 54.7% – 65.8% | 60.0% – 60.0% | 6.9% | $4.2166 | 60.0% | 57.4% – 62.1% | 60.0% | 59.0% – 61.1% | +0.0% | -4.7% |
| inflate | none | 70.0% | 70.0% | 63.9% – 76.7% | 70.0% – 70.0% | 12.5% | $4.6534 | 70.0% | 67.0% – 72.4% | 70.0% | 68.8% – 71.3% | +0.0% | -5.5% |
| inflate | none | 80.0% | 80.0% | 73.0% – 87.7% | 79.9% – 80.1% | 19.9% | $4.9811 | 80.0% | 76.6% – 82.8% | 80.0% | 78.7% – 81.4% | +0.0% | -6.3% |
| inflate | p99 | 60.0% | 60.0% | 54.8% – 65.4% | 59.9% – 60.0% | 7.0% | $1.6206 | 60.0% | 57.6% – 61.8% | 59.9% | 58.9% – 60.9% | -0.1% | -4.6% |
| inflate | p99 | 70.0% | 70.0% | 64.0% – 76.3% | 69.8% – 70.0% | 12.7% | $2.0555 | 70.0% | 67.2% – 72.1% | 69.9% | 68.7% – 71.0% | -0.1% | -5.3% |
| inflate | p99 | 80.0% | 80.0% | 73.1% – 87.2% | 79.8% – 80.0% | 20.2% | $2.3854 | 80.0% | 76.8% – 82.4% | 79.8% | 78.6% – 81.2% | -0.1% | -6.1% |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 2000 | $1.8405 | $1.6611 | $2.7815 | $4.5694 | $7.2745 | 1.67 | 2.9% | 11.1% |
| Overall · equal type weight | 2000 | $1.8405 | $1.6589 | $2.7815 | $4.5688 | $7.2745 | 1.68 | 2.9% | 11.1% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| code | 2000 | 0 | 0.0% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 35.6%; their spend per task $0.7394; tasks with loop signals 24.2%. Raw dollar totals below are accounting totals.

Repricing acceptance: PASS. 177257 of 177257 recorded-cost calls within 1% (100.0%); 177257 comparable calls (100.0% agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $3,680.9210; standard-rate reprice $3,680.9210; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1282 | 1995/2000 | 64.3% | 2000/1282 | $2.8712 |

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
| code | $3,680.9210 | $1,478.8213 | $0.0000 | 484 | 167.00 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-bcc7011373ad125069f6846365cca78c00acd33529a0868ac4c52577e1c8cae3 | $7.2745 | complete | success | False |
| task-ef4e26129214c57c09feeb081531b2f6243b50f9253aa6a20742aac7ae26e211 | $7.2350 | complete | fail | False |
| task-7db34faaae2ee67d4279747ec2f69536c3226f22c00ee810b188f229ec219a7f | $6.4488 | complete | fail | False |
| task-33b2c8e217c7486c02337312b252116dd656c0a4963c72c8914f0a3d19b1351c | $5.9697 | complete | fail | False |
| task-1f00ed7fd2ae55f609e10118fcaa8d7487eb94233fe9f4e286dac853611909f9 | $5.8102 | complete | success | False |
| task-8ce879d7521ffaa2b96b0eac1e561cbcb1e801fbaae1344fc9e8a3592655750b | $5.7826 | complete | fail | False |
| task-e97a98414cff302d44812e3f2bdbae22512a0fefb5c8ebcdf120e4157b54ded0 | $5.2379 | complete | fail | False |
| task-3e8114241c9b8c831511a5eb2cd8c87314ade6a6a7fd463209eaefe8ba5f3709 | $5.1301 | complete | success | False |
| task-87c9c074e4854129e3cba0e1694269fd55c20b5ee93819b6553d2b2e177dd21f | $5.0422 | complete | fail | False |
| task-ebbcfc1713b2739469f18790819b2732c771604db74637bdfa8741751fb693b3 | $5.0259 | complete | success | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-8434797ba300e8120c6dd4e50befc56745317feb056c64d8f7503e0f77bfc904 | run × 6 | 111 | False | $2.1177 |
| task-8319085d6bd2f60729cc4ee474674d3af9a0b0376a1a5b7bb2e3d436fee03045 | run × 3 | 153 | False | $4.3918 |
| task-0e3344f63343b8f5c368e5510cb4a7dad881ed0c86d52a99b9e2311799150479 | run × 3 | 78 | False | $1.3084 |
| task-6ee53e7afd599e1194f5f8f1adf1b1d4bf3c172c8a7ab125fef33b5a83643794 | run × 3 | 80 | False | $1.4273 |
| task-920bd6f0f8dd6ed3db51f16f2a3d5da091f97542c0883ed8e2d28a1dd6fb979c | run × 3 | 78 | False | $1.3792 |
| task-b6667a3f2cf6a9f4c7e040a4c340f45adfd8b4c87e222578792bfeb77d1d1299 | run × 3 | 118 | False | $2.5750 |
| task-b82effb720df7342fdcf0d572a1c415026b541cb0b9e9025939cd320442b97c4 | run × 3 | 92 | False | $2.0144 |
| task-947e5294f24c225d875b489b626b4bbcde1f1c9c07d12c209663efc77ee5a1e3 | run × 4 | 105 | False | $1.9115 |
| task-8ce879d7521ffaa2b96b0eac1e561cbcb1e801fbaae1344fc9e8a3592655750b | run × 3 | 180 | False | $5.7826 |
| task-4df8a328bcfbad8080e283a988474bf4c134372aa774bcb77e38d30956d17732 | run × 3; run × 4 | 111 | False | $2.1220 |
| task-4dd9f3fce53f1454af3e541668b9558c798c2c97871a116259e3ca7670cf4d90 | run × 3 | 158 | False | $3.5547 |
| task-9516a0e9629b22a5ffdfd82bdfbbf7401edbc0a46f28259a65693c27aa3c7e71 | run × 3 | 89 | False | $1.7215 |
| task-3d285f2b7695d16e30504306badf7a6c43016eb103c86b0f29218b07167f4f7a | run × 3 | 87 | False | $1.6699 |
| task-5854bcaae217b2445d7a413fba8456a56131ca646b267b80e66a2ad4f92910fe | run × 3 | 94 | False | $2.5378 |
| task-3a4d1981a4683f2aae46cb9efe83698925949a1d7df499dc46b9f574b601a267 | run × 3 | 73 | False | $1.2027 |
| task-28b8ce3e990b38e1fce01ff34d17ad7aac7cb75e381f1609a4312d546c7dc93a | run × 3 | 75 | False | $1.3174 |
| task-9b525ea73f76cc99fca37aa856bac430006466b7a782d173afaf95219314f98d | run × 4 | 127 | False | $3.0678 |
| task-75e72d70f85087b1529432d03645fdc8abfeaa78eb82cc0cdaab170beacc5b5f | run × 4 | 127 | False | $2.5478 |
| task-66981d0e361952260f449a8c595fe3e1651ba2af79da14053f1a985f22ccbee4 | run × 3 | 87 | False | $1.5931 |
| task-840c29ad710ae75a9ec8067ac4d52fc2eca50342dac70523e6e54a33d8f9225a | run × 3 | 80 | False | $1.4918 |
| task-5d6217f02d065bf7b40cf7b659d6bacaec757442a4e852450904701a68df3f9d | run × 3 | 105 | False | $2.3032 |
| task-9705ab43b91986ebe08223a0ae063926391ad14039361953a4fa3d8516ec28f5 | run × 5 | 84 | False | $1.4308 |
| task-8a74ca70f1f90f46756de9b1a153c98ab80592d29e6118d2de71fafbebce6440 | run × 3 | 79 | False | $1.5313 |
| task-8d05e3790316ec70fa6fa79731657107bcb1f52f6e1c44aa2db5340fd7616aec | run × 4; run × 3 | 83 | False | $1.6323 |
| task-704047472db638489de4c8bd55aa2064417177f8f59272afd0e676929f503e46 | run × 4 | 90 | False | $1.9602 |
| task-0be20757a37c8dbd6db8f707a9be0b46ba3660e94be09f0eb4d4fdcf299ad03c | run × 3 | 87 | False | $1.4935 |
| task-82db2b591c0197fc49501ccf40d91c55a5764098b509303bb95b1bbea9a642ec | run × 4 | 93 | False | $1.9887 |
| task-ecedf0d1759a928b88fc3b40bd3c3e605e34fcc5b833e26b853fcb97c7927189 | run × 3 | 175 | False | $4.5083 |
| task-100559d43d5c107e112c1958cca741d271f274c6ec6e1bf6778779f35894363f | run × 4 | 130 | False | $3.1741 |
| task-88974c2d6ea9fe8c20a3d6426324477950381c03bc551294691332fd3e14c203 | run × 3 | 119 | False | $2.3292 |
| task-a13aee003e9949e82ca50194c98ab94d6cb8af5bfe817c7d1480cc7f6225fc5d | run × 3 | 102 | False | $1.9777 |
| task-846e2cc342d028da6437be5ad3ee21165574cf94158d647d33e4886e7de1485a | run × 3 | 76 | False | $1.3225 |
| task-19bf77be5ff7e332abaecc1b791fdd03b049b4348d23451d5d40255c4f77f0f7 | run × 3 | 116 | False | $2.3838 |
| task-4b5edab15ef200f760399b1f9f2199c6069b269621147ad392cf6792a1d07ada | run × 5; run × 5 | 107 | False | $2.4576 |
| task-91af837a66f2231844314feeb6e60e408fc9e8886bae4e18aaf2bd5149ec5afc | run × 3 | 82 | False | $1.5573 |
| task-63e1e1b480d92589219f2897a6c8ddbe60b2b9865fa6ed4153a62612f7700071 | run × 3 | 111 | False | $2.3929 |
| task-3e9acc8a3dab282497e0d8f1589854259938b7f3a669a1f67e297bc39d650491 | run × 3; run × 4; run × 3 | 145 | False | $4.6280 |
| task-c8d614ae24eca0c140686554b9940c74f6ffe203451d72981f52812720b17d78 | run × 3 | 89 | False | $1.6286 |
| task-b405d33490ef3553646862528f0ae1dc33ab6bcef7f24d115fa4378eb947c398 | run × 3 | 88 | False | $1.5351 |
| task-b3080cefc084a48b18147197e249f3a24f57e8e5413222e1341d884b96ff1c55 | run × 3 | 64 | False | $1.1850 |
| task-6be7f54e8aa64219ab1ec9db8c0a446aa865d1785782b561b8aaa4b067e0f14c | run × 6 | 80 | False | $1.7719 |
| task-d45a4bc8a54d73f4e35c8cb1ea07c926e39b44bee67f637f5fd7fb62493dc406 | run × 3 | 108 | False | $2.2038 |
| task-33922070f6c66fbf7dd61fce29e6d6bec1c953ce2857905ec03c7d7e4cffdac5 | run × 3; run × 3 | 79 | False | $1.4597 |
| task-bcc7011373ad125069f6846365cca78c00acd33529a0868ac4c52577e1c8cae3 | run × 3 | 212 | False | $7.2745 |
| task-7dfdd28b30642e4d46c0436f15a69d5408ff0995f489685b683226e3533c43ee | run × 3 | 151 | False | $3.7127 |
| task-df13739b201311775464def0826fc0f054321d9355006e981f1f664c2af76d12 | run × 5 | 130 | False | $3.1390 |
| task-2428fd7aa086e65b7dced79d8963d2dec1b4f5380bb58b1c6f4125617c2bbe11 | run × 3 | 77 | False | $1.6105 |
| task-8a387b0cc2a0ec881d2317737aa25d4b5bc9d5c2504263a0e0ab02bc6e5fd546 | run × 3 | 83 | False | $1.9186 |
| task-d0f556ca9012860a6fc6be8e01a941e9673a79f253381b65289c5b2fe47ae23b | run × 3 | 81 | False | $1.5629 |
| task-75972ac6a82087a35c2cdd6f079602a21dbe142611ffb4ad05d36451ca295d40 | run × 3 | 120 | False | $2.1430 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | p95 | $3.2955 | 4.7% | $77.5948 | 2.1% | 5.0% | $79.6282 |
| code | p99 | $4.5694 | 1.0% | $15.1325 | 0.4% | 1.0% | $15.5844 |
| code | p99.5 | $4.9973 | 0.4% | $8.7234 | 0.2% | 0.5% | $8.9838 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 1 | 4.7% | $0.0388 | 2.1% |
| p99 | 1 | 1.0% | $0.0076 | 0.4% |
| p99.5 | 1 | 0.4% | $0.0044 | 0.2% |

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
| in_sample | exclude | none | 60.0% | $3.0674 | 60.0% | 59.1% – 60.9% | 7.1% | $4.2070 | 2000/2000 |
| in_sample | exclude | none | 70.0% | $2.6292 | 70.0% | 68.9% – 71.1% | 12.5% | $4.6452 | 2000/2000 |
| in_sample | exclude | none | 80.0% | $2.3006 | 80.0% | 78.8% – 81.2% | 19.9% | $4.9739 | 2000/2000 |
| in_sample | exclude | p99 | 60.0% | $3.0548 | 60.0% | 59.1% – 60.9% | 7.1% | $1.5603 | 2000/2000 |
| in_sample | exclude | p99 | 70.0% | $2.6184 | 70.0% | 69.0% – 71.0% | 12.8% | $1.9967 | 2000/2000 |
| in_sample | exclude | p99 | 80.0% | $2.2911 | 80.0% | 78.8% – 81.2% | 20.1% | $2.3240 | 2000/2000 |
| in_sample | inflate | none | 60.0% | $3.0674 | 60.0% | 59.1% – 60.9% | 7.1% | $4.2070 | 2000/2000 |
| in_sample | inflate | none | 70.0% | $2.6292 | 70.0% | 68.9% – 71.1% | 12.5% | $4.6452 | 2000/2000 |
| in_sample | inflate | none | 80.0% | $2.3006 | 80.0% | 78.8% – 81.2% | 19.9% | $4.9739 | 2000/2000 |
| in_sample | inflate | p99 | 60.0% | $3.0548 | 60.0% | 59.1% – 60.9% | 7.1% | $1.5603 | 2000/2000 |
| in_sample | inflate | p99 | 70.0% | $2.6184 | 70.0% | 69.0% – 71.0% | 12.8% | $1.9967 | 2000/2000 |
| in_sample | inflate | p99 | 80.0% | $2.2911 | 80.0% | 78.8% – 81.2% | 20.1% | $2.3240 | 2000/2000 |
| holdout | exclude | none | 60.0% | $3.0661 | 60.0% | 59.0% – 61.1% | 6.8% | $4.2083 | 445/1551 |
| holdout | exclude | none | 70.0% | $2.6281 | 70.0% | 68.8% – 71.3% | 11.9% | $4.6464 | 445/1551 |
| holdout | exclude | none | 80.0% | $2.2996 | 80.0% | 78.7% – 81.4% | 19.4% | $4.9749 | 445/1551 |
| holdout | exclude | p99 | 60.0% | $3.0553 | 59.9% | 58.9% – 60.9% | 6.8% | $1.3670 | 445/1551 |
| holdout | exclude | p99 | 70.0% | $2.6189 | 69.9% | 68.7% – 71.0% | 12.1% | $1.8035 | 445/1551 |
| holdout | exclude | p99 | 80.0% | $2.2915 | 79.8% | 78.6% – 81.2% | 19.6% | $2.1308 | 445/1551 |
| holdout | inflate | none | 60.0% | $3.0661 | 60.0% | 59.0% – 61.1% | 6.8% | $4.2083 | 445/1551 |
| holdout | inflate | none | 70.0% | $2.6281 | 70.0% | 68.8% – 71.3% | 11.9% | $4.6464 | 445/1551 |
| holdout | inflate | none | 80.0% | $2.2996 | 80.0% | 78.7% – 81.4% | 19.4% | $4.9749 | 445/1551 |
| holdout | inflate | p99 | 60.0% | $3.0553 | 59.9% | 58.9% – 60.9% | 6.8% | $1.3670 | 445/1551 |
| holdout | inflate | p99 | 70.0% | $2.6189 | 69.9% | 68.7% – 71.0% | 12.1% | $1.8035 | 445/1551 |
| holdout | inflate | p99 | 80.0% | $2.2915 | 79.8% | 78.6% – 81.2% | 19.6% | $2.1308 | 445/1551 |
| grouped_cv | exclude | none | 60.0% | $3.0674 | 60.0% | 54.7% – 65.8% | 6.9% | $4.2166 | 1600/2000 |
| grouped_cv | exclude | none | 70.0% | $2.6292 | 70.0% | 63.9% – 76.7% | 12.5% | $4.6534 | 1600/2000 |
| grouped_cv | exclude | none | 80.0% | $2.3006 | 80.0% | 73.0% – 87.7% | 19.9% | $4.9811 | 1600/2000 |
| grouped_cv | exclude | p99 | 60.0% | $3.0545 | 60.0% | 54.8% – 65.4% | 7.0% | $1.6206 | 1600/2000 |
| grouped_cv | exclude | p99 | 70.0% | $2.6181 | 70.0% | 64.0% – 76.3% | 12.7% | $2.0555 | 1600/2000 |
| grouped_cv | exclude | p99 | 80.0% | $2.2909 | 80.0% | 73.1% – 87.2% | 20.2% | $2.3854 | 1600/2000 |
| grouped_cv | inflate | none | 60.0% | $3.0674 | 60.0% | 54.7% – 65.8% | 6.9% | $4.2166 | 1600/2000 |
| grouped_cv | inflate | none | 70.0% | $2.6292 | 70.0% | 63.9% – 76.7% | 12.5% | $4.6534 | 1600/2000 |
| grouped_cv | inflate | none | 80.0% | $2.3006 | 80.0% | 73.0% – 87.7% | 19.9% | $4.9811 | 1600/2000 |
| grouped_cv | inflate | p99 | 60.0% | $3.0545 | 60.0% | 54.8% – 65.4% | 7.0% | $1.6206 | 1600/2000 |
| grouped_cv | inflate | p99 | 70.0% | $2.6181 | 70.0% | 64.0% – 76.3% | 12.7% | $2.0555 | 1600/2000 |
| grouped_cv | inflate | p99 | 80.0% | $2.2909 | 80.0% | 73.1% – 87.2% | 20.2% | $2.3854 | 1600/2000 |
| leave_one_run_out | exclude | none | 60.0% | $3.0674 | 60.0% | 57.4% – 62.1% | 7.0% | $4.2182 | 1500/2000 |
| leave_one_run_out | exclude | none | 70.0% | $2.6292 | 70.0% | 67.0% – 72.4% | 12.6% | $4.6548 | 1500/2000 |
| leave_one_run_out | exclude | none | 80.0% | $2.3006 | 80.0% | 76.6% – 82.8% | 19.8% | $4.9822 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 60.0% | $3.0541 | 60.0% | 57.6% – 61.8% | 7.1% | $1.6117 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 70.0% | $2.6178 | 70.0% | 67.2% – 72.1% | 12.8% | $2.0480 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 80.0% | $2.2906 | 80.0% | 76.8% – 82.4% | 20.0% | $2.3752 | 1500/2000 |
| leave_one_run_out | inflate | none | 60.0% | $3.0674 | 60.0% | 57.4% – 62.1% | 7.0% | $4.2182 | 1500/2000 |
| leave_one_run_out | inflate | none | 70.0% | $2.6292 | 70.0% | 67.0% – 72.4% | 12.6% | $4.6548 | 1500/2000 |
| leave_one_run_out | inflate | none | 80.0% | $2.3006 | 80.0% | 76.6% – 82.8% | 19.8% | $4.9822 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 60.0% | $3.0541 | 60.0% | 57.6% – 61.8% | 7.1% | $1.6117 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 70.0% | $2.6178 | 70.0% | 67.2% – 72.1% | 12.8% | $2.0480 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 80.0% | $2.2906 | 80.0% | 76.8% – 82.4% | 20.0% | $2.3752 | 1500/2000 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $3.0674 | 60.0% | 54.7% – 65.8% | 6.9% | $4.2166 | 1600/2000 |
| grouped_cv | exclude | none | 70.0% | $2.6292 | 70.0% | 63.9% – 76.7% | 12.5% | $4.6534 | 1600/2000 |
| grouped_cv | exclude | none | 80.0% | $2.3006 | 80.0% | 73.0% – 87.7% | 19.9% | $4.9811 | 1600/2000 |
| grouped_cv | exclude | p99 | 60.0% | $3.0545 | 60.0% | 54.8% – 65.4% | 7.0% | $1.6206 | 1600/2000 |
| grouped_cv | exclude | p99 | 70.0% | $2.6181 | 70.0% | 64.0% – 76.3% | 12.7% | $2.0555 | 1600/2000 |
| grouped_cv | exclude | p99 | 80.0% | $2.2909 | 80.0% | 73.1% – 87.2% | 20.2% | $2.3854 | 1600/2000 |
| grouped_cv | inflate | none | 60.0% | $3.0674 | 60.0% | 54.7% – 65.8% | 6.9% | $4.2166 | 1600/2000 |
| grouped_cv | inflate | none | 70.0% | $2.6292 | 70.0% | 63.9% – 76.7% | 12.5% | $4.6534 | 1600/2000 |
| grouped_cv | inflate | none | 80.0% | $2.3006 | 80.0% | 73.0% – 87.7% | 19.9% | $4.9811 | 1600/2000 |
| grouped_cv | inflate | p99 | 60.0% | $3.0545 | 60.0% | 54.8% – 65.4% | 7.0% | $1.6206 | 1600/2000 |
| grouped_cv | inflate | p99 | 70.0% | $2.6181 | 70.0% | 64.0% – 76.3% | 12.7% | $2.0555 | 1600/2000 |
| grouped_cv | inflate | p99 | 80.0% | $2.2909 | 80.0% | 73.1% – 87.2% | 20.2% | $2.3854 | 1600/2000 |
| holdout | exclude | none | 60.0% | $3.0661 | 60.0% | 59.0% – 61.1% | 6.8% | $4.2083 | 445/1551 |
| holdout | exclude | none | 70.0% | $2.6281 | 70.0% | 68.8% – 71.3% | 11.9% | $4.6464 | 445/1551 |
| holdout | exclude | none | 80.0% | $2.2996 | 80.0% | 78.7% – 81.4% | 19.4% | $4.9749 | 445/1551 |
| holdout | exclude | p99 | 60.0% | $3.0553 | 59.9% | 58.9% – 60.9% | 6.8% | $1.3670 | 445/1551 |
| holdout | exclude | p99 | 70.0% | $2.6189 | 69.9% | 68.7% – 71.0% | 12.1% | $1.8035 | 445/1551 |
| holdout | exclude | p99 | 80.0% | $2.2915 | 79.8% | 78.6% – 81.2% | 19.6% | $2.1308 | 445/1551 |
| holdout | inflate | none | 60.0% | $3.0661 | 60.0% | 59.0% – 61.1% | 6.8% | $4.2083 | 445/1551 |
| holdout | inflate | none | 70.0% | $2.6281 | 70.0% | 68.8% – 71.3% | 11.9% | $4.6464 | 445/1551 |
| holdout | inflate | none | 80.0% | $2.2996 | 80.0% | 78.7% – 81.4% | 19.4% | $4.9749 | 445/1551 |
| holdout | inflate | p99 | 60.0% | $3.0553 | 59.9% | 58.9% – 60.9% | 6.8% | $1.3670 | 445/1551 |
| holdout | inflate | p99 | 70.0% | $2.6189 | 69.9% | 68.7% – 71.0% | 12.1% | $1.8035 | 445/1551 |
| holdout | inflate | p99 | 80.0% | $2.2915 | 79.8% | 78.6% – 81.2% | 19.6% | $2.1308 | 445/1551 |
| in_sample | exclude | none | 60.0% | $3.0674 | 60.0% | 59.1% – 60.9% | 7.1% | $4.2070 | 2000/2000 |
| in_sample | exclude | none | 70.0% | $2.6292 | 70.0% | 68.9% – 71.1% | 12.5% | $4.6452 | 2000/2000 |
| in_sample | exclude | none | 80.0% | $2.3006 | 80.0% | 78.8% – 81.2% | 19.9% | $4.9739 | 2000/2000 |
| in_sample | exclude | p99 | 60.0% | $3.0548 | 60.0% | 59.1% – 60.9% | 7.1% | $1.5603 | 2000/2000 |
| in_sample | exclude | p99 | 70.0% | $2.6184 | 70.0% | 69.0% – 71.0% | 12.8% | $1.9967 | 2000/2000 |
| in_sample | exclude | p99 | 80.0% | $2.2911 | 80.0% | 78.8% – 81.2% | 20.1% | $2.3240 | 2000/2000 |
| in_sample | inflate | none | 60.0% | $3.0674 | 60.0% | 59.1% – 60.9% | 7.1% | $4.2070 | 2000/2000 |
| in_sample | inflate | none | 70.0% | $2.6292 | 70.0% | 68.9% – 71.1% | 12.5% | $4.6452 | 2000/2000 |
| in_sample | inflate | none | 80.0% | $2.3006 | 80.0% | 78.8% – 81.2% | 19.9% | $4.9739 | 2000/2000 |
| in_sample | inflate | p99 | 60.0% | $3.0548 | 60.0% | 59.1% – 60.9% | 7.1% | $1.5603 | 2000/2000 |
| in_sample | inflate | p99 | 70.0% | $2.6184 | 70.0% | 69.0% – 71.0% | 12.8% | $1.9967 | 2000/2000 |
| in_sample | inflate | p99 | 80.0% | $2.2911 | 80.0% | 78.8% – 81.2% | 20.1% | $2.3240 | 2000/2000 |
| leave_one_run_out | exclude | none | 60.0% | $3.0674 | 60.0% | 57.4% – 62.1% | 7.0% | $4.2182 | 1500/2000 |
| leave_one_run_out | exclude | none | 70.0% | $2.6292 | 70.0% | 67.0% – 72.4% | 12.6% | $4.6548 | 1500/2000 |
| leave_one_run_out | exclude | none | 80.0% | $2.3006 | 80.0% | 76.6% – 82.8% | 19.8% | $4.9822 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 60.0% | $3.0541 | 60.0% | 57.6% – 61.8% | 7.1% | $1.6117 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 70.0% | $2.6178 | 70.0% | 67.2% – 72.1% | 12.8% | $2.0480 | 1500/2000 |
| leave_one_run_out | exclude | p99 | 80.0% | $2.2906 | 80.0% | 76.8% – 82.4% | 20.0% | $2.3752 | 1500/2000 |
| leave_one_run_out | inflate | none | 60.0% | $3.0674 | 60.0% | 57.4% – 62.1% | 7.0% | $4.2182 | 1500/2000 |
| leave_one_run_out | inflate | none | 70.0% | $2.6292 | 70.0% | 67.0% – 72.4% | 12.6% | $4.6548 | 1500/2000 |
| leave_one_run_out | inflate | none | 80.0% | $2.3006 | 80.0% | 76.6% – 82.8% | 19.8% | $4.9822 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 60.0% | $3.0541 | 60.0% | 57.6% – 61.8% | 7.1% | $1.6117 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 70.0% | $2.6178 | 70.0% | 67.2% – 72.1% | 12.8% | $2.0480 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 80.0% | $2.2906 | 80.0% | 76.8% – 82.4% | 20.0% | $2.3752 | 1500/2000 |

### code · success-only billing

| Scope | Censoring | Cap | Target | Mean fold price / success | Loss ratio | 90% CI | Tasks losing | Worst loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $4.7752 | 60.0% | 48.1% – 76.1% | 36.0% | $7.2350 |
| grouped_cv | exclude | none | 65.0% | $4.4079 | 65.0% | 52.2% – 82.4% | 36.1% | $7.2350 |
| grouped_cv | exclude | none | 70.0% | $4.0930 | 70.0% | 56.2% – 88.8% | 36.4% | $7.2350 |
| grouped_cv | exclude | none | 80.0% | $3.5814 | 80.0% | 64.2% – 101.5% | 37.2% | $7.2350 |
| grouped_cv | exclude | p99 | 60.0% | $4.7793 | 60.0% | 48.1% – 76.3% | 36.1% | $4.7044 |
| grouped_cv | exclude | p99 | 65.0% | $4.4116 | 65.0% | 52.1% – 82.6% | 36.1% | $4.7044 |
| grouped_cv | exclude | p99 | 70.0% | $4.0965 | 70.0% | 56.1% – 89.0% | 36.4% | $4.7044 |
| grouped_cv | exclude | p99 | 80.0% | $3.5845 | 80.0% | 64.1% – 101.7% | 37.2% | $4.7044 |
| grouped_cv | inflate | none | 60.0% | $4.7752 | 60.0% | 48.1% – 76.1% | 36.0% | $7.2350 |
| grouped_cv | inflate | none | 65.0% | $4.4079 | 65.0% | 52.2% – 82.4% | 36.1% | $7.2350 |
| grouped_cv | inflate | none | 70.0% | $4.0930 | 70.0% | 56.2% – 88.8% | 36.4% | $7.2350 |
| grouped_cv | inflate | none | 80.0% | $3.5814 | 80.0% | 64.2% – 101.5% | 37.2% | $7.2350 |
| grouped_cv | inflate | p99 | 60.0% | $4.7793 | 60.0% | 48.1% – 76.3% | 36.1% | $4.7044 |
| grouped_cv | inflate | p99 | 65.0% | $4.4116 | 65.0% | 52.1% – 82.6% | 36.1% | $4.7044 |
| grouped_cv | inflate | p99 | 70.0% | $4.0965 | 70.0% | 56.1% – 89.0% | 36.4% | $4.7044 |
| grouped_cv | inflate | p99 | 80.0% | $3.5845 | 80.0% | 64.1% – 101.7% | 37.2% | $4.7044 |
| leave_one_run_out | exclude | none | 60.0% | $4.7748 | 60.0% | 56.4% – 62.9% | 36.0% | $7.2350 |
| leave_one_run_out | exclude | none | 65.0% | $4.4076 | 65.0% | 61.1% – 68.1% | 36.1% | $7.2350 |
| leave_one_run_out | exclude | none | 70.0% | $4.0927 | 70.0% | 65.8% – 73.4% | 36.4% | $7.2350 |
| leave_one_run_out | exclude | none | 80.0% | $3.5811 | 80.0% | 75.2% – 83.9% | 37.1% | $7.2350 |
| leave_one_run_out | exclude | p99 | 60.0% | $4.7791 | 60.0% | 56.7% – 62.8% | 36.1% | $4.6660 |
| leave_one_run_out | exclude | p99 | 65.0% | $4.4115 | 65.0% | 61.4% – 68.1% | 36.1% | $4.6660 |
| leave_one_run_out | exclude | p99 | 70.0% | $4.0964 | 70.0% | 66.2% – 73.3% | 36.4% | $4.6660 |
| leave_one_run_out | exclude | p99 | 80.0% | $3.5843 | 80.0% | 75.6% – 83.8% | 37.1% | $4.6660 |
| leave_one_run_out | inflate | none | 60.0% | $4.7748 | 60.0% | 56.4% – 62.9% | 36.0% | $7.2350 |
| leave_one_run_out | inflate | none | 65.0% | $4.4076 | 65.0% | 61.1% – 68.1% | 36.1% | $7.2350 |
| leave_one_run_out | inflate | none | 70.0% | $4.0927 | 70.0% | 65.8% – 73.4% | 36.4% | $7.2350 |
| leave_one_run_out | inflate | none | 80.0% | $3.5811 | 80.0% | 75.2% – 83.9% | 37.1% | $7.2350 |
| leave_one_run_out | inflate | p99 | 60.0% | $4.7791 | 60.0% | 56.7% – 62.8% | 36.1% | $4.6660 |
| leave_one_run_out | inflate | p99 | 65.0% | $4.4115 | 65.0% | 61.4% – 68.1% | 36.1% | $4.6660 |
| leave_one_run_out | inflate | p99 | 70.0% | $4.0964 | 70.0% | 66.2% – 73.3% | 36.4% | $4.6660 |
| leave_one_run_out | inflate | p99 | 80.0% | $3.5843 | 80.0% | 75.6% – 83.8% | 37.1% | $4.6660 |

### Success-only billing · highest viable target

| Type | Per-task price at 70% (all tasks billed) | Highest viable success-only target | Price per resolved task at that target | Why none |
| --- | --- | --- | --- | --- |
| code | $2.6181 | 70.0% | $4.0965 | — |

### code · fold fits at 70% target with cap

| Scope | Billing | Censoring | Fold | Train/test groups | Price | Cap | Score loss ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | all_tasks | exclude | 1 | 400/100 | $2.6256 | $4.5694 | 69.0% |
| grouped_cv | all_tasks | exclude | 2 | 400/100 | $2.6094 | $4.6281 | 71.3% |
| grouped_cv | all_tasks | exclude | 3 | 400/100 | $2.6112 | $4.4232 | 70.7% |
| grouped_cv | all_tasks | exclude | 4 | 400/100 | $2.5942 | $4.4400 | 73.0% |
| grouped_cv | all_tasks | exclude | 5 | 400/100 | $2.6503 | $4.6659 | 66.0% |
| grouped_cv | all_tasks | inflate | 1 | 400/100 | $2.6256 | $4.5694 | 69.0% |
| grouped_cv | all_tasks | inflate | 2 | 400/100 | $2.6094 | $4.6281 | 71.3% |
| grouped_cv | all_tasks | inflate | 3 | 400/100 | $2.6112 | $4.4232 | 70.7% |
| grouped_cv | all_tasks | inflate | 4 | 400/100 | $2.5942 | $4.4400 | 73.0% |
| grouped_cv | all_tasks | inflate | 5 | 400/100 | $2.6503 | $4.6659 | 66.0% |
| leave_one_run_out | all_tasks | exclude | 1 | 500/500 | $2.6180 | $4.6462 | 70.2% |
| leave_one_run_out | all_tasks | exclude | 2 | 500/500 | $2.6080 | $4.3936 | 70.8% |
| leave_one_run_out | all_tasks | exclude | 3 | 500/500 | $2.6075 | $4.5095 | 71.1% |
| leave_one_run_out | all_tasks | exclude | 4 | 500/500 | $2.6379 | $4.5694 | 67.9% |
| leave_one_run_out | all_tasks | inflate | 1 | 500/500 | $2.6180 | $4.6462 | 70.2% |
| leave_one_run_out | all_tasks | inflate | 2 | 500/500 | $2.6080 | $4.3936 | 70.8% |
| leave_one_run_out | all_tasks | inflate | 3 | 500/500 | $2.6075 | $4.5095 | 71.1% |
| leave_one_run_out | all_tasks | inflate | 4 | 500/500 | $2.6379 | $4.5694 | 67.9% |
| grouped_cv | success_only | exclude | 1 | 400/99 | $4.0918 | $4.5700 | 70.6% |
| grouped_cv | success_only | exclude | 2 | 399/100 | $4.0487 | $4.6288 | 74.2% |
| grouped_cv | success_only | exclude | 3 | 399/100 | $4.0607 | $4.4275 | 73.0% |
| grouped_cv | success_only | exclude | 4 | 399/100 | $4.0819 | $4.4435 | 71.1% |
| grouped_cv | success_only | exclude | 5 | 399/100 | $4.1994 | $4.6705 | 61.9% |
| grouped_cv | success_only | inflate | 1 | 400/99 | $4.0918 | $4.5700 | 70.6% |
| grouped_cv | success_only | inflate | 2 | 399/100 | $4.0487 | $4.6288 | 74.2% |
| grouped_cv | success_only | inflate | 3 | 399/100 | $4.0607 | $4.4275 | 73.0% |
| grouped_cv | success_only | inflate | 4 | 399/100 | $4.0819 | $4.4435 | 71.1% |
| grouped_cv | success_only | inflate | 5 | 399/100 | $4.1994 | $4.6705 | 61.9% |
| leave_one_run_out | success_only | exclude | 1 | 499/499 | $4.0808 | $4.6514 | 71.1% |
| leave_one_run_out | success_only | exclude | 2 | 499/499 | $4.0826 | $4.4007 | 70.8% |
| leave_one_run_out | success_only | exclude | 3 | 499/498 | $4.0845 | $4.5131 | 70.8% |
| leave_one_run_out | success_only | exclude | 4 | 499/499 | $4.1377 | $4.5718 | 67.4% |
| leave_one_run_out | success_only | inflate | 1 | 499/499 | $4.0808 | $4.6514 | 71.1% |
| leave_one_run_out | success_only | inflate | 2 | 499/499 | $4.0826 | $4.4007 | 70.8% |
| leave_one_run_out | success_only | inflate | 3 | 499/498 | $4.0845 | $4.5131 | 70.8% |
| leave_one_run_out | success_only | inflate | 4 | 499/499 | $4.1377 | $4.5718 | 67.4% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-f3153c387e440744c7518bab441d233465fcf46df23c6da8dc9ed6ca17987b74 · fixed $2.6184 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 2 | $0.0325 |
| read | 5 | $0.0619 |
| run | 24 | $0.3286 |
| edit | 8 | $0.1749 |
| finish | 1 | $0.0213 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-ff5ce3a9750bd2f503ab43ac2e855425a7e605ae983bb470bb4aca99bab7e5e4 · fixed $2.6184 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 4 | $0.0881 |
| run | 43 | $0.7813 |
| read | 13 | $0.1780 |
| edit | 9 | $0.2735 |
| finish | 1 | $0.0286 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-b2e4ce967b5828f469bc30c21763af627e24c50bbf368751023b2ff833a28cfd · fixed $2.6184 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 9 | $0.1547 |
| run | 44 | $0.7792 |
| read | 13 | $0.1979 |
| edit | 16 | $0.4993 |
| finish | 1 | $0.0321 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-f158164b68efdf841aae944e065913ec4d9fa87e3be977f0d363d74d73a2ceab · fixed $2.6184 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 7 | $0.2118 |
| run | 49 | $1.0155 |
| read | 23 | $0.3338 |
| edit | 16 | $0.5230 |
| finish | 1 | $0.0639 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-bcc7011373ad125069f6846365cca78c00acd33529a0868ac4c52577e1c8cae3 · fixed $2.6184 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 2 | $0.0497 |
| run | 116 | $3.8941 |
| read | 50 | $1.2652 |
| edit | 43 | $2.0020 |
| finish | 1 | $0.0634 |
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

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:38:09.580306+00:00. No network requests are required to view this file.

# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

2000 tasks. Price catalog 2026-10-23.1 · SHA-256 74182d05619a62951c47e44eb2c2222f86f1bf516325820588970e093abe012b.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Selected full Bai archives: 1. The repository contains additional model archives.

Task groups: 2000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 2000 records. Fields read: action, args, error, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Bai et al.; final output.jsonl task histories in claude-sonnet-3.7_4runs.tar.gz; intermediate critic attempts and other model archives excluded. Costs describe retained final trajectories, not all evaluation/retry overhead. Resolution is joined by run and instance_id from the SWE-bench Verified report.json results in the archive.

## Summary verdicts

REPRICING CHECK FAILED. Verdicts below describe standard-rate token costs, not validated recorded billing. Review the reconciliation discrepancy in Cost audit before using these prices.

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2025-04-09T13:59:59.100976+00:00; 0 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $1,474.9991. Overall distribution weights each of 1 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 100 iterations for 2000 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 2000 | 27 | 0 | VIABLE | grouped_cv: upper loss-ratio interval stays below 90% at the 70% target with p99 cap |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 2000 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

### code · grouped CV vs time split

| Censoring | Cap | Target | Grouped CV loss ratio | Held-out fold 90% CI (verdict) | Pooled 90% CI | Tasks losing | Worst loss | Leave-one-run-out loss ratio | Leave-one-run-out held-out 90% CI | Time split (leaks repeated tasks) loss ratio | Time split 90% CI | Difference: time split − grouped CV | Difference: upper CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exclude | none | 60.0% | 60.0% | 52.8% – 68.1% | 59.9% – 60.1% | 13.2% | $2.5693 | 60.0% | 57.2% – 63.0% | 58.9% | 56.8% – 60.9% | -1.1% | -7.2% |
| exclude | none | 70.0% | 70.0% | 61.6% – 79.4% | 69.9% – 70.1% | 18.2% | $2.7402 | 70.0% | 66.7% – 73.5% | 68.7% | 66.2% – 71.1% | -1.3% | -8.4% |
| exclude | none | 80.0% | 80.0% | 70.4% – 90.8% | 79.9% – 80.1% | 24.4% | $2.8684 | 80.0% | 76.3% – 84.0% | 78.5% | 75.7% – 81.2% | -1.5% | -9.5% |
| exclude | p99 | 60.0% | 60.0% | 52.9% – 67.8% | 59.9% – 60.0% | 13.3% | $1.4859 | 60.0% | 57.2% – 62.9% | 58.8% | 56.8% – 60.8% | -1.2% | -7.0% |
| exclude | p99 | 70.0% | 70.0% | 61.7% – 79.1% | 69.9% – 70.0% | 18.3% | $1.6562 | 70.0% | 66.8% – 73.3% | 68.6% | 66.3% – 70.9% | -1.4% | -8.2% |
| exclude | p99 | 80.0% | 80.0% | 70.5% – 90.4% | 79.8% – 80.0% | 24.6% | $1.7840 | 80.0% | 76.3% – 83.8% | 78.4% | 75.7% – 81.0% | -1.6% | -9.3% |
| inflate | none | 60.0% | 60.0% | 51.1% – 70.3% | 59.9% – 60.1% | 12.2% | $4.0831 | 60.0% | 56.1% – 64.3% | 58.7% | 56.1% – 61.3% | -1.3% | -9.0% |
| inflate | none | 70.0% | 70.0% | 59.6% – 82.0% | 69.9% – 70.1% | 17.0% | $4.2628 | 70.0% | 65.4% – 75.0% | 68.5% | 65.5% – 71.5% | -1.5% | -10.5% |
| inflate | none | 80.0% | 80.0% | 68.1% – 93.8% | 79.9% – 80.1% | 22.4% | $4.3976 | 80.0% | 74.8% – 85.7% | 78.3% | 74.8% – 81.8% | -1.7% | -12.0% |
| inflate | p99 | 60.0% | 60.1% | 51.5% – 69.4% | 59.7% – 60.2% | 12.8% | $3.2034 | 60.0% | 56.8% – 63.6% | 59.1% | 56.7% – 61.5% | -1.0% | -7.9% |
| inflate | p99 | 70.0% | 70.1% | 60.1% – 81.0% | 69.6% – 70.2% | 17.9% | $3.3797 | 70.0% | 66.3% – 74.2% | 68.9% | 66.1% – 71.7% | -1.2% | -9.2% |
| inflate | p99 | 80.0% | 80.1% | 68.7% – 92.5% | 79.6% – 80.3% | 23.2% | $3.5119 | 80.0% | 75.7% – 84.8% | 78.8% | 75.5% – 82.0% | -1.3% | -10.5% |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 1973 | $0.7156 | $0.5754 | $1.3349 | $2.3600 | $3.7656 | 2.32 | 3.9% | 14.8% |
| Overall · equal type weight | 1973 | $0.7156 | $0.5754 | $1.3353 | $2.3615 | $3.7656 | 2.32 | 3.8% | 14.8% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| code | 2000 | 27 | 1.4% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 39.5%; their spend per task $0.3638; tasks with loop signals 9.2%. Raw dollar totals below are accounting totals.

Repricing acceptance: FAIL. 83 of 88439 recorded-cost calls within 1% (0.1%); 88439 comparable calls (0.1% agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $1,728.2070; standard-rate reprice $1,474.9991; difference $253.2079.

Diagnostic: 88380 of 88380 comparable calls with cache writes match standard cost plus an additional base-input charge on cache-write tokens. This is an observed arithmetic pattern, not proof of its upstream cause. Public rates remain unchanged; this does not count as successful reconciliation.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1201 | 1991/2000 | 60.3% | 2000/1201 | $1.2281 |

### Unknown models

| Provider/model | Calls |
| --- | --- |

No available observations for this table.

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 2 | $0.0187 | $0.0139 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 4 | $0.0125 | $0.0083 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 6 | $0.0053 | $0.0047 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 8 | $0.0067 | $0.0055 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 10 | $0.0065 | $0.0054 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 12 | $0.0084 | $0.0064 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 14 | $0.0096 | $0.0073 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 16 | $0.0079 | $0.0064 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 18 | $0.0181 | $0.0172 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 20 | $0.0107 | $0.0079 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 22 | $0.0116 | $0.0107 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 24 | $0.0157 | $0.0132 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 26 | $0.0108 | $0.0083 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 28 | $0.0174 | $0.0167 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 30 | $0.0155 | $0.0110 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 32 | $0.0187 | $0.0178 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 34 | $0.0135 | $0.0102 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 36 | $0.0090 | $0.0082 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 38 | $0.0121 | $0.0095 |
| task-96129a81d3c3e7b4d8092f73b6058e3293754b0abe83cbb354eb9035c4fe914e | 40 | $0.0080 | $0.0074 |

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| code | $1,474.9991 | $727.5080 | $63.0752 | 184 | 100.00 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-053f0decb8bba16d38bf9238142972379007ec527fe00d33fc8cdde895b4dd1f | $3.7656 | complete | fail | False |
| task-9a69cd74100ab47799721a59e53b77a7d2114d088cc12cf471419464690b9768 | $3.4755 | complete | fail | False |
| task-c0ac425310c28e11b66bf017875553d83641bad7e29c3e45403019eae4407d46 | $3.2951 | complete | fail | False |
| task-ab7c2b07fb62dd62f1efd272e73a4f3336ac054c0f9b9593bdadbcefb62dffd5 | $3.2298 | complete | fail | True |
| task-090fd56b6552ceaa7c99e1a438718f00cb01449c14c9252b32a45e12f46f334e | $3.0090 | complete | fail | False |
| task-02433be349de2be3ba936c10eeb5da4ca62092a3845650eefc184372941f036a | $3.0010 | complete | fail | False |
| task-ad655ad37588db92bf24ef733f698c1c29f695ab534a3738414159e5dd12bc31 | $2.9908 | complete | fail | False |
| task-572926a6081a762bb616f342904cf5985853c16c5a388e0bdaa28b44861d1466 | $2.9525 | complete | fail | True |
| task-4fc52c25f90220fbc14896e0faafc747f4048a30091d99cdc2ca44fd052292e5 | $2.8990 | complete | fail | False |
| task-70190637708f6f3fc5e34919affd9434bdcd1b2ae99623cb66347b5716689a72 | $2.7736 | complete | fail | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-970c397a7ac9395a0100956de91e6e1f999d094de74abcf4581fe339721aa9e8 | run × 4 | 79 | False | $1.7102 |
| task-3a90bc3ca011576d65bc65b9273b04c6bb3a9dc75ef080c1f179b77197f4c779 | run × 3 | 73 | False | $1.2687 |
| task-e6be53751593bf1d8ef7467c3350924651b80b98fd2e5876394925756877bbf6 | run × 3 | 55 | False | $1.0835 |
| task-70bb62636dd8b3f7b362cd2d1e413355cbe47dce63304e13fbf0013963cdc2f8 | run × 3 | 61 | False | $0.6810 |
| task-8bbd24e2f4121672327f200787bbae4ee012edb67c27c5825a9cfa85d67e3906 | run × 3 | 49 | False | $0.6787 |
| task-5cb084efeb83cbb7dad3ae8be3a973afe1626a72ee04f5532519a1c47a9fcb6c | run × 3 | 58 | False | $1.0077 |
| task-6a971856b38f9e02666a495a296a2b982400c35799e7b8a4e1dfea07b815f213 | run × 3 | 30 | False | $0.2806 |
| task-769595262b04abd3895b0800b70f17d4e6e7181b0e4d53cbb6fd5edf33face55 | run × 3 | 59 | False | $0.8985 |
| task-6bfffb29b276209ed424d04c28adf7e054e70a10cf011a088ebecca7e623ec06 | run × 3 | 89 | False | $1.5786 |
| task-e1ab1bf455b02f325db6184a6a909d853f110165f6e0eff5e85469fbdd1fb4c8 | run × 3 | 94 | False | $2.3301 |
| task-bd56fea39e6019e812f40a0626b1d8197323c0dd4f1511d67e7c0a07402357e5 | run × 3 | 75 | False | $0.9733 |
| task-36787a8c320c25df7450113f2633e0c34cb89d206f1965916cca73b786b2382f | run × 5; run × 3 | 94 | False | $2.3709 |
| task-4c843f458491ce8f97beb7b1601685de7e8a2c5aea549569522f27006d10babb | run × 4 | 91 | False | $1.7434 |
| task-bebe8672878f96cb80b698879702af22ee4a84e35ed599a9aa3cc6510d9b9540 | run × 3 | 45 | False | $0.6972 |
| task-0ad76f915ed12444f059aae7f139f572c2f04a819b58f5040594b4d58c008242 | run × 3 | 37 | False | $0.5210 |
| task-dbe69d277adff6c1d1b1975e411251352f67a0fdb56392737d930c06db0c90e8 | run × 3 | 85 | False | $1.3595 |
| task-42a3dd0968386b9cf1edd717e3652acf2fdeed5672ffe8b906d1b5f938f10348 | run × 4 | 89 | False | $1.4031 |
| task-cd881ca85fdf0af04473cedb11c14278eecc4505d6c0c0e5a3e35f208226cce9 | run × 5 | 49 | False | $0.6022 |
| task-fdd968b1ccf46547dc1026c402a861fbed24a8893bee16bd297bc2142b678a40 | run × 6 | 81 | False | $1.7318 |
| task-3a2ba173c9cdcd6b0a004974671b02430a46d07747c32631f37980966f855754 | run × 3 | 60 | False | $1.2566 |
| task-6058040d8ee71c29e20a431e81b4a4b8e5695fb404aa82200d1206e3eabe91ca | run × 4 | 55 | False | $1.0960 |
| task-9d63ebaf7829ca253fa723e7e789de250ca4e69ee276b20855e54fbe646901ea | run × 3 | 100 | False | $2.0151 |
| task-495fe85ada0484e5974cd5fc8c07e542fc769ef285fabf99f06f91a843334aac | run × 3 | 53 | False | $0.7040 |
| task-2f7635155133b0527c2ecaefba190d34fa3275c02b2be2e359d6c5d3028f3c0d | run × 3 | 53 | False | $0.7449 |
| task-4e8502a2820e9cf997f9f5ac86257a3bc494c67e15fbfe2d2503c8836815d6d4 | run × 3 | 46 | False | $0.8445 |
| task-61db514bdce607d26017d2fc5a8b35f163cb2baa5a7de6bb9e65fb88b88c35af | run × 3 | 41 | False | $0.6367 |
| task-3a0f5c60fb8f00e93026c2120f0db912ec298128c076d96b2c24319dfcf28886 | run × 3 | 69 | False | $1.1751 |
| task-e9cc170eda0cef75d366a11977b3f896f9cfa589771861ddbe57ef3833d7f6dd | run × 3 | 41 | False | $0.5525 |
| task-1f2e665e4d30c4d5892e7d2b3de62369dc44727d4ed9a24ba47180e5e20c1001 | run × 4 | 73 | False | $1.7605 |
| task-89fa99b34d1fa74dad618c318adad4c88a8242121e2aee6cb6d0e3bd700fde48 | run × 3 | 42 | False | $0.9818 |
| task-f7e44986bcaa35383cc5409c5f9c1f47939ca991552972b91d92ab7f69a6bcaa | run × 3 | 41 | False | $0.5222 |
| task-4c4a33e906b789b2c03d5d570beaf3bb7496f327f476478d7795445a7360b170 | run × 3 | 40 | False | $0.4847 |
| task-2cfc889aa8da3a3e4ce9a1979d39293cae24c0e567bf5a15ac569d2b13a2e044 | run × 4 | 87 | False | $1.7728 |
| task-8701da632dd1f29aade5fc74899bfbdfc90d2e2018abe8a4c2bf5a56455693b5 | run × 5 | 79 | False | $1.6210 |
| task-547faad31771c45f6a25527b1893424a7cd05a88b997f26f6291b8c681e65f34 | run × 5 | 100 | False | $2.1451 |
| task-41b8465f6d581dbd5165c042c32d6ffb6047b6da616dc3eda00ff481d8a2a8f9 | run × 7 | 75 | False | $1.3772 |
| task-a9762167a5664ef1583b166a4f33d9fd74a74b693e75c1a5cb9028ec4417dcfd | run × 3 | 83 | False | $1.9297 |
| task-572926a6081a762bb616f342904cf5985853c16c5a388e0bdaa28b44861d1466 | run × 3 | 100 | False | $2.9525 |
| task-8b1d93a14cd973e4ad05685f6f731168bc8653647c68e5546e050f731eb8a3ea | run × 4; run × 3 | 57 | False | $0.9209 |
| task-e41a2f999f6332371d96da1d170205eff50a592a4c0023905adb832adb642a02 | run × 5 | 84 | False | $1.9061 |
| task-b7b7b06ed0e874a7f63eed382daaad4c8d43df19603d55d65eb1c267d3e8cfdf | run × 4 | 68 | False | $1.1301 |
| task-d6342edebdf53a4688d994604d3cf5001b4fe493bbb553fad43afecd31286261 | run × 3 | 71 | False | $1.4367 |
| task-5aff52a46cdd52571d82deb21f21bfd60e4bf82f5caeebdf9af1076d79c4987c | run × 3 | 61 | False | $1.2041 |
| task-0a762cc178df58145ca1d7d795926e0d9cda6bab59a79925808a4da5c4f356e3 | run × 3 | 49 | False | $0.7272 |
| task-ec679acca85289a92eca6556d5f84286a629bac70261881c9c7a153896add1ec | run × 4 | 73 | False | $1.2656 |
| task-6845aab0bcdeb13b3fd06b8c861cbb47d82f9dae1b4830a8e853e0dbec48ef9a | run × 3; run × 3 | 96 | False | $2.0475 |
| task-44b5344dd573507c6c1c78d7a1b3298bbf37b00811f2bba79c969124c62c6654 | read × 3 | 89 | False | $1.5057 |
| task-77b50ab73072d04187f5c8205cb1cbbcb16a7725dbcd65614e2b46ae32dfa0fa | run × 4 | 50 | False | $0.7646 |
| task-df4117ae969cb8de15b8d8e68fdc10a4730393353fa1134a14996fb878429c4d | run × 3 | 81 | False | $1.5750 |
| task-6ff8eafa4ec200fac313e1bcd39530b590b1a40b69a7c3485840815752dd6ce0 | run × 4 | 38 | False | $0.6051 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | p95 | $1.7339 | 4.5% | $35.8232 | 2.5% | 5.0% | $37.5015 |
| code | p99 | $2.3600 | 0.7% | $7.2244 | 0.5% | 1.0% | $7.5696 |
| code | p99.5 | $2.5852 | 0.5% | $4.3415 | 0.3% | 0.5% | $4.8002 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 1 | 4.5% | $0.0182 | 2.5% |
| p99 | 1 | 0.7% | $0.0037 | 0.5% |
| p99.5 | 1 | 0.5% | $0.0022 | 0.3% |

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
| in_sample | exclude | none | 60.0% | $1.1927 | 60.0% | 58.5% – 61.4% | 13.1% | $2.5729 | 1973/1973 |
| in_sample | exclude | none | 70.0% | $1.0223 | 70.0% | 68.3% – 71.7% | 18.1% | $2.7433 | 1973/1973 |
| in_sample | exclude | none | 80.0% | $0.8945 | 80.0% | 78.0% – 81.9% | 24.2% | $2.8711 | 1973/1973 |
| in_sample | exclude | p99 | 60.0% | $1.1866 | 60.0% | 58.6% – 61.4% | 13.2% | $1.2183 | 1973/1973 |
| in_sample | exclude | p99 | 70.0% | $1.0171 | 70.0% | 68.3% – 71.6% | 18.3% | $1.3878 | 1973/1973 |
| in_sample | exclude | p99 | 80.0% | $0.8900 | 80.0% | 78.1% – 81.9% | 24.7% | $1.5149 | 1973/1973 |
| in_sample | inflate | none | 60.0% | $1.2767 | 60.0% | 58.2% – 61.8% | 12.2% | $4.0658 | 2000/2000 |
| in_sample | inflate | none | 70.0% | $1.0943 | 70.0% | 67.9% – 72.1% | 16.9% | $4.2482 | 2000/2000 |
| in_sample | inflate | none | 80.0% | $0.9575 | 80.0% | 77.6% – 82.4% | 22.2% | $4.3850 | 2000/2000 |
| in_sample | inflate | p99 | 60.0% | $1.2526 | 60.0% | 58.3% – 61.7% | 12.7% | $3.1858 | 2000/2000 |
| in_sample | inflate | p99 | 70.0% | $1.0737 | 70.0% | 68.1% – 72.0% | 17.8% | $3.3648 | 2000/2000 |
| in_sample | inflate | p99 | 80.0% | $0.9395 | 80.0% | 77.8% – 82.2% | 23.2% | $3.4990 | 2000/2000 |
| holdout | exclude | none | 60.0% | $1.2039 | 58.9% | 56.8% – 60.9% | 12.5% | $2.5617 | 986/987 |
| holdout | exclude | none | 70.0% | $1.0319 | 68.7% | 66.2% – 71.1% | 17.3% | $2.7336 | 986/987 |
| holdout | exclude | none | 80.0% | $0.9030 | 78.5% | 75.7% – 81.2% | 22.3% | $2.8626 | 986/987 |
| holdout | exclude | p99 | 60.0% | $1.1983 | 58.8% | 56.8% – 60.8% | 12.5% | $1.2066 | 986/987 |
| holdout | exclude | p99 | 70.0% | $1.0271 | 68.6% | 66.3% – 70.9% | 17.5% | $1.3778 | 986/987 |
| holdout | exclude | p99 | 80.0% | $0.8987 | 78.4% | 75.7% – 81.0% | 22.4% | $1.5062 | 986/987 |
| holdout | inflate | none | 60.0% | $1.2905 | 58.7% | 56.1% – 61.3% | 11.2% | $4.0501 | 1000/1000 |
| holdout | inflate | none | 70.0% | $1.1062 | 68.5% | 65.5% – 71.5% | 16.1% | $4.2345 | 1000/1000 |
| holdout | inflate | none | 80.0% | $0.9679 | 78.3% | 74.8% – 81.8% | 21.1% | $4.3727 | 1000/1000 |
| holdout | inflate | p99 | 60.0% | $1.2620 | 59.1% | 56.7% – 61.5% | 11.8% | $3.1669 | 1000/1000 |
| holdout | inflate | p99 | 70.0% | $1.0817 | 68.9% | 66.1% – 71.7% | 17.1% | $3.3472 | 1000/1000 |
| holdout | inflate | p99 | 80.0% | $0.9465 | 78.8% | 75.5% – 82.0% | 21.9% | $3.4824 | 1000/1000 |
| grouped_cv | exclude | none | 60.0% | $1.1927 | 60.0% | 52.8% – 68.1% | 13.2% | $2.5693 | 1574/1973 |
| grouped_cv | exclude | none | 70.0% | $1.0223 | 70.0% | 61.6% – 79.4% | 18.2% | $2.7402 | 1574/1973 |
| grouped_cv | exclude | none | 80.0% | $0.8945 | 80.0% | 70.4% – 90.8% | 24.4% | $2.8684 | 1574/1973 |
| grouped_cv | exclude | p99 | 60.0% | $1.1866 | 60.0% | 52.9% – 67.8% | 13.3% | $1.4859 | 1574/1973 |
| grouped_cv | exclude | p99 | 70.0% | $1.0171 | 70.0% | 61.7% – 79.1% | 18.3% | $1.6562 | 1574/1973 |
| grouped_cv | exclude | p99 | 80.0% | $0.8900 | 80.0% | 70.5% – 90.4% | 24.6% | $1.7840 | 1574/1973 |
| grouped_cv | inflate | none | 60.0% | $1.2767 | 60.0% | 51.1% – 70.3% | 12.2% | $4.0831 | 1600/2000 |
| grouped_cv | inflate | none | 70.0% | $1.0943 | 70.0% | 59.6% – 82.0% | 17.0% | $4.2628 | 1600/2000 |
| grouped_cv | inflate | none | 80.0% | $0.9575 | 80.0% | 68.1% – 93.8% | 22.4% | $4.3976 | 1600/2000 |
| grouped_cv | inflate | p99 | 60.0% | $1.2513 | 60.1% | 51.5% – 69.4% | 12.8% | $3.2034 | 1600/2000 |
| grouped_cv | inflate | p99 | 70.0% | $1.0726 | 70.1% | 60.1% – 81.0% | 17.9% | $3.3797 | 1600/2000 |
| grouped_cv | inflate | p99 | 80.0% | $0.9385 | 80.1% | 68.7% – 92.5% | 23.2% | $3.5119 | 1600/2000 |
| leave_one_run_out | exclude | none | 60.0% | $1.1927 | 60.0% | 57.2% – 63.0% | 13.1% | $2.5697 | 1478/1973 |
| leave_one_run_out | exclude | none | 70.0% | $1.0223 | 70.0% | 66.7% – 73.5% | 18.1% | $2.7405 | 1478/1973 |
| leave_one_run_out | exclude | none | 80.0% | $0.8945 | 80.0% | 76.3% – 84.0% | 24.4% | $2.8687 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.1865 | 60.0% | 57.2% – 62.9% | 13.2% | $1.4966 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.0170 | 70.0% | 66.8% – 73.3% | 18.3% | $1.6654 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.8899 | 80.0% | 76.3% – 83.8% | 24.6% | $1.7920 | 1478/1973 |
| leave_one_run_out | inflate | none | 60.0% | $1.2767 | 60.0% | 56.1% – 64.3% | 12.2% | $4.0813 | 1500/2000 |
| leave_one_run_out | inflate | none | 70.0% | $1.0943 | 70.0% | 65.4% – 75.0% | 16.9% | $4.2634 | 1500/2000 |
| leave_one_run_out | inflate | none | 80.0% | $0.9575 | 80.0% | 74.8% – 85.7% | 22.3% | $4.4000 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.2525 | 60.0% | 56.8% – 63.6% | 12.7% | $3.1999 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.0736 | 70.0% | 66.3% – 74.2% | 17.8% | $3.3794 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.9394 | 80.0% | 75.7% – 84.8% | 23.2% | $3.5141 | 1500/2000 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $1.1927 | 60.0% | 52.8% – 68.1% | 13.2% | $2.5693 | 1574/1973 |
| grouped_cv | exclude | none | 70.0% | $1.0223 | 70.0% | 61.6% – 79.4% | 18.2% | $2.7402 | 1574/1973 |
| grouped_cv | exclude | none | 80.0% | $0.8945 | 80.0% | 70.4% – 90.8% | 24.4% | $2.8684 | 1574/1973 |
| grouped_cv | exclude | p99 | 60.0% | $1.1866 | 60.0% | 52.9% – 67.8% | 13.3% | $1.4859 | 1574/1973 |
| grouped_cv | exclude | p99 | 70.0% | $1.0171 | 70.0% | 61.7% – 79.1% | 18.3% | $1.6562 | 1574/1973 |
| grouped_cv | exclude | p99 | 80.0% | $0.8900 | 80.0% | 70.5% – 90.4% | 24.6% | $1.7840 | 1574/1973 |
| grouped_cv | inflate | none | 60.0% | $1.2767 | 60.0% | 51.1% – 70.3% | 12.2% | $4.0831 | 1600/2000 |
| grouped_cv | inflate | none | 70.0% | $1.0943 | 70.0% | 59.6% – 82.0% | 17.0% | $4.2628 | 1600/2000 |
| grouped_cv | inflate | none | 80.0% | $0.9575 | 80.0% | 68.1% – 93.8% | 22.4% | $4.3976 | 1600/2000 |
| grouped_cv | inflate | p99 | 60.0% | $1.2513 | 60.1% | 51.5% – 69.4% | 12.8% | $3.2034 | 1600/2000 |
| grouped_cv | inflate | p99 | 70.0% | $1.0726 | 70.1% | 60.1% – 81.0% | 17.9% | $3.3797 | 1600/2000 |
| grouped_cv | inflate | p99 | 80.0% | $0.9385 | 80.1% | 68.7% – 92.5% | 23.2% | $3.5119 | 1600/2000 |
| holdout | exclude | none | 60.0% | $1.2039 | 58.9% | 56.8% – 60.9% | 12.5% | $2.5617 | 986/987 |
| holdout | exclude | none | 70.0% | $1.0319 | 68.7% | 66.2% – 71.1% | 17.3% | $2.7336 | 986/987 |
| holdout | exclude | none | 80.0% | $0.9030 | 78.5% | 75.7% – 81.2% | 22.3% | $2.8626 | 986/987 |
| holdout | exclude | p99 | 60.0% | $1.1983 | 58.8% | 56.8% – 60.8% | 12.5% | $1.2066 | 986/987 |
| holdout | exclude | p99 | 70.0% | $1.0271 | 68.6% | 66.3% – 70.9% | 17.5% | $1.3778 | 986/987 |
| holdout | exclude | p99 | 80.0% | $0.8987 | 78.4% | 75.7% – 81.0% | 22.4% | $1.5062 | 986/987 |
| holdout | inflate | none | 60.0% | $1.2905 | 58.7% | 56.1% – 61.3% | 11.2% | $4.0501 | 1000/1000 |
| holdout | inflate | none | 70.0% | $1.1062 | 68.5% | 65.5% – 71.5% | 16.1% | $4.2345 | 1000/1000 |
| holdout | inflate | none | 80.0% | $0.9679 | 78.3% | 74.8% – 81.8% | 21.1% | $4.3727 | 1000/1000 |
| holdout | inflate | p99 | 60.0% | $1.2620 | 59.1% | 56.7% – 61.5% | 11.8% | $3.1669 | 1000/1000 |
| holdout | inflate | p99 | 70.0% | $1.0817 | 68.9% | 66.1% – 71.7% | 17.1% | $3.3472 | 1000/1000 |
| holdout | inflate | p99 | 80.0% | $0.9465 | 78.8% | 75.5% – 82.0% | 21.9% | $3.4824 | 1000/1000 |
| in_sample | exclude | none | 60.0% | $1.1927 | 60.0% | 58.5% – 61.4% | 13.1% | $2.5729 | 1973/1973 |
| in_sample | exclude | none | 70.0% | $1.0223 | 70.0% | 68.3% – 71.7% | 18.1% | $2.7433 | 1973/1973 |
| in_sample | exclude | none | 80.0% | $0.8945 | 80.0% | 78.0% – 81.9% | 24.2% | $2.8711 | 1973/1973 |
| in_sample | exclude | p99 | 60.0% | $1.1866 | 60.0% | 58.6% – 61.4% | 13.2% | $1.2183 | 1973/1973 |
| in_sample | exclude | p99 | 70.0% | $1.0171 | 70.0% | 68.3% – 71.6% | 18.3% | $1.3878 | 1973/1973 |
| in_sample | exclude | p99 | 80.0% | $0.8900 | 80.0% | 78.1% – 81.9% | 24.7% | $1.5149 | 1973/1973 |
| in_sample | inflate | none | 60.0% | $1.2767 | 60.0% | 58.2% – 61.8% | 12.2% | $4.0658 | 2000/2000 |
| in_sample | inflate | none | 70.0% | $1.0943 | 70.0% | 67.9% – 72.1% | 16.9% | $4.2482 | 2000/2000 |
| in_sample | inflate | none | 80.0% | $0.9575 | 80.0% | 77.6% – 82.4% | 22.2% | $4.3850 | 2000/2000 |
| in_sample | inflate | p99 | 60.0% | $1.2526 | 60.0% | 58.3% – 61.7% | 12.7% | $3.1858 | 2000/2000 |
| in_sample | inflate | p99 | 70.0% | $1.0737 | 70.0% | 68.1% – 72.0% | 17.8% | $3.3648 | 2000/2000 |
| in_sample | inflate | p99 | 80.0% | $0.9395 | 80.0% | 77.8% – 82.2% | 23.2% | $3.4990 | 2000/2000 |
| leave_one_run_out | exclude | none | 60.0% | $1.1927 | 60.0% | 57.2% – 63.0% | 13.1% | $2.5697 | 1478/1973 |
| leave_one_run_out | exclude | none | 70.0% | $1.0223 | 70.0% | 66.7% – 73.5% | 18.1% | $2.7405 | 1478/1973 |
| leave_one_run_out | exclude | none | 80.0% | $0.8945 | 80.0% | 76.3% – 84.0% | 24.4% | $2.8687 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.1865 | 60.0% | 57.2% – 62.9% | 13.2% | $1.4966 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.0170 | 70.0% | 66.8% – 73.3% | 18.3% | $1.6654 | 1478/1973 |
| leave_one_run_out | exclude | p99 | 80.0% | $0.8899 | 80.0% | 76.3% – 83.8% | 24.6% | $1.7920 | 1478/1973 |
| leave_one_run_out | inflate | none | 60.0% | $1.2767 | 60.0% | 56.1% – 64.3% | 12.2% | $4.0813 | 1500/2000 |
| leave_one_run_out | inflate | none | 70.0% | $1.0943 | 70.0% | 65.4% – 75.0% | 16.9% | $4.2634 | 1500/2000 |
| leave_one_run_out | inflate | none | 80.0% | $0.9575 | 80.0% | 74.8% – 85.7% | 22.3% | $4.4000 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 60.0% | $1.2525 | 60.0% | 56.8% – 63.6% | 12.7% | $3.1999 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.0736 | 70.0% | 66.3% – 74.2% | 17.8% | $3.3794 | 1500/2000 |
| leave_one_run_out | inflate | p99 | 80.0% | $0.9394 | 80.0% | 75.7% – 84.8% | 23.2% | $3.5141 | 1500/2000 |

### code · success-only billing

| Scope | Censoring | Cap | Target | Mean fold price / success | Loss ratio | 90% CI | Tasks losing | Worst loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | exclude | none | 60.0% | $1.9610 | 60.0% | 46.7% – 79.1% | 39.7% | $3.7656 |
| grouped_cv | exclude | none | 65.0% | $1.8101 | 65.0% | 50.6% – 85.7% | 40.3% | $3.7656 |
| grouped_cv | exclude | none | 70.0% | $1.6808 | 70.0% | 54.5% – 92.3% | 40.9% | $3.7656 |
| grouped_cv | exclude | none | 80.0% | $1.4707 | 80.0% | 62.3% – 105.5% | 41.8% | $3.7656 |
| grouped_cv | exclude | p99 | 60.0% | $1.9533 | 59.9% | 46.8% – 79.1% | 39.7% | $2.6782 |
| grouped_cv | exclude | p99 | 65.0% | $1.8030 | 64.9% | 50.7% – 85.7% | 40.3% | $2.6782 |
| grouped_cv | exclude | p99 | 70.0% | $1.6743 | 69.9% | 54.6% – 92.3% | 40.9% | $2.6782 |
| grouped_cv | exclude | p99 | 80.0% | $1.4650 | 79.9% | 62.4% – 105.5% | 41.8% | $2.6782 |
| grouped_cv | inflate | none | 60.0% | $2.1160 | 60.0% | 45.9% – 80.7% | 40.2% | $5.3387 |
| grouped_cv | inflate | none | 65.0% | $1.9533 | 65.0% | 49.7% – 87.4% | 40.5% | $5.3387 |
| grouped_cv | inflate | none | 70.0% | $1.8138 | 70.0% | 53.5% – 94.1% | 41.1% | $5.3387 |
| grouped_cv | inflate | none | 80.0% | $1.5870 | 80.0% | 61.1% – 107.6% | 42.0% | $5.3387 |
| grouped_cv | inflate | p99 | 60.0% | $2.0813 | 60.1% | 45.8% – 80.1% | 40.3% | $4.4346 |
| grouped_cv | inflate | p99 | 65.0% | $1.9212 | 65.1% | 49.6% – 86.8% | 40.8% | $4.4346 |
| grouped_cv | inflate | p99 | 70.0% | $1.7840 | 70.1% | 53.4% – 93.5% | 41.3% | $4.4346 |
| grouped_cv | inflate | p99 | 80.0% | $1.5610 | 80.1% | 61.0% – 106.8% | 42.1% | $4.4346 |
| leave_one_run_out | exclude | none | 60.0% | $1.9608 | 60.0% | 56.2% – 64.2% | 39.8% | $3.7656 |
| leave_one_run_out | exclude | none | 65.0% | $1.8099 | 65.0% | 60.9% – 69.5% | 40.2% | $3.7656 |
| leave_one_run_out | exclude | none | 70.0% | $1.6807 | 70.0% | 65.5% – 74.9% | 40.8% | $3.7656 |
| leave_one_run_out | exclude | none | 80.0% | $1.4706 | 80.0% | 74.9% – 85.6% | 41.6% | $3.7656 |
| leave_one_run_out | exclude | p99 | 60.0% | $1.9533 | 60.1% | 56.3% – 64.1% | 39.8% | $2.6782 |
| leave_one_run_out | exclude | p99 | 65.0% | $1.8031 | 65.1% | 60.9% – 69.4% | 40.3% | $2.6782 |
| leave_one_run_out | exclude | p99 | 70.0% | $1.6743 | 70.1% | 65.6% – 74.8% | 40.9% | $2.6782 |
| leave_one_run_out | exclude | p99 | 80.0% | $1.4650 | 80.1% | 75.0% – 85.4% | 41.6% | $2.6782 |
| leave_one_run_out | inflate | none | 60.0% | $2.1159 | 60.0% | 55.3% – 65.3% | 40.2% | $5.3534 |
| leave_one_run_out | inflate | none | 65.0% | $1.9531 | 65.0% | 59.9% – 70.8% | 40.6% | $5.3534 |
| leave_one_run_out | inflate | none | 70.0% | $1.8136 | 70.0% | 64.5% – 76.2% | 41.1% | $5.3534 |
| leave_one_run_out | inflate | none | 80.0% | $1.5869 | 80.0% | 73.7% – 87.1% | 42.1% | $5.3534 |
| leave_one_run_out | inflate | p99 | 60.0% | $2.0842 | 60.1% | 55.7% – 65.0% | 40.3% | $4.4490 |
| leave_one_run_out | inflate | p99 | 65.0% | $1.9239 | 65.1% | 60.3% – 70.5% | 40.8% | $4.4490 |
| leave_one_run_out | inflate | p99 | 70.0% | $1.7865 | 70.1% | 65.0% – 75.9% | 41.1% | $4.4490 |
| leave_one_run_out | inflate | p99 | 80.0% | $1.5632 | 80.1% | 74.2% – 86.7% | 42.1% | $4.4490 |

### Success-only billing · highest viable target

| Type | Per-task price at 70% (all tasks billed) | Highest viable success-only target | Price per resolved task at that target | Why none |
| --- | --- | --- | --- | --- |
| code | $1.0171 | 65.0% | $1.8030 | — |

### code · fold fits at 70% target with cap

| Scope | Billing | Censoring | Fold | Train/test groups | Price | Cap | Score loss ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grouped_cv | all_tasks | exclude | 1 | 398/100 | $1.0106 | $2.3634 | 72.4% |
| grouped_cv | all_tasks | exclude | 2 | 398/100 | $1.0211 | $2.3060 | 68.4% |
| grouped_cv | all_tasks | exclude | 3 | 399/99 | $1.0185 | $2.3621 | 69.5% |
| grouped_cv | all_tasks | exclude | 4 | 398/100 | $1.0136 | $2.3636 | 71.3% |
| grouped_cv | all_tasks | exclude | 5 | 399/99 | $1.0220 | $2.3635 | 68.4% |
| grouped_cv | all_tasks | inflate | 1 | 400/100 | $1.0577 | $2.3634 | 75.4% |
| grouped_cv | all_tasks | inflate | 2 | 400/100 | $1.0839 | $2.3060 | 64.8% |
| grouped_cv | all_tasks | inflate | 3 | 400/100 | $1.0754 | $2.3621 | 69.5% |
| grouped_cv | all_tasks | inflate | 4 | 400/100 | $1.0704 | $2.3636 | 71.2% |
| grouped_cv | all_tasks | inflate | 5 | 400/100 | $1.0754 | $2.3635 | 69.6% |
| leave_one_run_out | all_tasks | exclude | 1 | 498/492 | $1.0198 | $2.3418 | 69.2% |
| leave_one_run_out | all_tasks | exclude | 2 | 498/495 | $1.0128 | $2.3723 | 71.3% |
| leave_one_run_out | all_tasks | exclude | 3 | 498/495 | $1.0210 | $2.3599 | 68.9% |
| leave_one_run_out | all_tasks | exclude | 4 | 498/491 | $1.0145 | $2.3252 | 70.6% |
| leave_one_run_out | all_tasks | inflate | 1 | 500/500 | $1.0734 | $2.3418 | 70.1% |
| leave_one_run_out | all_tasks | inflate | 2 | 500/500 | $1.0774 | $2.3723 | 69.6% |
| leave_one_run_out | all_tasks | inflate | 3 | 500/500 | $1.0793 | $2.3599 | 68.5% |
| leave_one_run_out | all_tasks | inflate | 4 | 500/500 | $1.0643 | $2.3252 | 71.9% |
| grouped_cv | success_only | exclude | 1 | 397/100 | $1.6622 | $2.3641 | 72.5% |
| grouped_cv | success_only | exclude | 2 | 397/100 | $1.6803 | $2.2939 | 68.8% |
| grouped_cv | success_only | exclude | 3 | 398/99 | $1.6520 | $2.3630 | 74.8% |
| grouped_cv | success_only | exclude | 4 | 397/100 | $1.7006 | $2.3645 | 64.9% |
| grouped_cv | success_only | exclude | 5 | 399/98 | $1.6761 | $2.3638 | 69.5% |
| grouped_cv | success_only | inflate | 1 | 399/100 | $1.7555 | $2.3641 | 76.1% |
| grouped_cv | success_only | inflate | 2 | 399/100 | $1.8050 | $2.2939 | 64.6% |
| grouped_cv | success_only | inflate | 3 | 399/100 | $1.7620 | $2.3630 | 75.0% |
| grouped_cv | success_only | inflate | 4 | 399/100 | $1.8146 | $2.3645 | 65.1% |
| grouped_cv | success_only | inflate | 5 | 400/99 | $1.7826 | $2.3638 | 70.7% |
| leave_one_run_out | success_only | exclude | 1 | 497/490 | $1.6804 | $2.3436 | 69.0% |
| leave_one_run_out | success_only | exclude | 2 | 497/494 | $1.6671 | $2.3728 | 71.2% |
| leave_one_run_out | success_only | exclude | 3 | 497/494 | $1.6807 | $2.3601 | 69.0% |
| leave_one_run_out | success_only | exclude | 4 | 497/486 | $1.6687 | $2.3258 | 71.2% |
| leave_one_run_out | success_only | inflate | 1 | 499/498 | $1.7860 | $2.3436 | 70.1% |
| leave_one_run_out | success_only | inflate | 2 | 499/499 | $1.7925 | $2.3728 | 69.2% |
| leave_one_run_out | success_only | inflate | 3 | 499/499 | $1.7978 | $2.3601 | 68.2% |
| leave_one_run_out | success_only | inflate | 4 | 499/495 | $1.7696 | $2.3258 | 72.8% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### code · task-6c30f97031491c694e8e288e616f41db4d2b1548934fec68c76554df81bee6f3 · fixed $1.0171 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 7 | $0.0536 |
| read | 2 | $0.0151 |
| think | 1 | $0.0091 |
| edit | 1 | $0.0213 |
| finish | 1 | $0.0179 |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-666439e820ad0057535099036e9a04ecd60db923d6b99ffa39bb72f6683156fd · fixed $1.0171 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 24 | $0.2635 |
| read | 4 | $0.0407 |
| edit | 5 | $0.0846 |
| finish | 1 | $0.0186 |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-e530ff09276d6095bf17fd31ee89605cc225eb371137470ccab6b84774265872 · fixed $1.0171 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 29 | $0.3708 |
| read | 7 | $0.0738 |
| edit | 4 | $0.0940 |
| think | 1 | $0.0182 |
| finish | 1 | $0.0215 |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-533ffd66b140fc4d0a626f2f3ef37be814c4bb04cb28aca1e194dd787fa8bba8 · fixed $1.0171 (in_sample) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 33 | $0.4323 |
| read | 18 | $0.1892 |
| edit | 10 | $0.2071 |
| think | 2 | $0.0431 |
| finish | 1 | $0.0261 |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-053f0decb8bba16d38bf9238142972379007ec527fe00d33fc8cdde895b4dd1f · fixed $1.0171 (in_sample) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| run | 39 | $1.5375 |
| read | 19 | $0.2800 |
| edit | 35 | $1.8559 |
| think | 1 | $0.0455 |
| finish | 1 | $0.0468 |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |
| condensation (unlinked tool events) | 1 | — |

## Limits

Bai Appendix B Eq. 1–2 charges (prompt_tokens - cache_read_tokens) at the base input rate, then also charges cache creation. If prompt_tokens includes cache creation, this double counts writes at the base-input rate. The full Sonnet 3.7 selection matches this formula on 88,439/88,439 calls within 1%; provider-correct pricing remains the default and its recorded-cost check remains FAIL. This arithmetic agreement does not independently establish native token semantics or an actual provider invoice.

The cross-model check does not justify a universal Bai source-formula mode: the final-completion samples for GPT-5 and Sonnet 4.5 already match standard rates; Qwen records zero cost with no supported hosted tariff; Sonnet 4 has cache reads plus writes exceeding prompt_tokens. Five inspected Sonnet 3.7 raw records omit native input_tokens, so prompt = native input + cache writes + cache reads cannot be checked independently. See benchmarks/results/BAI_ACCOUNTING.md for the pinned sources, scope and metadata-only evidence. These samples are call-level diagnostics, not additional complete tasks in this report.

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:33:28.927327+00:00. No network requests are required to view this file.

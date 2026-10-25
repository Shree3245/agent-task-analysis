# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

2000 tasks. Price catalog 2026-10-23.1-bai-routes.1 · SHA-256 50395bc63c7d0dcd458b5e074bbc5b2883fbe4985bba4ee58f1fec65493f9069.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ. Bai analysis adds exact observed provider/proxy route aliases; dollar rates are unchanged. Qwen hosted and Kimi OpenRouter tariffs remain unknown.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Bai SWE-bench Verified: kimi-k2_4runs.tar.gz. Benchmark tasks, not production.

Task groups: 2000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out. Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained.

Import 1: openhands · 1 files · 2000 records. Fields read: action, args, error, instance_id, metadata.llm_config.model, metadata.max_iterations, metrics.costs, metrics.token_usages, report.empty_patch_ids, report.instance.resolved, report.resolved_ids, report.unresolved_ids, timestamp, tool_call_metadata.model_response.id

Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded.

## Summary verdicts

REPRICING CHECK FAILED. Verdicts below describe standard-rate token costs, not validated recorded billing. Review the reconciliation discrepancy in Cost audit before using these prices.

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2026-01-05T02:37:10.242612+00:00; 16 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $0.0000. Overall distribution weights each of 0 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

Configured harness iteration limits: 500 iterations for 2000 tasks. Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 2000 | 5 | 2000 | NOT VIABLE | 2000 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable grouped_cv or positive fitted price; inflate: no usable grouped_cv or positive fitted price |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| code | 2000 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | openhands | 2000 | 500 | 500 | 4 | grouped CV | 500 of 500 task groups repeat (up to 4 tasks each), so a time split would score tasks it was fit on |

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
| code | 2000 | 5 | 0.2% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 45.0%; their spend per task $0.0000; tasks with loop signals 51.1%. Raw dollar totals below are accounting totals.

Repricing acceptance: FAIL. 0 of 152054 recorded-cost calls within 1% (0.0%); 0 comparable calls (— agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.0000; standard-rate reprice $0.0000; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 1092 | 1991/2000 | 54.8% | 0/0 | — |

### Unknown models

| Provider/model | Calls |
| --- | --- |
| unknown/moonshotai/kimi-k2-0905 | 152054 |

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |

No available observations for this table.

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| code | $0.0000 | $0.0000 | $0.0000 | 1023 | 213.02 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-c3cf49e1d50aa5d6f8e0d8035fc5779bedc132e5a87bdb2e86c3bab201a007d7 | $0.0000 | lower bound | success | False |
| task-f7a690627557104e4c22b8306e0b649518683982ab18d2bebaea0d552c06e109 | $0.0000 | lower bound | success | False |
| task-9b62e3007fbe55e9e3780ca74ba4aa811c0de97bb37dac9666f56de691764f95 | $0.0000 | lower bound | success | False |
| task-82f061a9fd6a3e19400c5beb3467f60ce82a57f7ce98baf2fcd18caad5b12d1c | $0.0000 | lower bound | fail | False |
| task-f7545c985a301a63a3b6d613e36a85037376571535986c2fd1cfaf0e50ab4774 | $0.0000 | lower bound | success | False |
| task-2a43fb53912693b93d9db64980b0e89d7d71905a796e5eef05050e6b2c2cb10b | $0.0000 | lower bound | success | False |
| task-4cbe72b0320ae84708d8827d13f2f1b101eb9d38b8821a168443c8135ac90155 | $0.0000 | lower bound | fail | False |
| task-ab484797488c13d09d7a9c67e2c6ea5719cb2d4721544f68d2236b58946f6c50 | $0.0000 | lower bound | fail | False |
| task-6f2233c17cf84af3418f0e952a017cfcf5516cd0df87ed5cb6b8a377181d4c56 | $0.0000 | lower bound | success | False |
| task-17d91c2639b094065a35cb083e8ca39357d472ed1b4f73da50f73dd97a77f17f | $0.0000 | lower bound | success | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-c3cf49e1d50aa5d6f8e0d8035fc5779bedc132e5a87bdb2e86c3bab201a007d7 | run × 3 | 52 | False | $0.0000 |
| task-f7a690627557104e4c22b8306e0b649518683982ab18d2bebaea0d552c06e109 | run × 3 | 73 | False | $0.0000 |
| task-82f061a9fd6a3e19400c5beb3467f60ce82a57f7ce98baf2fcd18caad5b12d1c | read × 3; run × 4; run × 8; run × 3 | 84 | False | $0.0000 |
| task-f7545c985a301a63a3b6d613e36a85037376571535986c2fd1cfaf0e50ab4774 | run × 5 | 70 | False | $0.0000 |
| task-2a43fb53912693b93d9db64980b0e89d7d71905a796e5eef05050e6b2c2cb10b | run × 5 | 76 | False | $0.0000 |
| task-4cbe72b0320ae84708d8827d13f2f1b101eb9d38b8821a168443c8135ac90155 | run × 3; run × 3 | 46 | False | $0.0000 |
| task-ab484797488c13d09d7a9c67e2c6ea5719cb2d4721544f68d2236b58946f6c50 | run × 3; run × 5 | 109 | False | $0.0000 |
| task-17d91c2639b094065a35cb083e8ca39357d472ed1b4f73da50f73dd97a77f17f | run × 3; run × 3; run × 3 | 99 | False | $0.0000 |
| task-1159da7b3c3bcf6cd7eec637f5112ef36675b2622ab66c5c68a08a640c05112e | run × 5 | 107 | False | $0.0000 |
| task-96363d60a9b3c7306c15b905c8994d82c5cd21a6d012d6ea317fdd69aca855a0 | run × 7; run × 3; edit × 4; edit × 4; read × 3; edit × 3; run × 3; read × 3; run × 3; run × 3 | 190 | False | $0.0000 |
| task-7a01545ea058f66a05a37c2e047cdafdd03ea273a7aa10e77844ba20b97d5e44 | run × 3 | 96 | False | $0.0000 |
| task-6b0c3eb8177da01b42608666156eb6d669dfe482a9f36eaa30ea31f50d2034bd | run × 4; run × 14; run × 3 | 119 | False | $0.0000 |
| task-4291e56ace4a037564fde547346ffa17efdbef3a4d05b65e5003143b86713545 | run × 11 | 108 | False | $0.0000 |
| task-19cbc4c40e9ff035a0421591cd549b6f56f48503ddd62cf92f60d61712828285 | run × 3 | 51 | False | $0.0000 |
| task-0021bf16a9d463482f89ff27d5de9216d36466ea58a56e61ce0651fb0e02a721 | run × 3; run × 4 | 89 | False | $0.0000 |
| task-3f349c9bfed8e91934c6a29cebaf7da5c10ed7bfc7ffa886cc8e2d975d40cc16 | run × 4 | 147 | False | $0.0000 |
| task-596ba1f38309356a2b3a264534412064e4b509f463de9ece583a8f49934a64c2 | run × 3 | 52 | False | $0.0000 |
| task-4b007f2011290cb122f0971f9789f4efd34e32cf63b377d5e09cbdd32ff40444 | run × 3 | 72 | False | $0.0000 |
| task-d209ed9619a698353bdad2246280e5c4f787fdda1e74c620c15f0d744cde5c66 | run × 4; run × 6 | 116 | False | $0.0000 |
| task-bdfe76909504a11bda978b8ba0132b283dbff832dbc8aa989ad8d11fcbce64e3 | run × 7; run × 3; run × 10 | 91 | False | $0.0000 |
| task-cc63e6e0403466280c5d8dad1bbcdb8bc2ff9fa12433a7d68293cb33bcf5059f | run × 3; run × 7; run × 5 | 88 | False | $0.0000 |
| task-83bf4758eeb3df8d3503f5a258a05dd4dc80acbff360bbe7ba763a8d54617483 | run × 6; run × 4; run × 3; run × 4; run × 3; run × 3 | 148 | False | $0.0000 |
| task-d6127e5bad619e1806c723c3b96504c279e52297f4ca5ddb3e8a5563e83b2e91 | run × 3 | 63 | False | $0.0000 |
| task-ebf528cc489b1b88eca7394e7a2f85b6b960577da61211a0897e71e95ae4cb0d | run × 4 | 44 | False | $0.0000 |
| task-d43580acdc28e2a8d10e094e0232ad059e5d67d7eb5ae47cf005dca687adce7b | run × 13; run × 5; run × 6 | 164 | False | $0.0000 |
| task-20acf94985ab1d73f5f131d9516db7722dc40577dcaf27c62613f935e646bc47 | run × 3; run × 3; run × 5 | 107 | False | $0.0000 |
| task-20d7c08d7070c63d53ad82acc25920b3e9ff92d8ed0d5ee0d4bb266d6a750b0d | run × 3 | 57 | False | $0.0000 |
| task-4cf822657b37adbebacddef91d24ad13bf700502a1798492abbe710a78467e4a | run × 3 | 69 | False | $0.0000 |
| task-ae9fda11c5c7e3a5124519fcbed4c9f82f1a6fc1d9d4967a12b1a684afc0d1ee | run × 3; run × 7 | 66 | False | $0.0000 |
| task-493f6daa803610083a02cd8aa5b321bef87d28ab68132b7cb451955a1bb5ab57 | run × 3 | 50 | False | $0.0000 |
| task-5c2fc6b2a471b8537453347a686ffec4daf41137c087f374387861eef1d0f211 | run × 3 | 40 | False | $0.0000 |
| task-8e623f88ca481a1ef9eb5c79c95205b9394517e6720f87c02930927fb13757d4 | run × 3; run × 6 | 99 | False | $0.0000 |
| task-4a99db42a933c81032a34b2e14c1d3a3871433b5057ec6ba7985a40d1514b174 | run × 3 | 56 | False | $0.0000 |
| task-e3e1dc0864cdc35ae03a8c18cf2fc6dc9add9896fe135b97c6d253d6235e7795 | run × 8 | 57 | False | $0.0000 |
| task-4ffd18149c82df1a29ccaa571168527c70d4bd97693ac433fdd6ce21c572707c | run × 3 | 81 | False | $0.0000 |
| task-8713207f93a0de04cb5babf8c51153fe5490c230ef7025284f00020e5f5af903 | run × 3; run × 5 | 51 | False | $0.0000 |
| task-794d32846016a8393a3f8f7bdd5b0838d7e8308805484ba1f283e8232b5d07bc | run × 3; run × 5 | 87 | False | $0.0000 |
| task-2208d34a2c1f66db3bd3ef26f0c53d1063fdfd443f9ac32afdc079fba3a2bb5c | run × 5 | 53 | False | $0.0000 |
| task-ddaf127f9372824f26f81d11ab95f22c13980fd390f00e39c08f229ec3127fc1 | run × 5 | 72 | False | $0.0000 |
| task-01f6a80e9134ed079ca3f3b14e1f4244a5d75e6098f87fd7603f953184a06c3a | run × 4; run × 4 | 173 | False | $0.0000 |
| task-7cda33fa22ce8a071bfed941b0ea6e8baa53bcfecfebaf2aea6c6dc8be80924a | run × 4 | 79 | False | $0.0000 |
| task-292316dccb26f056765c78110e9fd8a0fd6ec16f98ed8240cb067fc6d55eccb8 | run × 7 | 82 | False | $0.0000 |
| task-d9f11d40ce8265abc4b27a2d553f7eb46b083a9425cffdc549f00c76d9cf2d7f | run × 5; run × 3 | 63 | False | $0.0000 |
| task-9c1829aeadd28b0623ff40fc1b0e92317fe013e73ba255025c341eb19a838146 | run × 3 | 80 | False | $0.0000 |
| task-ba7beee56320af834bc68c6b501c2144a60c420bf7074abdd8d6990baa770701 | run × 10; run × 4 | 111 | False | $0.0000 |
| task-6ca02dc6f8d576cfac0a02950b9441b2af7f282f02fc3d27b1caea63e374af44 | run × 4; run × 4; run × 3; run × 3; run × 3 | 165 | False | $0.0000 |
| task-d10667aa546c96927bfe04d396bf3793572349d1d02f9734722bb08c72397087 | run × 3 | 64 | False | $0.0000 |
| task-ab96cb98ba2319558e9c0626a53516e11931301b12ea60d9a633b12308532ed7 | run × 3 | 60 | False | $0.0000 |
| task-ffc1d426485014b07b29bab111506daa3bc7a752c7f869b8998085b1532eb9ee | run × 3 | 45 | False | $0.0000 |
| task-ecbc8836139f9797d81a0f201ef3fdd6ac7ee3efa6c11de2516c7bf82c2a4bd9 | run × 3; run × 3 | 66 | False | $0.0000 |

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

### code · task-c3cf49e1d50aa5d6f8e0d8035fc5779bedc132e5a87bdb2e86c3bab201a007d7 · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| task_tracking | 8 | ≥ $0.0000 |
| read | 10 | ≥ $0.0000 |
| think | 2 | ≥ $0.0000 |
| run | 26 | ≥ $0.0000 |
| edit | 5 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-f5402fe1636f56fccce16cb9cc81f1913856c04c91fbab74bcb13ac3a0d6d85e · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 1 | ≥ $0.0000 |
| read | 5 | ≥ $0.0000 |
| run | 26 | ≥ $0.0000 |
| edit | 7 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-3541abacd2de9e9b8f32a9cbaf4c2d1b72a771c68cf374d0578841a0a45038bc · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 1 | ≥ $0.0000 |
| read | 28 | ≥ $0.0000 |
| run | 55 | ≥ $0.0000 |
| edit | 35 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-1937c0396bec90b15a5cf116567b546fc31dd3aad25050291bce79ffceb71943 · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 1 | ≥ $0.0000 |
| read | 12 | ≥ $0.0000 |
| run | 28 | ≥ $0.0000 |
| edit | 12 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |
| system (unlinked tool events) | 1 | — |
| message (unlinked tool events) | 1 | — |
| recall (unlinked tool events) | 1 | — |

### code · task-c4cdfa1a4bef142767f51f11e9c488fa872d4901df9b2830bcb61a98940b3518 · fixed — (unavailable) · success · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| think | 1 | ≥ $0.0000 |
| read | 41 | ≥ $0.0000 |
| edit | 34 | ≥ $0.0000 |
| run | 72 | ≥ $0.0000 |
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

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:38:47.878292+00:00. No network requests are required to view this file.

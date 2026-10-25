# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

1000 tasks. Price catalog 2026-10-23.1 · SHA-256 74182d05619a62951c47e44eb2c2222f86f1bf516325820588970e093abe012b.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

ASSERT-KTH subset: 2 evaluation files across the selected scaffolds. Nano-agent lacks per-call token classes; R2E-Gym has step tokens. Absolute timestamps and hosted-vLLM dollar rates are unavailable. No costs are fabricated.

Task groups: 1000 tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.

Import 1: mini-swe-agent · 1 files · 500 records. Fields read: detailed_predictions.completion.tool_calls, instance_id

Import limitations: aggregate_usage_without_call_breakdown: 500

Import 2: swe-agent · 1 files · 500 records. Fields read: action, agent_args.llm_name, ds.instance_id, exit_reason, reward, token_usage_completion, token_usage_prompt

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: unavailable; 1000 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $0.0000. Overall distribution weights each of 0 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| code | 1000 | 169 | 1000 | NOT VIABLE | 1000 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable grouped_cv or positive fitted price; inflate: no usable grouped_cv or positive fitted price |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| code | 1000 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| code | mini-swe-agent, swe-agent | 1000 | 500 | 500 | 2 | grouped CV | 500 of 500 task groups repeat (up to 2 tasks each), so a time split would score tasks it was fit on |

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
| code | 1000 | 169 | 16.9% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 42.0%; their spend per task $0.0000; tasks with loop signals 45.4%. Raw dollar totals below are accounting totals.

Repricing acceptance: UNAVAILABLE. 0 of 0 recorded-cost calls within 1% (—); 0 comparable calls (— agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.0000; standard-rate reprice $0.0000; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| code | 80 | 500/1000 | 16.0% | 0/0 | — |

### Unknown models

| Provider/model | Calls |
| --- | --- |
| unknown/hosted_vllm/Qwen/Qwen3-32B | 15020 |
| unknown/Qwen/Qwen3-32B | 5859 |

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |

No available observations for this table.

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| code | $0.0000 | $0.0000 | $0.0000 | 454 | 42.00 |

### code · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-02a07a6c94dc31f14e3358d6b79ab7c318a2b08332004c7aa54ac39045f529ae | $0.0000 | lower bound | fail | False |
| task-6f83dd8f4edad47fdd6e7a81d6d66f12ca44b48b3dc061f32105092ade35f482 | $0.0000 | lower bound | success | False |
| task-210ba31cfc8ba36945b4335840c056a1849fb0c3640e2359525367b818e41822 | $0.0000 | lower bound | unknown | False |
| task-f86c696621777d26c28e780f9829a94c5fc11fb38394e10380557dbf0cf78808 | $0.0000 | lower bound | fail | True |
| task-1fe940049597447a297dd2c7ba09a3b071529301f37018d34351864380328996 | $0.0000 | lower bound | unknown | False |
| task-6f1bd656cdd7c53ed824267549e6f619d4d73425d618e5d961f7a8a36b4bdd9f | $0.0000 | lower bound | fail | True |
| task-1fb1d6c83b49d0f31c61af32135fc01a350b6f94bec49cab21d079b1a54539cd | $0.0000 | lower bound | unknown | False |
| task-5d892a874f9f912b97935e08dfb30a7bbfe0ee9d0890f1694d5be65ced414ca2 | $0.0000 | lower bound | unknown | False |
| task-f75324e1c751f3422dd7a5a7d2200d43e4c164f3305386b6ce52020675926c64 | $0.0000 | lower bound | fail | False |
| task-65fde4f2b8fcf9a8ba5357375368dbe807bca592ade2aba40a88bb49e3b7e682 | $0.0000 | lower bound | unknown | False |

### code · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-02a07a6c94dc31f14e3358d6b79ab7c318a2b08332004c7aa54ac39045f529ae | shell × 9; shell × 3 | 37 | False | $0.0000 |
| task-6f83dd8f4edad47fdd6e7a81d6d66f12ca44b48b3dc061f32105092ade35f482 | shell × 4 | 27 | False | $0.0000 |
| task-f86c696621777d26c28e780f9829a94c5fc11fb38394e10380557dbf0cf78808 | shell × 5; shell × 3; shell × 3; shell × 3; shell × 3 | 41 | False | $0.0000 |
| task-1fe940049597447a297dd2c7ba09a3b071529301f37018d34351864380328996 | apply_patch × 9; apply_patch × 12 | 36 | False | $0.0000 |
| task-6f1bd656cdd7c53ed824267549e6f619d4d73425d618e5d961f7a8a36b4bdd9f | shell × 4; shell × 3; shell × 10 | 41 | False | $0.0000 |
| task-f75324e1c751f3422dd7a5a7d2200d43e4c164f3305386b6ce52020675926c64 | shell × 3 | 12 | False | $0.0000 |
| task-65fde4f2b8fcf9a8ba5357375368dbe807bca592ade2aba40a88bb49e3b7e682 | apply_patch × 3 | 17 | False | $0.0000 |
| task-14235fde0da991096c5af8fce597a6e245d6e08b60691cf7e17b0203849aabf4 | shell × 6 | 41 | False | $0.0000 |
| task-fc9bf7cb65a1b82684f34b4543fff5044884aa905520259a6f72afba1d2819d9 | shell × 3; shell × 11; shell × 4 | 41 | False | $0.0000 |
| task-9cb2a86b75fec3a5f333c7edc0d6774a7294d0aaf15ae74915db026fda83d0c6 | shell × 6 | 37 | False | $0.0000 |
| task-84a59c68e71a860d6657d7e2e4847fbfff3d51648b8852eb1bd48b446daad900 | shell × 3 | 28 | False | $0.0000 |
| task-444e69ca209a8461cc1d6317cbbc358ece51bfef7052481dd103f740c2efeff3 | shell × 5; shell × 11; shell × 3 | 41 | False | $0.0000 |
| task-eadbf256c78dacb9f34dc88ea4a4fd4191a799663b7d6e23d98b774e985fab12 | shell × 3 | 26 | False | $0.0000 |
| task-74778f69d445152bbf7e59ef6c791afb99d042e96f1e495b6ac8f91a73bf2159 | shell × 6; shell × 3 | 32 | False | $0.0000 |
| task-c87d2f39baf19c4df069fe43fb6567e952c346afa509bbf6253d3d27d2a76f86 | shell × 4 | 41 | False | $0.0000 |
| task-ee482590cdd35d11091873239ea013f1e69cd79adb2dcf88e3aa991b23de81c1 | shell × 5; shell × 3 | 18 | False | $0.0000 |
| task-188a7db22feda81c69a000a293b5f44019a5b3f31e0bcce6014396c0c5a7e438 | shell × 6 | 31 | False | $0.0000 |
| task-238b7a8463fb0da63151da5bde9958e6d69e684b38421a2783741176a663854b | shell × 5; shell × 5 | 41 | False | $0.0000 |
| task-20041fcaa8295e90e741b9f7b4a2878ccef543eab025776b0a6789d8a3e01320 | shell × 6; shell × 3; shell × 3 | 41 | False | $0.0000 |
| task-6224ed64f251a980cfcedf432bc914d2fe07cec3ec46c7bc91d5180c257078fe | shell × 10; shell × 3 | 40 | False | $0.0000 |
| task-8bb9d262a190e78c864ec56a4e4956dcdb8b17565158fd52799feb2f46cd6400 | shell × 3; shell × 3; shell × 25; shell × 3 | 41 | False | $0.0000 |
| task-841e09a97172821d8476c915631fefe5fe04a906e88c96a3038252cc0eef24d0 | shell × 4; shell × 3; shell × 4; shell × 5 | 40 | False | $0.0000 |
| task-49a67c4486b1456ca3f301392d0e6bc5811050c0ca46b9fb182881f5f1ce8371 | shell × 4; shell × 3; shell × 4; shell × 6 | 41 | False | $0.0000 |
| task-d4c637af6bbe8c8f161d9f9409e70d6d934b65254a04b2abbcd844b25da27c5b | apply_patch × 7 | 29 | False | $0.0000 |
| task-dfd936720e88d3cf155aebc7eaa58fbf8a143526e530f4e7748f5d99fd6badd0 | shell × 3; shell × 3; shell × 5; shell × 3 | 40 | False | $0.0000 |
| task-5d031158aa069e0bb187f961bc22533a1496dd106867973bf24ef260c798fc0c | shell × 6 | 27 | False | $0.0000 |
| task-f05fb7ea7eb650cb86e48b634849d46e1e01239cec8480b778b0b8aa45d1f816 | shell × 4 | 14 | False | $0.0000 |
| task-778207cfca7e59ce42d674faefa2dc1f31e4a3ffb7776fb6151be79c0495f38b | shell × 7; shell × 7 | 41 | False | $0.0000 |
| task-ee02286125db44c5c6d1b5fdb395c0fa504fa1f6281cbffe6f563bacd019ef6b | shell × 8; shell × 10 | 41 | False | $0.0000 |
| task-4dc76b4f2d7b0193f137ec07b74290941a26610cc1f31547d09efe2b0a1a1316 | shell × 7; shell × 4; shell × 3 | 41 | False | $0.0000 |
| task-6c624070e36a1516c81be15b90b945bb5ef3305764554fede18c081aff50b4df | shell × 3; shell × 12; shell × 6 | 41 | False | $0.0000 |
| task-62f165abfc11f520786f08d08ee142604dfedc0b7111c3b8efcce8ff9f22bb12 | shell × 7 | 41 | False | $0.0000 |
| task-81401335a5995e0936875e0426b6544d0e47163732cb5074e4174786f8f8245e | shell × 4; shell × 3; shell × 9; shell × 4; shell × 4 | 40 | False | $0.0000 |
| task-7a7985d52d5370ce77dc077882ef06d8339f6d0b0e48903d54b242b74b481304 | shell × 5 | 18 | False | $0.0000 |
| task-39bc78e3697e0daf3f6324b42b9797ed752557bb7c95e056b2c959a314c0bc68 | shell × 7; shell × 4 | 40 | False | $0.0000 |
| task-1910b3258e67d129054dd47976705423a1bdec67db02d44d602df679366b11ca | apply_patch × 4; apply_patch × 7; apply_patch × 3 | 32 | False | $0.0000 |
| task-71e5408826f404c61446238682fc3069f18cfc8a3d36495020f0c19ae6a55bfa | shell × 5 | 40 | False | $0.0000 |
| task-9da19f3395bef67c19701ec13dba8179f5ec51c07f1af914f546167b8fd24c7e | apply_patch × 3 | 15 | False | $0.0000 |
| task-b9e6c0a80035ef37cc16b464a4892bec19425765c81a7fab98b1a1828196e0d9 | shell × 10 | 42 | False | $0.0000 |
| task-06c67d13debe9fe57186bf66ee6db6490ff87aa98ea8c51ee6d712fe58f8b5ff | shell × 3; shell × 3; shell × 3; shell × 10; shell × 6 | 41 | False | $0.0000 |
| task-c34f90fc4048ecf82c90130a2797987749b356fa9a58fbb837d48d904bf975b5 | shell × 3; shell × 7 | 41 | False | $0.0000 |
| task-6291d316101617aa8cdc128f7a19e4c72ad430cb048e2b228303af00ab1889f7 | shell × 4; shell × 3 | 41 | False | $0.0000 |
| task-83224770697f0a3ad3bf7455e01fccba7152160a6cda6f39db458b4b46933df6 | shell × 8; shell × 5; shell × 4; shell × 4 | 38 | False | $0.0000 |
| task-390b96d8fa81e57ad9953e7fe2f39f974413ba2e2b101410c622b77c008b5e6f | shell × 4 | 35 | False | $0.0000 |
| task-64b55d853f53061efe88389cb5977fdf64ef072a9025486142ddadd5003a5b5e | shell × 4; shell × 4; shell × 3 | 39 | False | $0.0000 |
| task-3e10ab1bb59e73dc04617520b0276f2ecb5e95b88cfedf5aac91783740739078 | shell × 7 | 41 | False | $0.0000 |
| task-335f928a53221e75a9fba9d9557cce74eb4b4b5e86b0d0f8aed768304fb8f793 | apply_patch × 5 | 17 | False | $0.0000 |
| task-d74559359f40044be2be9120bce69c87b65646bf6ad0a1d848296a600fc19115 | shell × 3 | 17 | False | $0.0000 |
| task-3e84d65de2795409d01ca2b02c070e4b1f02177469b51686533f9219d81d375d | shell × 6 | 29 | False | $0.0000 |
| task-dffefb2da37b84cc25ac5b82c3ba246fd6403011fbeeee8b1ef03240a6f6cf21 | shell × 4; shell × 8; shell × 3 | 40 | False | $0.0000 |

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

### code · task-02a07a6c94dc31f14e3358d6b79ab7c318a2b08332004c7aa54ac39045f529ae · fixed — (unavailable) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| shell | 37 | ≥ $0.0000 |

### code · task-2d075c52aeaf6650eb85388b9d3e9ca3ec128d7c7d6cb4833a53a9100cd5e46b · fixed — (unavailable) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| shell | 8 | ≥ $0.0000 |

### code · task-8cbedd31e405a0d6cb999866206d88548e5e375a63dd78c958ae608885338e1a · fixed — (unavailable) · fail · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| shell | 34 | ≥ $0.0000 |

### code · task-1425ceb0a06949fedbcfabb38aa9392b136b4114554c55b829633433eb2d5074 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| shell | 3 | ≥ $0.0000 |
| apply_patch | 2 | ≥ $0.0000 |
| Model-only calls | 1 | ≥ $0.0000 |

### code · task-b4e3e207f51ac68d00b41c86f7544874d90b12a235d9b97dc72ecc87f70a4735 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| shell | 3 | ≥ $0.0000 |
| apply_patch | 1 | ≥ $0.0000 |
| Model-only calls | 1 | ≥ $0.0000 |

## Limits

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by agent-task-analysis. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one agent-task-analysis install only.

Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:33:29.873775+00:00. No network requests are required to view this file.

# What this report saw

BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.

No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.

1781 tasks. Price catalog 2026-10-23.1 · SHA-256 74182d05619a62951c47e44eb2c2222f86f1bf516325820588970e093abe012b.

Public standard API list rates. Not negotiated, regional, batch, or tool-service pricing. Cache writes assume 5-minute Anthropic TTL. Historical invoices may differ.

Retained call fields: task_id, call_idx, ts_start, ts_end, provider, model, input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_tokens, tool_name, tool_args_hash, recorded_cost, capped, event_kind, parent_call_idx

Retained task fields: task_id, task_type, source, started_at, ended_at, n_calls, outcome, capped, cap_reason, task_group

Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.

Task IDs are SHA-256 aliases. Type and tool labels remain visible.

Exgentic v1: 39 of 39 published parquet shards. Missing cache breakdowns may overstate list-rate cost. Cloud-model rates without explicit catalog entries remain unknown.

Import 1: otel · 39 files · 1781 records. Fields read: benchmark, end_time, gen_ai.operation.name, gen_ai.output.messages, gen_ai.response.model, gen_ai.usage.input_tokens, gen_ai.usage.output_tokens, session_id, span_id, start_time

## Summary verdicts

VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.

Temporal cutoff: 2026-03-24T09:44:55.632639+00:00; 0 tasks excluded from the split (missing time or crossing the boundary). Minimum 30 uncapped tasks per training and test partition.

Actual known spend: $205.4191. Overall distribution weights each of 3 represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.

Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool&#x27;s p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown.

The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail.

### Verdicts

| Task type | Tasks | Capped | Unpriced | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| appworld | 406 | 0 | 312 | NOT VIABLE | 312 tasks (76.8%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |
| browsecompplus | 133 | 0 | 133 | NOT VIABLE | 133 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |
| swebench | 391 | 0 | 376 | NOT VIABLE | 376 tasks (96.2%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |
| tau2_airline | 196 | 0 | 196 | NOT VIABLE | 196 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |
| tau2_retail | 469 | 0 | 469 | NOT VIABLE | 469 tasks (100.0%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |
| tau2_telecom | 186 | 0 | 184 | NOT VIABLE | 184 tasks (98.9%) have unknown costs; the limit is under 2%; exclude: no usable holdout or positive fitted price |

### Unpriced tasks · verdict both ways

| Type | Unpriced | Share | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Upper 90% CI excluded → at p99 (capped runs excluded) | Upper 90% CI excluded → at p99 (capped runs inflated) |
| --- | --- | --- | --- | --- | --- | --- |
| appworld | 312 | 76.8% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |
| browsecompplus | 133 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |
| swebench | 376 | 96.2% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |
| tau2_airline | 196 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |
| tau2_retail | 469 | 100.0% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |
| tau2_telecom | 184 | 98.9% | NOT VIABLE | not tested: over the 2% limit | — → — | — → — |

### Validation split per pricing pool

| Type | Sources | Tasks with task_group | Distinct groups | Repeated groups | Max tasks per group | Verdict split | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| appworld | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| browsecompplus | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| swebench | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| tau2_airline | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| tau2_retail | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |
| tau2_telecom | otel | 0 | 0 | 0 | 0 | time split | no source in this pool sets task_group, so repeats cannot be detected |

### Cost shape · complete, uncapped tasks

| Type | n | Mean | Median | p90 | p99 | Max | p90/p50 | Top 1% spend | Top 5% spend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| appworld | 94 | $1.0724 | $0.6290 | $2.5106 | $4.4717 | $6.2184 | 3.99 | 6.2% | 20.8% |
| browsecompplus | 0 | — | — | — | — | — | — | — | — |
| swebench | 15 | $1.3323 | $0.9948 | $2.8591 | $3.2038 | $3.2255 | 2.87 | 16.1% | 16.1% |
| tau2_airline | 0 | — | — | — | — | — | — | — | — |
| tau2_retail | 0 | — | — | — | — | — | — | — | — |
| tau2_telecom | 2 | $0.2611 | $0.2611 | $0.2887 | $0.2949 | $0.2956 | 1.11 | 56.6% | 56.6% |
| Overall · equal type weight | 111 | $0.8886 | $0.4473 | $2.5299 | $3.6047 | $6.2184 | 5.66 | 5.4% | 20.0% |

### Cap applied by the harness · iteration limits

| Type | Tasks | Hit iteration limit | Share |
| --- | --- | --- | --- |
| appworld | 406 | 0 | 0.0% |
| browsecompplus | 133 | 0 | 0.0% |
| swebench | 391 | 0 | 0.0% |
| tau2_airline | 196 | 0 | 0.0% |
| tau2_retail | 469 | 0 | 0.0% |
| tau2_telecom | 186 | 0 | 0.0% |

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Cost audit

Equal-type overall: failed/aborted tasks 0.0%; their spend per task $0.0000; tasks with loop signals 11.2%. Raw dollar totals below are accounting totals.

Repricing acceptance: UNAVAILABLE. 0 of 0 recorded-cost calls within 1% (—); 0 comparable calls (— agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped.

Cost per resolved task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.

Comparable-call totals: recorded $0.0000; standard-rate reprice $0.0000; difference $0.0000.

Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work.

### Resolution outcomes and cost per resolved task

| Type | Resolved | Known outcomes / tasks | Resolve rate | Priced tasks / priced resolutions | Cost per resolved task (priced spend / confirmed resolutions) |
| --- | --- | --- | --- | --- | --- |
| appworld | 0 | 0/406 | — | 94/0 | — |
| browsecompplus | 0 | 0/133 | — | 0/0 | — |
| swebench | 0 | 0/391 | — | 15/0 | — |
| tau2_airline | 0 | 0/196 | — | 0/0 | — |
| tau2_retail | 0 | 0/469 | — | 0/0 | — |
| tau2_telecom | 0 | 0/186 | — | 2/0 | — |

### Unknown models

| Provider/model | Calls |
| --- | --- |
| openai/Azure/gpt-4.1 | 5225 |
| google/gcp/gemini-3-pro-preview | 4405 |
| deepseek/azure/DeepSeek-V3.2 | 5735 |
| anthropic/aws/claude-opus-4-5 | 9361 |
| unknown/azure/Kimi-K2.5 | 6767 |
| unknown/global.anthropic.claude-opus-4-5-20251101-v1:0 | 1886 |
| openai/Azure/gpt-5.2-2025-12-11 | 892 |

### Repricing mismatches · first 20

| Task | Call | Recorded | Repriced |
| --- | --- | --- | --- |

No available observations for this table.

### Spend audit

| Type | Known spend | Failed/aborted spend | Censored observed spend | Loop tasks | Call-count p99 |
| --- | --- | --- | --- | --- | --- |
| appworld | $184.9131 | $0.0000 | $0.0000 | 39 | 92.75 |
| browsecompplus | $0.0000 | $0.0000 | $0.0000 | 18 | 50.00 |
| swebench | $19.9838 | $0.0000 | $0.0000 | 68 | 150.10 |
| tau2_airline | $0.0000 | $0.0000 | $0.0000 | 0 | 17.10 |
| tau2_retail | $0.0000 | $0.0000 | $0.0000 | 0 | 20.00 |
| tau2_telecom | $0.5223 | $0.0000 | $0.0000 | 50 | 50.45 |

### appworld · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-1f2e847c10c29877b56684301cf0027ffcca074251f723ab56cefb2f1553464f | $6.2184 | complete | unknown | False |
| task-19c45d2c1212b478753f7efc8ac8c4508bfbe80fd7b8d004c8893f952ca24bdb | $4.3403 | complete | unknown | False |
| task-33d6fc13fd44877b73f41c6faf2ea1e057d866d497fe4ea51cd131ed83e53301 | $4.1193 | lower bound | unknown | False |
| task-8d1900b478a51fa4d0c25ed5f89326592f0510107e4f83c6deb6412d0313d6b0 | $3.6047 | complete | unknown | False |
| task-8db053be36233eba87ee5333abfb2b6dd65d94efc7d209b67547a6178bb501c6 | $3.4669 | lower bound | unknown | False |
| task-3f0f4897b6c6ebd6c54dc2b39d050c124e3645a938147938be38526127e9b333 | $3.3985 | complete | unknown | False |
| task-8be79070a40fce17e835bbdb2b757346de66b1c6a1c6c27f2ca9f50271b6c3bf | $3.3679 | complete | unknown | False |
| task-62b4466e3a4c1a1d7f353cb9d63b9a4932ed6d8e5d02c4f2e527e893cc21cafc | $3.3120 | complete | unknown | False |
| task-1cb4079d7a81504c201749b91bd050dc7933a9e6690a571ac659dee61039fc76 | $3.2438 | lower bound | unknown | False |
| task-f95ff6979d95a5c8957015deb47ecd9877892e5236cef544650af7c2dda49299 | $2.8673 | complete | unknown | False |

### appworld · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-91f49072040af9402ec070840f48209e94b46b5c3c054bc7fff6d73d2882adcd | venmo__add_to_venmo_balance × 3 | 28 | False | $2.3327 |
| task-7e7cee2d3b8769bc33a3f1621751ec38879eb8de0be5e33d53678cd43f3c0798 | spotify__next_song × 4 | 11 | False | $0.7908 |
| task-9fa9123a56249aec946c91c25efbd6a2f253bbda5de4b27d10b3f98675741e09 | finish × 5; finish × 13 | 22 | False | $2.4653 |
| task-6514f2d449e04a6ec932190182360debcdfd9cc73a86e141172e50eb5018a13f | finish × 18 | 22 | False | $2.5499 |
| task-16f8407eca261cc7b62775b77663c6e3c48c0082c41200fc3aafc14f12fc3c09 | mcp__environment__venmo__login × 24; mcp__environment__gmail__login × 3 | 80 | False | $0.0000 |
| task-dcb97e0d0d6010bbf5df5e66309a8ae0bc25cb6a52c01b9250cf49cb68407386 | venmo__search_friends × 3 | 33 | False | $2.5250 |
| task-ce66ca24e46051d8595a4bdf7f4d0195f8c6fadecfce5e8251c89e74b405eb92 | mcp__environment__venmo__show_venmo_balance × 3 | 18 | False | $0.0000 |
| task-1bf7b02b0f6a3176fcffe640a5228e62856650074f50d497bab2da76ec8f243b | spotify__next_song × 4; spotify__show_current_song × 4 | 14 | False | $0.0000 |
| task-5978cfdd7e261895335869f9d989663b5732c6431565c832abb2bcd54278d9d2 | finish × 4 | 23 | False | $2.7074 |
| task-03a9799d4d76b93cfe87c0767e9ea9372e82e6c3fbdadb908155438656e34b41 | venmo__search_friends × 3 | 20 | False | $0.3869 |
| task-73f1f1d7e0be8ccca5d10c347447cccdbe447604bf3c3e87fe11b490abcfd9e0 | todoist__show_projects × 3 | 30 | False | $0.0000 |
| task-a41393f168714a6475993d8149d20ff1f6fffb74a1c663625389aebccaff37aa | simple_note__search_notes × 3 | 56 | False | $1.2641 |
| task-8db053be36233eba87ee5333abfb2b6dd65d94efc7d209b67547a6178bb501c6 | todoist__show_tasks × 3 | 40 | False | $3.4669 |
| task-73c98d84baf2e078aa130353aca75325e727db52afaad81820eb2d713d0879d3 | finish × 4 | 15 | False | $1.5856 |
| task-a918de9c6c5652e1fdc51370314971fbf63c1e1a22ab3d894a5047ec2c82ebb5 | spotify__next_song × 4 | 21 | False | $0.4239 |
| task-d00502d66a31c9764ada3df30f21ce4a411b9079a7c8123781ac7a87f32e0b3e | mcp__environment__simple_note__login × 3 | 35 | False | $0.0000 |
| task-2340e4722e4fc7bd31abe3c0304791538f3a99a8e9970f2bdf9969726b75b8ec | todoist__show_tasks × 7 | 101 | False | $0.0000 |
| task-1b94aba5dc9e104cefa1c7e6b26edd8cdb97ae05b4764a922e1848df9e098b68 | spotify__show_current_song × 5; spotify__next_song × 4 | 16 | False | $0.0000 |
| task-0e355f58814f298a73514c08b392145ffe99c7d0a20423bde72effcad7af25c3 | venmo__show_transactions × 3 | 47 | False | $0.0000 |
| task-d69f9180884af265d52533e605aec24a2704f3c9151f2757b3e8e2de0076efe6 | phone__show_profile × 3 | 35 | False | $0.0000 |
| task-e370495246878ae05d095518f77955f8d535f977f41e9423cb6db2d8980b3577 | mcp__environment__venmo__search_friends × 3 | 46 | False | $0.0000 |
| task-03474ceed54f71b1aa1dc2b85bc6e2ca521a3ecc417e0c71eaeb659dc1d786f0 | mcp__environment__spotify__show_current_song × 5; mcp__environment__spotify__next_song × 4 | 21 | False | $0.0000 |
| task-f1091b694d16b16b0236979a11624360cb8307e15a1f716ed39ec24de964aa0b | venmo__search_friends × 3 | 67 | False | $1.7560 |
| task-508f22294cd2f92a0b20330451c8bca06d0ee92e1aa8fc04d27f6e6e5f0df64f | mcp__environment__spotify__next_song × 4 | 11 | False | $0.0000 |
| task-3f0f4897b6c6ebd6c54dc2b39d050c124e3645a938147938be38526127e9b333 | finish × 23 | 28 | False | $3.3985 |
| task-8d1900b478a51fa4d0c25ed5f89326592f0510107e4f83c6deb6412d0313d6b0 | finish × 10 | 29 | False | $3.6047 |
| task-034931e8cd4e30f885d02da77366392b09cdcf25a80ab873a2c7859e76e9d13f | mcp__environment__venmo__show_transactions × 5; mcp__environment__venmo__show_transactions × 3 | 44 | False | $0.0000 |
| task-63dd433c22a871f221f625607d70bba6a7905290e2e64aae07646377e42be24f | mcp__environment__todoist__show_projects × 3 | 49 | False | $0.0000 |
| task-fe8ee5c79e5bdb689dd46b2f75f965f782925fa122ac16b987d01c3c52595ea8 | venmo__show_transactions × 4 | 19 | False | $0.0000 |
| task-28a0641aee60089c881c957eb57092fb8753ed7da30597894de1e0b64feb90a1 | TodoWrite × 3 | 30 | False | $0.0000 |
| task-fb6e1e6409599889f4143085396ee7ca72e39a2357894b0a58055a2edf21293e | mcp__environment__finish × 3 | 14 | False | $0.0000 |
| task-a0f9254062ef3aa33521e26302cb6391d6c7873c09c2a1287aa418ea72d62587 | venmo__show_transactions × 3 | 110 | False | $0.0000 |
| task-8a0b03c05dbcf3a079ebffcca8c2c98f5e3cfc5f86733883dd3c3dce54650c95 | venmo__add_payment_card × 3 | 17 | False | $1.3654 |
| task-ba0c571b284aeaeb5297341db833b4e929bd7e79b71155dab1c4e66a7503d5a6 | venmo__show_transactions × 3 | 15 | False | $1.2839 |
| task-6f9005dd7ae891209f3d8f47beeba8986a4e2a6db7f4ae80a34f5fdf04bf0cd7 | phone__search_contacts × 3 | 16 | False | $0.0000 |
| task-157d8d5aab152d4759caabf47deaf26457b8eb757608e3ff4ea51cb7ba798912 | mcp__environment__todoist__show_tasks × 4; mcp__environment__todoist__show_tasks × 3 | 44 | False | $0.0000 |
| task-f6d6615248ea929954675691a36b4edfdb82e7898e7ccdae5a977e6b5235e874 | simple_note__search_notes × 3 | 37 | False | $2.8317 |
| task-9b9b2a0316e9d60941a602ef42ee1031393a1354e40c1c48b7b73d49ff459942 | venmo__login × 3 | 38 | False | $0.0000 |
| task-8f4b1ffd177c69bc13205c40495893d483169f8558b18eb187e5cc2ccf59e430 | mcp__environment__gmail__show_inbox_threads × 3 | 37 | False | $0.0000 |

### browsecompplus · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-56f6d4590044be1e39182878e3e309a1b323b7073956078b82de33187486413e | $0.0000 | lower bound | unknown | False |
| task-8dfd915bf62b817f0cff6f510e146f842277770ce9d750384cee1573ae2b8ac9 | $0.0000 | lower bound | unknown | False |
| task-aa051dfb7dde4d897750be20a6ee2305a91e88cf3dbce653073674c925da4184 | $0.0000 | lower bound | unknown | False |
| task-bef55f05c55511af83290955d34dd4a760c6d958d4321cffa677ab2a62d5d44b | $0.0000 | lower bound | unknown | False |
| task-d420f9ae821a90df6ca0e4c512a97399498cc59e9481bd5c7fe02fae22f6f7de | $0.0000 | lower bound | unknown | False |
| task-235a2e13a8ba35cb30181a411daed5fb9a714f41e3b853f699808873a3826a03 | $0.0000 | lower bound | unknown | False |
| task-a4368026cd0acfe13e4d49ea5e88e170bb24515385c840ebc9deb6bd7bd2556e | $0.0000 | lower bound | unknown | False |
| task-226d030646bc87767a80ace1a774c44f5a5683802081598b7bfdd09a8a3d9422 | $0.0000 | lower bound | unknown | False |
| task-418b5110da435ed058aaa655536f12973fede02727cc850a3a51dd7c957a2e1a | $0.0000 | lower bound | unknown | False |
| task-02539cbb5229646542801379cf30951b7840a8da4d71030db35beeed2b5c00ba | $0.0000 | lower bound | unknown | False |

### browsecompplus · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-d420f9ae821a90df6ca0e4c512a97399498cc59e9481bd5c7fe02fae22f6f7de | mcp__environment__search × 3 | 13 | False | $0.0000 |
| task-226d030646bc87767a80ace1a774c44f5a5683802081598b7bfdd09a8a3d9422 | TodoWrite × 3 | 30 | False | $0.0000 |
| task-418b5110da435ed058aaa655536f12973fede02727cc850a3a51dd7c957a2e1a | mcp__environment__search × 3; mcp__environment__search × 3 | 15 | False | $0.0000 |
| task-9e33a91af2fb23f32c9163c1b63224f9a0943a18e9cf082314706bbf33e4689c | mcp__environment__search × 3; mcp__environment__search × 4 | 17 | False | $0.0000 |
| task-17ead6677e21482ed39e55cad8ee1318913554bad4638319ae3a576418bb25a3 | mcp__environment__search × 3 | 13 | False | $0.0000 |
| task-36578fb487acbe0f8698904320f3f3e1a7f273afc4c238c86bbebc8b9822160c | mcp__environment__search × 3 | 26 | False | $0.0000 |
| task-5efa7ea033e49b55cc8667487b102918377860d68ce5fb47936f8a203293f03e | mcp__environment__search × 3; mcp__environment__search × 3 | 15 | False | $0.0000 |
| task-0386fa4b15b9eb692341454c4645dc66b7540c1185b9778b33bd54c985025955 | mcp__environment__search × 4 | 24 | False | $0.0000 |
| task-8b02f9144d41026e9d3656b0a6df79cbdd3a2da28bba2db74290678490801d65 | mcp__environment__search × 3 | 49 | False | $0.0000 |
| task-41216d3245da872f3b7f41832ee6d1b45fd477cd7c2c6d039ee39687b41343c1 | mcp__environment__search × 4 | 50 | False | $0.0000 |
| task-7951c4eca9b5f55cdf2ea436490184c279c15c8d26762c176f41b7856b840d2a | mcp__environment__search × 4; mcp__environment__search × 3; mcp__environment__search × 4 | 50 | False | $0.0000 |
| task-18d1288607fcc599979aa1a92af4088732d8df8bc32eec2b79bd18427abc678b | mcp__environment__search × 3; mcp__environment__search × 3 | 50 | False | $0.0000 |
| task-76e1d44faf8a0f13fc12f191fe0acd44afaea4cc0ed3ef967da5c806253a2be7 | TodoWrite × 3 | 17 | False | $0.0000 |
| task-1be86f434ca8ea91b868ec35b6f9eac46184bfd0dada1a5a786c7ea500f7d702 | mcp__environment__search × 4; mcp__environment__search × 5 | 50 | False | $0.0000 |
| task-4762059c292282b0244ae15ca4eb535b083749f9f789fec2c6a8fbec89c4c4f9 | mcp__environment__search × 3 | 34 | False | $0.0000 |
| task-31596e1e2bb25edbd3ae120343da5286b8b714d49638b892905b7cba17087bff | mcp__environment__search × 3; mcp__environment__search × 4 | 18 | False | $0.0000 |
| task-48089fa35874f2804d16cf3c21109851c924c73098199a5e095ec9612ea37fba | mcp__environment__search × 3 | 48 | False | $0.0000 |
| task-be35c3616ab4a4103b460d5d97dc7c624f3e5129740bbf6150ecd5bc4a2dc55a | mcp__environment__search × 3 | 47 | False | $0.0000 |

### swebench · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-669708dd2d59c2735f95c246ba2fc775d69101e789a95d73955729bf3c255286 | $3.2255 | complete | unknown | False |
| task-69fc2fca5b39f18760370c1ed6e232e8d58ec7fd7f4b9f431b3393027b9d0162 | $3.0708 | complete | unknown | False |
| task-c149f50c6bf7dd2b44c51b5ad48b0dd63219e6641e13b7a58672ae6bde0c8b09 | $2.5414 | complete | unknown | False |
| task-7f114415977cb64b92fdaf22729480201f32c83bf1d9164d2105605e783bd184 | $2.1475 | complete | unknown | False |
| task-60882718ef9b64ead1a929b128f9ede588eb197b7ee8c6077eda08be45836144 | $1.6015 | complete | unknown | False |
| task-5d186eed1b35048edb28dc2f3c956dbb96e00bd70e74776ebafe38915a30be72 | $1.3992 | complete | unknown | False |
| task-2618e48161954c6b2e5d024a55a47af845ad0764090dcb01e57dce2ab34b1fc1 | $1.1369 | complete | unknown | False |
| task-1c28d7d1d4d37da0e41b51dc2b3a921ee48520c0326b6dcfaa2285d0ad32303b | $0.9948 | complete | unknown | False |
| task-011412c900c2ba7be4e026f44c879a3b3ad7d071a3df6ed5e82edbfb246cb666 | $0.7946 | complete | unknown | False |
| task-bd9313b7a116b1630f71838ceb39c05cec18caec365622a9a2e15b9d89ff35ab | $0.6648 | complete | unknown | False |

### swebench · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-57a5cc75806ac70f71922afbd610db6e4251718fbc85ef7929afe2103109c37a | mcp__environment__bash × 3 | 21 | False | $0.0000 |
| task-4b3c8d304e900256148e01a02b32d48c43861f55fcf5b66873afb9f22ab4d596 | mcp__environment__bash × 4 | 35 | False | $0.0000 |
| task-b80f5404351a8fb4dfe3c941de74759a220ae1658b900eb8c796e0d9e4692367 | mcp__environment__bash × 3 | 35 | False | $0.0000 |
| task-eb93df40aca0929e23f15fb836bfd184970ef0d4060be88781aa3d51626599b6 | mcp__environment__bash × 3 | 58 | False | $0.0000 |
| task-2b0f092481f1231691ee87ffd07cfe3167e458e3ab8b4520bca27ecdd21ab756 | mcp__environment__bash × 3; mcp__environment__bash × 3; mcp__environment__bash × 4; mcp__environment__bash × 7 | 77 | False | $0.0000 |
| task-042b49804f8d3bf071792180cdea693bcafe08785f60168e6dd11188c50e257c | mcp__environment__bash × 4 | 51 | False | $0.0000 |
| task-0b3be75189aa0e5d379ea15db1dcb9db37a5e1614ace7d38eb0ed01d52d39e9e | mcp__environment__bash × 3 | 38 | False | $0.0000 |
| task-b7767342bf547fd05c6b1e3f3d9f10b70d547229b41b244f847149e225ce2921 | bash × 3 | 61 | False | $0.0000 |
| task-cc814f9903cf1d47d732d3bea1f0b8d99a954a1cc684162ff2213d13e8805b11 | mcp__environment__bash × 5; mcp__environment__bash × 3 | 104 | False | $0.0000 |
| task-567f93a815fc6ac313b0d0d0eb4ed19db41e3c3ca8eceb6489a8a8643291672d | mcp__environment__bash × 3 | 29 | False | $0.0000 |
| task-db804bf2a72bffe90b70161fd58061b0e451e05d3b68b14dad71cd754407a41e | mcp__environment__bash × 4 | 79 | False | $0.0000 |
| task-302814a8584629a6f7880f46f669e46e079e8eab08cd4a90b356db8d0c0dd40f | mcp__environment__bash × 4 | 35 | False | $0.0000 |
| task-fe8f78b01d326101cf20edcba16f85e6547671598a0d6e36b68f887448c0d6ad | mcp__environment__bash × 3; TodoWrite × 4 | 35 | False | $0.0000 |
| task-bc35d2e542781a0e52e5970ea1a2cb755e7a661e4ba17575a440047c8e0a2025 | mcp__environment__bash × 4 | 30 | False | $0.0000 |
| task-e7128dba391213e917331bbe24a82908e843794ea3e8029ec0ae1adc241d9a3c | mcp__environment__bash × 6 | 38 | False | $0.0000 |
| task-f76167d8a98520d3831ed255b3a8023ae2a100b02016547627bdf37200f354ee | mcp__environment__bash × 5; mcp__environment__bash × 3; mcp__environment__bash × 3; mcp__environment__bash × 7 | 59 | False | $0.0000 |
| task-4805abee5a06a78ef277a4a7c031d2e30a98db9e405ab918cee796bd27eefd25 | mcp__environment__bash × 3; mcp__environment__bash × 5; mcp__environment__bash × 3; mcp__environment__bash × 3 | 73 | False | $0.0000 |
| task-ab7333cefe1c5c58290699124fc8e9263eddf278b02f33d6d96ef6a4c6bd722f | mcp__environment__bash × 3 | 81 | False | $0.0000 |
| task-62248ce7dca501f272c7fd1ae902ecc9dcfdee3c62c64b291a1b2318b7fb07d0 | bash × 3 | 48 | False | $0.0000 |
| task-15f32a555448db3885fc37882c7e4cd434191d13bb3ac608df353a26289daacb | mcp__environment__bash × 3 | 38 | False | $0.0000 |
| task-f4b31a5a71550cd430c32c64d5183a4949994a4cc39ad2398928189c760f650e | mcp__environment__bash × 5; mcp__environment__bash × 3 | 104 | False | $0.0000 |
| task-da0a4006bd4a1cf30389a1d42a06425a8a912fa98e33f8e2bbd657e34ab872dc | mcp__environment__bash × 5; mcp__environment__bash × 3 | 67 | False | $0.0000 |
| task-5902cfd986a77231c9e0d2510af1b88fe60a1fc130a49b46c48f2808a18f8994 | bash × 4 | 77 | False | $0.0000 |
| task-69fc2fca5b39f18760370c1ed6e232e8d58ec7fd7f4b9f431b3393027b9d0162 | mcp__environment__bash × 8 | 53 | False | $3.0708 |
| task-4d2c3600abd1040b6850d762f419a04aabd06e0922cfddf700e4e9176b12faab | mcp__environment__bash × 3 | 90 | False | $0.0000 |
| task-e68269b66f45d1b18f2bf4893ac330e4410b60880b83bc8b204be865936eabd4 | bash × 5 | 55 | False | $0.0000 |
| task-79ae2c941cd6db2b917b32098acabacd76d2235de5798b629f5d026c3e1dd422 | mcp__environment__bash × 4 | 30 | False | $0.0000 |
| task-40dfe3bbdaeea7f132aa2957aab3ccad411b6e2cd33fc025b81a713461633793 | mcp__environment__bash × 3 | 35 | False | $0.0000 |
| task-e478535f76b1c5ece21d1b44123c11c8b3d1998c719ae0fa9c5ad81b93de9a6e | bash × 3; bash × 3 | 94 | False | $0.0000 |
| task-22782889c9be7703dbfad95b87f621fdbb1300789e7c32f319ea3a7aa26b92cf | mcp__environment__bash × 4 | 48 | False | $0.0000 |
| task-0263d7ebd6d76e4e789bce3ddd69cbfb33f71427863c7366a132ad5fbaf656d3 | mcp__environment__bash × 3 | 30 | False | $0.0000 |
| task-b53b8e65c269f3697b2c0b1801aa83c4821270e77037c194e9b7080309260ee7 | mcp__environment__bash × 6 | 38 | False | $0.0000 |
| task-639065c3c3dac49592735bee52feb08b534f1937c07ef35e02c08f1c03b216e6 | bash × 3 | 32 | False | $0.0000 |
| task-620ca67822bd1adfb190794b9b02c4852f02bfc34a01251842c29c8e50968586 | mcp__environment__bash × 3; TodoWrite × 4 | 35 | False | $0.0000 |
| task-f3e3fae91c481ab26f4192f36861df901c05bf3b7fd926fae1e1f92915e03c29 | mcp__environment__bash × 4 | 79 | False | $0.0000 |
| task-8aac7415ffc3acfdfed3bf966d2dd6eb3ae1d98e0b4f55c4b62f3e2f0ca987c5 | mcp__environment__bash × 4 | 51 | False | $0.0000 |
| task-6507c3d63871fa336df4ee2fd08e1fbe16ba7ffe3866a7129ae501ac06fd7cac | mcp__environment__bash × 17; mcp__environment__bash × 5; Read × 3; TodoWrite × 12; mcp__environment__bash × 3 | 150 | False | $0.0000 |
| task-25a39bf73b2b1fe3743a5f902a5b46c59ad8bd0d6f680d9bd9203066b4dbd608 | mcp__environment__bash × 5; mcp__environment__bash × 3; mcp__environment__bash × 3; mcp__environment__bash × 7 | 59 | False | $0.0000 |
| task-60882718ef9b64ead1a929b128f9ede588eb197b7ee8c6077eda08be45836144 | mcp__environment__bash × 3 | 36 | False | $1.6015 |
| task-c61f44d89765c8629cbaca50145e59a0a838cf0bb918e7c6a02166d8a9450ebe | mcp__environment__bash × 3 | 24 | False | $0.0000 |
| task-bbba735144dd406c7d4f3927976d7e3ba206d100ca2bc5c71a0eea3802af64a0 | mcp__environment__bash × 3; mcp__environment__bash × 4 | 47 | False | $0.0000 |
| task-d9d67fadcfdacb4cbce4c88a87ae01be76b1707c11c26292760d9ff6f98d8f13 | mcp__environment__bash × 3 | 30 | False | $0.0000 |
| task-57d4648623770130550ea25c636e6c647f1d3230a3b2acdd4180ab61a3314d75 | mcp__environment__bash × 3 | 24 | False | $0.0000 |
| task-e15d4c67c3d4b2d068653e2d2978a80003001fabdb91343e30cc7b27e0a59167 | mcp__environment__bash × 3 | 29 | False | $0.0000 |
| task-5447559491dcce69e2b32ab8a4e83b3a7b399f2b3b1628f39c6bcffa0ee22906 | mcp__environment__bash × 4 | 48 | False | $0.0000 |
| task-db36e05e22a7c617b11ffd7de3fbf4b7af8c2fa795a3a66c22293a852a515e5c | mcp__environment__bash × 5; mcp__environment__bash × 3; mcp__environment__bash × 4 | 57 | False | $0.0000 |
| task-1c1d6db7ad9e4fb314b7ec3b2b7c496d32771344cf52da4ba3c69525abeead86 | bash × 4 | 128 | False | $0.0000 |
| task-0e206951085d786ae1652ad4b4c60b48a4d7dce7d43cdda203f30936be6296f2 | mcp__environment__bash × 3 | 16 | False | $0.0000 |
| task-f4c0c9b0076a59f8d5036886d8ce8e87c4053cfc68f80242983d29c938ec5599 | mcp__environment__bash × 3 | 64 | False | $0.0000 |
| task-484e194164f3dc91f09034aa8abd09d3285bcb32b0302cc599344649419d4772 | mcp__environment__bash × 3; mcp__environment__bash × 3 | 36 | False | $0.0000 |

### tau2_airline · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-5a0b9e687382cbf34940560d1f14f09025f49d4e3a2a8900d124c9aebe21a2c2 | $0.0000 | lower bound | unknown | False |
| task-03d85eecf7d07b6d3e50bbac6faa0988dd7b7b047fcd8d15d082c4d98e56fa34 | $0.0000 | lower bound | unknown | False |
| task-b86cc893c0a576244278263c079b5f093012d35d3b8cae86641848461bad722f | $0.0000 | lower bound | unknown | False |
| task-e4c03b4d2ba7dffeae94aa68021194fa948a8feda67656de6b03ce019cd64b26 | $0.0000 | lower bound | unknown | False |
| task-4a7c2a8757a8bcffcb5bef722219a1c6723934308869111d38e503ee9737cceb | $0.0000 | lower bound | unknown | False |
| task-8936553c7775221f717b75702439d11b1f46d14842f4932976aa010351dbfa39 | $0.0000 | lower bound | unknown | False |
| task-2cd13d5414415469f6f6b46a4e12c51b7d933a631cbac15db8cbabe6989130f3 | $0.0000 | lower bound | unknown | False |
| task-6675e051a3940bd6857c8ebf7fe363604719b7b1249acc03ffbb1a36adad667a | $0.0000 | lower bound | unknown | False |
| task-741953599d4aca09adf06405b9c5000cd3d75764e9bc46c495d596447eec5b35 | $0.0000 | lower bound | unknown | False |
| task-06e10084d54978e5b10ad7ef6357d2b24d8bd9b1bfa31b217b38d5d929dcd4d4 | $0.0000 | lower bound | unknown | False |

### tau2_airline · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |

No available observations for this table.

### tau2_retail · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-c7716176a59360da1e1203acbd959f426a08086c0b0384eae1712501258223ff | $0.0000 | lower bound | unknown | False |
| task-b5c3d097b585247fb9c0a99a8119dda8bcb2cf7e64695be20b606a09f0b352ab | $0.0000 | lower bound | unknown | False |
| task-2b5cae2d035bdf059802121c5ff464d54a0705f08e2bde2f2b9356b035bf8219 | $0.0000 | lower bound | unknown | False |
| task-57de001b4cbcefe5ff6643d84263a33f3149aca4d9aa6c3772a0c79662da3178 | $0.0000 | lower bound | unknown | False |
| task-df6eff4649095d03057e55519f16f615e58a0c3889fc5517b4d50f29d4d45a73 | $0.0000 | lower bound | unknown | False |
| task-9a3e2e49cefc34d3e42f3b7e8c2d8d24db01ce117bcb7c4865c99631df707458 | $0.0000 | lower bound | unknown | False |
| task-510a5df364c6c0c6dbeb2122ffd7bf735ff33fa9f8cea41325cbbbf88b908be5 | $0.0000 | lower bound | unknown | False |
| task-83425f3e3420f1ac1573905dc936f9f250f967275b700c6ebe97035fe74c2a75 | $0.0000 | lower bound | unknown | False |
| task-d1daf2086608537a4e53aa65c75e3d5d648cda35ea65e1e942ef9fdaf9ebd6f1 | $0.0000 | lower bound | unknown | False |
| task-8fb155956e55892c37b751a70c2146b948def856b72ec2b9b16c8c8be29f4f1e | $0.0000 | lower bound | unknown | False |

### tau2_retail · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |

No available observations for this table.

### tau2_telecom · runaway tasks

| Task | Known cost | Coverage | Outcome | Capped |
| --- | --- | --- | --- | --- |
| task-ce50fefcf74db5153715126256ec00634d10c6128e0a7ddbb816eb7f218edfd5 | $0.2956 | complete | unknown | False |
| task-e7bd5e25241818364a0d5250582594f01efb62de3d79af2c281d98a90ac884a3 | $0.2267 | complete | unknown | False |
| task-3fb06b9991a15158af89c1b781788fcc97132421bbc739e457c1a514a9d1cdaa | $0.0000 | lower bound | unknown | False |
| task-9b2330faa4b8fb4dd66b03e221c3d61f8783fc98e113260060b02efdd68eef7e | $0.0000 | lower bound | unknown | False |
| task-b811773ddb8ecb6654e9b9cc5b9f213a234f3f30e821448a591a17c5bd31615f | $0.0000 | lower bound | unknown | False |
| task-3efe7f0b24e3c8e393a382a8ab4f4fdbdd537de323412bf5bbc6c813fe6636e0 | $0.0000 | lower bound | unknown | False |
| task-09cdc828c5e5fb73baf12f2e1349f3d57a555c82ab94221784e69450d0a1bbc3 | $0.0000 | lower bound | unknown | False |
| task-5eba6fc3debf302b4a21cb943d0b124a81589d22c7a2dce8bf323c7a74ab3c7b | $0.0000 | lower bound | unknown | False |
| task-d8074a149db11958f4d8933d0a05d7a121a5d79a46be9d11d5d08fb87d90a70b | $0.0000 | lower bound | unknown | False |
| task-4b108aeaf3ce50e8bcba0219a54017f9824e5c5953d155b916efc9e574d7e962 | $0.0000 | lower bound | unknown | False |

### tau2_telecom · loop signals

| Task | Repeated tools | Calls | Above 2 × p99 | Known cost |
| --- | --- | --- | --- | --- |
| task-3fb06b9991a15158af89c1b781788fcc97132421bbc739e457c1a514a9d1cdaa | can_send_mms × 4 | 24 | False | $0.0000 |
| task-9b2330faa4b8fb4dd66b03e221c3d61f8783fc98e113260060b02efdd68eef7e | run_speed_test × 3 | 13 | False | $0.0000 |
| task-3efe7f0b24e3c8e393a382a8ab4f4fdbdd537de323412bf5bbc6c813fe6636e0 | can_send_mms × 4; check_apn_settings × 3; run_speed_test × 4 | 53 | False | $0.0000 |
| task-7061ab0166a776b15501dc7181e19552a78da260c899cb8abae6a2ff5333d4e9 | can_send_mms × 4 | 39 | False | $0.0000 |
| task-5a0f680162702889973977e3a9ac4d69529ce44d9fe7dbe98d5116190da525c8 | run_speed_test × 3; can_send_mms × 5 | 37 | False | $0.0000 |
| task-85fc9c41f54c4fd7532448dddd4923ed75671bbde355627e6f64ea0aef85218c | check_network_status × 4; run_speed_test × 5 | 34 | False | $0.0000 |
| task-bdfa037a2510feb69b94f36c1c58e95eafc46d126b8c87697cfc0e4cce530088 | can_send_mms × 4 | 31 | False | $0.0000 |
| task-1e91e92d828469c508a3d6d9a16697ddd49b454e086eecdc6b13fbcf96eb844f | check_network_status × 3 | 11 | False | $0.0000 |
| task-3cd14435aba5484903d3f35ec78f39257c6be5e553ba750473d26bb44077a066 | can_send_mms × 4; check_status_bar × 3; run_speed_test × 3 | 32 | False | $0.0000 |
| task-5b20fe5817e2ef9d0420b2584c974862dd3d7e22d60209116aa0ed953ba4ddc9 | run_speed_test × 6; toggle_data × 3 | 32 | False | $0.0000 |
| task-73353735fd4e58fd500fd9a39d16e3014fb181329ca1e5493e1924d30406e71d | run_speed_test × 5 | 27 | False | $0.0000 |
| task-526fe65d48e4b4d0e55fbb14ffebf3ab5f598ec256e6185638c3f4952f66c545 | can_send_mms × 6 | 50 | False | $0.0000 |
| task-855edddaafef20ea882cedbe88eb4fb9436c79e38938b57824ae20d59a9b5505 | can_send_mms × 5 | 31 | False | $0.0000 |
| task-ac76d91497424e608ae0922641ca206cb8e69f7d93d3c2a8a026f00a80351224 | run_speed_test × 3 | 11 | False | $0.0000 |
| task-1970034164c656592270d329b50c814e30b5ab429056d7498bc4053467d3bddc | can_send_mms × 4 | 46 | False | $0.0000 |
| task-aeb7d9a9079c11f3ab39ae6b3ae8c97d329b4db5194a507de73a1da926b7c51a | can_send_mms × 3 | 20 | False | $0.0000 |
| task-2c573d530aafd25abec68144bf9c0b9cf9bc5ce53859a7356f843dbe67fe0137 | run_speed_test × 3 | 34 | False | $0.0000 |
| task-cdb8965b22d2fd207f4fc376ca790ab450336766c8e2de3ce9ded8b555153bfd | check_network_status × 3; run_speed_test × 3 | 26 | False | $0.0000 |
| task-9ca44c562d605038b412688c714a0b3f4e75ba23c5bd52491a1fe21232f074ab | can_send_mms × 5 | 34 | False | $0.0000 |
| task-f25983c9d7c007163c2ee8f52384bbb43dbf164844cbeb17c3fa73994adfa0a6 | check_status_bar × 3 | 29 | False | $0.0000 |
| task-a391489e9149b1db3d4220aaa304e694b5f029b6bdf83101a411a31ba126944e | check_network_status × 3 | 18 | False | $0.0000 |
| task-b5dc80fa179afd142af88b31d02d8df9a761220b6033abefe3485813811b0d76 | can_send_mms × 5 | 33 | False | $0.0000 |
| task-7afda00f5f63992b1a9da77cadcc4553230af6bebb936b31e06b84f2978deceb | can_send_mms × 4; run_speed_test × 3 | 31 | False | $0.0000 |
| task-cf97f29ed529aa57135398c3680830c6be202586db031a4b5203a160cf4f4456 | can_send_mms × 4 | 34 | False | $0.0000 |
| task-295375d1760295a792df3bea1c3819c0710c8922b98b2f3149605fafb7147b0e | toggle_airplane_mode × 3; toggle_data × 5; run_speed_test × 6 | 47 | False | $0.0000 |
| task-fe87003a22ae28a053d117ff37fb9dc606598e09d8a2d2dd2f835da31485c1d1 | run_speed_test × 3 | 24 | False | $0.0000 |
| task-fefe47204ac9bf9ed24bc553f916fc6e45a0838d19422550b4162467d80d28c8 | check_status_bar × 3 | 23 | False | $0.0000 |
| task-ff53ba3d915c21af7968e9bb9c96b4556114c33e188d03cb673eeba272843952 | run_speed_test × 3 | 15 | False | $0.0000 |
| task-b2cb6b56ea79af59db844b5b29aeba98c6e5cf013a971d9009884d2015b54473 | can_send_mms × 5; toggle_airplane_mode × 3; toggle_data × 3; run_speed_test × 4 | 44 | False | $0.0000 |
| task-2a0450e3890cb4a1985f4096e11519fcca6082a788a66d0bafd7880f96294c7d | check_network_status × 3 | 15 | False | $0.0000 |
| task-04674f40cee7a61886b4d71539cfb355e354e0a3cdd7e8dee8f8e5a4ee0255a4 | check_network_status × 4; can_send_mms × 6 | 37 | False | $0.0000 |
| task-1c7d018f900882a6bd2265b342584de56f11ab802037781483a06ecd6a43bc86 | can_send_mms × 7 | 38 | False | $0.0000 |
| task-97ac29e263d66cfa717762a877aaca123352e5c74d581047bfa2de54e6a8af47 | can_send_mms × 4 | 31 | False | $0.0000 |
| task-3cbe770882344793d61cd611f5bd5f2e3b8fc1f1d405b0731c995fba452b23e0 | check_network_status × 3; run_speed_test × 3 | 27 | False | $0.0000 |
| task-558defb293ec4008abb48cff3edc318d968a5835d40f2265314008729b414f96 | can_send_mms × 6 | 41 | False | $0.0000 |
| task-878bae8046047b0ce94acc7958b09b1ec95f6f44d6c5d7c88bcad9cfe8c787bc | toggle_data × 3; can_send_mms × 3; run_speed_test × 4 | 38 | False | $0.0000 |
| task-da254d451af4c53f51538febd4095618059eb305ab00a662ec8cf0c2289afa18 | run_speed_test × 3 | 14 | False | $0.0000 |
| task-5eee44274f113110c5105d2044dafb1edab783b01674456f4afd3cfc03a524ff | can_send_mms × 3 | 19 | False | $0.0000 |
| task-05be5176d79da0e137a6e0939faa08c529264333c1eea3519da8cc20d409b0dd | run_speed_test × 4 | 22 | False | $0.0000 |
| task-04e2039e578a45e4b413e0ed5936f975c7f2e9d8bb6c9d6d8e78ef3d4609cdb7 | check_network_status × 4; run_speed_test × 4 | 41 | False | $0.0000 |
| task-d4d830922336585fcfb3c88dc4149b35031ca1f2e5b461b817d750f4decf7e83 | can_send_mms × 3; check_network_status × 3 | 30 | False | $0.0000 |
| task-ebb64d0d4a8a776961c4f99bb0652178368aae7dc54f2a352765d1cf89356ceb | run_speed_test × 4 | 29 | False | $0.0000 |
| task-a0cd6d56f5f353748413a7189d66df21981e110195805f2e206f91607859b300 | can_send_mms × 3 | 20 | False | $0.0000 |
| task-05a9c043143d64993c16c626bdd407c0eadf38d3b6820e6609030946ce3af52f | can_send_mms × 4; run_speed_test × 3 | 54 | False | $0.0000 |
| task-fc1daa1eea4c0e33cf2362650049b3462e87635c5031a9eb031e590dd133b0dd | can_send_mms × 3; run_speed_test × 3 | 35 | False | $0.0000 |
| task-e0794323fec6cd090e9535b2b92ef4d23cc90cfb2692ac3e951c8bf960b361f5 | can_send_mms × 5 | 40 | False | $0.0000 |
| task-fba5d516f03fd2d16bbc18bbb20bb7b08ae462bcb7b96a3969d6197498fccee4 | check_network_status × 3; can_send_mms × 5 | 36 | False | $0.0000 |
| task-382c5931a5c53eec141918378f55947bc1be8bf4a52d17395c2e884f3b9f9f72 | run_speed_test × 4; can_send_mms × 3 | 37 | False | $0.0000 |
| task-48bd89fab2af768b3880ed390a3f84d038c84bb5a68bd01fa973bfdfb67c1fbb | run_speed_test × 5 | 30 | False | $0.0000 |
| task-1caab16a808000f6eb53f0d61ad44c95782833ad7ddd0608bb04335743d0452c | run_speed_test × 5; check_status_bar × 3 | 34 | False | $0.0000 |

## Catastrophe cap

Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only.

### Cap scenarios

| Type | Percentile | Cap | Stopped | Spend saved | Saved share | Ideal stopped | Ideal saved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| appworld | p95 | $3.3315 | 3.2% | $3.9847 | 4.0% | 5.3% | $4.2721 |
| appworld | p99 | $4.4717 | 1.1% | $1.7082 | 1.7% | 1.1% | $1.7467 |
| appworld | p99.5 | $5.3451 | 1.1% | $0.8614 | 0.9% | 1.1% | $0.8733 |
| swebench | p95 | $3.1172 | 6.7% | $0.0774 | 0.4% | 6.7% | $0.1082 |
| swebench | p99 | $3.2038 | 0.0% | $0.0000 | 0.0% | 6.7% | $0.0216 |
| swebench | p99.5 | $3.2146 | 0.0% | $0.0000 | 0.0% | 6.7% | $0.0108 |
| tau2_telecom | p95 | $0.2922 | 0.0% | $0.0000 | 0.0% | 50.0% | $0.0034 |
| tau2_telecom | p99 | $0.2949 | 0.0% | $0.0000 | 0.0% | 50.0% | $0.0007 |
| tau2_telecom | p99.5 | $0.2953 | 0.0% | $0.0000 | 0.0% | 50.0% | $0.0003 |

### Overall cap impact · equal type weight

| Percentile | Types represented | Stopped | Saved per task | Mean type saved share |
| --- | --- | --- | --- | --- |
| p95 | 3 | 3.3% | $0.0158 | 1.4% |
| p99 | 3 | 0.4% | $0.0061 | 0.6% |
| p99.5 | 3 | 0.4% | $0.0031 | 0.3% |

## Fixed-price simulation with confidence intervals

Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.

In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.

Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type&#x27;s mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the &lt;90% upper-CI decision is flagged in the verdict.

Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.

### appworld

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $1.7873 | 60.0% | 50.5% – 70.9% | 18.1% | $4.4311 | 94/94 |
| in_sample | exclude | none | 70.0% | $1.5320 | 70.0% | 58.9% – 82.7% | 20.2% | $4.6865 | 94/94 |
| in_sample | exclude | none | 80.0% | $1.3405 | 80.0% | 67.3% – 94.5% | 26.6% | $4.8780 | 94/94 |
| in_sample | exclude | p99 | 60.0% | $1.7570 | 60.0% | 50.9% – 70.1% | 18.1% | $2.7532 | 94/94 |
| in_sample | exclude | p99 | 70.0% | $1.5060 | 70.0% | 59.4% – 81.7% | 20.2% | $3.0042 | 94/94 |
| in_sample | exclude | p99 | 80.0% | $1.3177 | 80.0% | 67.8% – 93.4% | 26.6% | $3.1925 | 94/94 |
| in_sample | inflate | none | 60.0% | $1.7873 | 60.0% | 50.5% – 70.9% | 18.1% | $4.4311 | 94/94 |
| in_sample | inflate | none | 70.0% | $1.5320 | 70.0% | 58.9% – 82.7% | 20.2% | $4.6865 | 94/94 |
| in_sample | inflate | none | 80.0% | $1.3405 | 80.0% | 67.3% – 94.5% | 26.6% | $4.8780 | 94/94 |
| in_sample | inflate | p99 | 60.0% | $1.7570 | 60.0% | 50.9% – 70.1% | 18.1% | $2.7532 | 94/94 |
| in_sample | inflate | p99 | 70.0% | $1.5060 | 70.0% | 59.4% – 81.7% | 20.2% | $3.0042 | 94/94 |
| in_sample | inflate | p99 | 80.0% | $1.3177 | 80.0% | 67.8% – 93.4% | 26.6% | $3.1925 | 94/94 |

### browsecompplus

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### swebench

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $2.2204 | 60.0% | 42.2% – 79.5% | 20.0% | $1.0050 | 15/15 |
| in_sample | exclude | none | 70.0% | $1.9032 | 70.0% | 49.3% – 92.8% | 26.7% | $1.3222 | 15/15 |
| in_sample | exclude | none | 80.0% | $1.6653 | 80.0% | 56.3% – 106.0% | 26.7% | $1.5601 | 15/15 |
| in_sample | exclude | p99 | 60.0% | $2.2204 | 60.0% | 42.2% – 79.5% | 20.0% | $1.0050 | 15/15 |
| in_sample | exclude | p99 | 70.0% | $1.9032 | 70.0% | 49.3% – 92.8% | 26.7% | $1.3222 | 15/15 |
| in_sample | exclude | p99 | 80.0% | $1.6653 | 80.0% | 56.3% – 106.0% | 26.7% | $1.5601 | 15/15 |
| in_sample | inflate | none | 60.0% | $2.2204 | 60.0% | 42.2% – 79.5% | 20.0% | $1.0050 | 15/15 |
| in_sample | inflate | none | 70.0% | $1.9032 | 70.0% | 49.3% – 92.8% | 26.7% | $1.3222 | 15/15 |
| in_sample | inflate | none | 80.0% | $1.6653 | 80.0% | 56.3% – 106.0% | 26.7% | $1.5601 | 15/15 |
| in_sample | inflate | p99 | 60.0% | $2.2204 | 60.0% | 42.2% – 79.5% | 20.0% | $1.0050 | 15/15 |
| in_sample | inflate | p99 | 70.0% | $1.9032 | 70.0% | 49.3% – 92.8% | 26.7% | $1.3222 | 15/15 |
| in_sample | inflate | p99 | 80.0% | $1.6653 | 80.0% | 56.3% – 106.0% | 26.7% | $1.5601 | 15/15 |

### tau2_airline

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### tau2_retail

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

### tau2_telecom

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_sample | exclude | none | 60.0% | $0.4352 | 60.0% | 52.1% – 67.9% | 0.0% | $0.0000 | 2/2 |
| in_sample | exclude | none | 70.0% | $0.3731 | 70.0% | 60.8% – 79.2% | 0.0% | $0.0000 | 2/2 |
| in_sample | exclude | none | 80.0% | $0.3264 | 80.0% | 69.4% – 90.6% | 0.0% | $0.0000 | 2/2 |
| in_sample | exclude | p99 | 60.0% | $0.4352 | 60.0% | 52.1% – 67.9% | 0.0% | $0.0000 | 2/2 |
| in_sample | exclude | p99 | 70.0% | $0.3731 | 70.0% | 60.8% – 79.2% | 0.0% | $0.0000 | 2/2 |
| in_sample | exclude | p99 | 80.0% | $0.3264 | 80.0% | 69.4% – 90.6% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | none | 60.0% | $0.4352 | 60.0% | 52.1% – 67.9% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | none | 70.0% | $0.3731 | 70.0% | 60.8% – 79.2% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | none | 80.0% | $0.3264 | 80.0% | 69.4% – 90.6% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | p99 | 60.0% | $0.4352 | 60.0% | 52.1% – 67.9% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | p99 | 70.0% | $0.3731 | 70.0% | 60.8% – 79.2% | 0.0% | $0.0000 | 2/2 |
| in_sample | inflate | p99 | 80.0% | $0.3264 | 80.0% | 69.4% – 90.6% | 0.0% | $0.0000 | 2/2 |

### Overall · equal type weight

| Scope | Censoring | Cap | Target | Price | Loss ratio | 90% CI | Tasks losing | Worst loss | Train/test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

No available observations for this table.

Charts are embedded in the companion self-contained HTML; numerical results are above.

## Sample receipts

Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule.

### appworld · task-f4be68d9e9b5668d3ac4c478eec5c9ec3ede6b287877526f198e47ca466dbf4e · fixed $1.5060 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 14 | ≥ $0.0000 |

### appworld · task-5ca552be79e33079e7547e6c50c3a6fc76adbee869cd63eff8a81e3bb55c346b · fixed $1.5060 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 17 | ≥ $0.0000 |
| supervisor__show_account_passwords | 1 | ≥ $0.0000 |
| supervisor__show_profile | 1 | ≥ $0.0000 |
| venmo__login | 1 | ≥ $0.0000 |
| phone__login | 1 | ≥ $0.0000 |
| phone__search_contacts | 1 | ≥ $0.0000 |
| venmo__show_transactions | 7 | ≥ $0.0000 |
| venmo__create_transaction | 1 | ≥ $0.0000 |
| phone__send_text_message | 1 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |

### appworld · task-de6624a95d4ecb8baf8d8d9b379faa7f7484ffb70e332f0c0b5645bfd508730e · fixed $1.5060 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__supervisor__show_account_passwords | 1 | ≥ $0.0000 |
| mcp__environment__simple_note__login | 1 | ≥ $0.0000 |
| mcp__environment__simple_note__search_notes | 25 | ≥ $0.0000 |
| mcp__environment__simple_note__show_note | 8 | ≥ $0.0000 |

### appworld · task-89dd1c62e7eec22b1e249df35a58b0d2ffc7f827d0caa7bc39be986ee808762e · fixed $1.5060 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| supervisor__show_account_passwords | 1 | $0.0738 |
| venmo__login | 1 | $0.0733 |
| venmo__search_friends | 4 | $0.3072 |
| venmo__create_payment_request | 1 | $0.0784 |
| finish | 1 | $0.0760 |

### appworld · task-1f2e847c10c29877b56684301cf0027ffcca074251f723ab56cefb2f1553464f · fixed $1.5060 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| supervisor__show_account_passwords | 1 | $0.0736 |
| todoist__login | 1 | $0.0732 |
| todoist__show_projects | 4 | $0.3077 |
| todoist__show_tasks | 8 | $0.6686 |
| todoist__search_labels | 1 | $0.0818 |
| todoist__show_project | 1 | $0.0806 |
| todoist__show_notifications | 2 | $0.1627 |
| todoist__show_task | 8 | $0.6879 |
| todoist__create_label | 1 | $0.0876 |
| todoist__show_task_comments | 3 | $0.2632 |
| todoist__show_sections | 1 | $0.0925 |
| spotify__login | 1 | $0.0915 |
| spotify__search_songs | 12 | $1.1070 |
| spotify__search_artists | 3 | $0.2777 |
| spotify__show_playlist | 2 | $0.1831 |
| spotify__search_albums | 4 | $0.3729 |
| spotify__show_artist | 2 | $0.1826 |
| spotify__show_album | 2 | $0.1857 |
| spotify__show_song | 3 | $0.2808 |
| spotify__remove_song_from_playlist | 4 | $0.3811 |
| spotify__add_song_to_playlist | 3 | $0.2880 |
| todoist__post_task_comment | 1 | $0.0964 |
| todoist__update_task | 1 | $0.0965 |
| finish | 1 | $0.0956 |

### browsecompplus · task-56f6d4590044be1e39182878e3e309a1b323b7073956078b82de33187486413e · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__search | 48 | ≥ $0.0000 |
| mcp__environment__get_document | 1 | ≥ $0.0000 |
| mcp__environment__submit | 1 | ≥ $0.0000 |

### browsecompplus · task-f3a9e5fb3839d849b5de44526c97de004d09a1efa19b65ba6d07726302f4abc0 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| ListMcpResourcesTool | 1 | ≥ $0.0000 |
| mcp__environment__search | 11 | ≥ $0.0000 |
| TodoWrite | 2 | ≥ $0.0000 |
| mcp__environment__submit | 1 | ≥ $0.0000 |

### browsecompplus · task-d7728a89d91dbe30a40e18cd48fdbce6f996dc76a37dea2b94a62353a9cb7b65 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__search | 25 | ≥ $0.0000 |
| Model-only calls | 4 | ≥ $0.0000 |
| mcp__environment__get_document | 2 | ≥ $0.0000 |

### browsecompplus · task-349a65187a4ee22fab4b844784d66dc1b884bbb7fa675c4a2e69427a50c0c762 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| ListMcpResourcesTool | 1 | ≥ $0.0000 |
| mcp__environment__search | 7 | ≥ $0.0000 |
| mcp__environment__submit | 1 | ≥ $0.0000 |

### browsecompplus · task-412b3956760a917cf315e3b8e0820c47572ecc250db1dfa54c1dfac675cdc2e5 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__search | 10 | ≥ $0.0000 |
| TodoWrite | 2 | ≥ $0.0000 |
| mcp__environment__submit | 1 | ≥ $0.0000 |

### swebench · task-8fb8eb48d314016f27f1f0eb69f683809b06ecb9c5701740133037c682c3798e · fixed $1.9032 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 63 | ≥ $0.0000 |

### swebench · task-cb29d0d4da04ecd0fa400be379b25a93fda7df5fb594ae61e492e88efdd1befc · fixed $1.9032 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| bash | 26 | ≥ $0.0000 |
| Model-only calls | 2 | ≥ $0.0000 |
| finish | 1 | ≥ $0.0000 |

### swebench · task-75631cdf72837840de0255eda618b597777f4a74fd9d1ab6c140b6605851e73d · fixed $1.9032 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 26 | ≥ $0.0000 |

### swebench · task-177bfa9fe32bcc490c37779e3db63a22475d1cc6fba25aae454ce77aeb2af019 · fixed $1.9032 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__bash | 24 | ≥ $0.0000 |
| mcp__environment__finish | 1 | ≥ $0.0000 |
| Model-only calls | 1 | ≥ $0.0000 |

### swebench · task-669708dd2d59c2735f95c246ba2fc775d69101e789a95d73955729bf3c255286 · fixed $1.9032 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__bash | 57 | $3.1481 |
| mcp__environment__finish | 1 | $0.0774 |

### tau2_airline · task-5a0b9e687382cbf34940560d1f14f09025f49d4e3a2a8900d124c9aebe21a2c2 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__message | 3 | ≥ $0.0000 |
| mcp__environment__get_reservation_details | 1 | ≥ $0.0000 |
| Model-only calls | 1 | ≥ $0.0000 |

### tau2_airline · task-250ab61125032bbae2831fdd881d5e202e9da819a62b017a288289f181696678 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__message | 4 | ≥ $0.0000 |
| mcp__environment__get_user_details | 1 | ≥ $0.0000 |
| mcp__environment__get_reservation_details | 3 | ≥ $0.0000 |
| mcp__environment__search_direct_flight | 1 | ≥ $0.0000 |
| mcp__environment__update_reservation_flights | 1 | ≥ $0.0000 |

### tau2_airline · task-8163029ce4272762ed2117c80bdd0db1176cdbf74006ae348a16e10baf5bcda5 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 5 | ≥ $0.0000 |

### tau2_airline · task-9a2371a8c36763817bf27c6c45af3aa66bf46630386c90c05452abcae4378544 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 9 | ≥ $0.0000 |

### tau2_airline · task-5a8155ae082a7c611ed232bac708c32e48c4c83a3fc5d007b263f94a6fdf570b · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__message | 6 | ≥ $0.0000 |
| mcp__environment__get_user_details | 1 | ≥ $0.0000 |
| mcp__environment__get_reservation_details | 3 | ≥ $0.0000 |
| mcp__environment__get_flight_status | 1 | ≥ $0.0000 |
| mcp__environment__search_direct_flight | 2 | ≥ $0.0000 |
| mcp__environment__update_reservation_flights | 1 | ≥ $0.0000 |

### tau2_retail · task-c7716176a59360da1e1203acbd959f426a08086c0b0384eae1712501258223ff · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 10 | ≥ $0.0000 |

### tau2_retail · task-9d9a713bd5b7d3edad6dd3e92fe120fbd5d34835da87c0623087fd1bdfd26fa1 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__message | 5 | ≥ $0.0000 |
| mcp__environment__find_user_id_by_name_zip | 1 | ≥ $0.0000 |
| mcp__environment__get_user_details | 1 | ≥ $0.0000 |
| mcp__environment__get_order_details | 1 | ≥ $0.0000 |
| mcp__environment__modify_pending_order_address | 1 | ≥ $0.0000 |
| Model-only calls | 1 | ≥ $0.0000 |

### tau2_retail · task-28f3d7090e9e948fe995c09008a1a083039d1853a89917f28bcd6455ccff0288 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 5 | ≥ $0.0000 |

### tau2_retail · task-c66c910e02e862a4b9255a5410d71c883d1eeb8f309784b8b1628413bada5f5c · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 10 | ≥ $0.0000 |

### tau2_retail · task-7fe2f0d568500e39e82e123d0e2257fe0fb755d3a0cdcb9a7a3a58f4b48efe63 · fixed — (unavailable) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 4 | ≥ $0.0000 |

### tau2_telecom · task-3fb06b9991a15158af89c1b781788fcc97132421bbc739e457c1a514a9d1cdaa · fixed $0.3731 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 10 | ≥ $0.0000 |
| Shared tools: check_network_status, check_status_bar | 1 | ≥ $0.0000 |
| set_network_mode_preference | 1 | ≥ $0.0000 |
| can_send_mms | 4 | ≥ $0.0000 |
| Shared tools: check_apn_settings, run_speed_test | 1 | ≥ $0.0000 |
| Shared tools: check_data_restriction_status, check_vpn_status | 1 | ≥ $0.0000 |
| reboot_device | 2 | ≥ $0.0000 |
| run_speed_test | 1 | ≥ $0.0000 |
| Shared tools: check_installed_apps, check_wifi_calling_status | 1 | ≥ $0.0000 |
| Shared tools: check_app_permissions, reset_apn_settings | 1 | ≥ $0.0000 |
| grant_app_permission | 1 | ≥ $0.0000 |

### tau2_telecom · task-f25983c9d7c007163c2ee8f52384bbb43dbf164844cbeb17c3fa73994adfa0a6 · fixed $0.3731 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| Model-only calls | 12 | ≥ $0.0000 |
| can_send_mms | 2 | ≥ $0.0000 |
| Shared tools: check_network_status, check_status_bar | 1 | ≥ $0.0000 |
| toggle_airplane_mode | 1 | ≥ $0.0000 |
| reseat_sim_card | 1 | ≥ $0.0000 |
| check_status_bar | 2 | ≥ $0.0000 |
| check_network_mode_preference | 1 | ≥ $0.0000 |
| set_network_mode_preference | 1 | ≥ $0.0000 |
| check_apn_settings | 1 | ≥ $0.0000 |
| reset_apn_settings | 1 | ≥ $0.0000 |
| reboot_device | 1 | ≥ $0.0000 |
| Shared tools: check_apn_settings, check_app_permissions, check_wifi_calling_status | 1 | ≥ $0.0000 |
| toggle_wifi_calling | 1 | ≥ $0.0000 |
| check_installed_apps | 1 | ≥ $0.0000 |
| check_app_permissions | 1 | ≥ $0.0000 |
| grant_app_permission | 1 | ≥ $0.0000 |

### tau2_telecom · task-f99878e4385f93e2fb86a323e6a7ae9e2ee2ad6d2f0ddb9711fb17d78654fcf5 · fixed $0.3731 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| get_customer_by_phone | 1 | ≥ $0.0000 |
| get_details_by_id | 2 | ≥ $0.0000 |
| Model-only calls | 17 | ≥ $0.0000 |

### tau2_telecom · task-bc8ca0547ea8467569796084d4a71d497ea107458a37e04026951d5e717bb710 · fixed $0.3731 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| mcp__environment__message | 9 | ≥ $0.0000 |
| mcp__environment__get_customer_by_phone | 1 | ≥ $0.0000 |
| mcp__environment__get_details_by_id | 3 | ≥ $0.0000 |

### tau2_telecom · task-ce50fefcf74db5153715126256ec00634d10c6128e0a7ddbb816eb7f218edfd5 · fixed $0.3731 (in_sample) · unknown · capped=False

| Tool group | Calls/events | Attributed model cost |
| --- | --- | --- |
| get_customer_by_phone | 1 | $0.0144 |
| Model-only calls | 7 | $0.1825 |
| Shared tools: get_data_usage, get_details_by_id | 1 | $0.0155 |
| get_details_by_id | 3 | $0.0653 |
| refuel_data | 1 | $0.0178 |

## Limits

This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.

Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.

Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.

Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.

Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.

Only sanitized metadata was written by moira. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one moira install only.

Seed: 0. Bootstrap draws: 2,000. Report generated: 2026-10-24T04:33:29.613156+00:00. No network requests are required to view this file.

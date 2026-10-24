# What this report saw

Benchmark tasks, not production. Metadata only: SHA-256 task IDs, hashed instance groups and run IDs, timestamps, model, token classes, recorded dollars, tool names and argument hashes, iteration-cap signals, and SWE-bench resolution outcomes. No prompts, completions, code, raw arguments, tool outputs or raw instance names were retained.

## Model comparison

Provider-correct pricing is the default. Shape statistics describe fully priced, uncapped tasks only; their n and the unpriced task count are explicit. Resolve rate uses known SWE-bench outcomes. Cost per resolved task is all observed spend on fully priced tasks divided by their confirmed resolutions, so failed attempts are included; censored costs make it a lower bound. Every archive repeats 500 instances across four runs, so the price and interval come from grouped cross-validation: five folds hold out 20% of instances with all their runs, and the price (mean of fold prices at the 70% target with a p99 cap) is fit on training instances only. The interval is the loss ratio of a held-out fold across 1,000 instance-bootstrap draws that refit every price. VIABLE requires both intervals below 90%. Unpriced tasks must be under 2% of the archive, and the verdict must also hold when each unpriced held-out task is scored at the training p99 cost; both verdicts are shown. Success-only billing charges only resolved tasks: the highest of 60/65/70% targets that passes the same rule is shown with its price per resolved task, beside the per-task price that bills every attempt. Missing tariffs or inconsistent token classes are unavailable, never zero cost.

| Model archive | Tasks | Unpriced tasks | Priced uncapped n | Mean USD | p90/p50 | p99 USD | Resolve rate | Outcome coverage | Cost per resolved task USD | 70% price + p99 cap USD (grouped CV) | Grouped-CV 90% loss-ratio interval, capped runs excluded | Grouped-CV 90% loss-ratio interval, capped runs inflated | Verdict, unpriced excluded | Verdict, unpriced at training p99 | Verdict | Success-only: highest viable target | Success-only price per resolved task USD | Harness iteration limit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claude-sonnet-3.7_4runs | 2000 | 0 (0.0%) | 1973 | 0.7156 | 2.3199 | 2.3600 | 60.3% | 1991/2000 | 1.2281 | 1.0171 | 61.7% – 79.1% | 60.1% – 81.0% | VIABLE | no unpriced tasks | VIABLE | 65.0% | 1.8030 | 100 |
| claude-sonnet-4.5_4runs | 2000 | 0 (0.0%) | 2000 | 1.8405 | 1.6745 | 4.5694 | 64.3% | 1995/2000 | 2.8712 | 2.6181 | 64.0% – 76.3% | 64.0% – 76.3% | VIABLE | no unpriced tasks | VIABLE | 70.0% | 4.0965 | 500 |
| claude-sonnet-4_4runs | 1999 | 1999 (100.0%) | 0 | Unavailable | Unavailable | Unavailable | 68.9% | 1994/1999 | Unavailable | Unavailable | Unavailable | Unavailable | NOT VIABLE | not tested: over the 2% limit | NOT VIABLE | Unavailable | Unavailable | 500 |
| gpt-5_4runs | 2000 | 3 (0.1%) | 1988 | 0.4096 | 2.0676 | 1.4743 | 59.8% | 1996/2000 | 0.6951 | 0.5810 | 61.2% – 79.5% | 60.6% – 80.1% | VIABLE | VIABLE (upper 79.9% / 80.4%) | VIABLE | 65.0% | 1.0471 | 100 |
| gpt_5.2_4runs | 2000 | 28 (1.4%) | 1972 | 0.7664 | 2.4776 | 3.2951 | 63.1% | 1991/2000 | 1.2023 | 1.0777 | 59.5% – 81.3% | 59.5% – 81.3% | VIABLE | VIABLE (upper 85.1% / 85.1%) | VIABLE | 60.0% | 1.9698 | 500 |
| kimi-k2_4runs | 2000 | 2000 (100.0%) | 0 | Unavailable | Unavailable | Unavailable | 54.8% | 1991/2000 | Unavailable | Unavailable | Unavailable | Unavailable | NOT VIABLE | not tested: over the 2% limit | NOT VIABLE | Unavailable | Unavailable | 500 |

## Per-model reports

- [claude-sonnet-3.7_4runs](claude-sonnet-3.7_4runs.md) ([HTML](claude-sonnet-3.7_4runs.html))
- [claude-sonnet-4.5_4runs](claude-sonnet-4.5_4runs.md) ([HTML](claude-sonnet-4.5_4runs.html))
- [claude-sonnet-4_4runs](claude-sonnet-4_4runs.md) ([HTML](claude-sonnet-4_4runs.html))
- [gpt-5_4runs](gpt-5_4runs.md) ([HTML](gpt-5_4runs.html))
- [gpt_5.2_4runs](gpt_5.2_4runs.md) ([HTML](gpt_5.2_4runs.html))
- [kimi-k2_4runs](kimi-k2_4runs.md) ([HTML](kimi-k2_4runs.html))

Harness budgets differ across archives (including 100 versus 500 iterations), so this is not a matched-budget model comparison. Each report includes grouped and leave-one-run-out holdouts, the leaky time split for contrast, success-only billing where outcomes and costs are usable, harness cap rates, cost audit, and source limitations.

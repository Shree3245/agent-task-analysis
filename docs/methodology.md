# Statistical choices

Costs are standard USD LLM token costs under the selected catalog. Unknown rates or
main usage produce an unpriced call. Any such call makes its task incomplete for
cost estimation; its known spend is still shown as a lower bound. A recorded cost
is not substituted for missing tokens to make a reconciliation check pass.

Per-type cost shape uses complete, uncapped tasks, linear-interpolated empirical
quantiles, and the costliest `ceil(n × fraction)` tasks for top 1%/5% spend shares.
When p50 is zero the p90/p50 ratio is undefined. Overall task weights are `1/(K*n_k)`;
overall quantiles invert that weighted empirical distribution and tail shares use
fractional weighted mass. A type with no usable costs is excluded from that
distribution and explicitly counted as unpriced; no overall completeness is implied.

Loop evidence is at least N identical `(tool_name, SHA-256(args))` events (default 3)
or more than twice that type's p99 model-call count. This is a diagnostic signal.
Dollar audit totals include known spend on incomplete/censored tasks and identify it
as a lower bound. Equal-type audit rates and dollar-per-task averages are shown
separately from actual total dollars.

Caps at p95/p99/p99.5 are fitted on uncapped tasks. p99 is the fixed recommended
policy. `min(task_cost, cap)` is an ideal ceiling. Headline cap simulations instead
replay sequential model calls, stop after a call crosses the ceiling, and pay the
full crossing call. If that was the last call, no remaining work was stopped.
Saved spend is unfinished work; this replay cannot establish its value or outcome.

Without a cap, price is training mean / target. With a cap, use the replayed training
mean / target. Evaluation loss ratio is mean evaluation cost / that fixed price;
tasks losing money have cost greater than price, and worst loss is max(0, max cost
minus price). Payment is assumed for stopped/failed tasks too in the per-task price;
refund-adjusted prices and success-only billing are separate scenarios (below).

Bootstrap intervals are percentiles 5 and 95 of 2,000 task resamples. Fit price and cap
once; keep them fixed when bootstrapping evaluation tasks. Re-fitting price in every
evaluation sample would force the ratio back to its target. A deterministic seed is
reported. Type-specific independent seeds support the overall arithmetic mean of
type loss ratios; the overall bootstrap resamples within types before averaging.

The temporal cutoff is `earliest_start + 2/3 × (latest_end - earliest_start)` over
the dataset. Training tasks ended before it; evaluation tasks started at or after
it. Exclude straddlers and missing-time tasks. No cap or censoring-tail parameter is
fit on the evaluation partition. In-sample rows are descriptive and cannot produce
a positive verdict.

When a type has a `task_group` that appears more than once (for example, the same
SWE-bench instance in four runs), a time split scores tasks it was fit on, so the
verdict uses grouped cross-validation instead. Five folds each hold out 20% of groups
with all their runs; code asserts that no group is in both training and scoring.
Mean price, p99 cap and censoring tail are fit on training groups only. Out-of-fold
results are pooled into the loss ratio, tasks-losing share and worst loss. Intervals
come from 1,000 seeded cluster-bootstrap draws: groups are drawn with replacement,
every copy of a drawn group stays in one fold, and the whole cross-validation is
refit. The verdict interval is the 5th–95th percentile loss ratio of a single
held-out fold across those draws (a price fit on 80% of groups, sold on unseen
groups). The pooled out-of-fold interval is reported beside it, but with refit mean
prices and equal fold sizes pooled cost over pooled revenue cancels to the target,
so it is not a risk measure. Leave-one-run-out (fit on the other runs, score one) is
reported when hashed run IDs exist; it answers "same tasks, new run". The time split
stays as a side column labeled as leaking repeated tasks. Types without repeated
groups keep the time split. Every report has a "Validation split per pricing pool"
table stating, for each task type, its sources, how many tasks carry a task_group,
how many groups repeat, the split the verdict used, and why.

Censored costs are shown under two scenarios: exclude capped runs; or include them
with an increment equal to the training type's mean cost at/above its p95. This is
a stress assumption, not an estimate of hidden completion costs. For capped replay,
the unknown increment is modeled as one indivisible future call, so its overshoot
is paid. This conservative choice avoids claiming that a cap eliminates an unknown
tail for free. If no uncapped training costs exist, the scenario is unavailable.

The 70% target with p99 cap earns VIABLE only when its holdout upper 90% interval is
strictly below 90%, in both censoring scenarios when relevant, with at least 30
uncapped training and 30 uncapped holdout tasks by default, and under 2% unknown task costs
(see the unpriced-task rule below).
The sample floor is configurable (`--min-samples`, minimum 2), but lowering it weakens
evidence. All other cases are NOT VIABLE with a reason. Missing evidence is not proof
of economic failure. The report flags censoring scenarios that fall on opposite sides
of the upper-interval threshold.

Unpriced tasks (an unknown model, tariff or token class) are never fit on. A pool can
be VIABLE only when they are under 2% of its tasks, and only if the rule also holds
when each unpriced held-out task is scored at the training pool's p99 cost (or its
known partial cost, if higher), charged as one indivisible call. Both verdicts are
reported. At 2% or more the pool is NOT VIABLE.

Success-only billing (benchmark pools with outcomes) charges only resolved tasks:
price = training cost / (target × training resolutions). Reports give the highest of
the 60%, 65% and 70% targets at which success-only pricing passes the same VIABLE
rule, its price per resolved task, and the per-task price that bills every attempt.

Refund-adjusted prices apply to pools with a known outcome and at least one task that
is not a confirmed success. Two rules are reported on each pool's verdict split, at
the target with the p99 cap: failed and aborted tasks are refunded (unknown outcomes
pay), and only confirmed successes pay (the pessimistic bound). A task stopped by the
cap is refunded under both. Refunded tasks keep their cost and pay nothing; price =
training spend / (target × billable training tasks), and the held-out loss ratio is
held-out spend over that price times billable held-out tasks. Time-split intervals
resample (cost, billable) pairs; grouped pools use the same cluster bootstrap with
refit. Each rule gets a verdict under the same VIABLE rule.

`--since` and `--until` restrict a report to tasks that started in that window (a
bare `--until` date includes the whole day, UTC); tasks without a start time are
left out and counted. All windows below end at the latest task start in the report,
never the wall clock, so a report is reproducible from its data.

Drift: per pool, the weekly mean cost of complete, uncapped tasks, and the ratio of
the last `--recent-days` days (default 30) to the fit window (the time-split
training period, or the whole pool under grouped CV). "Reprice recommended" is set
when that ratio moves more than 25% either way; windows under the sample floor are
flagged as small. Recency-window pricing reports, beside the full-period price, a
price fit on only the last N days of the training period, scored on the same
holdout, and the in-sample price of the last N days of all data (what a recent fit
charges now, not yet validated).

Price catalogs may list dated rate changes per model (`changes: [{effective:
YYYY-MM-DD, input: ..., ...}]`; unlisted classes carry forward). Each call is priced
at the rates in effect when it started. For each change date after the data ends,
the report reprices every task at the rates in effect on that date, keeping usage
and the time split fixed, and shows the pool's spend change, the loss ratio if the
current verdict price is kept, the refit price, and the last-N-day price.

`--rates FILE` applies user rates for unlisted models or contract rates (`models:`
and optional `aliases:` and `description:` in catalog format). An override replaces
the whole catalog entry for its model. The report names the override file by
SHA-256, lists replaced and added models, and labels each pool's share of spend
priced at override rates.

Intervals omit future model/tariff drift, correlated repeated benchmark tasks,
unobserved failures, and all uncertainty from learning the price itself. Benchmark
samples and production mixes differ. No inference includes non-LLM compute, tool
service charges, human review, taxes, support, or refunds unless already embedded in
recorded cost—in which case it can cause a token-price reconciliation mismatch.

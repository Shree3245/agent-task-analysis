# Agent Task Analysis

**What do your agent tasks cost—and would a fixed price survive the expensive ones?**

`agent-task-analysis` reads your local agent-log exports, stores metadata in DuckDB, and writes a
self-contained HTML report plus Markdown. No account, hosted service, telemetry,
LLM classifier, or network connection is needed.

## Quickstart: a report on your own traces in 5 minutes

**1. Install** (Python 3.11+):

```sh
git clone https://github.com/Shree3245/agent-task-analysis.git
cd agent-task-analysis
python -m pip install .
agent-task-analysis demo            # optional: writes demo-report.html from bundled sample data
```

**2. Load your traces.** Pick the line that matches where your traces live:

```sh
# Braintrust: fetches the project's logs directly (asks for the API key if unset)
export BRAINTRUST_API_KEY=sk-...
agent-task-analysis braintrust --project "Your Project" --redact-task-ids --out report.html
# ...that one command also writes the report: skip to step 4.

# A file or folder you exported (JSON, JSONL or Parquet):
agent-task-analysis ingest otel ./traces.json          # OpenTelemetry GenAI spans (OTLP JSON)
agent-task-analysis ingest langfuse ./langfuse-export.json
agent-task-analysis ingest langsmith ./runs.jsonl
agent-task-analysis ingest litellm ./spend-logs.json
agent-task-analysis ingest csv ./calls.csv --columns columns.yaml   # any table: see "Generic CSV"
```

Each source has its own export steps and field list under
[quickstarts by source](#five-minute-quickstarts-by-source).

**3. Write the report:**

```sh
agent-task-analysis report --redact-task-ids --out report.html
```

This reads `.agent-task-analysis/agent-task-analysis.duckdb`, the default database for `ingest`. It also writes
`report.md` next to the HTML. Nothing is sent anywhere. The report opens in your
browser when it's written; pass `--no-open` to skip that (it is also skipped when
output is piped or run from a script).

**4. Read the answer at the top.** The report opens on a plain-language summary:
one row per task type with a status (ready to price, ready but costs moved, needs more
runs, too unpredictable), the price per run, and the margin it kept on runs it wasn't
fitted on. Click a row for the cost histogram, a price slider that rescales the tested
margin for any price you pick, and the things to watch for that type. Prices there are
tested without the p99 cap, because nothing stops a run at the cap once a price is
published.

Each type is tested on its newest runs. When the report-wide split leaves fewer than 30
runs on either side, that type holds out its newest third (at least 30) and fits on the
runs before it, so a type with about 60 runs or more usually gets a test. The cutoff used
is shown per type.

The full technical report (verdicts, simulations, drift, refunds, caps) is under
**Full technical report** below the summary.

**If something looks off:**

- **Everything is NOT VIABLE with "unknown costs":** your models aren't in the built-in
  price list. See the *Unknown models* table, then add their rates with
  `--rates rates.yaml` (format in [methodology](docs/methodology.md)).
- **One task type called `unknown`:** your traces carry no task type. Assign types with
  `agent-task-analysis classify --map types.yaml` (rules by tool name or call count, or per-task
  overrides), or set `task_type` on your root spans and re-export.
- **Tasks look split or merged wrongly:** the source needs a task or trace ID on every
  call. *What this report saw* lists `inferred_task_identity` under import limitations
  when it had to guess.

## Install and try it

Python 3.11 or newer:

```sh
python -m pip install .
agent-task-analysis demo --out demo-report.html
```

For development:

```sh
uv sync --locked --group dev
uv run agent-task-analysis demo
uv run pytest -q                  # sockets blocked throughout the test suite
uv run ruff check src tests benchmarks
uv build
```

The distribution is named `agent-task-analysis`; the executable and import package are
`agent-task-analysis`. Install from this checkout or its wheel; publication to PyPI is not part
of this repository's setup. Installation itself may download dependencies. After
installation, ingest, classify, report, and demo work offline.

Demo uses 37 public Exgentic sessions, reduced to metadata only, with provenance and
the CDLA-Permissive-2.0 license bundled in the wheel. It uses an isolated temporary
database. These are benchmark tasks, not production workloads; recorded costs are
absent, so its reconciliation result is **UNAVAILABLE**, not an invented pass.

## What is collected—and what is not

Retained: task ID/type/source, timestamps, provider/model, input/cached-input/cache-write/
output/reasoning token counts, tool names, keyed HMAC-SHA-256 hashes of tool arguments,
nullable recorded costs, outcome enums, and cap flags/reasons. Derived bookkeeping
includes task call counts, event indexes, and links from tool events to model calls.

**Never retained:** prompts, completions, code, tool outputs, raw tool arguments,
arbitrary metadata, user/workspace identifiers, source paths, or freeform errors.
The reader parses original records in memory and constructs new allowlisted records
before writing. It never stages raw logs on disk. Diagnostics use fixed error codes
without payload excerpts or traceback locals. Original files are opened read-only.
Argument hashes can reveal repeated inputs; hashes are pseudonyms, not encryption.

Default commands do not fetch anything; `agent-task-analysis braintrust` (below) is an explicit
network opt-in. DuckDB external access and extension
auto-install/load are disabled. Reports contain inline SVG/CSS, no CDN, and a policy
that blocks external resources. The only runtime network opt-in is:

```sh
agent-task-analysis report --update-prices https://your-public-host/prices.v2.yaml \
  --prices-sha256 EXPECTED_SHA256 --out report.html
```

This fetches only the supplied public catalog URL and sends no log metadata. It
requires HTTPS, rejects credentials/query strings, bounds download size, validates
the catalog, and supports a pinned SHA-256. No project update endpoint is assumed.
To change rates without networking, use `--prices ./your-prices.yaml`. Catalog
entries may list dated rate changes (`changes:`), which price each call at the rate in
force when it ran and project future changes. `--rates ./overrides.yaml` adds rates
for unlisted models or contract rates; the report labels every price that uses them.

Read [the privacy boundary](docs/privacy.md) and [canonical schema](docs/schema.md).

## Your first report

```sh
agent-task-analysis ingest otel ./export.json --db .agent-task-analysis/company.duckdb
agent-task-analysis classify --map ./types.yaml --db .agent-task-analysis/company.duckdb
agent-task-analysis report --db .agent-task-analysis/company.duckdb --target 0.7 \
  --redact-task-ids --out report.html
```

`--since`/`--until` restrict the report to tasks that started in a date window, and
`--recent-days N` (default 30) sets the window for the drift section and the
recent-window price shown beside the full-period price.

`report.html` opens in your default browser when it is written (`--no-open` to skip;
never when stdout is not a terminal). `report.md` is written alongside it. Each report starts
with **What this report saw**, including source fields read, canonical fields kept,
missing-data warnings, and the statement that no content was retained.

The default database is `.agent-task-analysis/agent-task-analysis.duckdb`. Use a different `--db` per collection.
Use `--namespace run-02` when different runs reuse task IDs. A whole-task reimport is
idempotent; a different history for an existing task is rejected rather than appended
or silently overwritten. Ingest a complete export for a run, or use a fresh database
for an updated snapshot. Related flat spans should be ingested together.

Task types use this precedence: explicit mapping > source metadata > ordered
metadata-only rules > `unknown`. See [mapping](config/types.example.yaml),
[rules](config/classification.example.yaml), and [CSV columns](config/csv-columns.example.yaml).

### When each call is logged as its own run

A price is per run, so the tool has to know which calls belong to one run: a trace, a
`task.id`, or a CSV `task_id`. Auto-instrumentation without a parent span often gives
every model call its own trace, which makes every call a "run". The report warns when
most runs of a type are a single model call, and when a fifth or more of runs have no
task type. Fixing the traces is best: wrap each agent run in one parent span, or set
`task.id` on every call. For history that is already logged, `--gap` rebuilds runs:

```sh
agent-task-analysis ingest otel ./otel.json --gap 60
```

Within one task type, a run continues while each next call starts at most 60 seconds
after the previous one ended. Calls are also split by session or user ID when the
traces have one (`session.id`, `user.id` or `enduser.id` in OpenTelemetry;
`metadata.session_id` or `metadata.user_id` in Braintrust; `sessionId` or `userId` in
Langfuse; a `session` column in CSV), so concurrent users don't merge. That ID is
hashed in memory and never stored. Without it, the import warns
`gap_grouping_without_session`. The report labels gap-built runs as estimates.

## Five-minute quickstarts by source

All commands below operate on a local export. Exporting from a hosted logging product
is a separate action performed with that product's UI/API; agent-task-analysis never authenticates
to it. A directory input recursively reads supported files. Keep unrelated exports
and downloaded manifest files outside the directory passed to `ingest`.

### OpenTelemetry GenAI

Save the collector's OTLP **JSON** export, an SDK JSON span array, or span-per-line
JSONL. Supported envelopes include `resourceSpans → scopeSpans → spans`, flat spans,
and session objects with `spans`. Binary protobuf is not supported. Preserve trace IDs,
timestamps, `gen_ai.request.model`, and usage attributes. Prefer `task.type` and
`task.outcome`; otherwise classification uses tool metadata.

```sh
agent-task-analysis ingest otel ./otel.json --db .agent-task-analysis/otel.duckdb
agent-task-analysis report --db .agent-task-analysis/otel.duckdb --out otel-report.html
```

Tool events use `gen_ai.tool.name` and `gen_ai.tool.call.arguments`; tool calls inside
`gen_ai.output.messages` are also supported. Message text is discarded. See
[the OTLP fixture](tests/fixtures/otel/sample.json).

### Braintrust

One command fetches a project's logs, imports metadata only, and writes the report:

```sh
export BRAINTRUST_API_KEY=...        # or leave unset to be prompted; never stored
agent-task-analysis braintrust --project "Support Bot" --redact-task-ids
```

Each trace (`root_span_id`) is one task. LLM spans are model calls (`metadata.model`,
`metrics.prompt_tokens`, `prompt_cached_tokens`, `prompt_cache_creation_tokens`,
`completion_tokens`, `completion_reasoning_tokens`; Braintrust's prompt and completion
totals include the cache and reasoning classes). Tool spans and tool calls in LLM
output are hashed for loop detection. The root span's `metadata.task_type` (or its span
name) is the task type, and `metadata.outcome` (or an error on the root span) the
outcome. Scorer spans are skipped. Options: `--org` when a project name exists in several
organizations, `--api-url https://api-eu.braintrust.dev` or a self-hosted data plane,
`--days` (default 90), `--settle-minutes` (default 30: traces active more recently may
still be running and are left out), and the usual report flags. Each run writes a new
database under `.agent-task-analysis/`. Saved fetch responses or JSON/JSONL exports of the same events
import with `agent-task-analysis ingest braintrust FILE`.

### Langfuse

Export traces with their observations, or generation/observation records retaining
`traceId`. Keep `usageDetails`/`usage`, `model`, start/end times, and optional
`calculatedTotalCost`/`costDetails.total`. Put task type/outcome in designated
`metadata.task_type`/`metadata.outcome` fields. Generations are billed; trace totals
and unrelated spans are not counted again.

```sh
agent-task-analysis ingest langfuse ./langfuse-export.json --db .agent-task-analysis/langfuse.duckdb
agent-task-analysis report --db .agent-task-analysis/langfuse.duckdb --out langfuse-report.html
```

[Supported fixture](tests/fixtures/langfuse/sample.json).

### LangSmith

Export a run tree with `child_runs`, or flat runs retaining `trace_id`. Preserve
`run_type`, `usage_metadata` or `outputs.llm_output.token_usage`, timestamps, optional
`total_cost`, and `extra.metadata.ls_model_name`/`ls_provider`. Task-type metadata
on a root is inherited by nested children.

```sh
agent-task-analysis ingest langsmith ./langsmith-runs.jsonl --db .agent-task-analysis/langsmith.duckdb
agent-task-analysis report --db .agent-task-analysis/langsmith.duckdb --out langsmith-report.html
```

[Supported fixture](tests/fixtures/langsmith/sample.json). A span called “successful”
does not establish that its parent task succeeded; retain task outcome metadata.

### LiteLLM spend logs

Export spend-log rows as JSON/JSONL, retaining `request_id`, `model`, `spend`, token
counts/details, `startTime`/`endTime`, and task/session metadata. If no task/session
identifier exists, each request becomes one task and the report flags that fallback.

```sh
agent-task-analysis ingest litellm ./spend.jsonl --db .agent-task-analysis/litellm.duckdb
agent-task-analysis report --db .agent-task-analysis/litellm.duckdb --out litellm-report.html
```

[Supported fixture](tests/fixtures/litellm/sample.json). Costs and tokens must describe
the same individual call; aggregate dashboard totals are not a call-level export.

### mini-swe-agent

Point at `.traj`/JSON files containing `messages` and `info`. Assistant-message usage
is read when available; `info.exit_status` supplies terminal/limit information.
Aggregate-only model statistics do not become invented per-call token counts.

```sh
agent-task-analysis ingest mini-swe-agent ./mini-trajectories/ --namespace run-01 --db .agent-task-analysis/mini.duckdb
agent-task-analysis report --db .agent-task-analysis/mini.duckdb --out mini-report.html
```

[Supported fixture](tests/fixtures/mini-swe-agent/sample.json). ASSERT-KTH's nano-agent
`detailed_predictions` variant is accepted, but aggregate-only token usage remains
unpriceable. Missing IDs use a digest of local file structure; paths are not retained.

### SWE-agent

Use `.traj` files containing `trajectory` steps plus `info`. Each step's `usage` or
`model_usage` supplies call tokens. Shell actions are hashed as arguments under
the tool name `shell`; commands are never stored or used for classification.

```sh
agent-task-analysis ingest swe-agent ./swe-trajectories/ --namespace run-01 --db .agent-task-analysis/swe.duckdb
agent-task-analysis report --db .agent-task-analysis/swe.duckdb --out swe-report.html
```

[Supported fixture](tests/fixtures/swe-agent/sample.json). Turn, dollar, and timeout
exit statuses map to controlled cap reasons, never copied error strings.

### OpenHands

Use event JSON, completion JSON with `response.usage`, or `output.jsonl` task rows
containing `metrics.token_usages` and aligned `metrics.costs`. The latter retains
per-call histories without counting the separately exported completion logs twice.
When using individual completion files, preserve task IDs or use the benchmark
archive reader for the published run/task directory layout.

```sh
agent-task-analysis ingest openhands ./output.jsonl --namespace run-01 --db .agent-task-analysis/openhands.duckdb
agent-task-analysis report --db .agent-task-analysis/openhands.duckdb --out openhands-report.html
```

[Supported fixture](tests/fixtures/openhands/sample.json). See
[benchmark instructions](benchmarks/README.md) for Bai's tar archives. Compact `_mini`
archives retain final completions only and cannot establish full task costs.

### HAL

Download traces explicitly and decrypt them with HAL's official script, outside this
repository. Agent Task Analysis accepts the decrypted envelope's `raw_logging_results` or Weave
call records. It uses `weave_task_id` where available, call usage, timestamps, and
evaluation success/failure IDs; parent summaries are not deliberately treated as
additional model calls.

```sh
# Decryption instructions and the pinned public script are documented separately.
agent-task-analysis ingest hal ./decrypted-evaluation.json --db .agent-task-analysis/hal.duckdb
agent-task-analysis report --db .agent-task-analysis/hal.duckdb --out hal-report.html
```

[Decrypt steps](benchmarks/README.md#hal-decryption),
[supported fixture](tests/fixtures/hal/sample.json). Do not commit decrypted files.

### Generic CSV

Copy the example column configuration, map your headings to canonical fields, and
declare whether token classes are `exclusive` or provider `native`. Do not map
prompts or outputs to metadata fields. Unknown/absent usage must be blank, not zero.

```sh
cp config/csv-columns.example.yaml columns.yaml
# Edit columns.yaml to match your local CSV headings.
agent-task-analysis ingest csv ./calls.csv --columns columns.yaml --db .agent-task-analysis/csv.duckdb
agent-task-analysis report --db .agent-task-analysis/csv.duckdb --out csv-report.html
```

Columns for IDs, models, usage, timestamps, tools, outcomes, and caps are supported;
arbitrary transformation expressions are not. [Supported fixture](tests/fixtures/csv/sample.csv).

## How to read the report

1. **Coverage first:** unknown models, missing usage, inferred task boundaries, and
   missing timestamps affect what can be concluded. Unknown-cost tasks remain visible
   with their known spend as a lower bound; they cannot be counted as free tasks.
2. **Cost shape and audit:** examine tails, repeat signals, failed/aborted spend, and
   the difference between recorded costs and standard-rate token costs. A repeat is
   evidence of repetition, not proof that the action was wasteful.
3. **Caps:** p95/p99/p99.5 show unfinished work and spend avoided. The recommended
   default is p99. Realistic replay pays the crossing call's overshoot; an idealized
   exact dollar ceiling is shown separately. Agent Task Analysis does not enforce a live cap.
4. **Fixed prices:** price is mean cost / target loss ratio; default targets are
   60%, 70%, and 80%. `--target` adds/selects another target while preserving the
   70% verdict scenario. Prices differ with/without the cap.
5. **Intervals/backtest:** the 90% intervals use 2,000 seeded task resamples. Prices
   and caps stay fixed during evaluation. Training ends two-thirds through elapsed
   time; evaluation starts in the final third. Boundary-straddling tasks are excluded.
6. **Censoring:** compare capped runs excluded against a disclosed tail-inflation
   scenario. The latter is an assumption, not their actual completion cost.
7. **Verdicts:** `VIABLE` requires the holdout upper interval below 90% at the 70%
   target with the p99 cap (grouped cross-validation replaces the time split when a
   `task_group` repeats; see `docs/methodology.md`), adequate uncapped samples in both partitions (default 30),
   and agreement under censoring sensitivity. `NOT VIABLE` may mean poor economics
   **or insufficient evidence**; the report names the reason. Unknown costs on 2% or
   more of a pool prevent a positive verdict; below that, the verdict must also hold with
   each unpriced task at the training p99 cost. In-sample economics alone cannot establish viability.

Overall distributions give every task type equal probability mass. Overall loss
ratios are arithmetic means of type loss ratios, with within-type bootstrap draws.
Accounting totals and maximum single-task loss retain their ordinary meanings.
Receipts show model calls grouped by tool name, charge each model call once, and
show no token counts. Tool service fees, compute, review, and refunds are not inferred.

Task IDs, task groups and tool arguments are hashed at ingest with HMAC-SHA-256 under a
per-install secret (`~/.agent-task-analysis/secret`, mode 600, never stored in a database or report),
so raw IDs never reach the database or a report. Hashes are consistent within one
install only; see [privacy](docs/privacy.md).
`--redact-task-ids` additionally re-aliases them in HTML and Markdown. Review tool/type labels
before sharing: hashing IDs does not make all metadata anonymous.

See [methodology](docs/methodology.md) and [public runs](benchmarks/README.md).
Code is Apache-2.0; bundled demo data has its own license.

## Validation status and limits

All adapter fixtures and the canary/offline suite are tested locally. Standard-rate
reference fixtures reconcile at 100%. Public runs deliberately retain missing data
and discrepancies: the Bai four-run Sonnet 3.7 export **does not meet the requested
99% recorded-cost agreement gate**. Its recorded totals match an extra base-input
charge on cache-write tokens; the report diagnoses this without changing rates.
The [Appendix B investigation](benchmarks/results/BAI_ACCOUNTING.md) reproduces
that arithmetic but finds different conventions across Claude exports, zero-cost
Qwen records, and missing native input counts. The proposed source-formula mode
was therefore not enabled; its prerequisite checks did not both hold.
The other selected public exports do not supply comparable per-call recorded costs.
See [the measured run results](benchmarks/results/RESULTS.md) for exact counts and scope.

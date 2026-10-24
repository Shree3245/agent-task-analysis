# Canonical local schema

DuckDB contains exactly two data tables. Schema version 4 is stored in the JSON
manifest in the `tasks` table comment. Export source formats and warnings are in
that manifest; raw values and input paths are not.

`calls` has: `task_id`, `call_idx`, `ts_start`, `ts_end`, `provider`, `model`,
`input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`,
`reasoning_tokens`, `tool_name`, `tool_args_hash`, `recorded_cost`, `capped`,
`event_kind`, and `parent_call_idx`. The primary key is `(task_id, call_idx)`.

`tasks` has: `task_id`, `task_type`, `source`, `started_at`, `ended_at`, `n_calls`,
`outcome`, `capped`, `cap_reason`, and `task_group`. The primary key is `task_id`.

`task_id` is the keyed HMAC-SHA-256 of `source[:namespace]:source-id`, computed at
ingest for every source; raw source IDs are never stored. Explicit overrides in
`classify --map` may still name the source ID (`otel:trace-001`); moira hashes it to
match. The manifest's `hash_key` is a fingerprint of the install key (never the key);
databases without a matching fingerprint (another install, or schema 3 and earlier)
are readable but refuse further writes.

`task_group` is optional: what makes two tasks the same work. For benchmark sources it
is the keyed HMAC-SHA-256 of the instance ID (OpenHands/Bai, SWE-agent and mini-swe-agent set it;
other adapters leave it null). Only the hash is stored, never the instance name.
Version 1 databases gain an empty `task_group` column the next time they are opened
for writing.

Extensions to the initial brief are `provider` (required by its privacy allowlist)
and `event_kind`/`parent_call_idx`. A model event owns tokens/cost exactly once.
Each tool event holds one tool name/hash, optionally linked to that model event.
Tool-only rows do not count as unpriced models. `n_calls` counts model events.
This preserves multi-tool turns without copying the same billed tokens onto each tool.

Token classes are non-overlapping after normalization. Main input/output counts
remain null when absent; absent optional cache/reasoning classes are treated as zero
and disclosed as an export-coverage assumption. Reasoning is priced at output rates.
USD recorded costs remain separate from recomputed cost, which is derived during
analysis and not stored as a second source of truth.

Timestamps are UTC ISO-8601 strings. Naive source timestamps are interpreted as UTC;
exports should include offsets. Missing times remain null. Stable chronological
ordering retains source order for ties and missing time. Do not infer a real temporal
backtest from exports that omitted time information.

Outcomes: `success`, `fail`, `aborted`, `unknown`. Cap reasons: `turn_limit`,
`dollar_limit`, `time_limit`, `other_limit`, or null. A failure alone is not a cap.
Task metadata is bounded and type-checked; negative/nonfinite usage or costs,
inconsistent token classes, reversed timestamps, and conflicting identities fail
with safe errors. Known event IDs deduplicate exact repeated spans; conflicting
events are rejected. Full-task reimports are idempotent; different snapshots require
a fresh database or explicit run namespace.

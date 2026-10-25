# Privacy boundary

Raw files are read-only inputs. `adapters/` constructs `Task` and `Call` records,
never a copied provider dictionary. Token counts and timestamps are normalized;
outcomes/cap reasons become enums. Tool arguments are canonicalized in memory and
hashed with keyed HMAC-SHA-256 (see below). Prompts, completions, source code, tool output, freeform
errors, original paths, and arbitrary attributes are never passed to storage.

DuckDB receives sanitized Python records through Arrow. Both tables and the ingest
manifest contain metadata only. The manifest lives in the `tasks` table comment,
so it commits transactionally with the data and no third data table is needed.
Database/WAL files, reports, and temporary demo files therefore contain no raw content.
The parser does not implement a raw-input cache, dead-letter queue, or debug dump.

The CLI catches parser/database exceptions without printing their messages or locals:
those exceptions can quote the rejected input. It emits fixed safe error codes.
Raw source contents still occupy process memory while being parsed. The guarantee
covers agent-task-analysis's writes, not OS swap, external profilers, shell history, or crash collectors.

`tests/test_privacy.py` generates a random canary in memory and injects it into each
source's prompts, outputs, and nested tool arguments. Original inputs are outside
the test work directory. Ingest, classify and report run inside the work directory;
tests scan every resulting file and decoded database record as well as stdout/stderr.
Decoded scans matter because raw-byte scans alone can miss compressed database values.
Malformed-record tests verify that parser errors do not leak payloads.

The full unit suite blocks sockets with pytest-socket. DuckDB external access,
extension loading, and auto-install are disabled. HTML uses inline SVG/CSS with a
restrictive Content Security Policy. The package imports no provider SDK or telemetry.

There are two runtime network opt-ins, and nothing else touches the network.
`report --update-prices HTTPS_URL` downloads a price catalog: it sends no metadata,
rejects credentials/query strings, validates the catalog, and supports SHA-256
verification. `agent-task-analysis braintrust --project NAME` reads that project's logs from the
Braintrust API (HTTPS only) with an API key taken from `BRAINTRUST_API_KEY` or a hidden
prompt; the key is never stored or printed. The API returns whole spans, so prompts and
completions do cross the network into memory: each event is cut down to allowlisted
metadata (IDs, span name/type, model, provider, numeric metrics, and the `task_type`,
`outcome`, `capped` and `cap_reason` metadata keys) as soon as its page arrives, error
text is reduced to its presence, and tool arguments are kept only until they are
hashed. Nothing raw is written to disk, and the project name is not stored. Separate `benchmarks/` scripts explicitly download
public research data; they are not installed as runtime CLI commands. HAL decryption
uses the upstream script outside this repo, not agent-task-analysis's ingest code.

## Keyed hashing

Task IDs, task groups, benchmark run IDs and tool arguments are hashed with
HMAC-SHA-256 under a random 32-byte secret, generated on first run at `~/.agent-task-analysis/secret`
(directory mode 700, file mode 600; override the directory with `AGENT_TASK_ANALYSIS_HOME`). The
secret is never written to a database or a report. Each kind of value is hashed in its
own domain, so a task ID and a tool argument with the same text do not collide.

Without the secret, a hash cannot be reversed by hashing candidate names, which plain
SHA-256 of a public benchmark instance allowed. The cost is that **hashes are
consistent within one install only**: the same task ingested on another machine, or
after the secret is deleted, gets different IDs, groups and argument hashes. Back up
the secret if you need to add to a database later. Each database records a short
fingerprint of its key (an HMAC of a fixed label, not the key) and refuses writes from
a different install; reading and reporting still work. Analysis results do not depend
on the key: grouped folds and bootstrap draws are ordered by each group's own cost
data, not its hash.

Task IDs are hashed at ingest, for every source, before anything is stored; the
database and every report hold only the hash. Databases from before keyed hashing hold
raw IDs or plain SHA-256: reports still read them (raw IDs are hashed on load), and agent-task-analysis
refuses to write more tasks into them. Treat hashes as pseudonyms, not anonymization.

Metadata values can themselves be sensitive: task types, tool names, timing, models,
and repeated argument hashes reveal patterns. `--redact-task-ids` re-aliases the
stored hashes in both reports so they cannot be matched against the local database.
Do not intentionally map content columns into allowlisted metadata fields.

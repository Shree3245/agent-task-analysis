# Public benchmark runs

These are **benchmark tasks, not production workloads**. Download scripts are
explicit research utilities, separate from the offline CLI. Raw inputs and decrypted
HAL data must live outside the repository. Reports contain only sanitized metadata.

Exact repositories, revisions, project pages, and known licenses are pinned in
[`sources.yaml`](sources.yaml). Downloads record SHA-256 checksums and sizes and
verify Hugging Face LFS hashes when supplied. The scripts support resume, explicit
file selection, and multiple download workers. `--max-files` explicitly selects a
subset; omit it to download all matching files. Do not accidentally download hundreds
of GB: review the sizes printed by the scripts and choose an appropriate glob.

Run from the repository root after `uv sync --locked --group dev`:

```sh
DATA_DIR="$HOME/agent-task-analysis-public-data"  # outside the repository; contains public raw data
mkdir -p "$DATA_DIR"
```

## Bai et al. OpenHands / SWE-bench Verified

The [paper project page](https://longjubai.github.io/agent_token_consumption/)
links to [loong0814/openhands_trajectories](https://huggingface.co/datasets/loong0814/openhands_trajectories).
This association was verified, not inferred from a similarly named dataset.
The supplied report uses the full Claude Sonnet 3.7 archive: four runs, 2,000 final
task trajectories. Other models and intermediate critic attempts are outside its scope.

```sh
uv run python benchmarks/download_openhands_bai.py \
  --out "$DATA_DIR/openhands-bai" --include 'claude-sonnet-3.7_4runs.tar.gz'
uv run python benchmarks/run_reports.py openhands-bai \
  --raw "$DATA_DIR/openhands-bai" --db "$DATA_DIR/bai.duckdb" \
  --out benchmarks/results/openhands-bai.html
```

`run_reports.py` streams final `output.jsonl` members directly from the archive and
uses aligned `metrics.token_usages`/`metrics.costs`. It joins SWE-bench Verified
resolution from the archive's `report.json` files by run and `instance_id` (shared
with `analyze_bai_models.py` in `bai.py`); instances without a result stay unknown. It never extracts raw members to
the repository. Separate completion files and intermediate critic snapshots are not
billed again. The `_mini.tar.gz` releases each retain one final completion per task;
the runner rejects those as evidence of complete task costs. The full collection is
about 42 GB compressed. Use another full-archive glob to include more models; raw
costs describe retained trajectories, not all discarded attempts or evaluation overhead.

The separate [Bai accounting investigation](results/BAI_ACCOUNTING.md) documents
the Appendix B formula, five raw token records, cross-model checks, and the
provider-correct verdict rerun. `audit_bai_costs.py` reproduces the source formula
as an offline diagnostic; it does not alter default pricing or its acceptance gate.

## ASSERT-KTH agentic-evals-artifacts

[Dataset](https://huggingface.co/datasets/ASSERT-KTH/agentic-evals-artifacts),
[authors' framework](https://github.com/ASSERT-KTH/agentic-evals-lab), CC-BY-4.0.
Credit: Bjarni Haukur Bjarnason, André Silva, and Martin Monperrus,
*On Randomness in Agentic Evals*, arXiv:2602.07150.

```sh
uv run python benchmarks/download_assert_kth.py --out "$DATA_DIR/assert-kth" \
  --include 'nano-agent-Qwen_Qwen3-32B-temp0/run_0/detailed_predictions.jsonl'
uv run python benchmarks/download_assert_kth.py --out "$DATA_DIR/assert-kth" \
  --include 'r2e-gym-Qwen_Qwen3-32B/traj_qwen32b_run_0/*.jsonl'
uv run python benchmarks/run_reports.py assert-kth \
  --raw "$DATA_DIR/assert-kth" --db "$DATA_DIR/assert.duckdb" \
  --out benchmarks/results/assert-kth.html
```

The supplied combined report includes those two runs (both scaffolds). Nano-agent
has aggregate token totals only; R2E-Gym includes per-step prompt/completion counts.
The hosted-vLLM model has no supplied dollar tariff, and absolute timestamps are
absent. Prices/backtests remain unavailable rather than being invented. Full JSONL
downloads are supported by omitting `--include` (about 48 GB for the full repository).
Prediction-only `preds.jsonl` is skipped; it cannot supply usage metadata.

## Exgentic agent-llm-traces

[Dataset](https://huggingface.co/datasets/Exgentic/agent-llm-traces),
CDLA-Permissive-2.0. The supplied report uses **all 39 v1 shards**, 1,781 sessions.
The similarly named v2 dataset is a different release and is not silently substituted.

```sh
uv run python benchmarks/download_exgentic.py --out "$DATA_DIR/exgentic"
uv run python benchmarks/run_reports.py exgentic \
  --raw "$DATA_DIR/exgentic" --db "$DATA_DIR/exgentic.duckdb" \
  --out benchmarks/results/exgentic.html
```

These are local Parquet sessions containing OTel spans. Per-call recorded cost and
cache breakdowns are absent. Cloud-provider model identifiers without explicit
catalog rates remain unknown; do not map them to a different provider's tariff by
guessing. A metadata-only subset of directly priced sessions is bundled for demo.

## HAL decryption

[HAL project](https://hal.cs.princeton.edu/),
[published traces](https://huggingface.co/datasets/agent-evals/hal_traces).
The report uses one GPT-4.1 SciCode evaluation (65 tasks, 288 calls); the complete
collection is about 113 GB. No data license is declared in the inspected dataset
metadata, so raw/decrypted traces are not redistributed here.

```sh
uv run python benchmarks/prepare_hal.py --out "$DATA_DIR/hal" \
  --include 'scicode_scicode_zero_shot_agent_gpt4120250414_1745265933_UPLOAD.zip'
curl --fail --location https://hal.cs.princeton.edu/static/downloads/hal-decrypt.sh \
  --output "$DATA_DIR/hal/hal-decrypt.sh"
# Inspect the official script before running it. It writes decrypted JSON beside the ZIP.
uv run --with cryptography bash "$DATA_DIR/hal/hal-decrypt.sh" \
  -F "$DATA_DIR/hal/scicode_scicode_zero_shot_agent_gpt4120250414_1745265933_UPLOAD.zip"
uv run python benchmarks/run_reports.py hal \
  --raw "$DATA_DIR/hal" --db "$DATA_DIR/hal.duckdb" \
  --out benchmarks/results/hal.html
```

The official script also supports `-D "$DATA_DIR/hal"`. Decryption is separate from
agent_task_analysis. The adapter reads `raw_logging_results`, uses `weave_task_id`, and imports
evaluation outcome IDs. It skips aggregate parent spans when child calls exist.
Never commit the script's decrypted JSON or input ZIP files.

## Reproduce and verify reports

Every report includes its scope, benchmark warning, missing-data limits, and catalog
version/hash. A companion `.provenance.json` records source revision and downloads.
Downloading additional files into one source directory lets the runner combine the
selected evaluations in one database/report. Use a fresh DB if adapter logic or input
snapshots change; conflicting reimports are deliberately rejected.

Optional browser QA uses an isolated headless Chrome context with networking disabled:

```sh
uv run --with playwright python benchmarks/verify_render.py \
  benchmarks/results/openhands-bai.html --out benchmarks/results/qa
```

It checks all seven sections, SVG charts, zero external requests, no JavaScript
errors, and desktop/mobile page bounds, then saves screenshots. This developer-only
utility is not shipped as a runtime command or invoked by ingest/report.

See [measured results and the unresolved reconciliation gate](results/RESULTS.md).

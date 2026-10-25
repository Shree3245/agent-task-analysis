"""Offline benchmark ingestion. Raw archive members are parsed in memory, never extracted."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from bai import RESOLUTION_FIELDS, read_archive
from agent_task_analysis.adapters.base import Context
from agent_task_analysis.cli import write_report
from agent_task_analysis.ingest import ingest
from agent_task_analysis.storage import connect, save, manifest


BAI_ACCOUNTING_LIMITS = [
    "Bai Appendix B Eq. 1–2 charges (prompt_tokens - cache_read_tokens) at the base "
    "input rate, then also charges cache creation. If prompt_tokens includes cache "
    "creation, this double counts writes at the base-input rate. The full Sonnet 3.7 "
    "selection matches this formula on 88,439/88,439 calls within 1%; provider-correct "
    "pricing remains the default and its recorded-cost check remains FAIL. This "
    "arithmetic agreement does not independently establish native token semantics "
    "or an actual provider invoice.",
    "The cross-model check does not justify a universal Bai source-formula mode: "
    "the final-completion samples for GPT-5 and Sonnet 4.5 already match standard "
    "rates; Qwen records zero cost with no supported hosted tariff; Sonnet 4 has "
    "cache reads plus writes exceeding prompt_tokens. Five inspected Sonnet 3.7 "
    "raw records omit native input_tokens, so prompt = native input + cache writes "
    "+ cache reads cannot be checked independently. See benchmarks/results/BAI_ACCOUNTING.md "
    "for the pinned sources, scope and metadata-only evidence. These samples are "
    "call-level diagnostics, not additional complete tasks in this report.",
]


def bai_archive(path, db):
    if "_mini" in path.name:
        raise ValueError(
            "Compact Bai archives retain final completions only; use full archives for task costs"
        )
    ctx = Context("openhands", namespace=path.name.removesuffix(".tar.gz"))
    archive = read_archive(path, ctx)
    tasks = list(archive.tasks.values())
    evidence = {
        "source": "openhands",
        "adapter_version": 2,
        "files": 1,
        "records": archive.rows,
        "tasks": len(tasks),
        "fields_read": sorted(ctx.fields | RESOLUTION_FIELDS),
        "warnings": ctx.warnings,
        "benchmark": True,
        "content_retained": False,
        "token_semantics": "native",
        "scope": "Bai et al.; final output.jsonl task histories in "
        + path.name
        + "; intermediate critic attempts and other model archives excluded. Costs describe retained final trajectories, not all evaluation/retry overhead. Resolution is joined by run and instance_id from the SWE-bench Verified report.json results in the archive.",
        "non_completion_members_skipped": archive.skipped,
    }
    with connect(db) as conn:
        result = save(conn, tasks, evidence)
        data = manifest(conn)
        extra = archive.manifest()
        data["benchmark_assignments"] = data.get("benchmark_assignments", {}) | extra.pop("benchmark_assignments")
        for key, value in extra.items():
            data[key] = data.get(key, 0) + value if isinstance(value, int) else data.get(key, {}) | value
        serialized = json.dumps(data).replace("'", "''")
        conn.execute(f"COMMENT ON TABLE tasks IS '{serialized}'")
    print(path.name + ": resolution join " + json.dumps(Counter(t.outcome for t in tasks)), flush=True)
    return result


def note_scope(db, text, notes=None):
    with connect(db) as conn:
        data = manifest(conn)
        data["benchmark_scope"] = text
        data["benchmark_limit_notes"] = notes or []
        serialized = json.dumps(data).replace("'", "''")
        conn.execute(f"COMMENT ON TABLE tasks IS '{serialized}'")


def run(source, raw, db, output):
    raw, db, output = Path(raw), Path(db), Path(output)
    if source == "openhands-bai":
        archives = sorted(p for p in raw.glob("*.tar.gz") if "_mini" not in p.name)
        if not archives:
            raise ValueError("Need full Bai archives; mini archives cannot establish task costs")
        for archive in archives:
            print(bai_archive(archive, db), flush=True)
        scope = f"Selected full Bai archives: {len(archives)}. The repository contains additional model archives."
    elif source == "exgentic":
        print(ingest("otel", raw / "data", db, benchmark=True), flush=True)
        scope = f"Exgentic v1: {len(list((raw / 'data').glob('*.parquet')))} of 39 published parquet shards. Missing cache breakdowns may overstate list-rate cost. Cloud-model rates without explicit catalog entries remain unknown."
    elif source == "assert-kth":
        inputs = sorted(
            p
            for p in raw.rglob("*.jsonl")
            if p.name == "detailed_predictions.jsonl" or ("r2e-gym" in str(p) and "eval" in p.name)
        )
        for path in inputs:
            namespace = hashlib.sha256(str(path.relative_to(raw).parent).encode()).hexdigest()[:16]
            model = "Qwen/Qwen3-32B" if "Qwen3-32B" in str(path) else "unknown"
            print(
                ingest(
                    "mini-swe-agent" if path.name == "detailed_predictions.jsonl" else "swe-agent",
                    path,
                    db,
                    namespace=namespace,
                    options={"model": model},
                    benchmark=True,
                ),
                flush=True,
            )
        scope = f"ASSERT-KTH subset: {len(inputs)} evaluation files across the selected scaffolds. Nano-agent lacks per-call token classes; R2E-Gym has step tokens. Absolute timestamps and hosted-vLLM dollar rates are unavailable. No costs are fabricated."
    else:
        inputs = sorted(p for p in raw.glob("*.json") if p.name != "download-manifest.json")
        for path in inputs:
            namespace = hashlib.sha256(path.stem.encode()).hexdigest()[:16]
            print(ingest("hal", path, db, namespace=namespace, benchmark=True), flush=True)
        scope = f"HAL subset: {len(inputs)} explicitly downloaded and decrypted evaluations. Decryption used HAL's published script outside this repository."
    note_scope(db, scope, BAI_ACCOUNTING_LIMITS if source == "openhands-bai" else None)
    summary = write_report(db, output, redact=True)
    manifest_path = raw / "download-manifest.json"
    provenance = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    summary |= {"scope": scope, "benchmark_not_production": True, "download": provenance}
    output.with_suffix(".provenance.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != "download"}), flush=True)
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", choices=["openhands-bai", "assert-kth", "exgentic", "hal"])
    p.add_argument("--raw", required=True, type=Path)
    p.add_argument("--db", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    run(args.source, args.raw, args.db, args.out)

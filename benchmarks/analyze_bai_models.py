"""Offline multi-model Bai analysis: run-specific resolution joins and grouped folds."""

import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path

from bai import RESOLUTION_FIELDS, read_archive
from moira.adapters.base import Context
from moira.pricing.catalog import load_catalog
from moira.report.model import make_report
from moira.report.render import render
from moira.storage import connect, save, load, manifest


def ingest_archive(path, db):
    if db.exists():
        with connect(db, read_only=True) as conn:
            if manifest(conn).get("bai_analysis_version") == 3:
                print(path.name + ": reusing sanitized analysis metadata", flush=True)
                return
        raise ValueError("Use a fresh database for the enriched analysis")
    ctx = Context("openhands", namespace=path.name.removesuffix(".tar.gz"))
    ctx.options["inconsistent_usage_as_unknown"] = True
    archive = read_archive(path, ctx)
    tasks = list(archive.tasks.values())
    evidence = {"source": "openhands", "adapter_version": 2, "files": 1, "records": archive.rows,
                "tasks": len(tasks), "fields_read": sorted(ctx.fields | RESOLUTION_FIELDS),
                "warnings": ctx.warnings, "benchmark": True, "content_retained": False,
                "scope": "Final output.jsonl trajectories; resolution joined by archive run and instance_id. Critic intermediates excluded."}
    with connect(db) as conn:
        save(conn, tasks, evidence)
        data = manifest(conn)
        data.update(bai_analysis_version=3,
                    benchmark_scope=f"Bai SWE-bench Verified: {path.name}. Benchmark tasks, not production.",
                    **archive.manifest())
        data["benchmark_limit_notes"] = [
            "Resolution is joined within each run by instance_id using SWE-bench report.json results. Empty patches are unresolved; missing/error-only results remain unknown. Instance IDs are retained only as the hashed task_group; run IDs only as hashes for leave-one-run-out.",
            "Five grouped folds keep all repeats of an instance together. Leave-one-run-out can still share instances with its training runs. Group-bootstrap draws refit every fold price; model-selection uncertainty is not captured.",
            "Costs use the supplied token classes and provider-correct exclusive pricing. Unresolvable token conventions and unsupported route tariffs remain unpriced. Cost per success includes failed attempts and is a lower bound where harness-censored costs remain. See BAI_ACCOUNTING.md for source accounting differences.",
        ]
        if path.name == "claude-sonnet-3.7_4runs.tar.gz":
            data["source_formula"] = "bai-sonnet-3.7"
        serialized = json.dumps(data).replace("'", "''")
        conn.execute(f"COMMENT ON TABLE tasks IS '{serialized}'")
    print(path.name + ": resolution join " + json.dumps(Counter(t.outcome for t in tasks))
          + "; models " + json.dumps(Counter(c.model for t in tasks for c in t.calls if c.event_kind == "model")), flush=True)


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if not k.startswith("_")}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def analyze(path, db_dir, out_dir, prices=None):
    slug = path.name.removesuffix(".tar.gz")
    db = db_dir / (slug + ".duckdb")
    ingest_archive(path, db)
    with connect(db, read_only=True) as conn:
        tasks, evidence = load(conn), manifest(conn)
    report = make_report(tasks, evidence, load_catalog(prices), redact=True)
    render(report, out_dir / (slug + ".html"))
    g = report["groups"][0]
    def pick(scope, censoring):
        return next((r for r in g["simulations"] if r["scope"] == scope and r["censoring"] == censoring
                     and r["target"] == .7 and r["capped"]), None)

    fitted = pick("in_sample", "exclude")
    grouped = {c: {k: r[k] for k in ("price", "loss_ratio", "ci", "pooled_ci", "tasks_lost")}
               for c in ("exclude", "inflate") if (r := pick("grouped_cv", c))}
    stressed = {r["censoring"]: {"ci": r["ci"]} for r in g["imputed"] if r["scope"] == "grouped_cv"
                and r["capped"] and r["target"] == .7}
    result = {"analysis_version": 3, "model_archive": slug, "tasks": report["n_tasks"],
              "model_calls": sum(t.n_calls for t in tasks), "outcomes": g["outcomes"],
              "shape": g["shape"], "n_unpriced": g["n_unpriced"], "n_capped": g["n_capped"],
              "known_spend": report["known_spend"],
              "in_sample_price_70_with_p99_cap": fitted["price"] if fitted else None,
              "grouped_cv_70_with_p99_cap": grouped, "validation": g["validation"],
              "grouped_cv_70_unpriced_at_p99": stressed, "success_viable": g["success_viable"],
              "fixed_price_70_uncapped": g["shape"].get("mean", 0) / .7 if g["shape"]["n"] else None,
              "verdict": g["verdict"], "simulations": clean(g["simulations"]),
              "success_billing": clean(g["success_billing"]),
              "source_formula_verification": report["source_formula_verification"],
              "reconciliation": report["reconciliation"],
              "price_catalog": report["catalog"],
              "resolution_reports": evidence["resolution_reports"],
              "resolution_conflicts": evidence["resolution_conflicts"],
              "harness_iteration_limits": evidence["harness_iteration_limits"]}
    (out_dir / (slug + ".analysis.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(slug + ": " + g["verdict"]["label"] + "; unpriced tasks " + str(g["n_unpriced"]), flush=True)


def comparison(out_dir):
    results = [json.loads(p.read_text()) for p in sorted(out_dir.glob("*.analysis.json"))]

    def fmt(v, percent=False):
        return "Unavailable" if v is None else f"{v:.1%}" if percent else f"{v:.4f}"

    def band(r, censoring):
        row = r["grouped_cv_70_with_p99_cap"].get(censoring)
        return " – ".join(fmt(v, True) for v in row["ci"]) if row else "Unavailable"

    def stressed(r):
        rows = r["grouped_cv_70_unpriced_at_p99"]
        if not r["n_unpriced"]:
            return "no unpriced tasks"
        if r["verdict"]["unpriced_at_p99"] is None:
            return "not tested: over the 2% limit"
        return r["verdict"]["unpriced_at_p99"] + " (upper " + " / ".join(
            fmt(rows[c]["ci"][1], True) for c in ("exclude", "inflate") if c in rows) + ")"

    headings = ["Model archive", "Tasks", "Unpriced tasks", "Priced uncapped n", "Mean USD",
                "p90/p50", "p99 USD", "Resolve rate", "Outcome coverage",
                "Cost per resolved task USD", "70% price + p99 cap USD (grouped CV)",
                "Grouped-CV 90% loss-ratio interval, capped runs excluded",
                "Grouped-CV 90% loss-ratio interval, capped runs inflated",
                "Verdict, unpriced excluded", "Verdict, unpriced at training p99", "Verdict",
                "Success-only: highest viable target", "Success-only price per resolved task USD",
                "Harness iteration limit"]
    rows = []
    for r in results:
        s, o, best = r["shape"], r["outcomes"], r["success_viable"] or {}
        price = r["grouped_cv_70_with_p99_cap"].get("exclude", {}).get("price")
        rows.append([r["model_archive"], str(r["tasks"]),
                     f"{r['n_unpriced']} ({r['verdict']['unpriced_share']:.1%})", str(s["n"]),
                     fmt(s.get("mean")), fmt(s.get("p90_p50")), fmt(s.get("p99")),
                     fmt(o["success_rate"], True), f"{o['known_outcomes']}/{r['tasks']}",
                     fmt(o["cost_per_success"]), fmt(price), band(r, "exclude"), band(r, "inflate"),
                     r["verdict"]["unpriced_excluded"], stressed(r), r["verdict"]["label"],
                     fmt(best.get("target"), True) if best.get("target") else "none of 60/65/70%" if best else "Unavailable",
                     fmt(best.get("price_per_resolved")), ", ".join(r["harness_iteration_limits"])])
    intro = ["# What this report saw", "",
             "Benchmark tasks, not production. Metadata only: SHA-256 task IDs, hashed instance groups and run IDs, timestamps, model, token classes, recorded dollars, tool names and argument hashes, iteration-cap signals, and SWE-bench resolution outcomes. No prompts, completions, code, raw arguments, tool outputs or raw instance names were retained.", "",
             "## Model comparison", "",
             "Provider-correct pricing is the default. Shape statistics describe fully priced, uncapped tasks only; their n and the unpriced task count are explicit. Resolve rate uses known SWE-bench outcomes. Cost per resolved task is all observed spend on fully priced tasks divided by their confirmed resolutions, so failed attempts are included; censored costs make it a lower bound. Every archive repeats 500 instances across four runs, so the price and interval come from grouped cross-validation: five folds hold out 20% of instances with all their runs, and the price (mean of fold prices at the 70% target with a p99 cap) is fit on training instances only. The interval is the loss ratio of a held-out fold across 1,000 instance-bootstrap draws that refit every price. VIABLE requires both intervals below 90%. Unpriced tasks must be under 2% of the archive, and the verdict must also hold when each unpriced held-out task is scored at the training p99 cost; both verdicts are shown. Success-only billing charges only resolved tasks: the highest of 60/65/70% targets that passes the same rule is shown with its price per resolved task, beside the per-task price that bills every attempt. Missing tariffs or inconsistent token classes are unavailable, never zero cost.", ""]
    md = intro + ["| " + " | ".join(headings) + " |", "| " + " | ".join(["---"] * len(headings)) + " |"]
    md += ["| " + " | ".join(row) + " |" for row in rows]
    md += ["", "## Per-model reports", ""]
    md += [f"- [{r['model_archive']}]({r['model_archive']}.md) ([HTML]({r['model_archive']}.html))" for r in results]
    md += ["", "Harness budgets differ across archives (including 100 versus 500 iterations), so this is not a matched-budget model comparison. Each report includes grouped and leave-one-run-out holdouts, the leaky time split for contrast, success-only billing where outcomes and costs are usable, harness cap rates, cost audit, and source limitations.", ""]
    (out_dir / "COMPARISON.md").write_text("\n".join(md))
    html = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Moira · Bai model comparison</title><style>body{font:16px system-ui;margin:32px;color:#183237}table{border-collapse:collapse;font-size:14px}td,th{padding:10px;border-bottom:1px solid #ccd;text-align:left}.scroll{overflow:auto}p{max-width:1000px}</style><h1>What this report saw</h1>'
    html += '<p>' + escape(intro[2]) + '</p><h2>Model comparison</h2><p>' + escape(intro[6]) + '</p><div class="scroll"><table><tr>'
    html += ''.join('<th>' + escape(v) + '</th>' for v in headings) + '</tr>'
    html += ''.join('<tr>' + ''.join('<td>' + escape(v) + '</td>' for v in row) + '</tr>' for row in rows)
    html += '</table></div><h2>Per-model reports</h2><ul>'
    html += ''.join(f'<li><a href="{escape(r["model_archive"])}.html">{escape(r["model_archive"])}</a></li>' for r in results) + '</ul></html>'
    (out_dir / "COMPARISON.html").write_text(html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="*", type=Path)
    parser.add_argument("--db-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--prices", type=Path)
    args = parser.parse_args()
    args.db_dir.mkdir(parents=True, exist_ok=True)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for archive in args.archives:
        analyze(archive, args.db_dir, args.out_dir, args.prices)
    comparison(args.out_dir)

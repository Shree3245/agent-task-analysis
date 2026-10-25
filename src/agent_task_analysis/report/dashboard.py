"""The plain-language pricing dashboard at the top of the HTML report.

Everything it shows comes from the report model; the page's script only rescales the
validated numbers for a price the reader picks. Prices here pass the interval rule
without the p99 cap, because nothing stops a run at the cap once a price is published.
"""

import base64
import hashlib
import json
from importlib.resources import files

STATUS = {
    "ready": "Ready to price",
    "watch": "Ready, but costs moved",
    "more": "Needs more runs",
    "risky": "Too unpredictable",
}


def pick(rows, scope, target, capped=False, censoring="exclude"):
    return next((r for r in rows if r["scope"] == scope and r["capped"] == capped
                 and r["censoring"] == censoring and abs(r["target"] - target) < 1e-9), None)


def day(value):
    return value[:10] if value else None


def human(value):
    """2026-09-28 -> Sep 28, 2026."""
    from datetime import date
    return date.fromisoformat(value).strftime("%b %d, %Y").replace(" 0", " ") if value else None


def more_reason(g, row, cutoff, min_samples):
    """Why a task type has too few runs to test a price, in the reader's terms."""
    unit = "task groups" if g["grouped"] else "runs"
    usable = g.get("n_total", 0) - g.get("n_capped", 0)
    if not g["grouped"] and usable < 2 * min_samples:
        return (f"Only {usable} runs so far. A price needs {min_samples} runs to set it "
                f"and {min_samples} newer ones to test it.")
    if row is None:
        counts = g.get("split_counts", {})
        if g["grouped"]:
            return "There are not enough task groups to hold some out and test a price on them."
        if counts.get("test", 0) == 0:
            return f"Every run started before {cutoff}, so there are no newer runs to test a price on."
        if counts.get("train", 0) == 0:
            return f"No runs started before {cutoff}, so there is nothing to set a price on."
        return "There are not enough runs to set a price and test it."
    if row["train_uncapped"] < min_samples:
        where = "in each training fold" if g["grouped"] else f"before {cutoff}"
        return f"Only {row['train_uncapped']} {unit} {where} to set a price. It needs {min_samples}."
    where = "in each held-out fold" if g["grouped"] else f"since {cutoff}"
    return f"Only {row['test_uncapped']} {unit} {where} to test a price on. It needs {min_samples}."


def tagging(report):
    """Notes when the traces don't seem to mark where a run starts and ends, or what kind it is."""
    imports = report["evidence"].get("imports", [])
    gap = max((i.get("gap_seconds") or 0 for i in imports), default=0)
    notes = []
    if gap:
        notes.append(f"Runs were rebuilt by grouping calls with no run ID wherever there was a quiet gap "
                     f"of {gap:g} seconds, so run counts and prices are estimates.")
        if any((i.get("warnings") or {}).get("gap_grouping_without_session") for i in imports):
            notes.append("The traces had no session or user ID, so overlapping calls from different "
                         "users may have been merged into one run.")
    else:
        single = [g["name"] for g in report["groups"]
                  if g["n_total"] >= report["min_samples"] and g.get("single_call_share", 0) >= 0.8]
        if single:
            notes.append(f"Most runs of {', '.join(single)} are a single model call. If one agent run "
                         "makes several calls, your traces are probably logging each call as its own "
                         "run, so these prices are per call. Wrap each run in one parent span or set "
                         "task.id on every call, or ingest again with --gap 60.")
    unknown = next((g for g in report["groups"] if g["name"] == "unknown"), None)
    if unknown and report["n_tasks"] and unknown["n_total"] / report["n_tasks"] >= 0.2:
        notes.append(f"{unknown['n_total']:,} runs ({unknown['n_total'] / report['n_tasks']:.0%}) have no "
                     "task type, so they share one blended price. Set task.type (OpenTelemetry) or "
                     "task_type in metadata (Braintrust), or pass --rules when ingesting.")
    return notes


def group_view(g, report):
    target, min_samples = report["target"], report["min_samples"]
    scope = "grouped_cv" if g["grouped"] else "holdout"
    split = g["split"]
    cutoff = human(day(split["cutoff"])) or "the split date"
    row = pick(g["simulations"], scope, target)
    enough = bool(row) and min(row["train_uncapped"], row["test_uncapped"]) >= min_samples
    d = g["drift"]
    moved = bool(d["reprice"] and not d["small"])
    if not enough:
        status = "more"
    elif g["uncapped_verdict"]["label"] == "VIABLE":
        status = "watch" if moved else "ready"
    else:
        status = "risky"
    cap = next((c for c in g["caps"] if abs(c["quantile"] - 0.99) < 1e-9), None)
    rate = next((p for p in report["projections"]
                 if p["type"] == g["name"] and p.get("spend_change")), None)
    success = None
    if g.get("success_viable") and g["success_viable"].get("price_per_resolved"):
        v = g["success_viable"]
        success = {"price": v["price_per_resolved"], "target": v["target"], "basis": "resolved"}
    elif g.get("refunds"):
        r = g["refunds"]["refund_unconfirmed"].get("row_uncapped")
        if r and r["ci"]:
            success = {"price": r["price"], "upper": r["ci"][1], "basis": "confirmed",
                       "target": target}
    outcomes = g["outcomes"]
    return {
        "name": g["name"],
        "status": status,
        "label": STATUS[status],
        "n": g["n_total"],
        "n_unpriced": g["n_unpriced"],
        "n_capped": g["n_capped"],
        "price": row["price"] if row else None,
        "loss": row["loss_ratio"] if row else None,
        "upper": row["ci"][1] if row and row["ci"] else None,
        "grouped": g["grouped"],
        "fit_window": None if g["grouped"] else split["fit_window"],
        "test_window": None if g["grouped"] else split["test_window"],
        "backdated": split["backdated"],
        "n_fit": row["train_uncapped"] if row else None,
        "n_test": row["test_uncapped"] if row else None,
        "reason": None if enough else more_reason(g, row, cutoff, min_samples),
        "risk_reasons": g["uncapped_verdict"]["reasons"] if status == "risky" else [],
        "costs": g["costs"],
        "max": g["shape"].get("max"),
        "median": g["shape"].get("median"),
        "cap": {"price": cap["cap"], "stopped": cap["stopped"]} if cap else None,
        "drift": {"ratio": d["ratio"], "moved": moved, "small": d["small"],
                  "recent_mean": d["recent_mean"], "fit_mean": d["fit_mean"],
                  "recent_n": d["recent_n"]},
        "rate": {"date": rate["date"], "models": rate["models"],
                 "change": rate["spend_change"]} if rate else None,
        "success": success,
        "success_share": (outcomes["successes"] / g["n_total"]) if g["n_total"] else None,
        "override_share": g.get("override_share"),
    }


def view(report):
    return {
        "target": report["target"],
        "min_samples": report["min_samples"],
        "n_tasks": report["n_tasks"],
        "spend": report["known_spend"],
        "start": day(report.get("data_start")),
        "end": day(report.get("data_end")),
        "cutoff": day(report.get("cutoff")),
        "benchmark": report["benchmark"],
        "overrides": bool(report.get("overrides")),
        "repricing": report["reconciliation"]["acceptance"],
        "tagging": tagging(report),
        "groups": [group_view(g, report) for g in report["groups"]],
    }


def script():
    return files("agent_task_analysis.report").joinpath("templates/dashboard.js").read_text()


def script_hash(source):
    return "sha256-" + base64.b64encode(hashlib.sha256(source.encode()).digest()).decode()


def data_json(report):
    # Inside <script type="application/json">: escape "<" so no value can close the tag.
    return json.dumps(view(report), separators=(",", ":")).replace("<", "\\u003c")

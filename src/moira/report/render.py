from html import escape
from pathlib import Path
from importlib.resources import files

from jinja2 import Environment, BaseLoader, select_autoescape


def usd(value):
    return "—" if value is None else f"${value:,.4f}"


def pct(value):
    return "—" if value is None else f"{value:.1%}"


def numeric(value):
    return "—" if value is None else f"{value:,.2f}"


def sections(report):
    result = []

    def section(title):
        item = {"title": title, "paragraphs": [], "tables": [], "charts": []}
        result.append(item)
        return item

    def table(s, title, headers, rows):
        s["tables"].append({"title": title, "headers": headers, "rows": rows})

    s = section("What this report saw")
    s["paragraphs"] += [
        "No content was kept: no prompts, completions, code, tool outputs, or raw tool arguments. Tool arguments were read only to compute a keyed HMAC-SHA-256 digest. Parsing used memory; only allowlisted metadata reached local storage.",
        f"{report['n_tasks']} tasks. Price catalog {report['catalog']['version']} · SHA-256 {report['catalog']['sha256']}.",
        report["catalog"]["description"],
        "Retained call fields: " + ", ".join(report["retained_call_fields"]),
        "Retained task fields: " + ", ".join(report["retained_task_fields"]),
        "Derived bookkeeping includes call indexes, source, outcomes, cap reasons, and parent-tool links. Fields absent from a source remain unknown; optional cache/reasoning classes absent from a usage object are treated as zero.",
        "Task IDs are SHA-256 aliases. Type and tool labels remain visible."
        if report["redacted"]
        else "Task IDs are keyed HMAC-SHA-256 digests of source IDs, applied at ingest; raw IDs are never stored. --redact-task-ids re-aliases them so this report's IDs cannot be matched against the local database.",
    ]
    if report.get("window"):
        w = report["window"]
        s["paragraphs"].append(
            f"Report window: tasks that started from {w['since'] or 'the first task'} through {w['until'] or 'the last task'} (UTC). {w['outside']} tasks outside the window and {w['untimed']} without a start time were left out."
        )
    if report.get("overrides"):
        o = report["overrides"]
        s["paragraphs"].append(
            f"RATE OVERRIDES APPLIED (file SHA-256 {o['sha256']}). These are user-supplied rates, not public list prices: "
            + ", ".join(o["models"]) + "."
            + (f" Replacing catalog rates: {', '.join(o['replaced'])}." if o["replaced"] else "")
            + (f" Not in the catalog: {', '.join(o['added'])}." if o["added"] else "")
            + (f" {o['description']}" if o["description"] else "")
            + " Prices that depend on them are labeled."
        )
    if report["benchmark"]:
        s["paragraphs"].insert(
            0,
            "BENCHMARK TASKS, NOT PRODUCTION WORKLOADS. These results do not establish production economics.",
        )
    if report["evidence"].get("benchmark_scope"):
        s["paragraphs"].append(report["evidence"]["benchmark_scope"])
    if report.get("task_groups"):
        s["paragraphs"].append(f"Task groups: {report['task_groups']} tasks carry a keyed HMAC-SHA-256 task_group (the source instance ID, hashed at ingest). Raw instance names are not stored in task_group.")
    if report["evidence"].get("benchmark_assignments"):
        s["paragraphs"].append("Additional benchmark metadata: keyed HMAC-SHA-256 run_id for leave-one-run-out."
                               + (" Configured harness iteration limits and resolution outcomes joined within each run. No evaluation outputs or patches were retained."
                                  if report["evidence"].get("resolution_reports") is not None else ""))
    for i, evidence in enumerate(report["evidence"].get("imports", []), 1):
        s["paragraphs"].append(
            f"Import {i}: {evidence['source']} · {evidence['files']} files · {evidence['records']} records. Fields read: "
            + ", ".join(evidence["fields_read"])
        )
        if evidence.get("warnings"):
            s["paragraphs"].append(
                "Import limitations: "
                + "; ".join(f"{k}: {v}" for k, v in evidence["warnings"].items())
            )
        if evidence.get("scope"):
            s["paragraphs"].append(evidence["scope"])
        if remote := evidence.get("remote"):
            s["paragraphs"].append(
                f"Fetched over the network from {remote['api_host']} at {remote['fetched_at']}: traces started in the last {remote['window_days']} days, {remote['traces']} kept. {remote['traces_in_progress']} traces active in the last {remote['settle_minutes']} minutes (possibly still running) and {remote['traces_before_window']} that started before the window were left out. Span content was discarded in memory; only the fields listed above were kept."
            )

    s = section("Summary verdicts")
    verification = report.get("source_formula_verification")
    if verification and verification["verified"]:
        s["paragraphs"] += [
            f"Token parsing: verified (source formula reproduced on {verification['matches']:,}/{verification['calls']:,} calls)",
            "Source recorded cost: uses a different cache-write convention, documented in BAI_ACCOUNTING.md",
        ]
    elif report["reconciliation"]["acceptance"] == "FAIL":
        s["paragraphs"].append(
            "REPRICING CHECK FAILED. Verdicts below describe standard-rate token costs, not validated recorded billing. Review the reconciliation discrepancy in Cost audit before using these prices."
        )
    s["paragraphs"] += [
        "VIABLE means the holdout 90% loss-ratio interval stays strictly below 90% at the 70% target with a p99 cap, under both censoring scenarios where applicable. NOT VIABLE can also mean insufficient evidence; read the reason.",
        f"Temporal cutoff: {report['cutoff'] or 'unavailable'}; {report['split_excluded']} tasks excluded from the split (missing time or crossing the boundary). Minimum {report['min_samples']} uncapped tasks per training and test partition.",
        f"Actual known spend: {usd(report['known_spend'])}. Overall distribution weights each of {report['priced_types']} represented types equally. Counts and total dollars are accounting totals, not type-balanced statistics.",
    ]
    if report["grouped"]:
        s["paragraphs"].append(
            "Verdict basis where task groups repeat: grouped_cv, five folds that each hold out 20% of task groups with all their runs. Mean price, p99 cap and censoring tail are fit on the training groups only. The verdict interval is the 5th–95th percentile loss ratio of a held-out fold across 1,000 seeded group-bootstrap draws, each rerunning the full cross-validation with refit prices. The pooled out-of-fold interval is shown beside it; with refit mean prices and similar fold sizes the pooled ratio cancels to nearly the target, so it is not a risk measure. The minimum sample threshold counts distinct uncapped groups in each fold. Types without repeated groups keep the time split."
        )
    overridden = bool(report.get("overrides"))
    table(
        s,
        "Verdicts",
        ["Task type", "Tasks", "Capped", "Unpriced", "Verdict", "Reason"]
        + (["Spend priced at override rates"] if overridden else []),
        [
            [
                g["name"],
                g["n_total"],
                g["n_capped"],
                g["n_unpriced"],
                g["verdict"]["label"],
                g["verdict"]["reason"],
            ]
            + ([pct(g["override_share"])] if overridden else [])
            for g in report["groups"]
        ],
    )
    if any(g["verdict"]["unpriced"] for g in report["groups"]):
        s["paragraphs"].append(
            "Unpriced tasks: a pool can be VIABLE only when under 2% of its tasks have unknown cost, and only if the rule also holds when each unpriced held-out task is scored at the training pool's p99 cost (or its known partial cost, if higher). Prices are fit on priced tasks only. Both verdicts are shown."
        )

        def upper(rows, scope, censoring):
            row = next((r for r in rows if r["scope"] == scope and r["censoring"] == censoring
                        and r["capped"] and abs(r["target"] - 0.7) < 1e-9), None)
            return pct(row["ci"][1]) if row else "—"

        table(s, "Unpriced tasks · verdict both ways",
              ["Type", "Unpriced", "Share", "Verdict, unpriced excluded", "Verdict, unpriced at training p99",
               "Upper 90% CI excluded → at p99 (capped runs excluded)", "Upper 90% CI excluded → at p99 (capped runs inflated)"],
              [[g["name"], v["unpriced"], pct(v["unpriced_share"]), v["unpriced_excluded"],
                v["unpriced_at_p99"] or "not tested: over the 2% limit",
                *(f"{upper(g['simulations'], scope, c)} → {upper(g['imputed'], scope, c)}" for c in ("exclude", "inflate"))]
               for g in report["groups"] if g["verdict"]["unpriced"]
               for v in [g["verdict"]] for scope in ["grouped_cv" if g["grouped"] else "holdout"]])
    table(s, "Validation split per pricing pool",
          ["Type", "Sources", "Tasks with task_group", "Distinct groups", "Repeated groups",
           "Max tasks per group", "Verdict split", "Why"],
          [[g["name"], v["sources"], v["grouped_tasks"], v["groups"], v["repeated_groups"],
            v["max_per_group"], "grouped CV" if v["split"] == "grouped_cv" else "time split", v["why"]]
           for g in report["groups"] for v in [g["validation"]]])
    for g in report["groups"]:
        if not g["grouped"]:
            continue
        index = {(r["scope"], r["censoring"], r["capped"], r["target"]): r for r in g["simulations"]}
        rows = []
        for (scope, mode, capped, target), r in index.items():
            if scope != "grouped_cv":
                continue
            run = index.get(("leave_one_run_out", mode, capped, target))
            split = index.get(("holdout", mode, capped, target))
            rows.append([
                mode, "p99" if capped else "none", pct(target), pct(r["loss_ratio"]),
                " – ".join(pct(v) for v in r["ci"]), " – ".join(pct(v) for v in r["pooled_ci"]),
                pct(r["tasks_lost"]), usd(r["worst_loss"]),
                pct(run["loss_ratio"]) if run else "—",
                " – ".join(pct(v) for v in run["ci"]) if run else "—",
                pct(split["loss_ratio"]) if split else "—",
                " – ".join(pct(v) for v in split["ci"]) if split else "—",
                f"{split['loss_ratio'] - r['loss_ratio']:+.1%}" if split else "—",
                f"{split['ci'][1] - r['ci'][1]:+.1%}" if split else "—",
            ])
        table(s, g["name"] + " · grouped CV vs time split",
              ["Censoring", "Cap", "Target", "Grouped CV loss ratio", "Held-out fold 90% CI (verdict)",
               "Pooled 90% CI", "Tasks losing", "Worst loss", "Leave-one-run-out loss ratio",
               "Leave-one-run-out held-out 90% CI", "Time split (leaks repeated tasks) loss ratio",
               "Time split 90% CI", "Difference: time split − grouped CV", "Difference: upper CI"],
              rows)
    rows = []
    for name, shape in [(g["name"], g["shape"]) for g in report["groups"]] + [
        ("Overall · equal type weight", report["overall_shape"])
    ]:
        rows.append(
            [
                name,
                shape["n"],
                *[usd(shape.get(k)) for k in ("mean", "median", "p90", "p99", "max")],
                numeric(shape.get("p90_p50")),
                pct(shape.get("top_1_share")),
                pct(shape.get("top_5_share")),
            ]
        )
    table(
        s,
        "Cost shape · complete, uncapped tasks",
        [
            "Type",
            "n",
            "Mean",
            "Median",
            "p90",
            "p99",
            "Max",
            "p90/p50",
            "Top 1% spend",
            "Top 5% spend",
        ],
        rows,
    )
    if report["benchmark"]:
        table(s, "Cap applied by the harness · iteration limits", ["Type", "Tasks", "Hit iteration limit", "Share"],
              [[g["name"], g["n_total"], g["outcomes"]["iteration_limited"],
                pct(g["outcomes"]["iteration_limit_share"])] for g in report["groups"]])
        s["paragraphs"].append(
            "The harness applied an iteration cap before this analysis. The cost-shape table excludes detected capped tasks; their observed costs are censored lower bounds. Its remaining tail is selected by the harness and must not be interpreted as an unrestricted natural tail."
        )
        if report["evidence"].get("harness_iteration_limits"):
            s["paragraphs"].append("Configured harness iteration limits: " + "; ".join(
                f"{limit} iterations for {count} tasks" for limit, count in report["evidence"]["harness_iteration_limits"].items())
                + ". Zero detected hits does not establish an unrestricted run; only explicit cap signals are counted.")
    s["charts"] = [g["distribution"] for g in report["groups"]]

    days = report["recent_days"]
    s = section("Drift and recency")
    s["paragraphs"] += [
        f"Windows use task start times and end at the latest start in this report ({report['data_end'] or 'unavailable'}), not today's date. Recent window: the last {days} days. Fit window: the tasks the verdict price is fit on (the time-split training period, or the whole pool under grouped CV). Means use complete, uncapped tasks.",
        f"Reprice recommended when the recent mean differs from the fit-window mean by more than {report['drift_limit']:.0%}. With fewer than {report['min_samples']} tasks in either window the ratio is noisy; it is flagged but still shown.",
    ]
    table(s, "Drift per pool",
          ["Type", "Fit window", "Fit tasks", "Fit mean", f"Recent window (last {days} days)",
           "Recent tasks", "Recent mean", "Recent ÷ fit", "Reprice recommended"],
          [[g["name"], " – ".join(d["fit_window"]) if d["fit_window"] else "—", d["fit_n"],
            usd(d["fit_mean"]), " – ".join(d["recent_window"]) if d["recent_window"] else "—",
            d["recent_n"], usd(d["recent_mean"]), numeric(d["ratio"]),
            ("YES" if d["reprice"] else "no") + (" (small sample)" if d["small"] else "")
            if d["ratio"] is not None else "—"]
           for g in report["groups"] for d in [g["drift"]]])

    def fit_cells(row):
        if not row:
            return ["—", "—", "—", "—"]
        return [usd(row["price"]), f"{row['train_uncapped']}/{row['test_uncapped']}",
                pct(row["loss_ratio"]), " – ".join(pct(v) for v in row["ci"])]

    s["paragraphs"].append(
        f"Recency-window pricing at the {report['target']:.0%} target, p99 cap, capped runs excluded. The full-period price is fit on the whole time-split training period; the recent-fit price on its last {days} days only. Both are scored on the same holdout. The current price is fit in-sample on the last {days} days of all data: it is what a recent fit charges now, and it has no holdout yet."
    )
    table(s, "Recency-window pricing",
          ["Type", "Full-period price", "Train/test uncapped", "Holdout loss ratio", "90% CI",
           "Recent-fit window", "Recent-fit price", "Train/test uncapped", "Holdout loss ratio",
           "90% CI", f"Current price (last {days} days, not validated)", "Current window tasks"],
          [[g["name"], *fit_cells(r["full"]),
            " – ".join(r.get("recent_window") or []) or "—", *fit_cells(r["recent"]),
            usd(r["current"]["price"]) if r["current"] else "—",
            r["current"]["n_train"] if r["current"] else 0]
           for g in report["groups"] for r in [g["recency"]]])
    table(s, "Weekly mean cost · complete, uncapped tasks", ["Type", "Week of", "Tasks", "Mean", "Total"],
          [[g["name"], w["week"], w["n"], usd(w["mean"]), usd(w["total"])]
           for g in report["groups"] for w in g["weekly"]])

    if report["rate_changes"]:
        s = section("Scheduled rate changes")
        s["paragraphs"].append(
            "The price catalog lists dated rate changes on " + ", ".join(report["rate_changes"])
            + ". Each recorded call is priced at the rates in effect when it started. Projections below reprice every task at the rates in effect on a change date after the data ends, keeping the same tasks and time split: the loss ratio if today's verdict price is kept, the refit price at the target, and the current last-"
            + f"{days}-day price under the new rates. Pools whose verdict uses grouped CV are projected on the time split; this shows the tariff effect, not a new verdict."
        )
        if not report["future_rate_changes"]:
            s["paragraphs"].append("No listed change falls after the latest task in this report.")
        table(s, "Projected prices and loss ratios after each rate change",
              ["Type", "Effective", "Models changing", "Pool spend change", "Current verdict price",
               "Loss ratio if kept", "90% CI", "Refit price at target",
               f"Current price (last {days} days) under new rates"],
              [[p["type"], p["date"], ", ".join(p["models"]), pct(p["spend_change"]) if p["spend_change"] is None else f"{p['spend_change']:+.1%}",
                usd(p["price_now"]), pct(p["kept"]["loss_ratio"]) if p["kept"] else "—",
                " – ".join(pct(v) for v in p["kept"]["ci"]) if p["kept"] else "—",
                usd(p["price"]), usd(p["current_price"])] for p in report["projections"]])

    s = section("Cost audit")
    macro = report["overall_audit"]
    if macro:
        s["paragraphs"].append(
            f"Equal-type overall: failed/aborted tasks {pct(macro['failed_aborted_fraction'])}; their spend per task {usd(macro['failed_aborted_spend_per_task'])}; tasks with loop signals {pct(macro['loop_fraction'])}. Raw dollar totals below are accounting totals."
        )
    r = report["reconciliation"]
    status = "Provider-correct / source-recorded agreement (different cache-write convention)" if verification and verification["verified"] else f"Repricing acceptance: {r['acceptance']}"
    s["paragraphs"].append(
        f"{status}. {r.get('within_one_percent', 0)} of {r.get('recorded_calls', 0)} recorded-cost calls within 1% ({pct(r['agreement'])}); {r.get('comparable_calls', 0)} comparable calls ({pct(r['comparable_agreement'])} agreement). Unknown/unpriceable calls stay in the recorded-cost denominator. Recorded zero is checked, not skipped."
    )
    # Benchmarks resolve tasks (SWE-bench); other sources only report success.
    done = "resolved" if report["benchmark"] else "successful"
    table(s, f"Resolution outcomes and cost per {done} task",
          ["Type", "Resolved", "Known outcomes / tasks", "Resolve rate" if report["benchmark"] else "Success rate",
           "Priced tasks / priced resolutions" if report["benchmark"] else "Priced tasks / priced successes",
           "Cost per resolved task (priced spend / confirmed resolutions)" if report["benchmark"] else "Priced spend / confirmed success"],
          [[g["name"], g["outcomes"]["successes"],
            f"{g['outcomes']['known_outcomes']}/{g['n_total']}", pct(g["outcomes"]["success_rate"]),
            f"{g['outcomes']['priced_tasks']}/{g['outcomes']['priced_successes']}",
            usd(g["outcomes"]["cost_per_success"])] for g in report["groups"]])
    s["paragraphs"].append(f"Cost per {done} task includes unsuccessful attempts: total observed spend on fully priced tasks divided by their confirmed resolutions. Unknown outcomes are not counted as confirmed successes or labeled failures; resolving them may change the denominator. Harness-censored costs remain lower bounds. Incomplete-cost tasks are excluded from this ratio, with coverage shown. Success rate uses known resolution outcomes.")
    totals = r["totals"]
    s["paragraphs"].append(
        f"Comparable-call totals: recorded {usd(totals['recorded_comparable'])}; standard-rate reprice {usd(totals['repriced_comparable'])}; difference {usd(totals['recorded_comparable'] - totals['repriced_comparable'])}."
    )
    diagnostic = r["extra_cache_write_input_charge_diagnostic"]
    if (
        diagnostic.get("calls")
        and diagnostic.get("matches", 0) / diagnostic["calls"] >= 0.99
        and r["acceptance"] == "FAIL"
    ):
        s["paragraphs"].append(
            f"Diagnostic: {diagnostic.get('matches', 0)} of {diagnostic['calls']} comparable calls with cache writes match standard cost plus an additional base-input charge on cache-write tokens. This is an observed arithmetic pattern, not proof of its upstream cause. Public rates remain unchanged; this does not count as successful reconciliation."
        )
    table(s, "Unknown models", ["Provider/model", "Calls"], list(r["unknown_models"].items()))
    table(
        s,
        "Repricing mismatches · first 20",
        ["Task", "Call", "Recorded", "Repriced"],
        [
            [m["task_id"], m["call_idx"], usd(m["recorded"]), usd(m["repriced"])]
            for m in r["mismatches"]
        ],
    )
    table(
        s,
        "Spend audit",
        [
            "Type",
            "Known spend",
            "Failed/aborted spend",
            "Censored observed spend",
            "Loop tasks",
            "Call-count p99",
        ],
        [
            [
                g["name"],
                usd(g["audit"]["known_spend"]),
                usd(g["audit"]["failed_aborted_spend"]),
                usd(g["audit"]["censored_spend"]),
                g["audit"]["loop_tasks"],
                numeric(g["audit"]["call_p99"]),
            ]
            for g in report["groups"]
        ],
    )
    for g in report["groups"]:
        table(
            s,
            g["name"] + " · runaway tasks",
            ["Task", "Known cost", "Coverage", "Outcome", "Capped"],
            [
                [
                    t["task_id"],
                    usd(t["cost"]),
                    "complete" if t["complete"] else "lower bound",
                    t["outcome"],
                    t["capped"],
                ]
                for t in g["audit"]["runaways"]
            ],
        )
        table(
            s,
            g["name"] + " · loop signals",
            ["Task", "Repeated tools", "Calls", "Above 2 × p99", "Known cost"],
            [
                [
                    t["task_id"],
                    "; ".join(f"{x['tool']} × {x['repeats']}" for x in t["repeated"]),
                    t["calls"],
                    t["above_call_threshold"],
                    usd(t["known_cost"]),
                ]
                for t in g["audit"]["loops"]
            ],
        )
    s["paragraphs"].append(
        "Repeated tool + argument hash is a signal, not proof of wasted work. Incomplete task spend is a lower bound. Failed or aborted tasks may still have produced useful work."
    )

    s = section("Catastrophe cap")
    s["paragraphs"].append(
        "Recommended cap: p99, a stated policy rather than an optimized verdict. Saved spend represents UNFINISHED WORK, NOT FREE MONEY. Replay stops after the crossing model call and pays its overshoot; the ideal dollar ceiling is shown separately. Thresholds here describe full-sample uncapped tasks; holdout simulations fit their thresholds on training only."
    )
    table(
        s,
        "Cap scenarios",
        [
            "Type",
            "Percentile",
            "Cap",
            "Stopped",
            "Spend saved",
            "Saved share",
            "Ideal stopped",
            "Ideal saved",
        ],
        [
            [
                g["name"],
                f"p{r['quantile'] * 100:g}",
                usd(r["cap"]),
                pct(r["stopped"]),
                usd(r["saved"]),
                pct(r["saved_share"]),
                pct(r["ideal_stopped"]),
                usd(r["ideal_saved"]),
            ]
            for g in report["groups"]
            for r in g["caps"]
        ],
    )
    table(
        s,
        "Overall cap impact · equal type weight",
        ["Percentile", "Types represented", "Stopped", "Saved per task", "Mean type saved share"],
        [
            [
                f"p{r['quantile'] * 100:g}",
                r["types"],
                pct(r["stopped"]),
                usd(r["saved_per_task"]),
                pct(r["saved_share"]),
            ]
            for r in report["overall_caps"]
        ],
    )

    s = section("Fixed-price simulation with confidence intervals")
    s["paragraphs"] += [
        "Price = fitted mean cost ÷ target loss ratio. Capped prices use replayed mean cost. Loss ratio = cost/revenue; over 100% loses money. Intervals are 5th/95th percentiles of 2,000 seeded task resamples with fitted prices and caps held fixed.",
        "In-sample results are descriptive. Holdout prices, p99 caps and censoring tails use only tasks ended before two-thirds of the elapsed period; score tasks starting in the final third. No future data is used for fitting.",
        "Exclude: capped runs are omitted. Inflate: each capped observed cost receives the training type's mean cost in its upper 5% tail. For cap replay this unknown tail is one indivisible future call, a conservative sensitivity assumption, not an observed completion cost. A change in the <90% upper-CI decision is flagged in the verdict.",
        "Overall loss ratios and percentages are arithmetic means across types; intervals resample within types then average. Overall price is the mean type price, not a universal price. Overall rows appear only when every type has the scenario.",
    ]
    if report["grouped"]:
        s["paragraphs"].append("Grouped CV and leave-one-run-out rows pool out-of-fold costs and revenues into the loss ratio, tasks-losing share and worst loss. Each fold fits its own price, p99 cap and censoring tail using training data only. Displayed price is the mean fitted fold price, not a single price used for every held-out task. Their 90% CI is the held-out fold loss ratio across 1,000 group-bootstrap draws that refit every price. Leave-one-run-out fits on the other runs and scores one run: same tasks, new run, so it shares groups across training and scoring by design. Charts and sample receipts use descriptive in-sample prices; time-split rows do not drive grouped verdicts.")
    for name, rows in [(g["name"] + (f" · override rates priced {pct(g['override_share'])} of spend" if g.get("override_share") else ""),
                        g["simulations"]) for g in report["groups"]] + [
        ("Overall · equal type weight", report["overall_simulations"])
    ]:
        table(
            s,
            name,
            [
                "Scope",
                "Censoring",
                "Cap",
                "Target",
                "Price",
                "Loss ratio",
                "90% CI",
                "Tasks losing",
                "Worst loss",
                "Train/test",
            ],
            [
                [
                    r["scope"],
                    r["censoring"],
                    "p99" if r["capped"] else "none",
                    pct(r["target"]),
                    usd(r["price"]),
                    pct(r["loss_ratio"]),
                    " – ".join(pct(v) for v in r["ci"]),
                    pct(r["tasks_lost"]),
                    usd(r["worst_loss"]),
                    f"{r['n_train']}/{r['n_test']}",
                ]
                for r in rows
            ],
        )
    s["charts"] = [g["loss_curve"] for g in report["groups"] if g["loss_curve"]]
    if any(g.get("refunds") for g in report["groups"]):
        s["paragraphs"].append(
            f"Refund-adjusted prices at the {report['target']:.0%} target, p99 cap, capped runs excluded, on each pool's verdict split. Refunded tasks still cost what they cost but pay nothing, and a task stopped by the cap is refunded. 'Fail/aborted refunded' bills unknown outcomes; 'only confirmed successes pay' refunds them too, the pessimistic bound. Price = training spend ÷ (target × billable training tasks). Verdicts use the same rule as the per-task verdict."
        )
        rule_names = {"refund_failed": "fail/aborted refunded", "refund_unconfirmed": "only confirmed successes pay"}
        table(s, "Refund-adjusted prices",
              ["Type", "Refund rule", "Failed/aborted", "Unknown outcome", "Per-task price (no refunds)",
               "Price per billed task", "Billed training tasks", "Loss ratio", "90% CI", "Verdict", "Reason"],
              [[g["name"], rule_names[rule], g["outcomes"]["known_outcomes"] - g["outcomes"]["successes"],
                g["n_total"] - g["outcomes"]["known_outcomes"],
                usd(next((r["price"] for r in g["simulations"] if r["scope"] == ("grouped_cv" if g["grouped"] else "holdout")
                          and r["censoring"] == "exclude" and r["capped"] and abs(r["target"] - report["target"]) < 1e-9), None)),
                usd(row["price"]) if row else "—",
                (row.get("train_billable") if row and "train_billable" in row else min(f["train_billable"] for f in row["folds"]) if row else "—"),
                pct(row["loss_ratio"]) if row else "—", " – ".join(pct(v) for v in row["ci"]) if row else "—",
                v["verdict"]["label"], v["verdict"]["reason"]]
               for g in report["groups"] if g.get("refunds")
               for rule, v in g["refunds"].items() for row in [v["row"]]])
    if any(g["success_billing"] for g in report["groups"]):
        s["paragraphs"].append("Success-only billing: price = all training costs / (target loss ratio × billable training successes). Failed attempts still incur costs but generate no revenue. A replay cap that stops a previously successful task makes it unbillable; earlier completion outcomes are not invented. This scenario uses fully priced tasks with known outcomes only; excluded outcomes and cost coverage are shown above. Its fold assignments are unchanged. Censored completion costs remain a sensitivity assumption.")
        for g in report["groups"]:
            table(s, g["name"] + " · success-only billing", ["Scope", "Censoring", "Cap", "Target", "Mean fold price / success", "Loss ratio", "90% CI", "Tasks losing", "Worst loss"],
                  [[r["scope"], r["censoring"], "p99" if r["capped"] else "none", pct(r["target"]),
                    usd(r["price"]), pct(r["loss_ratio"]), " – ".join(pct(v) for v in r["ci"]),
                    pct(r["tasks_lost"]), usd(r["worst_loss"])] for r in g["success_billing"]])
        table(s, "Success-only billing · highest viable target",
              ["Type", "Per-task price at 70% (all tasks billed)", "Highest viable success-only target",
               "Price per resolved task at that target", "Why none"],
              [[g["name"], usd(v["per_task_price_70"]), pct(v["target"]) if v["target"] else "none of 60/65/70%",
                usd(v["price_per_resolved"]), v["reason"] or "—"]
               for g in report["groups"] if (v := g["success_viable"])])
    if report["grouped"]:
        for g in report["groups"]:
            table(s, g["name"] + " · fold fits at 70% target with cap", ["Scope", "Billing", "Censoring", "Fold", "Train/test groups", "Price", "Cap", "Score loss ratio"],
                  [[r["scope"], r.get("billing", "all_tasks"), r["censoring"], f["fold"],
                    f"{f['train_groups']}/{f['test_groups']}", usd(f["price"]), usd(f["cap"]), pct(f["loss_ratio"])]
                   for r in g["simulations"] + g["success_billing"] if r["target"] == .7 and r["capped"]
                   for f in r.get("folds", [])])

    s = section("Sample receipts")
    s["paragraphs"].append(
        "Up to five deterministic examples per type across the cost range. Each model call is charged once. Shared-tool groups avoid double counting; unlinked tool events have no invented service charge. These receipts assume payment even for stopped tasks. The separate success-only scenario above changes that billing rule."
    )
    for g in report["groups"]:
        for receipt in g["receipts"]:
            title = f"{g['name']} · {receipt['task_id']} · fixed {usd(receipt['fixed_price'])} ({receipt['price_basis']}) · {receipt['outcome']} · capped={receipt['capped']}"
            table(
                s,
                title,
                ["Tool group", "Calls/events", "Attributed model cost"],
                [
                    [
                        r["tool"],
                        r["calls"],
                        ("≥ " if r["unknown"] and r["cost"] is not None else "") + usd(r["cost"]),
                    ]
                    for r in receipt["groups"]
                ],
            )

    s = section("Limits")
    if verification and verification["verified"]:
        s["paragraphs"].append("The 'Token parsing: verified' label is scoped to reproducing the source formula from parsed token metadata. It establishes arithmetic consistency, not an independent check of missing native input counters or an authenticated provider invoice. Provider-correct exclusive token pricing remains the default.")
    s["paragraphs"] += report["evidence"].get("benchmark_limit_notes", [])
    s["paragraphs"] += [
        "This is an LLM-cost simulation, not a profit forecast. Compute, human review, tools, retries absent from logs, support, refunds, taxes, and negotiated rates are not inferred. Listed rates may not reproduce historical invoices.",
        "Capped observations are censored lower bounds. Tail inflation is a sensitivity assumption; unknown completion costs are not identifiable from these logs. Caps can stop useful work and change outcomes.",
        "Bootstrap intervals describe variation in sampled tasks, conditional on fitted prices. They do not capture all training uncertainty, correlation between repeated benchmark tasks, tariff changes, or production drift. Small samples cannot establish tail safety.",
        "Per-type quantiles use linear interpolation; overall weighted quantiles use the inverse weighted CDF. Per-type top shares use ceil(fraction × n) tasks; overall tails use fractional weighted mass. A zero median makes p90/p50 undefined.",
        "Task boundaries, cap signals, outcomes and timestamps depend on export coverage. Unknown outcomes remain unknown. Missing timestamps prevent temporal validation; missing models or usage prevent complete-cost pricing. Tools without arguments cannot be assessed for identical-argument loops.",
        "Only sanitized metadata was written by moira. Parsing necessarily uses memory; operating-system swap and external crash collectors are outside this guarantee. Keyed IDs and argument digests are pseudonyms, not anonymization; they are consistent within one moira install only.",
        *(["Grouped intervals resample whole task groups with replacement, keep every run of a drawn group in one fold, and refit prices, caps and censoring tails in each of 1,000 draws. They describe variation across groups like these, not new kinds of task or production drift."] if report["grouped"] else []),
        "Drift ratios and recency prices describe the observed period. A recent window is smaller than the full period, so its prices and intervals are noisier; the current last-window price is in-sample. Rate-change projections hold usage fixed and change only rates.",
        f"Seed: {report['seed']}. Bootstrap draws: 2,000. Report generated: {report['generated_at']}. No network requests are required to view this file.",
    ]
    return result


def render(report, output):
    parts = sections(report)
    template = files("moira.report").joinpath("templates/report.html.j2").read_text()
    env = Environment(loader=BaseLoader(), autoescape=select_autoescape(default=True))
    html = env.from_string(template).render(sections=parts)
    md = []

    def cell(value):
        return escape(str(value)).replace("|", "\\|").replace("\n", " ")

    for i, section in enumerate(parts):
        md += [("# " if i == 0 else "## ") + section["title"], ""]
        for paragraph in section["paragraphs"]:
            md += [cell(paragraph), ""]
        for table in section["tables"]:
            md += [
                "### " + cell(table["title"]),
                "",
                "| " + " | ".join(table["headers"]) + " |",
                "| " + " | ".join("---" for _ in table["headers"]) + " |",
            ]
            md += ["| " + " | ".join(cell(v) for v in row) + " |" for row in table["rows"]]
            if not table["rows"]:
                md += ["", "No available observations for this table."]
            md.append("")
        if section["charts"]:
            md += [
                "Charts are embedded in the companion self-contained HTML; numerical results are above.",
                "",
            ]
    output = Path(output)
    if output.suffix.lower() != ".html":
        raise ValueError("output_must_end_in_html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    output.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    return output

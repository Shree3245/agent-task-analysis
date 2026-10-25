import argparse
from importlib.resources import files
import json
from pathlib import Path
import sys

import yaml

from agent_task_analysis import __version__
from agent_task_analysis.adapters import SOURCES
from agent_task_analysis.privacy import SafeError


def config(path):
    if not path:
        return {}
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict):
        raise SafeError("configuration_must_be_a_mapping")
    return data


def bound(value, end=False):
    """An ISO date or timestamp; a bare --until date includes that whole day (UTC)."""
    from datetime import datetime, timedelta, timezone

    try:
        if len(value) == 10:
            moment = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
            return moment + timedelta(days=1) if end else moment, len(value) == 10
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise SafeError("invalid_since_or_until") from None
    return (moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)), False


def select_window(tasks, since=None, until=None):
    """Keep tasks that started in [since, until); tasks without a start time are dropped
    once either bound is set."""
    from datetime import datetime

    if not since and not until:
        return tasks, None
    start = bound(since)[0] if since else None
    stop, whole_day = bound(until, end=True) if until else (None, False)
    if start and stop and start >= stop:
        raise SafeError("since_must_precede_until")
    kept, outside, untimed = [], 0, 0
    for task in tasks:
        if not task.started_at:
            untimed += 1
            continue
        moment = datetime.fromisoformat(task.started_at)
        if (start and moment < start) or (stop and (moment >= stop if whole_day else moment > stop)):
            outside += 1
        else:
            kept.append(task)
    return kept, {"since": since, "until": until, "outside": outside, "untimed": untimed}


def write_report(
    db, output, *, target=0.7, prices=None, redact=False, seed=0, min_samples=30, repeat=3,
    since=None, until=None, recent_days=30, rates=None,
):
    from agent_task_analysis.storage import connect, load, manifest
    from agent_task_analysis.pricing.catalog import load_catalog
    from agent_task_analysis.report.model import make_report
    from agent_task_analysis.report.render import render

    with connect(db, read_only=True) as conn:
        tasks, evidence = load(conn), manifest(conn)
    tasks, window = select_window(tasks, since, until)
    if not tasks:
        raise SafeError("database_has_no_tasks" if not window else "no_tasks_in_window")
    report = make_report(
        tasks,
        evidence,
        load_catalog(prices, overrides=rates),
        target=target,
        redact=redact,
        seed=seed,
        min_samples=min_samples,
        repeat=repeat,
        recent_days=recent_days,
        window=window,
    )
    render(report, output)
    return {
        "tasks": len(tasks),
        "types": len(report["groups"]),
        "repricing": report["reconciliation"]["acceptance"],
        "repricing_agreement": report["reconciliation"]["agreement"],
    }


def show(output):
    """Open the finished report in the default browser. Skipped when stdout is not a
    terminal (scripts, CI), so piped JSON output never launches anything."""
    import webbrowser

    path = Path(output).resolve()
    if not sys.stdout.isatty():
        return
    try:
        opened = webbrowser.open(path.as_uri())
    except Exception:
        opened = False
    if opened:
        print(f"agent-task-analysis: opened {path} in your browser", file=sys.stderr)
    else:
        print(f"agent-task-analysis: report written to {path}", file=sys.stderr)


def api_key(env):
    import getpass
    import os

    key = os.environ.get(env)
    if not key and sys.stdin.isatty():
        key = getpass.getpass("Braintrust API key (not stored): ")
    if not key:
        raise SafeError("braintrust_api_key_required_set_" + env)
    return key.strip()


def braintrust(args):
    """Fetch -> metadata-only import into a new database -> report."""
    import hashlib
    from datetime import datetime, timezone
    from agent_task_analysis.ingest import ingest_records
    from agent_task_analysis.remote.braintrust import fetch

    if args.days < 1 or args.settle_minutes < 0:
        raise SafeError("invalid_days_or_settle_minutes")
    db = args.db
    if db is None:
        tag = hashlib.sha256(f"{args.org or ''}/{args.project}".encode()).hexdigest()[:10]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        db = Path(".agent-task-analysis") / f"braintrust-{tag}-{stamp}.duckdb"
    if Path(db).exists():
        raise SafeError("database_exists_use_a_new_db_path")
    events, stats = fetch(args.project, api_key(args.api_key_env), org=args.org,
                          api_url=args.api_url, days=args.days,
                          settle_minutes=args.settle_minutes)
    print(f"agent-task-analysis: fetched {stats['events']} spans in {stats['traces']} finished traces "
          f"({stats['traces_in_progress']} still active, {stats['traces_before_window']} "
          f"older than {args.days} days left out)", file=sys.stderr)
    if not events:
        raise SafeError("no_finished_traces_in_window")
    ingest_records("braintrust", ((f"api:{i}", e) for i, e in enumerate(events)), db,
                   options={"drop_tasks_without_model_calls": True},
                   extra_evidence={"remote": stats})
    result = write_report(db, args.out, target=args.target, prices=args.prices,
                          redact=args.redact_task_ids, seed=args.seed,
                          min_samples=args.min_samples, recent_days=args.recent_days,
                          rates=args.rates)
    return result | {"db": str(db), "out": str(args.out)}


def parser():
    p = argparse.ArgumentParser(
        prog="agent-task-analysis", description="Private, offline cost audits for agent logs"
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    ing = sub.add_parser("ingest", help="Read local logs and retain metadata only")
    ing.add_argument("source", choices=SOURCES)
    ing.add_argument("path", type=Path)
    ing.add_argument("--db", type=Path, default=Path(".agent-task-analysis/agent-task-analysis.duckdb"))
    ing.add_argument(
        "--namespace", default="", help="Distinguish evaluation runs with reused task IDs"
    )
    ing.add_argument("--columns", type=Path, help="CSV mapping YAML")
    ing.add_argument("--rules", type=Path, help="Metadata-only classifier YAML")
    ing.add_argument("--benchmark", action="store_true")
    cls = sub.add_parser("classify", help="Override task types locally")
    cls.add_argument("--map", required=True, type=Path)
    cls.add_argument("--db", type=Path, default=Path(".agent-task-analysis/agent-task-analysis.duckdb"))
    rep = sub.add_parser("report", help="Write self-contained HTML plus Markdown")
    rep.add_argument("--db", type=Path, default=Path(".agent-task-analysis/agent-task-analysis.duckdb"))
    rep.add_argument("--target", type=float, default=0.7)
    rep.add_argument("--out", type=Path, default=Path("report.html"))
    rep.add_argument("--prices", type=Path)
    rep.add_argument("--redact-task-ids", action="store_true")
    rep.add_argument("--seed", type=int, default=0)
    rep.add_argument("--min-samples", type=int, default=30)
    rep.add_argument("--loop-repeat", type=int, default=3)
    rep.add_argument("--since", help="Only tasks that started on or after this ISO date/time")
    rep.add_argument("--until", help="Only tasks that started before the end of this ISO date, or at/before this time")
    rep.add_argument("--recent-days", type=int, default=30,
                     help="Recency window for drift and recent-window pricing")
    rep.add_argument("--rates", type=Path,
                     help="Rate-override YAML for unlisted models or contract rates")
    rep.add_argument("--no-open", action="store_true",
                     help="Do not open the report in a browser when it is written")
    rep.add_argument(
        "--update-prices",
        metavar="HTTPS_URL",
        help="Explicit opt-in: fetch a versioned YAML catalog",
    )
    rep.add_argument("--prices-sha256", help="Expected SHA-256 for an explicit price update")
    bt = sub.add_parser("braintrust", help="Fetch a Braintrust project's logs (network opt-in) and write a report")
    bt.add_argument("--project", required=True, help="Braintrust project name")
    bt.add_argument("--org", help="Organization name, if the project name exists in several")
    bt.add_argument("--api-key-env", default="BRAINTRUST_API_KEY",
                    help="Environment variable holding the API key (prompted if unset)")
    bt.add_argument("--api-url", default="https://api.braintrust.dev",
                    help="https://api-eu.braintrust.dev or a self-hosted data plane URL")
    bt.add_argument("--days", type=int, default=90, help="Fetch traces started in the last N days")
    bt.add_argument("--settle-minutes", type=int, default=30,
                    help="Leave out traces active in the last N minutes (still running)")
    bt.add_argument("--db", type=Path, help="New database path (default: a new file under .agent-task-analysis/)")
    bt.add_argument("--out", type=Path, default=Path("braintrust-report.html"))
    bt.add_argument("--target", type=float, default=0.7)
    bt.add_argument("--prices", type=Path)
    bt.add_argument("--rates", type=Path)
    bt.add_argument("--recent-days", type=int, default=30)
    bt.add_argument("--min-samples", type=int, default=30)
    bt.add_argument("--seed", type=int, default=0)
    bt.add_argument("--redact-task-ids", action="store_true")
    bt.add_argument("--no-open", action="store_true",
                    help="Do not open the report in a browser when it is written")
    demo = sub.add_parser("demo", help="Run bundled metadata sample offline")
    demo.add_argument("--out", type=Path, default=Path("demo-report.html"))
    demo.add_argument("--no-open", action="store_true",
                      help="Do not open the report in a browser when it is written")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "ingest":
            from agent_task_analysis.ingest import ingest

            options = config(args.columns)
            if args.rules:
                options["rules"] = config(args.rules)["rules"]
            result = ingest(
                args.source,
                args.path,
                args.db,
                namespace=args.namespace,
                options=options,
                benchmark=args.benchmark,
            )
        elif args.command == "classify":
            from agent_task_analysis.classify import apply_map

            result = {"updated_tasks": apply_map(args.db, config(args.map))}
        elif args.command == "braintrust":
            if not 0 < args.target < 1 or args.min_samples < 2 or args.recent_days < 1:
                raise SafeError("invalid_target_or_sample_threshold")
            result = braintrust(args)
        elif args.command == "report":
            if not 0 < args.target < 1 or args.min_samples < 2 or args.loop_repeat < 2:
                raise SafeError("invalid_target_or_sample_threshold")
            if args.recent_days < 1:
                raise SafeError("invalid_recent_days")
            if args.update_prices:
                from agent_task_analysis.pricing.update import update_prices

                args.prices = args.prices or args.db.parent / "prices.updated.yaml"
                update_prices(args.update_prices, args.prices, args.prices_sha256)
            result = write_report(
                args.db,
                args.out,
                target=args.target,
                prices=args.prices,
                redact=args.redact_task_ids,
                seed=args.seed,
                min_samples=args.min_samples,
                repeat=args.loop_repeat,
                since=args.since,
                until=args.until,
                recent_days=args.recent_days,
                rates=args.rates,
            )
        else:
            import tempfile
            from agent_task_analysis.ingest import ingest

            # Temporary files contain sanitized metadata only, never source content.
            with tempfile.TemporaryDirectory(prefix="agent-task-analysis-demo-") as temp:
                db = Path(temp) / "demo.duckdb"
                sample = files("agent_task_analysis").joinpath("data/demo/sample.jsonl")
                ingest("otel", Path(str(sample)), db, benchmark=True)
                from agent_task_analysis.storage import connect, manifest

                provenance = json.loads(
                    files("agent_task_analysis").joinpath("data/demo/provenance.json").read_text()
                )
                with connect(db) as conn:
                    evidence = manifest(conn)
                    evidence["benchmark_scope"] = (
                        "Bundled metadata-only public Exgentic sample; "
                        + provenance["selection"]
                        + " Source: "
                        + provenance["source"]
                        + " @ "
                        + provenance["revision"]
                        + ". "
                        + provenance["recorded_costs"]
                    )
                    serialized = json.dumps(evidence).replace("'", "''")
                    conn.execute(f"COMMENT ON TABLE tasks IS '{serialized}'")
                result = write_report(db, args.out, redact=True)
        print(json.dumps(result, sort_keys=True))
        if args.command in ("report", "braintrust", "demo") and not args.no_open:
            show(args.out)
        return 0
    except SafeError as exc:
        print("agent-task-analysis: " + str(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("agent-task-analysis: interrupted", file=sys.stderr)
        return 130
    except Exception:
        # Parser/database exceptions can quote content: never echo their messages/locals.
        print(
            "agent-task-analysis: operation_failed (invalid input, configuration, or local I/O); no payload logged",
            file=sys.stderr,
        )
        return 2

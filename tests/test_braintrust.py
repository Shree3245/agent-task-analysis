from datetime import datetime, timedelta, timezone
import uuid

import pytest

from agent_task_analysis.adapters.braintrust import extract
from agent_task_analysis.adapters.base import Context
from agent_task_analysis.cli import main
from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.pricing.reprice import call_cost
from agent_task_analysis.privacy import SafeError
from agent_task_analysis.remote import braintrust as remote
from agent_task_analysis.storage import connect, load, manifest

NOW = datetime(2025, 3, 1, 12, tzinfo=timezone.utc)


def at(minutes_ago):
    return (NOW - timedelta(minutes=minutes_ago)).timestamp()


def trace(name, minutes_ago, canary, *, calls=2, tools=1, error=False, model="claude-sonnet-4-5"):
    """One root task span, `calls` Anthropic-style LLM spans, `tools` tool spans."""
    start = at(minutes_ago)
    root = {"id": f"{name}-root", "span_id": name, "root_span_id": name, "is_root": True,
            "created": datetime.fromtimestamp(start, timezone.utc).isoformat(),
            "span_attributes": {"name": "answer_question", "type": "task"},
            "metadata": {"user_email": canary, "model": model},
            "input": canary, "output": canary, "metrics": {"start": start, "end": start + 50}}
    if error:
        root["error"] = "Traceback ... " + canary
    events = [root]
    for i in range(calls):
        t = start + 10 * i
        events.append({
            "id": f"{name}-llm{i}", "span_id": f"{name}-llm{i}", "root_span_id": name,
            "span_parents": [name], "created": datetime.fromtimestamp(t, timezone.utc).isoformat(),
            "span_attributes": {"name": "anthropic.messages.create", "type": "llm"},
            "metadata": {"model": model, "provider": "anthropic", "system": canary},
            "input": [{"role": "user", "content": canary}],
            "output": [{"type": "text", "text": canary},
                       {"type": "tool_use", "id": "tu", "name": "search", "input": {"q": canary}}],
            # Braintrust totals: prompt_tokens includes cache reads and writes.
            "metrics": {"start": t, "end": t + 5, "prompt_tokens": 1000 + 300 + 200,
                        "prompt_cached_tokens": 300, "prompt_cache_creation_tokens": 200,
                        "completion_tokens": 100, "tokens": 1600}})
    for i in range(tools):
        events.append({"id": f"{name}-tool{i}", "span_id": f"{name}-tool{i}", "root_span_id": name,
                       "created": datetime.fromtimestamp(start + 1, timezone.utc).isoformat(),
                       "span_attributes": {"name": "search", "type": "tool"},
                       "input": {"q": canary}, "output": canary, "metrics": {"start": start + 1}})
    events.append({"id": f"{name}-score", "span_id": f"{name}-score", "root_span_id": name,
                   "span_attributes": {"name": "Factuality", "type": "score", "purpose": "scorer"},
                   "metadata": {"model": "gpt-4o-mini"}, "created": root["created"],
                   "metrics": {"start": start, "prompt_tokens": 50, "completion_tokens": 5}})
    return events


class FakeAPI:
    def __init__(self, pages, projects=None):
        self.pages, self.calls = pages, []
        self.projects = projects or [{"id": "proj-1", "name": "Support Bot", "org_id": "o1"}]

    def __call__(self, method, url, key, body=None):
        self.calls.append((method, url, key, body))
        if method == "GET":
            return {"objects": self.projects}
        index = int(body.get("cursor") or 0)
        return {"events": self.pages[index],
                "cursor": str(index + 1) if index + 1 < len(self.pages) else None}


def test_adapter_prices_inclusive_braintrust_metrics_and_reads_trace_metadata():
    ctx = Context("braintrust")
    pieces = list(extract({"events": trace("t1", 120, "c", error=True)}, ctx, "f"))
    llm = [c for p in pieces for c in p.calls if c.event_kind == "model"]
    assert len(llm) == 2 and ctx.warnings.get("scorer_span_skipped") == 1
    call = llm[0]
    assert (call.input_tokens, call.cached_input_tokens, call.cache_write_input_tokens,
            call.output_tokens) == (1000, 300, 200, 100)
    assert call_cost(call, load_catalog())[0] == pytest.approx(
        (1000 * 3 + 300 * 0.3 + 200 * 3.75 + 100 * 15) / 1e6)
    root = next(p for p in pieces if p.task_type != "unknown")
    assert root.task_type == "answer_question" and root.outcome == "fail"
    tools = [c for p in pieces for c in p.calls if c.event_kind == "tool"]
    assert len(tools) == 3 and all(len(c.tool_args_hash) == 64 for c in tools)
    assert len({p.task_id for p in pieces}) == 1


def test_older_exclusive_prompt_tokens_and_one_hour_cache_writes_are_flagged():
    ctx = Context("braintrust")
    event = {"id": "e", "span_id": "s", "root_span_id": "r",
             "span_attributes": {"type": "llm"}, "metadata": {"model": "claude-sonnet-4-5"},
             "metrics": {"prompt_tokens": 100, "prompt_cached_tokens": 500,
                         "prompt_cache_creation_5m_tokens": 10,
                         "prompt_cache_creation_1h_tokens": 20, "completion_tokens": 7}}
    (piece,) = extract(event, ctx, "f")
    call = piece.calls[0]
    assert (call.input_tokens, call.cached_input_tokens, call.cache_write_input_tokens) == (100, 500, 30)
    assert ctx.warnings == {"prompt_tokens_exclusive_of_cache": 1,
                            "cache_write_1h_priced_at_5m_rate": 1}


def test_fetch_pages_dedupes_and_leaves_out_running_and_old_traces():
    new = trace("new", 120, "c")
    stale_version = dict(new[1], metrics={"prompt_tokens": 1})  # older version on a later page
    pages = [new + trace("running", 5, "c"), [stale_version] + trace("old", 60 * 24 * 100, "c")]
    api = FakeAPI(pages)
    events, stats = remote.fetch("Support Bot", "sk-test", days=90, call=api, now=NOW)
    assert {e["root_span_id"] for e in events} == {"new"}
    assert next(e for e in events if e["id"] == "new-llm0")["metrics"]["prompt_tokens"] == 1500
    assert (stats["traces"], stats["traces_in_progress"], stats["traces_before_window"]) == (1, 1, 1)
    assert api.calls[0][1] == "https://api.braintrust.dev/v1/project?project_name=Support+Bot"
    assert api.calls[1][1] == "https://api.braintrust.dev/v1/project_logs/proj-1/fetch"
    assert [c[3] for c in api.calls[1:]] == [{"limit": 200}, {"limit": 200, "cursor": "1"}]


def test_project_lookup_and_url_checks():
    with pytest.raises(SafeError, match="project_not_found"):
        remote.fetch("Nope", "k", call=FakeAPI([[]], projects=[{"id": "x", "name": "Other"}]), now=NOW)
    two = [{"id": "a", "name": "Bot", "org_id": "o1"}, {"id": "b", "name": "Bot", "org_id": "o2"}]
    with pytest.raises(SafeError, match="several_orgs"):
        remote.fetch("Bot", "k", call=FakeAPI([[]], projects=two), now=NOW)
    with pytest.raises(SafeError, match="https"):
        remote.fetch("Bot", "k", api_url="http://api.braintrust.dev", call=FakeAPI([[]]), now=NOW)


def test_braintrust_command_keeps_no_content_key_or_project(tmp_path, monkeypatch, capsys):
    canary, key = "PRIVATE_" + uuid.uuid4().hex, "sk-" + uuid.uuid4().hex
    now = datetime.now(timezone.utc)
    shift = (now - NOW).total_seconds()

    def moved(events):
        for e in events:
            for k in ("start", "end"):
                if k in e.get("metrics", {}):
                    e["metrics"][k] += shift
            e["created"] = datetime.fromisoformat(e["created"]).timestamp() + shift
            e["created"] = datetime.fromtimestamp(e["created"], timezone.utc).isoformat()
        return events

    pages = [moved([e for i in range(40) for e in trace(f"{canary}-t{i}", 60 * (i + 2), canary,
                                                        error=i % 4 == 0)])]
    monkeypatch.setattr(remote, "http", FakeAPI(pages, [{"id": "p", "name": canary, "org_id": "o"}]))
    monkeypatch.setenv("BRAINTRUST_API_KEY", key)
    monkeypatch.chdir(tmp_path)
    db, out = tmp_path / "bt.duckdb", tmp_path / "bt.html"
    assert main(["braintrust", "--project", canary, "--db", str(db), "--out", str(out)]) == 0
    with connect(db, read_only=True) as conn:
        tasks = load(conn)
        evidence = manifest(conn)
    assert len(tasks) == 40 and {t.outcome for t in tasks} == {"fail", "unknown"}
    assert evidence["imports"][0]["remote"]["traces"] == 40
    md = out.with_suffix(".md").read_text()
    assert "Fetched over the network from api.braintrust.dev" in md
    for file in tmp_path.rglob("*"):
        if file.is_file():
            data = file.read_bytes()
            assert canary.encode() not in data and key.encode() not in data, file.name
    captured = capsys.readouterr()
    assert canary not in captured.out + captured.err and key not in captured.out + captured.err
    # A rerun never appends to an existing database.
    assert main(["braintrust", "--project", canary, "--db", str(db), "--out", str(out)]) == 2


def test_missing_key_fails_without_prompting(monkeypatch, tmp_path):
    monkeypatch.delenv("BRAINTRUST_API_KEY", raising=False)
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    monkeypatch.chdir(tmp_path)
    assert main(["braintrust", "--project", "x"]) == 2


def test_report_opens_in_browser_only_on_a_terminal(monkeypatch, tmp_path):
    import webbrowser

    from agent_task_analysis import cli

    opened = []
    monkeypatch.setattr(webbrowser, "open", lambda url: opened.append(url) or True)
    out = tmp_path / "r.html"
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False, raising=False)
    cli.show(out)
    assert opened == []
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True, raising=False)
    cli.show(out)
    assert opened == [out.resolve().as_uri()]

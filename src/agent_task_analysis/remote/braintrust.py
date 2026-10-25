"""Fetch a Braintrust project's logs over its REST API. Explicit opt-in: only
`agent-task-analysis braintrust` calls this module.

The API returns whole spans, prompts and completions included. Each event is cut down
in memory to the allowlisted metadata the braintrust adapter reads, as soon as its page
arrives; tool arguments are kept only until the adapter hashes them. Nothing raw is
written to disk, and the API key is never stored or printed.
"""

from datetime import datetime, timedelta, timezone
import json
import time
from urllib.parse import quote, urlencode, urlsplit

from agent_task_analysis.adapters.braintrust import output_tools
from agent_task_analysis.privacy import SafeError
from agent_task_analysis.schema import timestamp

API_URL = "https://api.braintrust.dev"
PAGE_TRACES = 200
RETRIES = 4
METADATA = ("model", "provider", "task_type", "task.type", "outcome", "task.outcome",
            "capped", "cap_reason")


def http(method, url, key, body=None):
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json",
               "User-Agent": "agent-task-analysis-braintrust/0.1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(RETRIES + 1):
        try:
            with urlopen(Request(url, data=data, headers=headers, method=method), timeout=120) as r:
                return json.loads(r.read())
        except HTTPError as error:
            if error.code in (401, 403):
                raise SafeError("braintrust_api_key_rejected") from None
            if error.code == 404:
                raise SafeError("braintrust_not_found") from None
            if error.code != 429 and error.code < 500 or attempt == RETRIES:
                raise SafeError(f"braintrust_http_{error.code}") from None
            wait = error.headers.get("Retry-After") if error.headers else None
            time.sleep(min(60, float(wait) if wait and wait.isdigit() else 2 ** attempt))
        except (URLError, TimeoutError, ValueError):
            if attempt == RETRIES:
                raise SafeError("braintrust_unreachable") from None
            time.sleep(2 ** attempt)


def check_url(api_url):
    parts = urlsplit(api_url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.query:
        raise SafeError("braintrust_api_url_must_be_https_without_credentials")
    return api_url.rstrip("/")


def project_id(call, api_url, key, project, org=None):
    query = {"project_name": project} | ({"org_name": org} if org else {})
    found = (call("GET", f"{api_url}/v1/project?{urlencode(query)}", key) or {}).get("objects") or []
    found = [p for p in found if isinstance(p, dict) and p.get("name") == project]
    if not found:
        raise SafeError("braintrust_project_not_found")
    if len({p.get("org_id") for p in found}) > 1:
        raise SafeError("braintrust_project_name_in_several_orgs_use_org")
    return found[0]["id"]


def slim(event):
    """Allowlisted metadata only; prompts, completions, scores and free text are dropped."""
    attributes = event.get("span_attributes") or {}
    metadata = event.get("metadata") or {}
    metrics = event.get("metrics") or {}
    result = {k: event.get(k) for k in ("id", "span_id", "root_span_id", "is_root", "created")}
    result["span_attributes"] = {k: attributes.get(k) for k in ("name", "type", "purpose")
                                 if isinstance(attributes, dict)}
    result["metadata"] = {k: metadata[k] for k in METADATA
                          if isinstance(metadata, dict) and k in metadata}
    result["metrics"] = {k: v for k, v in metrics.items() if isinstance(metrics, dict)
                         and isinstance(v, (int, float)) and not isinstance(v, bool)}
    # Presence only: the error text is never kept.
    result["error"] = True if event.get("error") not in (None, "", {}) else None
    kind = result["span_attributes"].get("type")
    if kind == "tool":
        result["input"] = event.get("input")
    elif kind == "llm" or "prompt_tokens" in result["metrics"]:
        tools = output_tools(event.get("output"))
        result["output"] = {"tool_calls": [
            {"function": {"name": (t.get("function") or t).get("name"),
                          "arguments": (t.get("function") or t).get("arguments",
                                                                   (t.get("function") or t).get("input"))}}
            for t in tools if isinstance(t, dict)]}
    return result


def fetch(project, key, *, org=None, api_url=API_URL, days=90, settle_minutes=30, call=None,
          now=None):
    """Returns (events, stats) for traces that started in the last `days` and have been
    quiet for `settle_minutes` (a trace still running would be priced on partial spend)."""
    call = call or http
    api_url = check_url(api_url)
    now = now or datetime.now(timezone.utc)
    since = (now - timedelta(days=days)).isoformat()
    settled = (now - timedelta(minutes=settle_minutes)).isoformat()
    pid = project_id(call, api_url, key, project, org)
    url = f"{api_url}/v1/project_logs/{quote(pid, safe='')}/fetch"
    seen, cursor, pages = {}, None, 0
    while True:
        page = call("POST", url, key, {"limit": PAGE_TRACES} | ({"cursor": cursor} if cursor else {}))
        events = (page or {}).get("events") or []
        pages += 1
        older = 0
        for event in events:
            if not isinstance(event, dict) or not event.get("id"):
                continue
            created = timestamp(event.get("created"))
            older += bool(created and created < since)
            # Pages run newest first and may repeat older versions of a row: keep the first.
            seen.setdefault(event["id"], slim(event))
        cursor = (page or {}).get("cursor")
        if not events or not cursor or older == len(events):
            break
    traces = {}
    for event in seen.values():
        traces.setdefault(event.get("root_span_id") or event.get("span_id"), []).append(event)
    kept, stats = [], {"pages": pages, "events": len(seen), "traces_before_window": 0,
                       "traces_in_progress": 0}
    for events in traces.values():
        times = [t for e in events for t in (timestamp(e.get("created")),
                 timestamp(e["metrics"].get("start")), timestamp(e["metrics"].get("end"))) if t]
        if times and min(times) < since:
            stats["traces_before_window"] += 1
        elif times and max(times) > settled:
            stats["traces_in_progress"] += 1
        else:
            kept.extend(events)
    stats["traces"] = len(traces) - stats["traces_before_window"] - stats["traces_in_progress"]
    return kept, stats | {"api_host": urlsplit(api_url).hostname, "fetched_at": now.isoformat(),
                          "window_days": days, "settle_minutes": settle_minutes}

import json
import re

from conftest import FIXTURES
from agent_task_analysis.cli import main
from agent_task_analysis.ingest import ingest
from agent_task_analysis.report.dashboard import STATUS, more_reason


def dashboard_data(html):
    return json.loads(re.search(r'id="report-data">(.*?)</script>', html, re.S).group(1))


def test_report_embeds_one_dashboard_entry_per_task_type(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["demo", "--no-open"]) == 0
    data = dashboard_data((tmp_path / "demo-report.html").read_text())
    assert data["groups"] and data["n_tasks"] > 0
    for g in data["groups"]:
        assert g["status"] in STATUS and g["label"] == STATUS[g["status"]]
        assert g["costs"] == sorted(g["costs"])
        if g["status"] in ("ready", "watch"):
            assert g["price"] > 0 and g["upper"] < 0.9
        if g["status"] == "more":
            assert g["reason"]


def test_dashboard_data_has_no_task_ids_or_markup(tmp_path):
    db = tmp_path / "db.duckdb"
    ingest("otel", FIXTURES / "otel/sample.json", db)
    out = tmp_path / "report.html"
    assert main(["report", "--db", str(db), "--out", str(out), "--no-open"]) == 0
    blob = re.search(r'id="report-data">(.*?)</script>', out.read_text(), re.S).group(1)
    assert "task_id" not in blob and "otel:task-1" not in blob and "<" not in blob


def test_more_reason_names_the_missing_side():
    few = {"grouped": False, "n_total": 7, "n_capped": 0, "split_counts": {"train": 7, "test": 0}}
    assert more_reason(few, None, "Sep 28, 2026", 30).startswith("Only 7 runs so far.")
    g = {"grouped": False, "n_total": 90, "n_capped": 0, "split_counts": {"train": 90, "test": 0}}
    assert "no newer runs" in more_reason(g, None, "Sep 28, 2026", 30)
    row = {"train_uncapped": 45, "test_uncapped": 12}
    assert more_reason(g, row, "Sep 28, 2026", 30) == (
        "Only 12 runs since Sep 28, 2026 to test a price on. It needs 30.")


def test_backdated_split_holds_out_the_newest_third_after_training_ends():
    from datetime import datetime, timedelta
    from types import SimpleNamespace
    from agent_task_analysis.analysis.backtest import backdated_split

    start = datetime(2026, 9, 1)

    def task(i):
        begin = start + timedelta(hours=i)
        return SimpleNamespace(task=SimpleNamespace(
            started_at=begin.isoformat(), ended_at=(begin + timedelta(minutes=30)).isoformat(),
            capped=False))

    tasks = [task(i) for i in range(90)]
    cutoff, train, test = backdated_split(tasks, 30)
    assert len(test) == 30 and len(train) == 60
    assert max(t.task.ended_at for t in train) < cutoff <= min(t.task.started_at for t in test)
    assert backdated_split(tasks[:59], 30) is None  # cannot fill both sides

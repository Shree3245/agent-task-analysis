from conftest import FIXTURES
from agent_task_analysis.cli import main
from agent_task_analysis.ingest import ingest


def test_offline_demo_and_report_order(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["demo"]) == 0  # pytest-socket blocks all networking for the entire suite
    html = (tmp_path / "demo-report.html").read_text()
    titles = [
        "What this report saw",
        "Summary verdicts",
        "Cost audit",
        "Catastrophe cap",
        "Fixed-price simulation with confidence intervals",
        "Sample receipts",
        "Limits",
    ]
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert "<svg " in html and "<script" not in html
    assert 'src="http' not in html and 'href="http' not in html
    assert (tmp_path / "demo-report.md").exists()


def test_task_ids_are_redacted_everywhere(tmp_path):
    db = tmp_path / "db.duckdb"
    ingest("otel", FIXTURES / "otel/sample.json", db)
    out = tmp_path / "report.html"
    assert main(["report", "--db", str(db), "--out", str(out), "--redact-task-ids"]) == 0
    assert "otel:task-1" not in out.read_text() + out.with_suffix(".md").read_text()

from pathlib import Path
import pytest

from agent_task_analysis import privacy
from agent_task_analysis.ingest import ingest
from agent_task_analysis.storage import connect, load
from agent_task_analysis.pricing.catalog import load_catalog
from agent_task_analysis.pricing.reprice import call_cost

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def agent_task_analysis_home(tmp_path_factory, monkeypatch):
    """Never touch the real ~/.agent-task-analysis: one keyed install per test session."""
    home = tmp_path_factory.getbasetemp() / "agent-task-analysis-home"
    monkeypatch.setenv("AGENT_TASK_ANALYSIS_HOME", str(home))
    monkeypatch.setattr(privacy, "_secret", None)
    return home
CSV_OPTIONS = {
    "token_semantics": "exclusive",
    "columns": {
        k: k
        for k in (
            "task_id",
            "task_type",
            "provider",
            "model",
            "input_tokens",
            "output_tokens",
            "recorded_cost",
            "tool_name",
            "tool_args",
        )
    },
}


def check_adapter(source, tmp_path):
    file = FIXTURES / source / ("sample.csv" if source == "csv" else "sample.json")
    db = tmp_path / "test.duckdb"
    result = ingest(source, file, db, options=CSV_OPTIONS if source == "csv" else {})
    assert result["inserted_tasks"] == result["inserted_calls"] == 1
    with connect(db, read_only=True) as conn:
        tasks = load(conn)
    call = next(c for c in tasks[0].calls if c.event_kind == "model")
    assert call.input_tokens == 150 and call.output_tokens == 20
    assert call_cost(call, load_catalog())[0] == pytest.approx(0.0000345)
    assert any(c.tool_args_hash and len(c.tool_args_hash) == 64 for c in tasks[0].calls)
    assert "__CONTENT_PLACEHOLDER__" not in repr(tasks[0].row()) + repr(
        [c.row() for c in tasks[0].calls]
    )

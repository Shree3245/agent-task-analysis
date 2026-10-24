import json
import uuid

import pytest
import yaml
from conftest import CSV_OPTIONS, FIXTURES
from moira.adapters import SOURCES
from moira.cli import main
from moira.storage import connect, load, manifest


@pytest.mark.parametrize("source", SOURCES)
def test_canary_never_written(source, tmp_path, monkeypatch, capsys):
    canary = "PRIVATE_" + uuid.uuid4().hex
    inputs, work = tmp_path / "original-inputs", tmp_path / "work"
    inputs.mkdir()
    work.mkdir()
    suffix = ".csv" if source == "csv" else ".json"
    original = FIXTURES / source / ("sample" + suffix)
    source_file = inputs / ("sample" + suffix)
    # The fixture's task ID ("task-1") carries the canary too: IDs must be hashed at ingest.
    source_file.write_text(
        original.read_text()
        .replace("__CONTENT_PLACEHOLDER__", canary)
        .replace("task-1", "id-" + canary)
    )
    assert source_file.read_text().count("id-" + canary) == 1
    monkeypatch.chdir(work)
    monkeypatch.setenv("TMPDIR", str(work))
    args = ["ingest", source, str(source_file)]
    if source == "csv":
        columns = work / "columns.yaml"
        columns.write_text(yaml.safe_dump(CSV_OPTIONS))
        args += ["--columns", str(columns)]
    assert main(args) == 0
    (work / "types.yaml").write_text("types:\n  code: code_review\n")
    assert main(["classify", "--map", "types.yaml"]) == 0
    assert main(["report", "--out", "report.html", "--redact-task-ids"]) == 0
    assert main(["report", "--out", "unredacted.html"]) == 0
    with connect(work / ".moira/moira.duckdb", read_only=True) as conn:
        for task in load(conn):
            assert canary not in json.dumps(task.row())
            assert canary not in json.dumps([c.row() for c in task.calls])
        assert canary not in json.dumps(manifest(conn))
    # Original fixtures are outside the work directory. Scan every generated artifact,
    # including database/WAL bytes, plus decoded DB values above (compression independent).
    for file in work.rglob("*"):
        if file.is_file():
            assert canary.encode() not in file.read_bytes(), file.name
    captured = capsys.readouterr()
    assert canary not in captured.out + captured.err


def test_error_does_not_echo_parser_content(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    canary = uuid.uuid4().hex
    bad = tmp_path.parent / f"bad-{canary}.json"
    try:
        bad.write_text('{"prompt": "' + canary + '", INVALID}')
        assert main(["ingest", "otel", str(bad)]) == 2
        captured = capsys.readouterr()
        assert canary not in captured.out + captured.err
        assert not (tmp_path / ".moira").exists()
    finally:
        bad.unlink(missing_ok=True)

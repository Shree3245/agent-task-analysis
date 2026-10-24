from conftest import FIXTURES
import pytest
from moira.ingest import ingest
from moira.storage import connect, load
from moira.privacy import SafeError, digest


def test_idempotency(tmp_path):
    fixture = FIXTURES / "otel/sample.json"
    db = tmp_path / "db.duckdb"
    assert ingest("otel", fixture, db)["inserted_tasks"] == 1
    assert ingest("otel", fixture, db)["duplicate_tasks"] == 1
    with connect(db, read_only=True) as conn:
        assert len(load(conn)) == 1
        assert len(conn.execute("SHOW TABLES").fetchall()) == 2


def test_conflict_is_atomic(tmp_path):
    original = FIXTURES / "otel/sample.json"
    db = tmp_path / "db.duckdb"
    ingest("otel", original, db)
    altered = tmp_path / "altered.json"
    altered.write_text(original.read_text().replace('"150"', '"999"'))
    with pytest.raises(SafeError, match="conflicting_task"):
        ingest("otel", altered, db)
    with connect(db, read_only=True) as conn:
        assert load(conn)[0].calls[0].input_tokens == 150


def test_full_sha256_canonicalizes_arguments():
    assert digest('{"b": 2, "a":1}') == digest({"a": 1, "b": 2})
    assert len(digest({"a": 1})) == 64

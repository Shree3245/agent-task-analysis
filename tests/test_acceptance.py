from conftest import CSV_OPTIONS, FIXTURES
from moira.adapters import SOURCES
from moira.ingest import ingest
from moira.storage import connect, load
from moira.pricing.catalog import load_catalog
from moira.pricing.reprice import reconcile


def test_standard_rate_reference_exports_meet_reconciliation_gate(tmp_path):
    db = tmp_path / "all-sources.duckdb"
    for source in SOURCES:
        fixture = FIXTURES / source / ("sample.csv" if source == "csv" else "sample.json")
        ingest(source, fixture, db, options=CSV_OPTIONS if source == "csv" else {})
    with connect(db, read_only=True) as conn:
        result = reconcile(load(conn), load_catalog())
    assert result["recorded_calls"] >= 5
    assert result["agreement"] >= 0.99
    assert result["acceptance"] == "PASS"

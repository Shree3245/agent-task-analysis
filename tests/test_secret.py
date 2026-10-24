import os
import stat

import pytest

from conftest import FIXTURES
from moira import privacy
from moira.cli import main
from moira.ingest import ingest
from moira.privacy import SafeError, digest, group_digest, task_digest
from moira.storage import connect


def fresh(monkeypatch, home):
    monkeypatch.setenv("MOIRA_HOME", str(home))
    monkeypatch.setattr(privacy, "_secret", None)


def test_secret_is_created_once_with_mode_600(tmp_path, monkeypatch):
    fresh(monkeypatch, tmp_path / "home")
    first = privacy.secret()
    path = tmp_path / "home/secret"
    assert len(first) == 32 and stat.S_IMODE(path.stat().st_mode) == 0o600
    assert stat.S_IMODE(path.parent.stat().st_mode) == 0o700
    monkeypatch.setattr(privacy, "_secret", None)
    assert privacy.secret() == first
    assert sorted(p.name for p in path.parent.iterdir()) == ["secret"]


def test_digests_are_keyed_per_install_and_domain_separated(tmp_path, monkeypatch):
    fresh(monkeypatch, tmp_path / "a")
    a = (task_digest("x"), group_digest("x"), digest("x"))
    assert len(set(a)) == 3 and all(len(v) == 64 for v in a)
    fresh(monkeypatch, tmp_path / "b")
    b = (task_digest("x"), group_digest("x"), digest("x"))
    assert not set(a) & set(b)


def test_open_secret_permissions_are_refused(tmp_path, monkeypatch):
    fresh(monkeypatch, tmp_path / "home")
    privacy.secret()
    os.chmod(tmp_path / "home/secret", 0o644)
    monkeypatch.setattr(privacy, "_secret", None)
    with pytest.raises(SafeError, match="mode_600"):
        privacy.secret()


def test_secret_never_reaches_database_or_reports(tmp_path, monkeypatch):
    fresh(monkeypatch, tmp_path / "home")
    key = privacy.secret()
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    assert main(["ingest", "otel", str(FIXTURES / "otel/sample.json")]) == 0
    assert main(["report", "--out", "report.html"]) == 0
    for file in work.rglob("*"):
        if file.is_file():
            data = file.read_bytes()
            assert key not in data and key.hex().encode() not in data, file.name


def test_database_from_another_install_refuses_writes(tmp_path, monkeypatch):
    db = tmp_path / "db.duckdb"
    fresh(monkeypatch, tmp_path / "a")
    ingest("otel", FIXTURES / "otel/sample.json", db)
    fresh(monkeypatch, tmp_path / "b")
    with pytest.raises(SafeError, match="different_key"):
        ingest("otel", FIXTURES / "otel/sample.json", db)
    with connect(db, read_only=True):
        pass  # Reading (reporting) still works; IDs are opaque either way.


def test_grouped_results_do_not_depend_on_the_install_key(tmp_path, monkeypatch):
    import hashlib
    from synthetic import grouped
    from moira.analysis.grouped import cross_validate
    from moira.analysis.history import build_history
    from moira.pricing.catalog import load_catalog

    def run(salt):
        tasks = grouped(capped_every=9)
        for t in tasks:  # A different install gives every group a different digest.
            t.task_group = hashlib.sha256((salt + t.task_group).encode()).hexdigest()
        rows = cross_validate(build_history(tasks, load_catalog()), [0.7], scope="grouped_cv", draws=100)
        return [(r["censoring"], r["capped"], r["loss_ratio"], r["ci"]) for r in rows]

    assert run("install-a") == run("install-b")


def test_time_split_interval_does_not_depend_on_task_order():
    from synthetic import ungrouped
    from moira.analysis.backtest import time_split
    from moira.analysis.fixed_price import simulations
    from moira.analysis.history import build_history
    from moira.pricing.catalog import load_catalog

    h = build_history(ungrouped(), load_catalog())
    _, train, test, _ = time_split(h)
    a = simulations(train, test, [0.7], scope="holdout")
    b = simulations(train[::-1], test[::-1], [0.7], scope="holdout")
    # Equal up to float summation order in the training mean.
    assert [r["ci"] for r in a] == [pytest.approx(r["ci"], rel=1e-12) for r in b]

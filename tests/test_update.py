import pytest
from moira.privacy import SafeError
from moira.pricing.update import update_prices
from moira.pricing.catalog import validate


def test_price_update_requires_explicit_safe_https_url(tmp_path):
    for url in [
        "http://example.com/prices.yaml",
        "https://user:secret@example.com/p",
        "https://example.com/p?task=private",
    ]:
        with pytest.raises(SafeError):
            update_prices(url, tmp_path / "p.yaml")
    assert not (tmp_path / "p.yaml").exists()


def test_catalog_rejects_nan_and_unresolved_aliases():
    with pytest.raises(SafeError):
        validate(
            {
                "schema_version": 1,
                "version": "v1",
                "currency": "USD",
                "models": {"x/y": {"input": float("nan"), "output": 1}},
            }
        )

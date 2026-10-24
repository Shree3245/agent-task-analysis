import datetime
import hashlib
from importlib.resources import files
import math
from pathlib import Path

import yaml

from moira.privacy import SafeError

RATE_CLASSES = ("input", "cached_input", "cache_write", "output")


def check_rates(rate):
    for name in RATE_CLASSES:
        value = rate.get(name)
        if value is not None and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            or value < 0
        ):
            raise SafeError("invalid_price_rate")


def effective_date(value):
    """A rate change takes effect at 00:00 UTC on its date."""
    if isinstance(value, datetime.datetime):
        value = value.date()
    if isinstance(value, str):
        try:
            value = datetime.date.fromisoformat(value)
        except ValueError:
            raise SafeError("invalid_rate_change_date") from None
    if not isinstance(value, datetime.date):
        raise SafeError("invalid_rate_change_date")
    return value.isoformat()


def check_models(models):
    if not isinstance(models, dict):
        raise SafeError("invalid_price_catalog")
    for key, rates in models.items():
        if not isinstance(key, str) or "/" not in key or not isinstance(rates, dict):
            raise SafeError("invalid_price_catalog")
        changes = rates.get("changes", [])
        if not isinstance(changes, list):
            raise SafeError("invalid_rate_changes")
        for rate in (rates, rates.get("long_context", {}), *changes,
                     *(c.get("long_context", {}) for c in changes if isinstance(c, dict))):
            if not isinstance(rate, dict):
                raise SafeError("invalid_rate_changes")
            check_rates(rate)
        if "input" not in rates or "output" not in rates:
            raise SafeError("missing_price_rate")
        dates = [effective_date(c.get("effective")) for c in changes]
        if len(set(dates)) != len(dates):
            raise SafeError("duplicate_rate_change_date")
        for change, date in zip(changes, dates):
            change["effective"] = date
        changes.sort(key=lambda c: c["effective"])


def validate(data):
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != 1
        or data.get("currency") != "USD"
    ):
        raise SafeError("invalid_price_catalog")
    if not isinstance(data.get("version"), str):
        raise SafeError("invalid_price_catalog")
    check_models(data.get("models"))
    for alias, target in data.get("aliases", {}).items():
        if target not in data["models"]:
            raise SafeError("invalid_price_alias")
    return data


def load_catalog(path=None, overrides=None):
    raw = (
        Path(path).read_bytes()
        if path
        else files("moira.pricing").joinpath("data/prices.v1.yaml").read_bytes()
    )
    data = validate(yaml.safe_load(raw)) | {"sha256": hashlib.sha256(raw).hexdigest()}
    return apply_overrides(data, overrides) if overrides else data


def apply_overrides(catalog, path):
    """User rates for unlisted models or contract rates. An override replaces the whole
    catalog entry for its model, including any dated changes the catalog lists."""
    raw = Path(path).read_bytes()
    data = yaml.safe_load(raw)
    if not isinstance(data, dict) or data.get("currency", "USD") != "USD" or not data.get("models"):
        raise SafeError("invalid_rate_overrides")
    check_models(data["models"])
    models = catalog["models"] | data["models"]
    aliases = catalog.get("aliases", {}) | (data.get("aliases") or {})
    if any(target not in models for target in aliases.values()):
        raise SafeError("invalid_price_alias")
    return catalog | {"models": models, "aliases": aliases, "overrides": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "description": " ".join(str(data.get("description") or "").split())[:1000],
        "replaced": sorted(set(data["models"]) & set(catalog["models"])),
        "added": sorted(set(data["models"]) - set(catalog["models"])),
        "models": sorted(data["models"]),
    }}


def rates_at(rates, when=None):
    """Rates in effect at an ISO timestamp; without one, the base rates."""
    if not rates.get("changes"):
        return rates
    result = {k: v for k, v in rates.items() if k != "changes"}
    day = when[:10] if when else None
    for change in rates["changes"]:
        if day is None or change["effective"] > day:
            break
        tier = change.get("long_context")
        result |= {k: v for k, v in change.items() if k in RATE_CLASSES}
        if tier:
            result["long_context"] = result.get("long_context", {}) | tier
    return result


def change_dates(catalog):
    return sorted({c["effective"] for rates in catalog["models"].values()
                   for c in rates.get("changes", [])})

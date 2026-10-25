"""The sole runtime network path. Only cli --update-prices calls this function."""

import hashlib
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from agent_task_analysis.pricing.catalog import validate
from agent_task_analysis.privacy import SafeError


def update_prices(url, destination, expected_sha256=None):
    # Imported here, never from ingest/report or package initialization.
    from urllib.request import Request, urlopen

    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query:
        raise SafeError("prices_require_public_https_url_without_credentials_or_query")
    with urlopen(
        Request(url, headers={"User-Agent": "agent-task-analysis-price-update/0.1"}), timeout=30
    ) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise SafeError("price_catalog_size_limit")
    checksum = hashlib.sha256(raw).hexdigest()
    if expected_sha256 and checksum != expected_sha256:
        raise SafeError("price_catalog_checksum_mismatch")
    validate(yaml.safe_load(raw))
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_bytes(raw)
    temp.replace(path)
    return checksum

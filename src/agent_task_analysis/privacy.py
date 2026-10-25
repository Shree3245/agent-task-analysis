"""Identifiers and tool arguments leave an adapter only as keyed digests (HMAC-SHA-256).

The key is a random per-install secret (~/.agent-task-analysis/secret, mode 600). It is never written
to a database or report, so digests are consistent within one install only.
"""

import hashlib
import hmac
import json
import os
from pathlib import Path
import re

SECRET_BYTES = 32
IDENTITY_HASH = re.compile(r"[0-9a-f]{64}")
_secret = None


class SafeError(Exception):
    """Messages are developer-authored codes, never input excerpts."""


def secret_path():
    return Path(os.environ.get("AGENT_TASK_ANALYSIS_HOME") or Path.home() / ".agent-task-analysis") / "secret"


def secret():
    """Create the key on first use; a hard link publishes it atomically, fully written."""
    global _secret
    if _secret is None:
        path = secret_path()
        if not path.exists():
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            temp = path.with_name(f".secret.{os.getpid()}.tmp")
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(os.urandom(SECRET_BYTES))
            try:
                os.link(temp, path)
            except FileExistsError:
                pass  # Another process created it first; use theirs.
            finally:
                temp.unlink()
        if path.stat().st_mode & 0o077:
            raise SafeError("secret_file_must_be_mode_600")
        key = path.read_bytes()
        if len(key) != SECRET_BYTES:
            raise SafeError("invalid_secret_file")
        _secret = key
    return _secret


def keyed(domain, data):
    # Domains keep a task ID, a task group and a tool argument with equal text distinct.
    return hmac.new(secret(), domain + b"\0" + data, hashlib.sha256).hexdigest()


def key_id():
    """Fingerprint stored in a database to refuse mixing two installs' digests."""
    return keyed(b"key-id", b"agent-task-analysis")[:16]


def digest(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, RecursionError):
            pass
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    except (TypeError, ValueError, RecursionError):
        raise SafeError("invalid_tool_arguments") from None
    return keyed(b"tool-args", encoded)


def label(value, default="unknown", limit=256):
    if value is None or value == "":
        return default
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise SafeError("invalid_metadata_label")
    value = str(value)
    if len(value) > limit or re.search(r"[\x00-\x1f\x7f]", value):
        raise SafeError("invalid_metadata_label")
    return value


def task_digest(value):
    """Task IDs are stored only as keyed digests, never as source names."""
    return keyed(b"task-id", label(value, limit=1024).encode())


def group_digest(value):
    return None if value is None or value == "" else keyed(b"task-group", label(value, limit=1024).encode())


def run_digest(value):
    return keyed(b"run-id", label(value, limit=1024).encode())


def redacted_id(task_id):
    return "task-" + hashlib.sha256(task_id.encode()).hexdigest()

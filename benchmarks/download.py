"""Explicit research-only download command. Not imported by the moira package."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import fnmatch
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml

SOURCES = yaml.safe_load(Path(__file__).with_name("sources.yaml").read_text())["sources"]


def fetch_json(url):
    with urlopen(url, timeout=60) as response:
        return json.load(response)


def catalog(source):
    spec = SOURCES[source]
    url = f"https://huggingface.co/api/datasets/{spec['repo']}/tree/{spec['revision']}?recursive=true&limit=1000"
    entries = []
    while url:
        with urlopen(url, timeout=60) as response:
            entries.extend(json.load(response))
            link = response.headers.get("Link", "")
            url = next(
                (
                    part.split(">")[0].strip().lstrip("<")
                    for part in link.split(",")
                    if 'rel="next"' in part
                ),
                None,
            )
    return [x for x in entries if x["type"] == "file"]


def download(source, destination, *, include=None, max_files=None, workers=4):
    spec = SOURCES[source]
    destination = Path(destination)
    repo_root = Path(__file__).resolve().parents[1]
    if destination.resolve().is_relative_to(repo_root):
        raise ValueError("Raw public downloads must be outside this repository")
    available = catalog(source)
    selected = [x for x in available if fnmatch.fnmatch(x["path"], include or spec["include"])]
    selected.sort(key=lambda x: x["path"])
    if max_files:
        selected = selected[:max_files]
    if not selected:
        raise ValueError("No files match selection")
    print(
        f"{source}: {len(selected)} files, {sum(x['size'] for x in selected) / 1e6:.1f} MB",
        flush=True,
    )

    def one(entry):
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe remote file path")
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        expected = entry.get("lfs", {}).get("oid")
        if not path.exists() or path.stat().st_size != entry["size"]:
            partial = path.with_suffix(path.suffix + ".part")
            offset = partial.stat().st_size if partial.exists() else 0
            url = f"https://huggingface.co/datasets/{spec['repo']}/resolve/{spec['revision']}/{quote(entry['path'])}"
            request = Request(url, headers={"Range": f"bytes={offset}-"} if offset else {})
            with urlopen(request, timeout=120) as response:
                append = offset and response.status == 206
                with partial.open("ab" if append else "wb") as handle:
                    while block := response.read(1024 * 1024):
                        handle.write(block)
            if partial.stat().st_size != entry["size"]:
                raise ValueError("Download size mismatch")
            partial.replace(path)
        hasher = hashlib.sha256()
        with path.open("rb") as handle:
            while block := handle.read(1024 * 1024):
                hasher.update(block)
        checksum = hasher.hexdigest()
        if expected and checksum != expected:
            raise ValueError("Download checksum mismatch")
        print(f"verified {entry['path']}", flush=True)
        return {"path": entry["path"], "bytes": entry["size"], "sha256": checksum}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(one, selected))
    previous_path = destination / "download-manifest.json"
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    if previous and (previous.get("repo"), previous.get("revision")) != (
        spec["repo"],
        spec["revision"],
    ):
        raise ValueError("Do not mix dataset revisions in one download directory")
    combined = {r["path"]: r for r in previous.get("files", [])}
    combined.update({r["path"]: r for r in records})
    records = [combined[k] for k in sorted(combined)]
    manifest = {
        "source": source,
        **spec,
        "selected_files": len(records),
        "available_files": len(available),
        "selection": include or spec["include"],
        "max_files": max_files,
        "files": records,
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "download-manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main(source=None):
    parser = argparse.ArgumentParser(description=__doc__)
    if source is None:
        parser.add_argument("source", choices=SOURCES)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--include", help="Glob; default is specified in sources.yaml")
    parser.add_argument(
        "--max-files", type=int, help="Explicit subset limit; omitted means all matching files"
    )
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    download(
        source or args.source,
        args.out,
        include=args.include,
        max_files=args.max_files,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()

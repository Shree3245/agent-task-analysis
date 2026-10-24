"""Shared Bai archive reader: final trajectories plus run-specific SWE-bench resolutions.

Raw archive members are parsed in memory, never extracted. Instance and run names are
used only to join outcomes; tasks keep a hashed task_group and a hashed run_id.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
import json
from pathlib import Path
import tarfile

from moira.adapters import adapter
from moira.privacy import run_digest

MAX_RECORD = 128 * 1024 * 1024
RESOLUTION_FIELDS = {"instance_id", "metadata.max_iterations", "report.resolved_ids",
                     "report.unresolved_ids", "report.empty_patch_ids",
                     "report.instance.resolved"}


@dataclass
class Archive:
    tasks: dict = field(default_factory=dict)
    runs: dict = field(default_factory=dict)
    rows: int = 0
    skipped: int = 0
    reports: int = 0
    conflicts: int = 0
    cap_limits: Counter = field(default_factory=Counter)

    def manifest(self):
        return {"benchmark_assignments": self.runs, "resolution_reports": self.reports,
                "resolution_conflicts": self.conflicts,
                "harness_iteration_limits": dict(self.cap_limits)}


def read_archive(path, ctx):
    result = Archive()
    identities = {}
    outcomes = defaultdict(dict)
    conflicts = set()

    def outcome(run, instance, resolved):
        key = (run, instance)
        if key in conflicts:
            return
        value = "success" if resolved else "fail"
        old = outcomes[run].get(instance)
        if old and old != value:
            outcomes[run][instance] = "unknown"
            conflicts.add(key)
        else:
            outcomes[run][instance] = value

    with tarfile.open(path, "r|gz") as archive:
        for member in archive:
            if not member.isfile():
                continue
            parts = Path(member.name).parts
            if parts[-1] == "report.json":
                report = json.load(archive.extractfile(member))
                if "resolved_ids" in report:
                    run = "/".join(parts[:-1])
                    for instance in report.get("resolved_ids", []):
                        outcome(run, instance, True)
                    for key in ("unresolved_ids", "empty_patch_ids"):
                        for instance in report.get(key, []):
                            outcome(run, instance, False)
                    result.reports += 1
                elif "eval_outputs" in parts:
                    run = "/".join(parts[:parts.index("eval_outputs")])
                    for instance, detail in report.items():
                        if isinstance(detail, dict) and isinstance(detail.get("resolved"), bool):
                            outcome(run, instance, detail["resolved"])
                continue
            # Full archives also contain one summary row per task with aligned per-call
            # token/cost arrays. Reading these avoids duplicate history and duplicate billing.
            if parts[-1] != "output.jsonl":
                result.skipped += 1
                continue
            if len(parts) < 2:
                raise ValueError("Unrecognized Bai archive layout")
            run = "/".join(parts[:-1])
            with archive.extractfile(member) as stream:
                while line := stream.readline(MAX_RECORD + 1):
                    if len(line) > MAX_RECORD:
                        raise ValueError("Oversized archive record")
                    root = json.loads(line)
                    instance = str(root["instance_id"])
                    ctx.options["task_id"] = parts[-2] + ":" + instance
                    limit = (root.get("metadata") or {}).get("max_iterations")
                    if isinstance(limit, int):
                        result.cap_limits[limit] += 1
                    for task in adapter("openhands")(root, ctx, str(result.rows)):
                        task.finalize()
                        old = result.tasks.get(task.task_id)
                        if old:
                            # Some archives repeat summary rows in different output files.
                            if [c.row() for c in old.calls] != [c.row() for c in task.calls]:
                                raise ValueError("Conflicting task summaries; do not double count")
                            continue
                        result.tasks[task.task_id] = task
                        identities[task.task_id] = (run, instance)
                        # Hashed run identity, used only for leave-one-run-out.
                        result.runs[task.task_id] = {"run_id": run_digest(run)}
                    result.rows += 1
                    if result.rows % 500 == 0:
                        print(f"{path.name}: parsed {result.rows} final trajectories", flush=True)
    for task_id, task in result.tasks.items():
        run, instance = identities[task_id]
        # Only evaluation results determine benchmark resolution, not agent 'finish'.
        task.outcome = outcomes[run].get(instance, "unknown")
    result.conflicts = len(conflicts)
    return result

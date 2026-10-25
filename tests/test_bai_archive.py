"""The shared Bai reader joins run-specific resolutions and never keeps raw names."""

import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile

from agent_task_analysis.adapters.base import Context
from agent_task_analysis.privacy import group_digest, task_digest

BENCHMARKS = Path(__file__).resolve().parents[1] / "benchmarks"
sys.path.insert(0, str(BENCHMARKS))
spec = importlib.util.spec_from_file_location("bai", BENCHMARKS / "bai.py")
bai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bai)


def record(instance):
    usage = {"model": "claude-3-7-sonnet-20250219", "prompt_tokens": 1000,
             "completion_tokens": 100, "cache_read_input_tokens": 0,
             "cache_creation_input_tokens": 0, "response_id": "r1"}
    return {"instance_id": instance,
            "metadata": {"llm_config": {"model": "litellm_proxy/claude-3-7-sonnet-20250219"},
                         "max_iterations": 100},
            "metrics": {"token_usages": [usage],
                        "costs": [{"cost": 0.0045, "timestamp": 1744200000.0}]},
            "history": [{"action": "run", "args": {"command": "ls"}, "timestamp": "2025-04-09T12:00:00",
                         "tool_call_metadata": {"model_response": {"id": "r1"}}}]}


def archive(tmp_path):
    members = {
        "model/run-1/output.jsonl": "\n".join(json.dumps(record(i)) for i in ("repo__a-1", "repo__b-2")),
        "model/run-1/report.json": json.dumps({"resolved_ids": ["repo__a-1"], "unresolved_ids": ["repo__b-2"]}),
        "model/run-2/output.jsonl": "\n".join(json.dumps(record(i)) for i in ("repo__a-1", "repo__b-2")),
        # Per-instance layout; repo__b-2 has no result in run 2 and stays unknown.
        "model/run-2/eval_outputs/repo__a-1/report.json": json.dumps({"repo__a-1": {"resolved": False}}),
        "model/run-2/other.txt": "ignored",
    }
    path = tmp_path / "model_4runs.tar.gz"
    with tarfile.open(path, "w:gz") as tar:
        for name, text in members.items():
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return path


def test_resolutions_join_within_each_run_and_ids_are_hashed(tmp_path):
    result = bai.read_archive(archive(tmp_path), Context("openhands", namespace="model_4runs"))
    by_name = {}
    for run in ("run-1", "run-2"):
        for instance in ("repo__a-1", "repo__b-2"):
            task_id = task_digest(f"openhands:model_4runs:{run}:{instance}")
            by_name[(run, instance)] = result.tasks[task_id]
    assert {k: t.outcome for k, t in by_name.items()} == {
        ("run-1", "repo__a-1"): "success", ("run-1", "repo__b-2"): "fail",
        ("run-2", "repo__a-1"): "fail", ("run-2", "repo__b-2"): "unknown"}
    assert by_name[("run-1", "repo__a-1")].task_group == group_digest("repo__a-1")
    assert by_name[("run-2", "repo__a-1")].task_group == group_digest("repo__a-1")
    assert result.reports == 1 and result.skipped == 1 and result.cap_limits == {100: 4}
    assert len({r["run_id"] for r in result.runs.values()}) == 2
    assert "repo__" not in json.dumps([t.row() for t in result.tasks.values()] + [result.manifest()])

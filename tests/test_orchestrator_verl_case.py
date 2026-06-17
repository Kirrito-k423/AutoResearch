"""Tests for `autoresearch run verl-case` orchestration."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.orchestrator.verl_case import run_verl_case_orchestration


case_config = importlib.import_module("workspace-adapter.verl.case_config")
case_runner = importlib.import_module("workspace-adapter.verl.case_runner")


def _config_file(
    tmp_path: Path,
    *,
    dependency_path: Path | None = None,
    server_workdir: str = "/root",
) -> Path:
    dep_yaml = ""
    if dependency_path is not None:
        dep_yaml = f"""
  dependency_repo_paths:
    verl: {dependency_path}
"""
    path = tmp_path / "config.yaml"
    path.write_text(
        f"""
version: 1
servers:
  - name: A2-AK-225
    host: 192.168.9.225
    user: root
    conda_env: verl-env
    workdir: {server_workdir}
verl_case:
  cache_root: {tmp_path / "cache"}
  output_tokens: [2048, 4096]
  inference_modes: [sync, async]
{dep_yaml}
""",
        encoding="utf-8",
    )
    return path


def _rows(run_config, *, failed_key: str | None = None):
    rows = []
    for matrix_row in run_config.matrix:
        failed = matrix_row.key == failed_key
        rows.append(
            case_config.VerlCaseResultRow(
                run_id=run_config.run_id,
                input_tokens=matrix_row.input_tokens,
                output_tokens=matrix_row.output_tokens,
                inference_mode=matrix_row.inference_mode,
                ignore_eos=matrix_row.ignore_eos,
                status="failed" if failed else "passed",
                elapsed_seconds=1.0,
                tokens_per_second=2.0,
                latency_ms=500.0,
                sample_count=2,
                accuracy=0.5,
                consistency=1.0,
                error="oom" if failed else None,
            )
        )
    return rows


def _remote_result(run_config, *, failed_key: str | None = None):
    rows = _rows(run_config, failed_key=failed_key)
    ok = all(row.status == "passed" for row in rows)
    return case_runner.VerlCaseRunResult(
        ok=ok,
        run_id=run_config.run_id,
        rows=rows,
        commands=["docker pull image", "docker run row"],
        remote_matrix_path="/home/t00906153/autoresearch/runs/run123/matrix-results.jsonl",
        remote_log_path="/home/t00906153/autoresearch/runs/run123/verl-case.log",
        error=None if ok else "one or more matrix rows failed",
    )


def _fake_provenance(path, **kwargs):
    return case_config.RepoProvenance(
        repo=Path(path).name,
        path=str(path),
        upstream_url=kwargs.get("upstream_url"),
        branch="codex/test",
        commit_sha="abc123",
        dirty=False,
        commit_push_attempted=bool(kwargs.get("allow_commit_push")),
    )


def _fake_report(*, run_id, open_report=False, runs_root=None):
    report = Path(runs_root) / run_id / "report.html"
    report.write_text("<html></html>", encoding="utf-8")
    return 0, {"ok": True, "run_id": run_id, "report": str(report), "opened": False, "warnings": []}


def test_verl_case_readiness_failure_skips_remote_runner(tmp_path):
    config = _config_file(tmp_path)

    with patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, {"ok": False, "error": "hw failed"})), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case") as remote:
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=tmp_path / "runs",
        )

    assert exit_code == 1
    assert payload["failed_step"] == "readiness"
    assert payload["manifest"] is None
    remote.assert_not_called()


def test_verl_case_orchestration_success_creates_local_artifacts(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def remote(spec, run_config, **kwargs):
        assert spec.name == "A2-AK-225"
        assert spec.workdir == "/home/t00906153"
        assert kwargs["proxy_url"] == "http://127.0.0.1:17892"
        assert kwargs["remote_output_path"] == "/home/t00906153/autoresearch/runs/run123"
        return _remote_result(run_config)

    with patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=remote), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["command"] == "verl-case"
    assert payload["run_id"] == "run123"
    assert Path(payload["manifest"]).exists()
    assert Path(payload["config_snapshot"]).exists()
    assert Path(payload["provenance"]).exists()
    assert Path(payload["matrix_results"]).exists()
    assert Path(payload["log_path"]).exists()
    assert Path(payload["report"]).exists()
    assert Path(runs_root / "run123" / "wandb" / "files" / "wandb-summary.json").exists()
    matrix_lines = Path(payload["matrix_results"]).read_text(encoding="utf-8").splitlines()
    assert len(matrix_lines) == 4
    manifest = json.loads(Path(payload["manifest"]).read_text(encoding="utf-8"))
    assert manifest["formal_case"]["matrix_results"] == payload["matrix_results"]
    assert manifest["config_snapshot"] == payload["config_snapshot"]
    assert manifest["provenance"][0]["commit_sha"] == "abc123"
    assert manifest["prom_pushed"] is True
    assert manifest["wandb_path"] == str(wandb_dir)


def test_verl_case_matrix_failure_sets_failed_step_matrix(tmp_path):
    config = _config_file(tmp_path)
    wandb_dir = tmp_path / "runs" / "run123" / "wandb"

    def remote(_spec, run_config, **_kwargs):
        return _remote_result(run_config, failed_key="async-1024-4096")

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=remote), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=tmp_path / "runs",
        )

    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["failed_step"] == "matrix"
    assert Path(payload["matrix_results"]).exists()


def test_verl_case_missing_dependency_repo_is_warning_not_failure(tmp_path):
    config = _config_file(tmp_path, dependency_path=tmp_path / "missing-verl")
    wandb_dir = tmp_path / "runs" / "run123" / "wandb"

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance) as capture, \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=lambda _spec, run_config, **_kwargs: _remote_result(run_config)), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            config=str(config),
            run_id="run123",
            runs_root=tmp_path / "runs",
            allow_git_push=True,
        )

    assert exit_code == 0
    assert any("dependency repo path missing: verl" in item for item in payload["warnings"])
    assert capture.call_args_list[0].kwargs["allow_commit_push"] is True


def test_verl_case_cli_outputs_single_json_object():
    runner = CliRunner()
    payload = {"ok": True, "command": "verl-case", "run_id": "run123"}

    with patch("autoresearch.orchestrator.verl_case.run_verl_case_orchestration", return_value=(0, payload)) as mock:
        result = runner.invoke(
            main,
            [
                "run",
                "verl-case",
                "--server",
                "A2-AK-225",
                "--config",
                "config/config.yaml",
                "--timeout",
                "12",
                "--skip-readiness",
            ],
        )

    assert result.exit_code == 0
    assert json.loads(result.output) == payload
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
    assert mock.call_args.kwargs["timeout"] == 12.0
    assert mock.call_args.kwargs["skip_readiness"] is True


def test_verl_case_docker_stack_override_allows_readiness_to_continue(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    remote_called = False

    readiness_payload = {
        "ok": False,
        "command": "check",
        "server": "A2-AK-225",
        "config": str(config),
        "failed_step": "stack",
        "summary": {"total": 8, "passed": 4, "warned": 0, "failed": 1, "skipped": 2, "failed_step": "stack"},
        "steps": [
            {"id": "config", "label": "customer-config", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "services", "label": "local-services-health", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "hw", "label": "server-hardware-probe", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "net", "label": "network-check", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "reach", "label": "service-reachability", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {
                "id": "stack",
                "label": "train-stack-health",
                "ok": False,
                "status": "fail",
                "exit_code": 1,
                "diagnosis": "bash: line 1: python: command not found",
                "payload": {"ok": False, "severity": "fail", "error": "bash: line 1: python: command not found"},
            },
            {"id": "collect", "label": "data-collection", "ok": True, "status": "skipped", "exit_code": None, "diagnosis": "x", "payload": {"ok": None, "skipped": True}},
            {"id": "report", "label": "experiment-report", "ok": True, "status": "skipped", "exit_code": None, "diagnosis": "x", "payload": {"ok": None, "skipped": True}},
        ],
    }

    def remote(_spec, run_config, **_kwargs):
        nonlocal remote_called
        remote_called = True
        return _remote_result(run_config)

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, readiness_payload)), \
         patch("autoresearch.orchestrator.verl_case._docker_formal_stack_ready", return_value=(True, "docker ok")), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=remote), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    assert remote_called is True
    assert any("stack override" in item for item in payload["warnings"])

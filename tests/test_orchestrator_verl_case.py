"""Tests for `autoresearch run verl-case` orchestration."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from workspace_core.config import ServerSpec

from autoresearch.cli import main
from autoresearch.orchestrator.verl_case import run_verl_case_orchestration


case_config = importlib.import_module("workspace-adapter.verl.case_config")
case_runner = importlib.import_module("workspace-adapter.verl.case_runner")
data_prep = importlib.import_module("workspace-adapter.verl.data_prep")


@pytest.fixture(autouse=True)
def _mock_remote_tree_fetch(monkeypatch):
    def fake_collect_tree(_spec, _remote_dir, local_dir, **_kwargs):
        path = Path(local_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("autoresearch.orchestrator.verl_case.collect_tree", fake_collect_tree)


def _config_file(
    tmp_path: Path,
    *,
    dependency_path: Path | None = None,
    server_workdir: str = "/root",
    extra_servers: str = "",
    extra_verl_case: str = "",
    artifact_root: Path | None = None,
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
{extra_servers}
verl_case:
  cache_root: {tmp_path / "cache"}
  artifact_root: {artifact_root or (tmp_path / "data-runs")}
  output_tokens: [2048, 4096]
  inference_modes: [sync, async]
{dep_yaml}
{extra_verl_case}
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
                case_id=matrix_row.key,
                input_tokens=matrix_row.input_tokens,
                output_tokens=matrix_row.output_tokens,
                inference_mode=matrix_row.inference_mode,
                ignore_eos=matrix_row.ignore_eos,
                status="failed" if failed else "passed",
                elapsed_seconds=1.0,
                tokens_per_second=2.0,
                latency_ms=500.0,
                sample_count=2,
                completed_training_steps=2 if failed else 3,
                target_training_steps=run_config.config.training_steps,
                device_count=getattr(matrix_row, "device_count", None),
                visible_devices=getattr(matrix_row, "visible_devices", None),
                train_batch_size=getattr(matrix_row, "train_batch_size", None),
                ppo_mini_batch_size=getattr(matrix_row, "ppo_mini_batch_size", None),
                ppo_micro_batch_size_per_gpu=getattr(matrix_row, "ppo_micro_batch_size_per_gpu", None),
                failure_class="oom" if failed else None,
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


def _fake_model_cache(tmp_path: Path):
    model_dir = tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B"
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "config.json").write_text("{}", encoding="utf-8")
    (model_dir / "model.safetensors.index.json").write_text(
        json.dumps({"weight_map": {"model.embed_tokens.weight": "model.safetensors-00001-of-00001.safetensors"}}),
        encoding="utf-8",
    )
    (model_dir / "model.safetensors-00001-of-00001.safetensors").write_bytes(b"stub")
    model_sync = importlib.import_module("workspace-adapter.verl.model_sync")
    return model_sync.PreparedModelCache(
        model_id="Qwen/Qwen3.5-2B",
        cache_root=tmp_path / "cache",
        model_cache=model_dir,
        ready=True,
        downloaded=False,
    )


def _fake_prepared_dataset(tmp_path: Path, *, with_parquet: bool = False):
    dataset_cache = tmp_path / "cache" / "datasets" / "hiyouga__geometry3k"
    dataset_cache.mkdir(parents=True, exist_ok=True)
    train_parquet = dataset_cache / "train.parquet"
    test_parquet = dataset_cache / "test.parquet"
    if with_parquet:
        train_parquet.write_bytes(b"train")
        test_parquet.write_bytes(b"test")
    return data_prep.PreparedGeometry3K(
        dataset_id="hiyouga/geometry3k",
        cache_root=tmp_path / "cache",
        model_cache=tmp_path / "cache" / "models" / "Qwen__Qwen3.5-2B",
        dataset_cache=dataset_cache,
        image_dir=dataset_cache / "images",
        jsonl_path=dataset_cache / "geometry3k-verl.jsonl",
        sample_count=0,
        ready=with_parquet,
        train_parquet=train_parquet if with_parquet else None,
        test_parquet=test_parquet if with_parquet else None,
    )


def test_verl_case_readiness_failure_skips_remote_runner(tmp_path):
    config = _config_file(tmp_path)

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, {"ok": False, "error": "hw failed"})), \
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


def test_verl_case_skip_readiness_skips_formal_host_qualification(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host") as qualify, \
         patch("autoresearch.orchestrator.verl_case.run_check_all") as readiness, \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=lambda _spec, run_config, **_kwargs: _remote_result(run_config)), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
            skip_readiness=True,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    qualify.assert_not_called()
    readiness.assert_not_called()
    assert any("host qualification skipped" in warning for warning in payload["warnings"])


def test_verl_case_orchestration_success_creates_local_artifacts(tmp_path, monkeypatch):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    ensured = []
    run_configs = []

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def remote(spec, run_config, **kwargs):
        run_configs.append(run_config)
        assert spec.name == "A2-AK-225"
        assert spec.workdir == "/home/t00906153"
        assert kwargs["proxy_url"] == "http://127.0.0.1:17892"
        assert kwargs["remote_output_path"] == "/home/t00906153/autoresearch/runs/run123"
        assert run_config.config.trainer_val_only is False
        assert run_config.extra["case_matrix_kind"] == "training_tuning"
        if len(run_configs) == 1:
            assert run_config.matrix[0].case_id.startswith("train-1npu-bs1-")
            assert run_config.matrix[0].device_count == 1
            assert run_config.matrix[0].visible_devices == [0]
            assert run_config.matrix[0].train_batch_size == 1
        else:
            assert run_config.extra["training_tuning_stage"] == "single_node_promotion"
            assert run_config.matrix[0].case_id.startswith("train-8npu-bs")
            assert run_config.matrix[0].device_count == 8
            assert run_config.matrix[0].visible_devices == list(range(8))
        return _remote_result(run_config)

    def collect_with_stage_timing(_spec, _remote_dir, local_dir, **_kwargs):
        row_dir = Path(local_dir) / "train-1npu-bs1-mini1-micro1-1024-2048"
        row_dir.mkdir(parents=True, exist_ok=True)
        (row_dir / "run123-train-1npu-bs1-mini1-micro1-1024-2048.log").write_text(
            "global_step: 1 timing_raw: {'rollout_generate_seconds': 1.5, 'actor_log_prob_ms': 250}\n",
            encoding="utf-8",
        )
        return Path(local_dir)

    monkeypatch.setattr("autoresearch.orchestrator.verl_case.collect_tree", collect_with_stage_timing)
    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.ensure_proxy_tunnel", side_effect=lambda *args, **kwargs: ensured.append((args, kwargs)) or {"remote_proxy_url": "http://127.0.0.1:17892"}), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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
    assert Path(runs_root / "run123" / "1-wandb" / "files" / "wandb-summary.json").exists()
    matrix_lines = Path(payload["matrix_results"]).read_text(encoding="utf-8").splitlines()
    assert len(matrix_lines) == 5
    assert any("train-8npu-bs" in line for line in matrix_lines)
    manifest = json.loads(Path(payload["manifest"]).read_text(encoding="utf-8"))
    assert manifest["formal_case"]["matrix_results"] == payload["matrix_results"]
    assert manifest["config_snapshot"] == payload["config_snapshot"]
    assert manifest["provenance"][0]["commit_sha"] == "abc123"
    assert manifest["prom_pushed"] is True
    prom_evidence = json.loads((runs_root / "run123" / "2-prometheus" / "formal-case-prometheus.json").read_text(encoding="utf-8"))
    assert prom_evidence["metrics_pushed"] == ["autoresearch_npu_count"]
    assert "autoresearch_npu_hbm_used_mib" in prom_evidence["missing_resource_metrics"]
    assert manifest["artifact_layout"]["sections"]["report"] == "0-report"
    assert manifest["wandb_path"] == str(runs_root / "run123" / "1-wandb")
    assert manifest["formal_case"]["rows_dir"] == str(runs_root / "run123" / "6-rows" / "cases")
    assert manifest["formal_case"]["stage_timings"] == str(runs_root / "run123" / "6-rows" / "stage-timings.jsonl")
    stage_lines = (runs_root / "run123" / "6-rows" / "stage-timings.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(stage_lines) == 2
    assert json.loads(stage_lines[0])["stage"] == "rollout"
    assert (runs_root / "run123" / "6-rows" / "cases" / "train-1npu-bs1-mini1-micro1-1024-2048" / "stage-timings.jsonl").exists()
    assert manifest["formal_case"]["rebuild_environment_script"] == str(runs_root / "run123" / "restore" / "rebuild-environment.sh")
    assert Path(runs_root / "run123" / "README.md").exists()
    assert Path(runs_root / "run123" / "RUN.md").exists()
    assert Path(runs_root / "run123" / "restore" / "rebuild-environment.sh").exists()
    assert ensured
    assert ensured[0][0][0] == "A2-AK-225"
    assert ensured[0][1]["remote_proxy_port"] == 17892


def test_verl_case_orchestration_saves_telemetry_prometheus_evidence(tmp_path, monkeypatch):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    telemetry_calls = []

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def collect_with_telemetry(_spec, _remote_dir, local_dir, **_kwargs):
        row_dir = Path(local_dir) / "sync-1024-2048"
        row_dir.mkdir(parents=True, exist_ok=True)
        (row_dir / "npu-telemetry.jsonl").write_text(
            json.dumps(
                {
                    "run_id": "run123",
                    "case_id": "sync-1024-2048",
                    "server": "A2-AK-225",
                    "device_id": 0,
                    "source": "npu-smi-watch",
                    "hbm_used_mib": 1234,
                    "hbm_total_mib": 65536,
                    "ai_core_utilization_percent": 71,
                    "npu_utilization_percent": 44,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return Path(local_dir)

    def push_telemetry(_spec, run_id, samples, **kwargs):
        telemetry_calls.append((run_id, list(samples), kwargs.get("exposition")))
        return True

    monkeypatch.setattr("autoresearch.orchestrator.verl_case.collect_tree", collect_with_telemetry)
    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=lambda _spec, run_config, **_kwargs: _remote_result(run_config)), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.push_telemetry_metrics", side_effect=push_telemetry), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    prom_evidence = json.loads((runs_root / "run123" / "2-prometheus" / "formal-case-prometheus.json").read_text(encoding="utf-8"))
    assert prom_evidence["telemetry_samples"] == 1
    assert prom_evidence["missing_resource_metrics"] == []
    assert "autoresearch_npu_hbm_used_mib" in prom_evidence["metrics_pushed"]
    exposition_path = Path(prom_evidence["telemetry_openmetrics_file"])
    assert exposition_path.exists()
    exposition = exposition_path.read_text(encoding="utf-8")
    assert 'case_id="sync-1024-2048"' in exposition
    assert telemetry_calls
    assert telemetry_calls[0][0] == "run123"
    assert telemetry_calls[0][1][0]["source"] == "npu-smi-watch"


def test_verl_case_orchestration_rebuilds_telemetry_from_host_raw_log(tmp_path, monkeypatch):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    telemetry_calls = []

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def collect_with_host_raw(_spec, _remote_dir, local_dir, **_kwargs):
        row_dir = Path(local_dir) / "train-1npu-bs1-mini1-micro1-1024-2048"
        row_dir.mkdir(parents=True, exist_ok=True)
        (row_dir / "host-npu-smi-watch.raw.log").write_text(
            """
2026-06-22 21:20:01
| NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
| Chip                      | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
| 0     910B2               | OK            | 108.8       39                0    / 0             |
| 0                         | 0000:C1:00.0  | 7           0    / 0          49290/ 65536         |
""",
            encoding="utf-8",
        )
        return Path(local_dir)

    def push_telemetry(_spec, run_id, samples, **kwargs):
        telemetry_calls.append((run_id, list(samples), kwargs.get("exposition")))
        return True

    monkeypatch.setattr("autoresearch.orchestrator.verl_case.collect_tree", collect_with_host_raw)
    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=lambda _spec, run_config, **_kwargs: _remote_result(run_config)), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.push_telemetry_metrics", side_effect=push_telemetry), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["ok"] is True
    normalized = (
        runs_root / "run123" / "6-rows" / "cases" / "train-1npu-bs1-mini1-micro1-1024-2048" / "host-npu-telemetry.jsonl"
    )
    assert normalized.exists()
    prom_evidence = json.loads((runs_root / "run123" / "2-prometheus" / "formal-case-prometheus.json").read_text(encoding="utf-8"))
    assert prom_evidence["telemetry_samples"] == 1
    assert prom_evidence["missing_resource_metrics"] == []
    assert telemetry_calls[0][1][0]["source"] == "host-npu-smi-watch"
    assert telemetry_calls[0][1][0]["hbm_used_mib"] == 49290


def test_verl_case_defaults_to_configured_artifact_root_and_readable_run_id(tmp_path):
    artifact_root = tmp_path / "warehouse-runs"
    config = _config_file(tmp_path, artifact_root=artifact_root)

    def sync_all(_run_id, _spec, **_kwargs):
        wandb_dir = artifact_root / _run_id / "wandb"
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=lambda _spec, run_config, **_kwargs: _remote_result(run_config)), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
        )

    assert exit_code == 0
    assert payload["run_id"].startswith("Qwen35-2B-GRPO-1Kto4K-")
    assert "-train-modes-sync-async-noignoreeos" in payload["run_id"]
    assert Path(payload["manifest"]).is_relative_to(artifact_root)


def test_verl_case_orchestration_stages_cached_geometry3k_parquet(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def remote(spec, run_config, **kwargs):
        assert spec.name == "A2-AK-225"
        assert kwargs["remote_dataset_path"] == "/home/t00906153/autoresearch/dataset"
        return _remote_result(run_config)

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_geometry3k", return_value=_fake_prepared_dataset(tmp_path, with_parquet=True)), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
         patch("autoresearch.orchestrator.verl_case.stage_geometry3k", return_value="/home/t00906153/autoresearch/dataset") as stage_dataset, \
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
    stage_dataset.assert_called_once()


def test_verl_case_matrix_failure_sets_failed_step_matrix(tmp_path):
    config = _config_file(tmp_path)
    wandb_dir = tmp_path / "runs" / "run123" / "wandb"

    def remote(_spec, run_config, **_kwargs):
        result = _remote_result(run_config)
        for row in result.rows:
            row.status = "failed"
            row.failure_class = "oom"
            row.error = "oom"
        result.ok = False
        result.error = "no training tuning case completed"
        return result

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance) as capture, \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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
    assert capture.call_args_list[0].kwargs["branch_prefix"] is None


def test_capture_provenance_skips_local_vllm_for_veomni(tmp_path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    verl_repo = tmp_path / "verl"
    verl_repo.mkdir()
    vllm_repo = tmp_path / "vllm"
    vllm_repo.mkdir()
    veomni_repo = tmp_path / "veomni"
    veomni_repo.mkdir()

    config = case_config.VerlCaseConfig(
        execution_profile="veomni",
        dependency_repo_paths={
            "verl": str(verl_repo),
            "vllm": str(vllm_repo),
            "veomni": str(veomni_repo),
        }
    )

    with patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance) as capture:
        rows, warnings = importlib.import_module("autoresearch.orchestrator.verl_case")._capture_provenance(
            repo_root=repo_root,
            case_config=config,
            allow_git_push=False,
            run_id="run123",
            server_name="A3-AX-180",
        )

    captured_paths = [Path(call.args[0]) for call in capture.call_args_list]

    assert all("vllm" not in item for item in warnings)
    assert repo_root in captured_paths
    assert verl_repo in captured_paths
    assert veomni_repo in captured_paths
    assert vllm_repo not in captured_paths
    assert [row.repo for row in rows] == ["repo", "verl", "veomni"]


def test_capture_provenance_keeps_local_vllm_for_fsdp(tmp_path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    verl_repo = tmp_path / "verl"
    verl_repo.mkdir()
    vllm_repo = tmp_path / "vllm"
    vllm_repo.mkdir()

    config = case_config.VerlCaseConfig(
        execution_profile="fsdp",
        dependency_repo_paths={
            "verl": str(verl_repo),
            "vllm": str(vllm_repo),
        },
    )

    with patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance) as capture:
        rows, warnings = importlib.import_module("autoresearch.orchestrator.verl_case")._capture_provenance(
            repo_root=repo_root,
            case_config=config,
            allow_git_push=False,
            run_id="run123",
            server_name="A2-AK-225",
        )

    captured_paths = [Path(call.args[0]) for call in capture.call_args_list]

    assert warnings == []
    assert repo_root in captured_paths
    assert verl_repo in captured_paths
    assert vllm_repo in captured_paths
    assert [row.repo for row in rows] == ["repo", "verl", "vllm"]


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
                "--artifact-root",
                "/tmp/ar-data",
                "--skip-readiness",
            ],
        )

    assert result.exit_code == 0
    assert json.loads(result.output) == payload
    assert mock.call_args.kwargs["server"] == "A2-AK-225"
    assert mock.call_args.kwargs["timeout"] == 12.0
    assert mock.call_args.kwargs["artifact_root"] == "/tmp/ar-data"
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

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, readiness_payload)), \
         patch("autoresearch.orchestrator.verl_case._docker_formal_stack_ready", return_value=(True, "docker ok")), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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


def test_verl_case_formal_readiness_ignores_archon_and_host_python(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    remote_called = False

    readiness_payload = {
        "ok": False,
        "command": "check",
        "server": "A2-AK-225",
        "config": str(config),
        "failed_step": "services",
        "summary": {"total": 8, "passed": 3, "warned": 0, "failed": 2, "skipped": 2, "failed_step": "services"},
        "steps": [
            {"id": "config", "label": "customer-config", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {
                "id": "services",
                "label": "local-services-health",
                "ok": False,
                "status": "fail",
                "exit_code": 1,
                "diagnosis": "1 service(s) unhealthy",
                "payload": {
                    "ok": False,
                    "services": [
                        {"name": "archon", "healthy": False, "error": "connection refused"},
                        {"name": "wandb", "healthy": True, "error": None},
                        {"name": "prometheus", "healthy": True, "error": None},
                        {"name": "grafana", "healthy": True, "error": None},
                        {"name": "pushgateway", "healthy": True, "error": None},
                    ],
                },
            },
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

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, readiness_payload)), \
         patch("autoresearch.orchestrator.verl_case._docker_formal_stack_ready", return_value=(True, "docker ok")), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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
    assert any("services override" in item for item in payload["warnings"])
    assert any("stack override" in item for item in payload["warnings"])


def test_verl_case_formal_readiness_ignores_remote_huggingface_when_local_stage_works(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    remote_called = False

    readiness_payload = {
        "ok": False,
        "command": "check",
        "server": "A2-AK-225",
        "config": str(config),
        "failed_step": "net",
        "summary": {"total": 8, "passed": 4, "warned": 0, "failed": 1, "skipped": 2, "failed_step": "net"},
        "steps": [
            {"id": "config", "label": "customer-config", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "services", "label": "local-services-health", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "hw", "label": "server-hardware-probe", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {
                "id": "net",
                "label": "network-check",
                "ok": False,
                "status": "fail",
                "exit_code": 1,
                "diagnosis": "A2-AK-225/huggingface failed",
                "payload": {
                    "ok": False,
                    "severity": "fail",
                    "data": {
                        "rows": [
                            {"location": "local", "target_label": "huggingface", "status": "warn"},
                            {"location": "remote", "target_label": "huggingface", "status": "fail"},
                            {"location": "remote", "target_label": "github", "status": "warn"},
                        ]
                    },
                },
            },
            {"id": "reach", "label": "service-reachability", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "stack", "label": "train-stack-health", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
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

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, readiness_payload)), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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
    assert any("net override" in item for item in payload["warnings"])


def test_verl_case_prepare_fails_when_explicit_host_not_qualified(tmp_path):
    config = _config_file(tmp_path)

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(False, "resource busy")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all") as readiness, \
         patch("autoresearch.orchestrator.verl_case.run_verl_case") as remote:
        exit_code, payload = run_verl_case_orchestration(
            server="A2-AK-225",
            config=str(config),
            run_id="run123",
            runs_root=tmp_path / "runs",
        )

    assert exit_code == 1
    assert payload["failed_step"] == "prepare"
    readiness.assert_not_called()
    remote.assert_not_called()


def test_verl_case_formal_readiness_ignores_local_huggingface_when_prepare_is_authoritative(tmp_path):
    config = _config_file(tmp_path)
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"
    remote_called = False

    readiness_payload = {
        "ok": False,
        "command": "check",
        "server": "A2-AK-225",
        "config": str(config),
        "failed_step": "net",
        "summary": {"total": 8, "passed": 4, "warned": 0, "failed": 1, "skipped": 2, "failed_step": "net"},
        "steps": [
            {"id": "config", "label": "customer-config", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "services", "label": "local-services-health", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "hw", "label": "server-hardware-probe", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {
                "id": "net",
                "label": "network-check",
                "ok": False,
                "status": "fail",
                "exit_code": 1,
                "diagnosis": "local/huggingface failed",
                "payload": {
                    "ok": False,
                    "severity": "fail",
                    "data": {
                        "rows": [
                            {"location": "local", "target_label": "huggingface", "status": "fail"},
                            {"location": "remote", "target_label": "huggingface", "status": "warn"},
                            {"location": "remote", "target_label": "github", "status": "warn"},
                        ]
                    },
                },
            },
            {"id": "reach", "label": "service-reachability", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
            {"id": "stack", "label": "train-stack-health", "ok": True, "status": "pass", "exit_code": 0, "diagnosis": None, "payload": {"ok": True}},
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

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", return_value=(True, "ok")), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(1, readiness_payload)), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/runs/run123/model"), \
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
    assert any("net override" in item for item in payload["warnings"])


def test_qualify_formal_case_host_reuses_running_container_after_resource_busy():
    orchestrator = importlib.import_module("autoresearch.orchestrator.verl_case")
    calls = []

    def fake_run_in_env(spec, command, *, conda_env, workdir, timeout):
        calls.append(command)
        if command.startswith("docker --version"):
            return 0, "", ""
        if command.startswith("docker image inspect"):
            return 0, "", ""
        if command.startswith("docker run"):
            return 1, "", "Resource_Busy(EL0005)\nrtGetDevMsg execution failed\n507899"
        if command.startswith("docker ps --filter status=running"):
            return 0, "verl-8.5.2-a2\n", ""
        if "ps -eo args=" in command:
            return 0, "", ""
        if "AR_FORMAL_SMOKE_OK=1" in command:
            return 0, "AR_FORMAL_SMOKE_OK=1\nAR_FORMAL_SMOKE_VALUE=[1.0]\n", ""
        raise AssertionError(command)

    with patch("autoresearch.orchestrator.verl_case.run_in_env", side_effect=fake_run_in_env):
        ok, detail = orchestrator._qualify_formal_case_host(
            ServerSpec(name="A2-AK-225", host="192.168.9.225", user="root", workdir="/home/t00906153"),
            docker_image="quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5",
            config_path="/tmp/config.yaml",
            local_proxy_url=None,
            remote_proxy_port=17892,
        )

    assert ok is True
    assert "reused running container verl-8.5.2-a2" in detail
    assert any(command.startswith("docker exec -i verl-8.5.2-a2") for command in calls)


def test_verl_case_auto_selects_first_qualified_host(tmp_path):
    config = _config_file(
        tmp_path,
        extra_servers="""
  - name: A3-AX-180
    host: 192.168.13.180
    user: root
    conda_env: verl-env
    workdir: /home/t00906153
""",
    )
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"

    def qualify(spec, **_kwargs):
        if spec.name == "A2-AK-225":
            return False, "resource busy"
        return True, "exact image NPU smoke passed"

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    def remote(spec, run_config, **_kwargs):
        assert spec.name == "A3-AX-180"
        assert run_config.server == "A3-AX-180"
        return _remote_result(run_config)

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", side_effect=qualify), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})) as readiness, \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=remote), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["server"] == "A3-AX-180"
    assert any("auto-selected host: A3-AX-180" in item for item in payload["warnings"])
    assert readiness.call_args.kwargs["server"] == "A3-AX-180"


def test_verl_case_uses_server_docker_image_override(tmp_path):
    a3_image = "quay.io/ascend/verl:verl-8.5.2-a3-ubuntu22.04-py3.11-qwen3-5"
    config = _config_file(
        tmp_path,
        extra_servers="""
  - name: A3-AX-180
    host: 192.168.13.180
    user: root
    conda_env: verl-env
    workdir: /home/t00906153
""",
        extra_verl_case=f"""
  docker_images_by_server:
    A3-AX-180: {a3_image}
""",
    )
    runs_root = tmp_path / "runs"
    wandb_dir = runs_root / "run123" / "wandb"

    def qualify(spec, **kwargs):
        assert spec.name == "A3-AX-180"
        assert kwargs["docker_image"] == a3_image
        return True, "exact image NPU smoke passed"

    def remote(spec, run_config, **_kwargs):
        assert spec.name == "A3-AX-180"
        assert run_config.config.docker_image == a3_image
        return _remote_result(run_config)

    def sync_all(_run_id, _spec, **_kwargs):
        (wandb_dir / "files").mkdir(parents=True, exist_ok=True)
        return wandb_dir

    with patch("autoresearch.orchestrator.verl_case._qualify_formal_case_host", side_effect=qualify), \
         patch("autoresearch.orchestrator.verl_case.run_check_all", return_value=(0, {"ok": True})), \
         patch("autoresearch.orchestrator.verl_case.capture_repo_provenance", side_effect=_fake_provenance), \
         patch("autoresearch.orchestrator.verl_case.prepare_model_cache", return_value=_fake_model_cache(tmp_path)), \
         patch("autoresearch.orchestrator.verl_case.stage_model_cache", return_value="/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B"), \
         patch("autoresearch.orchestrator.verl_case.run_verl_case", side_effect=remote), \
         patch("autoresearch.orchestrator.verl_case.sync_all_runs", side_effect=sync_all), \
         patch("autoresearch.orchestrator.verl_case.push_metrics", return_value=True), \
         patch("autoresearch.orchestrator.verl_case.run_render", side_effect=_fake_report):
        exit_code, payload = run_verl_case_orchestration(
            server="A3-AX-180",
            config=str(config),
            run_id="run123",
            runs_root=runs_root,
        )

    assert exit_code == 0
    assert payload["server"] == "A3-AX-180"

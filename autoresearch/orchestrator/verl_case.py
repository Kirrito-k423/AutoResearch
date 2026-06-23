"""Implementation for `autoresearch run verl-case`."""
from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datalake.manifest import RunManifest
from datalake.manifest import write as write_manifest
from datalake.logs.collector import LogFetchError, collect_tree
from datalake.prometheus import (
    RESOURCE_METRIC_NAMES,
    PushError,
    build_latest_telemetry_exposition,
    build_telemetry_exposition,
    push_metrics,
    push_telemetry_metrics,
)
from datalake.wandb.sync import WandbSyncError, sync_all_runs
from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.progress import emit_progress

from autoresearch.collect.cli import generate_run_id
from autoresearch.net.tunnel import ensure_tunnel as ensure_proxy_tunnel
from autoresearch.report.cli import run_render

from .checks import DEFAULT_CONFIG_PATH, DEFAULT_REMOTE_PROXY_PORT, run_check_all
from .models import StepResult, skipped_step, step_result, summarize_steps


case_config_mod = importlib.import_module("workspace-adapter.verl.case_config")
case_runner_mod = importlib.import_module("workspace-adapter.verl.case_runner")
container_runtime_mod = importlib.import_module("workspace-adapter.verl.container_runtime")
data_prep_mod = importlib.import_module("workspace-adapter.verl.data_prep")
docker_mod = importlib.import_module("workspace-adapter.verl.docker")
model_sync_mod = importlib.import_module("workspace-adapter.verl.model_sync")
provenance_mod = importlib.import_module("workspace-adapter.verl.provenance")
source_sync_mod = importlib.import_module("workspace-adapter.verl.source_sync")
stage_timing_mod = importlib.import_module("workspace-adapter.verl.stage_timing")
telemetry_mod = importlib.import_module("workspace-adapter.verl.telemetry")
conda_utils_mod = importlib.import_module("workspace-adapter.common.conda_utils")

VerlCaseConfig = case_config_mod.VerlCaseConfig
VerlCaseRunConfig = case_config_mod.VerlCaseRunConfig
VerlTrainingTuningRow = case_config_mod.VerlTrainingTuningRow
build_length_matrix = case_config_mod.build_length_matrix
build_training_tuning_matrix = case_config_mod.build_training_tuning_matrix
build_readable_run_id = case_config_mod.build_readable_run_id
now_utc = case_config_mod.now_utc
write_immutable_config = case_config_mod.write_immutable_config
build_docker_pull_command = docker_mod.build_docker_pull_command
build_docker_run_command = docker_mod.build_docker_run_command
run_verl_case = case_runner_mod.run_verl_case
discover_reusable_container = container_runtime_mod.discover_reusable_container
is_resource_busy_error = container_runtime_mod.is_resource_busy_error
prepare_geometry3k = data_prep_mod.prepare_geometry3k
stage_geometry3k = data_prep_mod.stage_geometry3k
prepare_model_cache = model_sync_mod.prepare_model_cache
stage_model_cache = model_sync_mod.stage_model_cache
capture_repo_provenance = provenance_mod.capture_repo_provenance
run_in_env = conda_utils_mod.run_in_env
filter_dependency_repo_paths = source_sync_mod.filter_dependency_repo_paths
parse_npu_smi_watch_output = telemetry_mod.parse_npu_smi_watch_output
extract_stage_timings_from_log = stage_timing_mod.extract_stage_timings_from_log
write_stage_timings_jsonl = stage_timing_mod.write_stage_timings_jsonl
SOURCE_HOST_NPU_SMI_WATCH = telemetry_mod.SOURCE_HOST_NPU_SMI_WATCH
SOURCE_NPU_SMI_WATCH = telemetry_mod.SOURCE_NPU_SMI_WATCH
DEFAULT_NPU_TELEMETRY_INTERVAL_SECONDS = telemetry_mod.DEFAULT_NPU_TELEMETRY_INTERVAL_SECONDS


DEFAULT_PUSHGATEWAY_URL = "http://127.0.0.1:17891"
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_LOCAL_PROXY_URL = "http://127.0.0.1:7890"
FORMAL_ARTIFACT_LAYOUT_VERSION = 1
FORMAL_ARTIFACT_SECTIONS = {
    "report": "0-report",
    "wandb": "1-wandb",
    "prometheus": "2-prometheus",
    "raw_logs": "3-raw-logs",
    "config": "4-config",
    "provenance": "5-provenance",
    "rows": "6-rows",
    "restore": "restore",
}
DEPENDENCY_REPOS = {
    "verl": "https://github.com/verl-project/verl.git",
    "vllm": "https://github.com/vllm-project/vllm.git",
    "transformers": "https://github.com/huggingface/transformers.git",
    "mindspeed": "https://github.com/Ascend/MindSpeed.git",
    "veomni": "https://github.com/ByteDance-Seed/VeOmni.git",
}


def _formal_artifact_layout(run_dir: Path) -> dict[str, Any]:
    paths = {key: run_dir / value for key, value in FORMAL_ARTIFACT_SECTIONS.items()}
    return {
        "version": FORMAL_ARTIFACT_LAYOUT_VERSION,
        "sections": dict(FORMAL_ARTIFACT_SECTIONS),
        "paths": paths,
    }


def run_verl_case_orchestration(
    *,
    server: str | None = None,
    config: str | None = None,
    workdir: str | None = None,
    timeout: float = 3600.0,
    run_id: str | None = None,
    cache_root: str | Path | None = None,
    pushgateway_url: str = DEFAULT_PUSHGATEWAY_URL,
    prometheus_url: str = DEFAULT_PROMETHEUS_URL,
    local_proxy_url: str | None = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    allow_git_push: bool = False,
    skip_readiness: bool = False,
    open_report: bool = False,
    runs_root: Path | None = None,
    artifact_root: str | Path | None = None,
    repo_root: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run the formal Verl case and persist local-first artifacts."""
    cfg_path = config or DEFAULT_CONFIG_PATH
    steps: list[StepResult] = []
    warnings: list[str] = []
    started_at = datetime.now(timezone.utc)

    try:
        cfg = from_path(cfg_path)
        preliminary_config = _adapter_config(
            cfg,
            cache_root=cache_root,
            artifact_root=artifact_root,
            workdir=workdir or cfg.verl_case.remote_workdir,
        )
        root = Path(runs_root).expanduser() if runs_root else Path(preliminary_config.artifact_root).expanduser()
        rid = run_id or _unique_run_id(root, build_readable_run_id(preliminary_config, started_at))
        run_dir = root / rid
        run_dir.mkdir(parents=True, exist_ok=True)
        artifact_layout = _formal_artifact_layout(run_dir)
        for path in artifact_layout["paths"].values():
            Path(path).mkdir(parents=True, exist_ok=True)

        emit_progress("orch.verl_case.start", server=server, run_id=rid, config=cfg_path)
        spec, selection_warnings = _resolve_spec(
            cfg,
            server,
            default_docker_image=cfg.verl_case.docker_image,
            docker_images_by_server=cfg.verl_case.docker_images_by_server,
            config_path=cfg_path,
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
            skip_host_qualification=skip_readiness,
        )
        warnings.extend(selection_warnings)
        server_name = spec.name
        resolved_workdir = workdir or cfg.verl_case.remote_workdir or getattr(spec, "workdir", "")
        spec = spec.model_copy(update={"workdir": resolved_workdir})
        adapter_config = _adapter_config(
            cfg,
            cache_root=cache_root,
            artifact_root=artifact_root,
            workdir=resolved_workdir,
            server_name=server_name,
        )
    except Exception as exc:
        step = step_result(
            step_id="prepare",
            label="formal-case-prepare",
            exit_code=2,
            payload={"ok": False, "error": str(exc)},
        )
        steps.append(step)
        return _finish_payload(
            rid=run_id or generate_run_id(),
            server=server,
            config=cfg_path,
            steps=steps,
            warnings=warnings,
        )

    if skip_readiness:
        steps.append(
            skipped_step(
                "readiness",
                "skills-1-6-readiness",
                "--skip-readiness provided; formal case will run without preflight checks.",
            )
        )
    else:
        emit_progress("orch.verl_case.readiness", server=server_name)
        readiness_exit, readiness_payload = run_check_all(
            server=server_name,
            config=cfg_path,
            stack_libs=("verl",),
            remote_proxy_port=remote_proxy_port,
        )
        readiness_exit, readiness_payload, readiness_override_warnings = _maybe_relax_readiness_for_formal_case(
            readiness_exit=readiness_exit,
            readiness_payload=readiness_payload,
            spec=spec,
        )
        warnings.extend(readiness_override_warnings)
        readiness_step = step_result(
            step_id="readiness",
            label="skills-1-6-readiness",
            exit_code=readiness_exit,
            payload=readiness_payload,
        )
        steps.append(readiness_step)
        if not readiness_step["ok"]:
            steps.extend(
                [
                    skipped_step("prepare", "formal-case-prepare", "readiness failed"),
                    skipped_step("run", "verl-formal-run", "readiness failed"),
                    skipped_step("matrix", "matrix-results", "readiness failed"),
                    skipped_step("collect", "local-artifacts", "readiness failed"),
                    skipped_step("report", "experiment-report", "readiness failed"),
                ]
            )
            return _finish_payload(
                rid=rid,
                server=server_name,
                config=cfg_path,
                steps=steps,
                warnings=warnings,
                failed_step_override="readiness",
            )

    emit_progress("orch.verl_case.prepare", run_id=rid)
    remote_dataset_path = f"{resolved_workdir}/autoresearch/dataset"
    try:
        provenance_rows, provenance_warnings = _capture_provenance(
            repo_root=repo_root or Path.cwd(),
            case_config=adapter_config,
            allow_git_push=allow_git_push,
            run_id=rid,
            server_name=server_name,
        )
        warnings.extend(provenance_warnings)
        prepared = prepare_geometry3k(adapter_config, adapter_config.cache_root)
        prepared_model = prepare_model_cache(
            adapter_config,
            adapter_config.cache_root,
            proxy_url=local_proxy_url,
        )
        remote_model_path = stage_model_cache(
            spec,
            local_model_dir=prepared_model.model_cache,
            remote_model_dir=f"{resolved_workdir}/autoresearch/runs/{rid}/model",
            remote_shared_model_root=f"{resolved_workdir}/autoresearch/model-cache",
        )
        if prepared.train_parquet and prepared.test_parquet:
            remote_dataset_path = stage_geometry3k(
                spec,
                prepared,
                remote_dataset_dir=remote_dataset_path,
            )
        else:
            warnings.append(
                "geometry3k 本地缓存缺少 parquet；formal case 将回退到容器内预处理。"
            )
        container_proxy_url = _container_proxy_url(
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
        )
        run_config = VerlCaseRunConfig(
            run_id=rid,
            created_at=now_utc(),
            server=server_name,
            config=adapter_config,
            matrix=_build_case_matrix(adapter_config),
            provenance=provenance_rows,
            extra={
                "case_matrix_kind": _case_matrix_kind(adapter_config),
                "execution_profile": getattr(adapter_config, "execution_profile", "fsdp"),
                "cache": {
                    **prepared.model_dump(mode="json"),
                    "local_model_cache": prepared_model.model_dump(mode="json"),
                },
                "pushgateway_url": pushgateway_url,
                "prometheus_url": prometheus_url,
                "local_proxy_url": local_proxy_url,
                "remote_proxy_port": remote_proxy_port,
                "container_proxy_url": container_proxy_url,
                "remote_model_path": remote_model_path,
                "remote_dataset_path": remote_dataset_path,
            },
        )
        config_snapshot = write_immutable_config(run_config, artifact_layout["paths"]["config"])
        provenance_path = _write_json(
            artifact_layout["paths"]["provenance"] / "provenance.json",
            [item.model_dump(mode="json") for item in provenance_rows],
        )
        rebuild_env_path = _write_rebuild_environment_script(artifact_layout["paths"]["restore"], provenance_rows)
        _write_artifact_readme(run_dir, run_config, rebuild_env_path)
    except Exception as exc:
        steps.append(
            step_result(
                step_id="prepare",
                label="formal-case-prepare",
                exit_code=2,
                payload={"ok": False, "error": str(exc), "warnings": warnings},
            )
        )
        steps.extend(
            [
                skipped_step("run", "verl-formal-run", "prepare failed"),
                skipped_step("matrix", "matrix-results", "prepare failed"),
                skipped_step("collect", "local-artifacts", "prepare failed"),
                skipped_step("report", "experiment-report", "prepare failed"),
            ]
        )
        return _finish_payload(
            rid=rid,
            server=server_name,
            config=cfg_path,
            steps=steps,
            warnings=warnings,
            failed_step_override="prepare",
        )
    steps.append(
        step_result(
            step_id="prepare",
            label="formal-case-prepare",
            exit_code=0,
            payload={
                "ok": True,
                "config_snapshot": str(config_snapshot),
                "provenance": str(provenance_path),
                "remote_model_path": remote_model_path,
                "warnings": warnings,
            },
        )
    )

    emit_progress("orch.verl_case.run", run_id=rid, matrix_rows=len(run_config.matrix))
    try:
        if local_proxy_url:
            emit_progress(
                "orch.verl_case.proxy.ensure",
                run_id=rid,
                server=server_name,
                remote_proxy_port=remote_proxy_port,
            )
            ensure_proxy_tunnel(
                server_name,
                config_path=cfg_path,
                local_proxy_url=local_proxy_url,
                remote_proxy_port=remote_proxy_port,
            )
        remote_result = _run_verl_case_sequence(
            spec,
            run_config,
            timeout=timeout,
            proxy_url=container_proxy_url,
            remote_model_path=remote_model_path,
            remote_dataset_path=remote_dataset_path,
            remote_output_path=f"{resolved_workdir}/autoresearch/runs/{rid}",
        )
        run_exit = 0
        run_payload = {"ok": True, "remote": remote_result.model_dump(mode="json")}
    except Exception as exc:
        remote_result = None
        run_exit = 2
        run_payload = {"ok": False, "error": str(exc)}
    steps.append(
        step_result(
            step_id="run",
            label="verl-formal-run",
            exit_code=run_exit,
            payload=run_payload,
        )
    )

    matrix_path: Path | None = None
    remote_rows_dir: Path | None = None
    stage_timings_path: Path | None = None
    log_path = _write_log(artifact_layout["paths"]["raw_logs"] / f"{rid}-orchestration.log", run_config, remote_result, warnings)
    if remote_result is not None and remote_result.rows:
        matrix_path = _write_matrix(artifact_layout["paths"]["rows"] / "matrix-results.jsonl", remote_result.rows)
        try:
            remote_rows_dir = collect_tree(
                spec,
                f"{resolved_workdir}/autoresearch/runs/{rid}/rows",
                artifact_layout["paths"]["rows"] / "cases",
            )
        except LogFetchError as exc:
            warnings.append(f"formal row artifact fetch failed: {exc}")
        if remote_rows_dir is not None:
            stage_timings_path = _write_stage_timings_from_rows(
                remote_rows_dir,
                artifact_layout["paths"]["rows"] / "stage-timings.jsonl",
                run_id=rid,
            )
    telemetry_rows = _read_telemetry_rows(artifact_layout["paths"]["rows"], run_id=rid, server=server_name)
    telemetry_exposition = build_telemetry_exposition(telemetry_rows)
    telemetry_latest_exposition = build_latest_telemetry_exposition(telemetry_rows)
    telemetry_exposition_path = None
    telemetry_latest_exposition_path = None
    if telemetry_exposition.strip():
        telemetry_exposition_path = _write_text(
            artifact_layout["paths"]["prometheus"] / "telemetry-openmetrics.prom",
            telemetry_exposition,
        )
    if telemetry_latest_exposition.strip():
        telemetry_latest_exposition_path = _write_text(
            artifact_layout["paths"]["prometheus"] / "telemetry-latest-openmetrics.prom",
            telemetry_latest_exposition,
        )
    matrix_ok = bool(remote_result and remote_result.ok and matrix_path and matrix_path.exists())
    matrix_payload = {
        "ok": matrix_ok,
        "matrix_results": str(matrix_path) if matrix_path else None,
        "rows": len(remote_result.rows) if remote_result is not None else 0,
    }
    if not matrix_ok:
        matrix_payload["error"] = (
            remote_result.error
            if remote_result is not None and remote_result.error
            else "matrix-results.jsonl missing or matrix row failed"
        )
    steps.append(
        step_result(
            step_id="matrix",
            label="matrix-results",
            exit_code=0 if matrix_ok else 1,
            payload=matrix_payload,
        )
    )

    emit_progress("orch.verl_case.collect", run_id=rid)
    wandb_path: Path | None = None
    if remote_result is not None and remote_result.rows:
        try:
            sync_all_runs(
                rid,
                spec,
                workdir=f"{resolved_workdir}/autoresearch/runs/{rid}",
                local_runs_root=root,
                local_wandb_dir=artifact_layout["paths"]["wandb"],
            )
            wandb_path = artifact_layout["paths"]["wandb"]
            _write_formal_wandb_summary(
                wandb_path,
                remote_result,
                npu_count=int(getattr(adapter_config, "n_gpus_per_node", 0) or 0),
            )
        except WandbSyncError as exc:
            warnings.append(f"formal wandb sync failed: {exc}")

    prom_pushed = False
    count_prom_pushed = False
    telemetry_prom_pushed = False
    npu_count = int(getattr(adapter_config, "n_gpus_per_node", 0) or 0)
    if npu_count > 0:
        try:
            count_prom_pushed = push_metrics(
                spec,
                rid,
                npu_count,
                pushgateway_url=pushgateway_url,
            )
        except PushError as exc:
            warnings.append(f"formal prom push failed: {exc}")
    if telemetry_latest_exposition.strip():
        try:
            telemetry_prom_pushed = push_telemetry_metrics(
                spec,
                rid,
                telemetry_rows,
                pushgateway_url=pushgateway_url,
                exposition=telemetry_latest_exposition,
            )
        except PushError as exc:
            warnings.append(f"formal telemetry prom push failed: {exc}")
    prom_pushed = count_prom_pushed or telemetry_prom_pushed

    prom_metrics = _write_json(
        artifact_layout["paths"]["prometheus"] / "formal-case-prometheus.json",
        {
            "run_id": rid,
            "pushgateway_url": pushgateway_url,
            "prometheus_url": prometheus_url,
            "prom_pushed": prom_pushed,
            "count_prom_pushed": count_prom_pushed,
            "telemetry_prom_pushed": telemetry_prom_pushed,
            "npu_count": npu_count,
            "metrics_pushed": (
                (["autoresearch_npu_count"] if count_prom_pushed else [])
                + (list(RESOURCE_METRIC_NAMES) if telemetry_prom_pushed else [])
            ),
            "metrics_available": (
                ["autoresearch_npu_count"]
                + (list(RESOURCE_METRIC_NAMES) if telemetry_rows else [])
            ),
            "missing_resource_metrics": [] if telemetry_rows else list(RESOURCE_METRIC_NAMES),
            "telemetry_samples": len(telemetry_rows),
            "telemetry_sample_interval_seconds": (
                DEFAULT_NPU_TELEMETRY_INTERVAL_SECONDS if telemetry_rows else None
            ),
            "telemetry_openmetrics_file": str(telemetry_exposition_path) if telemetry_exposition_path else None,
            "telemetry_latest_openmetrics_file": (
                str(telemetry_latest_exposition_path)
                if telemetry_latest_exposition_path
                else None
            ),
            "row_count": len(remote_result.rows) if remote_result is not None else 0,
            "note": (
                "已保存 npu-smi watch HBM/Core/NPU telemetry，可从本地 evidence 重建资源曲线。"
                if telemetry_rows
                else "当前 evidence 未找到 npu-smi watch 采样行；资源曲线需要检查 rows/*/npu-telemetry.jsonl。"
            ),
        },
    )
    manifest_path = _write_manifest(
        run_id=rid,
        spec=spec,
        workdir=resolved_workdir,
        run_dir=run_dir,
        root=root,
        started_at=started_at,
        config_snapshot=config_snapshot,
        provenance_rows=provenance_rows,
        matrix_path=matrix_path,
        log_path=log_path,
        prom_metrics=prom_metrics,
        prom_pushed=prom_pushed,
        remote_result=remote_result,
        wandb_path=wandb_path,
        remote_rows_dir=remote_rows_dir,
        rebuild_env_path=rebuild_env_path,
        artifact_layout=artifact_layout,
        stage_timings_path=stage_timings_path,
    )
    collect_payload = {
        "ok": (
            manifest_path.exists()
            and log_path.exists()
            and provenance_path.exists()
            and wandb_path is not None
            and prom_pushed
        ),
        "manifest": str(manifest_path),
        "log_path": str(log_path),
        "prom_metrics_file": str(prom_metrics),
        "wandb_path": str(wandb_path) if wandb_path else None,
        "prom_pushed": prom_pushed,
    }
    if matrix_path is not None:
        collect_payload["matrix_results"] = str(matrix_path)
    steps.append(
        step_result(
            step_id="collect",
            label="local-artifacts",
            exit_code=0 if collect_payload["ok"] else 1,
            payload=collect_payload,
        )
    )

    emit_progress("orch.verl_case.report", run_id=rid)
    try:
        report_exit, report_payload = run_render(
            run_id=rid,
            open_report=open_report,
            runs_root=root,
        )
    except Exception as exc:
        report_exit, report_payload = 1, {"ok": False, "run_id": rid, "error": str(exc)}
    report_file = Path(report_payload["report"]) if report_payload.get("report") else None
    if report_exit == 0 and report_file is None:
        report_exit = 1
        report_payload = {
            **report_payload,
            "ok": False,
            "error": "report path missing",
        }
    elif report_exit == 0 and report_file is not None and not report_file.exists():
        report_exit = 1
        report_payload = {
            **report_payload,
            "ok": False,
            "error": f"report file missing: {report_file}",
        }
    steps.append(
        step_result(
            step_id="report",
            label="experiment-report",
            exit_code=report_exit,
            payload=report_payload,
        )
    )

    return _finish_payload(
        rid=rid,
        server=server_name,
        config=cfg_path,
        steps=steps,
        warnings=warnings,
        manifest=manifest_path,
        config_snapshot=config_snapshot,
        provenance_path=provenance_path,
        matrix_path=matrix_path,
        log_path=log_path,
        report_path=report_file,
    )


def _adapter_config(
    cfg: Any,
    *,
    cache_root: str | Path | None,
    artifact_root: str | Path | None = None,
    workdir: str,
    server_name: str | None = None,
) -> Any:
    payload = cfg.verl_case.model_dump(mode="json")
    payload["remote_workdir"] = workdir
    if server_name is not None:
        payload["docker_image"] = _docker_image_for_server(cfg, server_name)
    if cache_root is not None:
        payload["cache_root"] = str(cache_root)
    if artifact_root is not None:
        payload["artifact_root"] = str(artifact_root)
    return VerlCaseConfig.model_validate(payload)


def _docker_image_for_server(cfg: Any, server_name: str) -> str:
    overrides = getattr(cfg.verl_case, "docker_images_by_server", {}) or {}
    return overrides.get(server_name, cfg.verl_case.docker_image)


def _case_matrix_kind(adapter_config: Any) -> str:
    if getattr(adapter_config, "trainer_val_only", False):
        return "length_validation"
    if getattr(adapter_config, "case_mode", "training") == "validation":
        return "length_validation"
    return "training_tuning"


def _build_case_matrix(adapter_config: Any) -> list[Any]:
    if _case_matrix_kind(adapter_config) == "training_tuning":
        return build_training_tuning_matrix(adapter_config)
    return build_length_matrix(adapter_config)


def _run_verl_case_sequence(
    spec: ServerSpec,
    run_config: Any,
    **kwargs: Any,
) -> Any:
    if _case_matrix_kind(run_config.config) != "training_tuning":
        return run_verl_case(spec, run_config, **kwargs)

    single_card_result = run_verl_case(spec, run_config, **kwargs)
    promotion_rows = _build_single_node_promotion_rows(run_config.config, single_card_result.rows)
    if not promotion_rows:
        return _with_training_tuning_status(single_card_result)

    promotion_config = run_config.model_copy(
        update={
            "matrix": promotion_rows,
            "extra": {
                **(run_config.extra or {}),
                "case_matrix_kind": "training_tuning",
                "training_tuning_stage": "single_node_promotion",
            },
        }
    )
    promotion_result = run_verl_case(spec, promotion_config, **kwargs)
    combined_rows = [*single_card_result.rows, *promotion_result.rows]
    combined_commands = [*single_card_result.commands, *promotion_result.commands]
    ok = _training_tuning_has_pass(combined_rows)
    return case_runner_mod.VerlCaseRunResult(
        ok=ok,
        run_id=run_config.run_id,
        rows=combined_rows,
        commands=combined_commands,
        remote_matrix_path=promotion_result.remote_matrix_path or single_card_result.remote_matrix_path,
        remote_log_path=promotion_result.remote_log_path or single_card_result.remote_log_path,
        error=None if ok else "no training tuning case completed",
    )


def _with_training_tuning_status(result: Any) -> Any:
    ok = _training_tuning_has_pass(result.rows)
    return case_runner_mod.VerlCaseRunResult(
        ok=ok,
        run_id=result.run_id,
        rows=result.rows,
        commands=result.commands,
        remote_matrix_path=result.remote_matrix_path,
        remote_log_path=result.remote_log_path,
        error=None if ok else "no training tuning case completed",
    )


def _training_tuning_has_pass(rows: list[Any]) -> bool:
    return any(getattr(row, "status", None) == "passed" for row in rows)


def _build_single_node_promotion_rows(adapter_config: Any, rows: list[Any]) -> list[Any]:
    devices = [int(device) for device in getattr(adapter_config, "single_node_devices", [])]
    single_card_devices = [int(device) for device in getattr(adapter_config, "single_card_devices", [])]
    if len(devices) <= max(1, len(single_card_devices)):
        return []
    stable_rows = [
        row for row in rows
        if getattr(row, "status", None) == "passed" and getattr(row, "train_batch_size", None)
    ]
    if not stable_rows:
        return []
    best = max(stable_rows, key=lambda row: int(getattr(row, "train_batch_size", 0) or 0))
    per_device_batch_candidates = _unique_positive_ints(
        [
            *list(getattr(adapter_config, "tuning_train_batch_sizes", []) or []),
            int(getattr(best, "train_batch_size", 0) or 0),
            int(getattr(adapter_config, "train_batch_size", 0) or 0),
        ]
    )
    batch_candidates = _unique_positive_ints(
        [per_device_batch_size * len(devices) for per_device_batch_size in per_device_batch_candidates]
    )
    rows_out: list[Any] = []
    for train_batch_size in batch_candidates:
        rows_out.append(
            VerlTrainingTuningRow(
                case_id=(
                    f"train-{len(devices)}npu-bs{train_batch_size}"
                    f"-mini{int(best.ppo_mini_batch_size or 1)}"
                    f"-micro{int(best.ppo_micro_batch_size_per_gpu or 1)}"
                    f"-{int(best.input_tokens)}-{int(best.output_tokens)}"
                ),
                input_tokens=int(best.input_tokens),
                output_tokens=int(best.output_tokens),
                inference_mode=best.inference_mode,
                ignore_eos=bool(best.ignore_eos),
                device_count=len(devices),
                visible_devices=devices,
                train_batch_size=train_batch_size,
                ppo_mini_batch_size=int(best.ppo_mini_batch_size or 1),
                ppo_micro_batch_size_per_gpu=int(best.ppo_micro_batch_size_per_gpu or 1),
                rollout_n=int(getattr(adapter_config, "rollout_n", 1) or 1),
            )
        )
    return rows_out


def _unique_positive_ints(values: list[Any]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []
    for value in values:
        try:
            number = int(value)
        except (TypeError, ValueError):
            continue
        if number <= 0 or number in seen:
            continue
        seen.add(number)
        result.append(number)
    return result


def _resolve_spec(
    cfg: Any,
    server: str | None,
    *,
    default_docker_image: str,
    docker_images_by_server: dict[str, str] | None = None,
    config_path: str,
    local_proxy_url: str | None,
    remote_proxy_port: int,
    skip_host_qualification: bool = False,
) -> tuple[ServerSpec, list[str]]:
    if not cfg.servers:
        raise ConfigError("config.servers 为空，无法选择运行机器")
    if skip_host_qualification:
        if server is None:
            item = cfg.servers[0]
            return item, [f"formal case host qualification skipped; selected first host: {item.name}"]
        for item in cfg.servers:
            if item.name == server:
                return item, [f"formal case host qualification skipped for explicit host: {item.name}"]
        raise ConfigError(f"未找到服务器: {server}")
    if server is None:
        failures: list[str] = []
        for item in cfg.servers:
            docker_image = _docker_image_from_mapping(
                item.name,
                default_docker_image=default_docker_image,
                docker_images_by_server=docker_images_by_server,
            )
            ok, detail = _qualify_formal_case_host(
                item,
                docker_image=docker_image,
                config_path=config_path,
                local_proxy_url=local_proxy_url,
                remote_proxy_port=remote_proxy_port,
            )
            if ok:
                return item, [f"formal case auto-selected host: {item.name} ({detail})"]
            failures.append(f"{item.name}: {detail}")
        raise ConfigError("没有找到可运行 formal case 的宿主机: " + "; ".join(failures))
    for item in cfg.servers:
        if item.name == server:
            docker_image = _docker_image_from_mapping(
                item.name,
                default_docker_image=default_docker_image,
                docker_images_by_server=docker_images_by_server,
            )
            ok, detail = _qualify_formal_case_host(
                item,
                docker_image=docker_image,
                config_path=config_path,
                local_proxy_url=local_proxy_url,
                remote_proxy_port=remote_proxy_port,
            )
            if not ok:
                raise ConfigError(f"formal case 宿主机不可用: {item.name}: {detail}")
            return item, []
    raise ConfigError(f"未找到服务器: {server}")


def _docker_image_from_mapping(
    server_name: str,
    *,
    default_docker_image: str,
    docker_images_by_server: dict[str, str] | None,
) -> str:
    return (docker_images_by_server or {}).get(server_name, default_docker_image)


def _container_proxy_url(
    *,
    local_proxy_url: str | None,
    remote_proxy_port: int,
) -> str | None:
    if not local_proxy_url:
        return None
    return f"http://127.0.0.1:{remote_proxy_port}"


def _maybe_relax_readiness_for_formal_case(
    *,
    readiness_exit: int,
    readiness_payload: dict[str, Any],
    spec: ServerSpec,
) -> tuple[int, dict[str, Any], list[str]]:
    if readiness_exit == 0:
        return readiness_exit, readiness_payload, []

    steps = list(readiness_payload.get("steps") or [])
    warnings: list[str] = []

    services_step = next((step for step in steps if step.get("id") == "services"), None)
    if services_step and services_step.get("status") == "fail":
        service_rows = list((services_step.get("payload") or {}).get("services") or [])
        unhealthy = [row.get("name") for row in service_rows if not row.get("healthy")]
        if unhealthy == ["archon"]:
            services_step["ok"] = True
            services_step["status"] = "warn"
            services_step["exit_code"] = 0
            services_step["diagnosis"] = "Archon 未启动，但 formal case 不依赖 archon。"
            payload = dict(services_step.get("payload") or {})
            payload["ok"] = True
            payload["severity"] = "warn"
            payload["formal_case_optional"] = ["archon"]
            payload["message"] = "本地服务检查通过 (formal case 忽略 archon)"
            services_step["payload"] = payload
            warnings.append(f"readiness services override: ignore local archon for formal case on {spec.name}")

    stack_step = next((step for step in steps if step.get("id") == "stack"), None)
    if stack_step and stack_step.get("status") == "fail":
        detail = str(
            stack_step.get("diagnosis")
            or (stack_step.get("payload") or {}).get("error")
            or ""
        )
        if "python: command not found" in detail:
            docker_ok, docker_detail = _docker_formal_stack_ready(spec)
            if docker_ok:
                stack_step["ok"] = True
                stack_step["status"] = "warn"
                stack_step["exit_code"] = 0
                stack_step["diagnosis"] = f"宿主机 Python 栈缺失，但 Docker formal stack 可用: {docker_detail}"
                payload = dict(stack_step.get("payload") or {})
                payload["ok"] = True
                payload["severity"] = "warn"
                payload["docker_override"] = docker_detail
                payload["message"] = "训练栈检查通过 (formal case docker override)"
                stack_step["payload"] = payload
                warnings.append(f"readiness stack override: {spec.name} host python 缺失，但 Docker/NPU 可用于 formal case")

    net_step = next((step for step in steps if step.get("id") == "net"), None)
    if net_step and net_step.get("status") == "fail":
        rows = list((((net_step.get("payload") or {}).get("data") or {}).get("rows") or []))
        failed_rows = [row for row in rows if _net_probe_row_failed(row)]
        only_huggingface_failed = bool(failed_rows) and all(
            row.get("target_label") == "huggingface"
            for row in failed_rows
        )
        only_remote_hf_failed = bool(failed_rows) and all(
            row.get("location") == "remote" and row.get("target_label") == "huggingface"
            for row in failed_rows
        )
        local_hf_ok = any(
            row.get("location") == "local"
            and row.get("target_label") == "huggingface"
            and not _net_probe_row_failed(row)
            for row in rows
        )
        if only_huggingface_failed:
            net_step["ok"] = True
            net_step["status"] = "warn"
            net_step["exit_code"] = 0
            if only_remote_hf_failed and local_hf_ok:
                net_step["diagnosis"] = "远端 huggingface 不可达，但 formal case 依赖本地模型缓存和 SSH stage，可继续。"
            else:
                net_step["diagnosis"] = "huggingface 可达性失败，但 formal case 以本地缓存准备结果为准，可继续到 prepare 阶段。"
            payload = dict(net_step.get("payload") or {})
            payload["ok"] = True
            payload["severity"] = "warn"
            payload["formal_case_optional"] = ["huggingface"]
            payload["message"] = "网络检查通过 (formal case 以本地缓存准备替代 huggingface 直连)"
            net_step["payload"] = payload
            warnings.append(
                f"readiness net override: ignore huggingface reachability gating for formal case on {spec.name}"
            )

    if not warnings:
        return readiness_exit, readiness_payload, []

    summary = summarize_steps(steps)
    updated_payload = {
        **readiness_payload,
        "ok": summary["failed"] == 0,
        "failed_step": summary["failed_step"],
        "summary": summary,
        "steps": steps,
    }
    return (0 if summary["failed"] == 0 else readiness_exit), updated_payload, warnings


def _net_probe_row_failed(row: dict[str, Any]) -> bool:
    if row.get("ok") is False:
        return True
    if row.get("ok") is True:
        return False
    return str(row.get("status") or "").strip().lower() == "fail"


def _docker_formal_stack_ready(spec: ServerSpec) -> tuple[bool, str]:
    command = (
        "docker --version >/dev/null 2>&1"
        " && ls /dev/davinci0 /dev/davinci7 /dev/davinci_manager /dev/devmm_svm /dev/hisi_hdc >/dev/null 2>&1"
    )
    code, stdout, stderr = run_in_env(
        spec,
        command,
        conda_env="",
        workdir=getattr(spec, "workdir", "") or "/root",
        timeout=15.0,
    )
    if code == 0:
        return True, "docker command and ascend devices detected"
    detail = (stderr or stdout or "").strip()[:200] or f"exit={code}"
    return False, detail


def _qualify_formal_case_host(
    spec: ServerSpec,
    *,
    docker_image: str,
    config_path: str,
    local_proxy_url: str | None,
    remote_proxy_port: int,
) -> tuple[bool, str]:
    docker_ok, docker_detail = _docker_formal_stack_ready(spec)
    if not docker_ok:
        return False, f"docker/ascend precheck failed: {docker_detail}"
    host_workdir = getattr(spec, "workdir", "") or "/root"

    def _runner(target: ServerSpec, command: str, command_timeout: float) -> tuple[int, str, str]:
        return run_in_env(
            target,
            command,
            conda_env="",
            workdir=host_workdir,
            timeout=command_timeout,
        )

    proxy_url = None
    if local_proxy_url:
        ensure_proxy_tunnel(
            spec.name,
            config_path=config_path,
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
        )
        proxy_url = _container_proxy_url(
            local_proxy_url=local_proxy_url,
            remote_proxy_port=remote_proxy_port,
        )

    inspect = f"docker image inspect {json.dumps(docker_image)} >/dev/null 2>&1"
    inspect_code, _inspect_stdout, _inspect_stderr = _runner(spec, inspect, 60.0)
    if inspect_code != 0:
        pull = build_docker_pull_command(docker_image, proxy_url=proxy_url)
        pull_code, pull_stdout, pull_stderr = _runner(spec, pull, 900.0)
        if pull_code != 0:
            detail = (pull_stderr or pull_stdout or "").strip()[:240] or f"exit={pull_code}"
            return False, f"docker pull failed: {detail}"

    smoke = build_docker_run_command(
        image=docker_image,
        run_id=f"host-smoke-{_sanitize_name(spec.name)}",
        model_mount="/tmp",
        dataset_mount="/tmp",
        output_mount="/tmp",
        command=_formal_host_smoke_command(),
        proxy_url=proxy_url,
        device_count=8,
        container_name=f"autoresearch-host-smoke-{_sanitize_name(spec.name)}",
    )
    code, stdout, stderr = _runner(spec, smoke, 240.0)
    output = (stdout or "") + ("\n" + stderr if stderr else "")
    if code == 0 and "AR_FORMAL_SMOKE_OK=1" in output:
        return True, "exact image NPU smoke passed"
    if is_resource_busy_error(output):
        container_name, reusable_detail = discover_reusable_container(
            spec,
            image=docker_image,
            runner=_runner,
            timeout=240.0,
        )
        if container_name:
            return True, reusable_detail
    detail = output.strip().splitlines()[-1] if output.strip() else f"exit={code}"
    return False, f"exact image NPU smoke failed: {detail[:240]}"


def _formal_host_smoke_command() -> str:
    command = (
        "python3 -c "
        "\"import torch, torch_npu; "
        "left = torch.ones((2, 3), device='npu'); "
        "right = torch.zeros((1, 3), device='npu'); "
        "value = torch.cat([left, right], dim=0).sum().cpu().item(); "
        "torch.npu.synchronize(); "
        "print('AR_FORMAL_SMOKE_OK=1'); "
        "print('AR_FORMAL_SMOKE_VALUE=' + repr(value))\""
    )
    return "/bin/bash -lc " + json.dumps(command)


def _sanitize_name(value: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    return safe.strip("-") or "host"


def _capture_provenance(
    *,
    repo_root: Path,
    case_config: Any,
    allow_git_push: bool,
    run_id: str,
    server_name: str,
) -> tuple[list[Any], list[str]]:
    rows: list[Any] = []
    warnings: list[str] = []
    # Keep provenance on the caller's current branch by default. Earlier
    # versions created one branch per experiment run, which made Git history
    # hard to read and left many long-lived provenance branches behind.
    branch_prefix = None
    rows.append(
        capture_repo_provenance(
            repo_root,
            fork_owner=case_config.github_owner,
            allow_commit_push=allow_git_push,
            branch_prefix=branch_prefix,
        )
    )
    configured_paths = filter_dependency_repo_paths(
        dependency_repo_paths=dict(getattr(case_config, "dependency_repo_paths", {}) or {}),
        server=server_name,
        model_id=str(getattr(case_config, "model_id", "")),
        execution_profile=str(getattr(case_config, "execution_profile", "fsdp")),
    )
    for repo, upstream_url in DEPENDENCY_REPOS.items():
        raw_path = configured_paths.get(repo)
        if not raw_path:
            continue
        path = Path(raw_path).expanduser()
        if not path.exists():
            warnings.append(f"dependency repo path missing: {repo}={path}")
            continue
        rows.append(
            capture_repo_provenance(
                path,
                upstream_url=upstream_url,
                fork_owner=case_config.github_owner,
                allow_commit_push=allow_git_push,
                branch_prefix=branch_prefix,
            )
        )
    return rows, warnings


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_matrix(path: Path, rows: list[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(row.model_dump_json() + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")
    return path


def _read_telemetry_rows(rows_dir: Path, *, run_id: str, server: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not rows_dir.exists():
        return rows
    row_dirs_with_jsonl = set()
    for path in sorted(rows_dir.glob("**/*npu-telemetry.jsonl")):
        loaded = _read_telemetry_jsonl(path)
        if loaded:
            rows.extend(loaded)
            row_dirs_with_jsonl.add(path.parent)

    for path in sorted(rows_dir.glob("**/*npu-smi-watch.raw.log")):
        source = SOURCE_HOST_NPU_SMI_WATCH if path.name.startswith("host-") else SOURCE_NPU_SMI_WATCH
        if source == SOURCE_NPU_SMI_WATCH and path.parent in row_dirs_with_jsonl:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        parsed = parse_npu_smi_watch_output(
            text,
            run_id=run_id,
            case_id=path.parent.name,
            server=server,
            source=source,
        )
        if not parsed:
            continue
        normalized_path = (
            path.parent / "host-npu-telemetry.jsonl"
            if source == SOURCE_HOST_NPU_SMI_WATCH
            else path.parent / "npu-telemetry.from-raw.jsonl"
        )
        normalized_rows = [sample.model_dump(mode="json") for sample in parsed]
        normalized_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in normalized_rows),
            encoding="utf-8",
        )
        rows.extend(normalized_rows)
    return rows


def _read_telemetry_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return rows
    for line in lines:
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _write_stage_timings_from_rows(rows_dir: Path, output_path: Path, *, run_id: str) -> Path:
    all_rows: list[Any] = []
    if rows_dir.exists():
        for case_dir in sorted(path for path in rows_dir.iterdir() if path.is_dir()):
            case_rows: list[Any] = []
            for log_path in sorted(case_dir.glob("*.log")):
                try:
                    text = log_path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                case_rows.extend(
                    extract_stage_timings_from_log(
                        text,
                        run_id=run_id,
                        case_id=case_dir.name,
                    )
                )
            case_rows = _dedupe_stage_timings(case_rows)
            if case_rows:
                write_stage_timings_jsonl(case_dir / "stage-timings.jsonl", case_rows)
                all_rows.extend(case_rows)
    return write_stage_timings_jsonl(output_path, _dedupe_stage_timings(all_rows))


def _dedupe_stage_timings(rows: list[Any]) -> list[Any]:
    seen: set[tuple[str, str, int | None, str, str]] = set()
    deduped: list[Any] = []
    for row in rows:
        key = (
            str(getattr(row, "case_id", "")),
            str(getattr(row, "stage", "")),
            getattr(row, "step", None),
            str(getattr(row, "original_key", "")),
            str(getattr(row, "source", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def _write_log(path: Path, run_config: Any, remote_result: Any, warnings: list[str]) -> Path:
    lines = [
        f"run_id={run_config.run_id}",
        f"server={run_config.server}",
        f"matrix_rows={len(run_config.matrix)}",
    ]
    if warnings:
        lines.extend(f"warning={item}" for item in warnings)
    if remote_result is not None:
        lines.append(f"remote_log_path={remote_result.remote_log_path}")
        lines.append(f"remote_matrix_path={remote_result.remote_matrix_path}")
        lines.extend(f"command={command}" for command in remote_result.commands)
        for row in remote_result.rows:
            lines.append(
                "row="
                + json.dumps(
                    {
                        "mode": row.inference_mode,
                        "input_tokens": row.input_tokens,
                        "output_tokens": row.output_tokens,
                        "status": row.status,
                        "error": row.error,
                    },
                    ensure_ascii=False,
                )
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _write_manifest(
    *,
    run_id: str,
    spec: ServerSpec,
    workdir: str,
    run_dir: Path,
    root: Path,
    started_at: datetime,
    config_snapshot: Path,
    provenance_rows: list[Any],
    matrix_path: Path | None,
    log_path: Path,
    prom_metrics: Path,
    prom_pushed: bool,
    remote_result: Any,
    wandb_path: Path | None,
    remote_rows_dir: Path | None = None,
    rebuild_env_path: Path | None = None,
    artifact_layout: dict[str, Any] | None = None,
    stage_timings_path: Path | None = None,
) -> Path:
    artifact_layout_payload = None
    if artifact_layout:
        artifact_layout_payload = {
            "version": artifact_layout.get("version"),
            "sections": artifact_layout.get("sections"),
        }
    formal_case = {
        "kind": "verl-case",
        "matrix_results": str(matrix_path) if matrix_path else None,
        "log_path": str(log_path),
        "rows_dir": str(remote_rows_dir) if remote_rows_dir else str(run_dir / FORMAL_ARTIFACT_SECTIONS["rows"]),
        "remote_matrix_path": remote_result.remote_matrix_path if remote_result is not None else None,
        "remote_log_path": remote_result.remote_log_path if remote_result is not None else None,
        "row_count": len(remote_result.rows) if remote_result is not None else 0,
        "ok": bool(remote_result and remote_result.ok and matrix_path and matrix_path.exists()),
        "wandb_restore_script": str(wandb_path / "rebuild-wandb.sh") if wandb_path else None,
        "rebuild_environment_script": str(rebuild_env_path) if rebuild_env_path else None,
        "stage_timings": str(stage_timings_path) if stage_timings_path else None,
        "artifact_layout": artifact_layout_payload,
    }
    manifest = RunManifest(
        run_id=run_id,
        started_at=started_at,
        finished_at=datetime.now(timezone.utc),
        server=spec.name,
        conda_env=getattr(spec, "conda_env", "") or "",
        lib="verl",
        workdir_remote=workdir,
        workdir_local=run_dir,
        artifact_layout=artifact_layout_payload,
        formal_case=formal_case,
        exit_code=0 if formal_case["ok"] else 1,
        error=None if formal_case["ok"] else "formal case matrix failed",
        config_snapshot=config_snapshot,
        provenance=[row.model_dump(mode="json") for row in provenance_rows],
        wandb_run_id=run_id,
        wandb_path=wandb_path,
        log_files=[log_path],
        prom_pushed=prom_pushed,
        prom_metrics_file=prom_metrics,
    )
    return write_manifest(manifest, root=root)


def _unique_run_id(root: Path, base: str) -> str:
    """Return a readable run id that will not overwrite an existing data bundle."""
    candidate = base
    suffix = 2
    while (Path(root).expanduser() / candidate).exists():
        candidate = f"{base}-r{suffix}"
        suffix += 1
    return candidate


def _write_rebuild_environment_script(run_dir: Path, provenance_rows: list[Any]) -> Path:
    """Write a portable helper that checks out every recorded code commit."""
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        'TARGET_ROOT="${1:-$PWD/rebuilt-code}"',
        'mkdir -p "$TARGET_ROOT"',
        "",
    ]
    for row in provenance_rows:
        payload = row.model_dump(mode="json") if hasattr(row, "model_dump") else dict(row)
        repo = str(payload.get("repo") or "repo")
        commit = payload.get("commit_sha")
        url = payload.get("fork_url") or payload.get("upstream_url")
        if not commit or not url:
            continue
        safe_repo = _sanitize_name(repo)
        lines.extend(
            [
                f'if [ ! -d "$TARGET_ROOT/{safe_repo}/.git" ]; then',
                f"  git clone {json.dumps(str(url))} \"$TARGET_ROOT/{safe_repo}\"",
                "fi",
                f'git -C "$TARGET_ROOT/{safe_repo}" fetch --all --tags',
                f'git -C "$TARGET_ROOT/{safe_repo}" checkout {json.dumps(str(commit))}',
                "",
            ]
        )
    path = run_dir / "rebuild-environment.sh"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o755)
    return path


def _write_artifact_readme(run_dir: Path, run_config: Any, rebuild_env_path: Path) -> Path:
    """Write the human entry point for a copied formal-case data bundle."""
    mode = "验证矩阵" if getattr(run_config.config, "trainer_val_only", True) else "GRPO 训练矩阵"
    text = f"""# AutoResearch Verl Case 数据包

运行 ID: `{run_config.run_id}`
模型: `{run_config.config.model_id}`
数据集: `{run_config.config.dataset_id}`
算法: `GRPO`
模式: `{mode}`

重要入口:

- `manifest.json`: 交付件索引和来源真相
- `0-report/report.html`: 客户阅读入口
- `1-wandb/rebuild-wandb.sh`: 将原始 W&B offline runs 重新导入本地 W&B
- `2-prometheus/`: telemetry JSON/OpenMetrics 与 Prometheus evidence
- `3-raw-logs/`: 编排日志与可审计原始日志入口
- `4-config/`: 不可变配置快照
- `5-provenance/provenance.json`: 代码仓和依赖仓 git commit 锁定信息
- `6-rows/matrix-results.jsonl`: 每个 case 的矩阵/调参结果
- `6-rows/stage-timings.jsonl`: Verl GRPO 各阶段耗时归一化结果
- `6-rows/cases/`: 每个 case 的 Verl 日志、验证输出、NPU telemetry 和 result 文件
- `restore/{Path(rebuild_env_path).name}`: 按记录的 git commit 重建代码环境
"""
    path = run_dir / "RUN.md"
    path.write_text(text, encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# AutoResearch Verl Case 数据包\n\n主入口见 `RUN.md`；客户报告见 `0-report/report.html`。\n",
        encoding="utf-8",
    )
    return path


def _write_formal_wandb_summary(
    wandb_root: Path,
    remote_result: Any,
    *,
    npu_count: int,
) -> Path:
    rows = list(getattr(remote_result, "rows", []) or [])
    passed_rows = [row for row in rows if getattr(row, "status", None) == "passed"]

    def _avg(name: str) -> float | None:
        values = [
            float(value)
            for row in rows
            if (value := getattr(row, name, None)) is not None
        ]
        if not values:
            return None
        return sum(values) / len(values)

    summary = {
        "matrix_rows": len(rows),
        "passed_rows": len(passed_rows),
        "failed_rows": len(rows) - len(passed_rows),
        "sample_count": sum(int(getattr(row, "sample_count", 0) or 0) for row in rows),
        "tokens_per_second": _avg("tokens_per_second"),
        "latency_ms": _avg("latency_ms"),
        "accuracy": _avg("accuracy"),
        "consistency": _avg("consistency"),
        "npu_count": npu_count,
        "_step": len(rows),
    }
    summary_path = wandb_root / "files" / "wandb-summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary_path


def _finish_payload(
    *,
    rid: str,
    server: str | None,
    config: str,
    steps: list[StepResult],
    warnings: list[str],
    failed_step_override: str | None = None,
    manifest: Path | None = None,
    config_snapshot: Path | None = None,
    provenance_path: Path | None = None,
    matrix_path: Path | None = None,
    log_path: Path | None = None,
    report_path: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    summary = summarize_steps(steps)
    ok = summary["failed"] == 0
    failed_step = failed_step_override or summary["failed_step"]
    payload = {
        "ok": ok,
        "command": "verl-case",
        "server": server,
        "config": config,
        "run_id": rid,
        "manifest": str(manifest) if manifest else None,
        "config_snapshot": str(config_snapshot) if config_snapshot else None,
        "provenance": str(provenance_path) if provenance_path else None,
        "matrix_results": str(matrix_path) if matrix_path else None,
        "log_path": str(log_path) if log_path else None,
        "report": str(report_path) if report_path else None,
        "warnings": warnings,
        "failed_step": failed_step,
        "summary": {**summary, "failed_step": failed_step},
        "steps": steps,
    }
    emit_progress(
        "orch.verl_case.result",
        level="info" if ok else "error",
        ok=ok,
        failed_step=failed_step,
    )
    return (0 if ok else 1), payload

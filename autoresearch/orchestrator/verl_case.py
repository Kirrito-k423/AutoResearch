"""Implementation for `autoresearch run verl-case`."""
from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datalake.manifest import RunManifest
from datalake.manifest import write as write_manifest
from datalake.prometheus import PushError, push_metrics
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
data_prep_mod = importlib.import_module("workspace-adapter.verl.data_prep")
model_sync_mod = importlib.import_module("workspace-adapter.verl.model_sync")
provenance_mod = importlib.import_module("workspace-adapter.verl.provenance")
conda_utils_mod = importlib.import_module("workspace-adapter.common.conda_utils")

VerlCaseConfig = case_config_mod.VerlCaseConfig
VerlCaseRunConfig = case_config_mod.VerlCaseRunConfig
build_length_matrix = case_config_mod.build_length_matrix
now_utc = case_config_mod.now_utc
write_immutable_config = case_config_mod.write_immutable_config
run_verl_case = case_runner_mod.run_verl_case
prepare_geometry3k = data_prep_mod.prepare_geometry3k
stage_geometry3k = data_prep_mod.stage_geometry3k
prepare_model_cache = model_sync_mod.prepare_model_cache
stage_model_cache = model_sync_mod.stage_model_cache
capture_repo_provenance = provenance_mod.capture_repo_provenance
run_in_env = conda_utils_mod.run_in_env


DEFAULT_PUSHGATEWAY_URL = "http://127.0.0.1:17891"
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_LOCAL_PROXY_URL = "http://127.0.0.1:7890"
DEPENDENCY_REPOS = {
    "verl": "https://github.com/verl-project/verl.git",
    "vllm": "https://github.com/vllm-project/vllm.git",
    "transformers": "https://github.com/huggingface/transformers.git",
    "mindspeed": "https://github.com/Ascend/MindSpeed.git",
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
    repo_root: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run the formal Verl case and persist local-first artifacts."""
    rid = run_id or generate_run_id()
    cfg_path = config or DEFAULT_CONFIG_PATH
    root = Path(runs_root).expanduser() if runs_root else Path("~/.autoresearch/runs").expanduser()
    run_dir = root / rid
    run_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ("wandb", "prom"):
        (run_dir / subdir).mkdir(parents=True, exist_ok=True)

    emit_progress("orch.verl_case.start", server=server, run_id=rid, config=cfg_path)
    steps: list[StepResult] = []
    warnings: list[str] = []
    started_at = datetime.now(timezone.utc)

    try:
        cfg = from_path(cfg_path)
        spec = _resolve_spec(cfg, server)
        server_name = spec.name
        resolved_workdir = workdir or cfg.verl_case.remote_workdir or getattr(spec, "workdir", "")
        spec = spec.model_copy(update={"workdir": resolved_workdir})
        adapter_config = _adapter_config(cfg, cache_root=cache_root, workdir=resolved_workdir)
    except Exception as exc:
        step = step_result(
            step_id="prepare",
            label="formal-case-prepare",
            exit_code=2,
            payload={"ok": False, "error": str(exc)},
        )
        steps.append(step)
        return _finish_payload(
            rid=rid,
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
            matrix=build_length_matrix(adapter_config),
            provenance=provenance_rows,
            extra={
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
        config_snapshot = write_immutable_config(run_config, run_dir)
        provenance_path = _write_json(
            run_dir / "provenance.json",
            [item.model_dump(mode="json") for item in provenance_rows],
        )
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
        remote_result = run_verl_case(
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
    log_path = _write_log(run_dir / "verl-case.log", run_config, remote_result, warnings)
    if remote_result is not None and remote_result.rows:
        matrix_path = _write_matrix(run_dir / "matrix-results.jsonl", remote_result.rows)
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
            wandb_path = sync_all_runs(
                rid,
                spec,
                workdir=f"{resolved_workdir}/autoresearch/runs/{rid}",
                local_runs_root=root,
            )
            _write_formal_wandb_summary(
                wandb_path,
                remote_result,
                npu_count=int(getattr(adapter_config, "n_gpus_per_node", 0) or 0),
            )
        except WandbSyncError as exc:
            warnings.append(f"formal wandb sync failed: {exc}")

    prom_pushed = False
    npu_count = int(getattr(adapter_config, "n_gpus_per_node", 0) or 0)
    if npu_count > 0:
        try:
            prom_pushed = push_metrics(
                spec,
                rid,
                npu_count,
                pushgateway_url=pushgateway_url,
            )
        except PushError as exc:
            warnings.append(f"formal prom push failed: {exc}")

    prom_metrics = _write_json(
        run_dir / "prom" / "formal-case-prometheus.json",
        {
            "run_id": rid,
            "pushgateway_url": pushgateway_url,
            "prometheus_url": prometheus_url,
            "prom_pushed": prom_pushed,
            "npu_count": npu_count,
            "row_count": len(remote_result.rows) if remote_result is not None else 0,
            "note": "formal-case evidence; matrix details remain in matrix-results.jsonl",
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


def _adapter_config(cfg: Any, *, cache_root: str | Path | None, workdir: str) -> Any:
    payload = cfg.verl_case.model_dump(mode="json")
    payload["remote_workdir"] = workdir
    if cache_root is not None:
        payload["cache_root"] = str(cache_root)
    return VerlCaseConfig.model_validate(payload)


def _resolve_spec(cfg: Any, server: str | None) -> ServerSpec:
    if not cfg.servers:
        raise ConfigError("config.servers 为空，无法选择运行机器")
    if server is None:
        return cfg.servers[0]
    for item in cfg.servers:
        if item.name == server:
            return item
    raise ConfigError(f"未找到服务器: {server}")


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


def _capture_provenance(
    *,
    repo_root: Path,
    case_config: Any,
    allow_git_push: bool,
    run_id: str,
) -> tuple[list[Any], list[str]]:
    rows: list[Any] = []
    warnings: list[str] = []
    branch_prefix = f"codex/verl-case-{run_id}-"
    rows.append(
        capture_repo_provenance(
            repo_root,
            fork_owner=case_config.github_owner,
            allow_commit_push=allow_git_push,
            branch_prefix=branch_prefix,
        )
    )
    configured_paths = dict(getattr(case_config, "dependency_repo_paths", {}) or {})
    for repo, upstream_url in DEPENDENCY_REPOS.items():
        raw_path = configured_paths.get(repo)
        if not raw_path:
            warnings.append(f"dependency repo path not configured: {repo}")
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


def _write_matrix(path: Path, rows: list[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(row.model_dump_json() + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")
    return path


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
) -> Path:
    formal_case = {
        "kind": "verl-case",
        "matrix_results": str(matrix_path) if matrix_path else None,
        "log_path": str(log_path),
        "remote_matrix_path": remote_result.remote_matrix_path if remote_result is not None else None,
        "remote_log_path": remote_result.remote_log_path if remote_result is not None else None,
        "row_count": len(remote_result.rows) if remote_result is not None else 0,
        "ok": bool(remote_result and remote_result.ok and matrix_path and matrix_path.exists()),
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

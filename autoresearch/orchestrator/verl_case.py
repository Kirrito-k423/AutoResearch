"""Implementation for `autoresearch run verl-case`."""
from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datalake.manifest import RunManifest
from datalake.manifest import write as write_manifest
from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.progress import emit_progress

from autoresearch.collect.cli import generate_run_id
from autoresearch.report.cli import run_render

from .checks import DEFAULT_CONFIG_PATH, DEFAULT_REMOTE_PROXY_PORT, run_check_all
from .models import StepResult, skipped_step, step_result, summarize_steps


case_config_mod = importlib.import_module("workspace-adapter.verl.case_config")
case_runner_mod = importlib.import_module("workspace-adapter.verl.case_runner")
data_prep_mod = importlib.import_module("workspace-adapter.verl.data_prep")
provenance_mod = importlib.import_module("workspace-adapter.verl.provenance")

VerlCaseConfig = case_config_mod.VerlCaseConfig
VerlCaseRunConfig = case_config_mod.VerlCaseRunConfig
build_length_matrix = case_config_mod.build_length_matrix
now_utc = case_config_mod.now_utc
write_immutable_config = case_config_mod.write_immutable_config
run_verl_case = case_runner_mod.run_verl_case
prepare_geometry3k = data_prep_mod.prepare_geometry3k
capture_repo_provenance = provenance_mod.capture_repo_provenance


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
    provenance_rows, provenance_warnings = _capture_provenance(
        repo_root=repo_root or Path.cwd(),
        case_config=adapter_config,
        allow_git_push=allow_git_push,
        run_id=rid,
    )
    warnings.extend(provenance_warnings)
    prepared = prepare_geometry3k(adapter_config, adapter_config.cache_root)
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
            "cache": prepared.model_dump(mode="json"),
            "pushgateway_url": pushgateway_url,
            "prometheus_url": prometheus_url,
            "local_proxy_url": local_proxy_url,
            "remote_proxy_port": remote_proxy_port,
            "container_proxy_url": container_proxy_url,
        },
    )
    config_snapshot = write_immutable_config(run_config, run_dir)
    provenance_path = _write_json(
        run_dir / "provenance.json",
        [item.model_dump(mode="json") for item in provenance_rows],
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
                "warnings": warnings,
            },
        )
    )

    emit_progress("orch.verl_case.run", run_id=rid, matrix_rows=len(run_config.matrix))
    try:
        remote_result = run_verl_case(
            spec,
            run_config,
            timeout=timeout,
            proxy_url=container_proxy_url,
            remote_model_path=f"{resolved_workdir}/autoresearch/model",
            remote_dataset_path=f"{resolved_workdir}/autoresearch/dataset",
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
    prom_metrics = _write_json(
        run_dir / "prom" / "formal-case-prometheus.json",
        {
            "run_id": rid,
            "pushgateway_url": pushgateway_url,
            "prometheus_url": prometheus_url,
            "note": "formal-case evidence placeholder; detailed metrics are in matrix-results.jsonl",
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
        remote_result=remote_result,
    )
    collect_payload = {
        "ok": manifest_path.exists() and log_path.exists() and provenance_path.exists(),
        "manifest": str(manifest_path),
        "log_path": str(log_path),
        "prom_metrics_file": str(prom_metrics),
        "wandb_path": str(run_dir / "wandb"),
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
    remote_result: Any,
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
        wandb_path=run_dir / "wandb",
        log_files=[log_path],
        prom_pushed=False,
        prom_metrics_file=prom_metrics,
    )
    return write_manifest(manifest, root=root)


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

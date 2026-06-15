"""Click commands for Skill 07 data collection."""
from __future__ import annotations

import json
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import click

from autoresearch.collect.manifest import build_manifest
from autoresearch.collect.minimal import collect_minimal, _resolve_spec, _resolve_workdir
from datalake.logs import LogFetchError, collect_log
from datalake.manifest import write as write_manifest
from datalake.prometheus import PushError, push_metrics
from datalake.wandb.sync import WandbSyncError, sync_run


_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode_base32(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(_CROCKFORD[value & 31])
        value >>= 5
    return "".join(reversed(chars))


def generate_run_id() -> str:
    """Generate a compact ULID-like run id without an extra dependency."""
    millis = int(time.time() * 1000)
    randomness = secrets.randbits(80)
    return _encode_base32(millis, 10) + _encode_base32(randomness, 16)


def run_collect(
    *,
    server: str,
    lib: str,
    config: str | None,
    workdir: str | None,
    timeout: float,
    run_id: str | None = None,
    pushgateway_url: str = "http://localhost:9091",
    local_runs_root: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run the end-to-end collection workflow and return ``(exit_code, payload)``."""
    rid = run_id or generate_run_id()
    started_at = datetime.now(timezone.utc)
    errors: list[str] = []

    spec = _resolve_spec(server, config)
    resolved_workdir = _resolve_workdir(spec, workdir)
    conda_env = getattr(spec, "conda_env", "") or ""
    root = Path(local_runs_root).expanduser() if local_runs_root else Path("~/.autoresearch/runs").expanduser()

    try:
        minimal_result = collect_minimal(
            server,
            lib=lib,
            config_path=config,
            workdir_override=resolved_workdir,
            timeout=timeout,
            run_id=rid,
        )
    except Exception as exc:
        minimal_result = {
            "lib": lib,
            "sum_value": None,
            "npu_count": None,
            "elapsed_ms": 0,
            "exit_code": -1,
            "stdout": "",
            "stderr": "",
            "error": str(exc),
            "timeout": False,
            "wandb_run_id": None,
            "remote_log_path": f"{resolved_workdir}/runs/{rid}.log",
        }
        errors.append(f"minimal failed: {exc}")

    wandb_path = None
    wandb_run_id = minimal_result.get("wandb_run_id") or rid
    if minimal_result.get("exit_code") == 0:
        try:
            wandb_path = sync_run(
                str(wandb_run_id),
                spec,
                workdir=resolved_workdir,
                local_runs_root=root,
            )
        except WandbSyncError as exc:
            errors.append(f"wandb sync failed: {exc}")
    else:
        errors.append("wandb sync skipped: minimal run failed")

    log_path = None
    try:
        log_path = collect_log(
            rid,
            spec,
            workdir_override=resolved_workdir,
            local_runs_root=root,
            remote_log_path=minimal_result.get("remote_log_path"),
        )
    except LogFetchError as exc:
        errors.append(f"log collect failed: {exc}")

    prom_pushed = False
    npu_count = minimal_result.get("npu_count")
    if isinstance(npu_count, int):
        try:
            prom_pushed = push_metrics(
                spec,
                rid,
                npu_count,
                pushgateway_url=pushgateway_url,
            )
        except PushError as exc:
            errors.append(f"prom push failed: {exc}")
    else:
        errors.append("prom push skipped: npu_count missing")

    finished_at = datetime.now(timezone.utc)
    manifest = build_manifest(
        rid,
        spec,
        lib,
        conda_env,
        resolved_workdir,
        minimal_result,
        wandb_path,
        log_path,
        prom_pushed,
        started_at=started_at,
        finished_at=finished_at,
        error="; ".join(errors) if errors else None,
        local_runs_root=root,
    )
    manifest_path = write_manifest(manifest, root=root)

    ok = minimal_result.get("exit_code") == 0 and wandb_path is not None and log_path is not None
    payload = {
        "ok": ok,
        "run_id": rid,
        "manifest": str(manifest_path),
        "exit_code": minimal_result.get("exit_code"),
        "wandb_path": str(wandb_path) if wandb_path else None,
        "log_path": str(log_path) if log_path else None,
        "prom_pushed": prom_pushed,
        "errors": errors,
    }
    return (0 if ok else 1), payload


@click.command(name="run")
@click.option("--server", required=True, help="config 中的服务器名称.")
@click.option("--lib", "lib", default="verl", type=click.Choice(["verl", "veomni"]))
@click.option("--workdir", default=None, help="覆盖 config.servers[].workdir.")
@click.option("--config", "cfg_path", default=None, help="配置文件路径.")
@click.option("--timeout", default=30.0, type=float, help="minimal 1-step timeout 秒数.")
@click.option("--run-id", default=None, help="指定 run id; 默认自动生成 ULID-like id.")
@click.option("--pushgateway-url", default="http://localhost:9091", help="远程可访问的 pushgateway URL.")
def run(
    server: str,
    lib: str,
    workdir: str | None,
    cfg_path: str | None,
    timeout: float,
    run_id: str | None,
    pushgateway_url: str,
) -> None:
    """跑最小实验并采集 wandb/log/prom/manifest."""
    try:
        exit_code, payload = run_collect(
            server=server,
            lib=lib,
            config=cfg_path,
            workdir=workdir,
            timeout=timeout,
            run_id=run_id,
            pushgateway_url=pushgateway_url,
        )
    except Exception as exc:
        payload = {"ok": False, "error": str(exc)}
        exit_code = 2
    click.echo(json.dumps(payload, ensure_ascii=False, indent=2))
    raise click.exceptions.Exit(exit_code)

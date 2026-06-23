"""Long-running NPU telemetry monitor for configured servers."""
from __future__ import annotations

import importlib
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.progress import emit_progress
from workspace_core.ssh import HostSpec, SSHClient

from datalake.prometheus import build_machine_latest_telemetry_exposition
from autoresearch.hw.parser import parse_npu_smi_info


RunInEnv = Callable[[ServerSpec, str, float], tuple[int, str, str]]
PushText = Callable[[str, str], bool]

run_in_env = importlib.import_module("workspace-adapter.common.conda_utils").run_in_env
telemetry_mod = importlib.import_module("workspace-adapter.verl.telemetry")
parse_npu_smi_watch_output = telemetry_mod.parse_npu_smi_watch_output

NPU_SMI_ONCE_COMMAND = (
    "NPU_SMI_BIN=$(command -v npu-smi"
    " || { test -x /usr/local/sbin/npu-smi && echo /usr/local/sbin/npu-smi; }"
    " || { test -x /usr/local/Ascend/driver/tools/npu-smi"
    " && echo /usr/local/Ascend/driver/tools/npu-smi; }"
    " || { test -x /usr/local/Ascend/ascend-toolkit/latest/tools/npu-smi"
    " && echo /usr/local/Ascend/ascend-toolkit/latest/tools/npu-smi; }); "
    'test -n "$NPU_SMI_BIN" || exit 127; '
    'date "+%Y-%m-%d %H:%M:%S"; "$NPU_SMI_BIN" info'
)


def run_monitor(
    *,
    server: str | None,
    all_servers: bool = False,
    config: str | Path | None = None,
    interval_seconds: float = 0.5,
    duration_seconds: float | None = None,
    once: bool = False,
    pushgateway_url: str = "http://localhost:9091",
    lang: str = "zh",
    runner: RunInEnv | None = None,
    push_text: PushText | None = None,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> int:
    """CLI boundary: sample server NPU telemetry and push machine metrics."""
    emit_progress("hw.monitor.start", server=server, all=all_servers)
    selected_runner = runner or _run_command
    selected_push = push_text or _push_text
    try:
        if interval_seconds < 0.5:
            raise ConfigError("monitor interval must be >= 0.5 seconds")
        servers = _select_servers(server=server, all_servers=all_servers, config=config)
        data = _monitor_loop(
            servers,
            interval_seconds=interval_seconds,
            duration_seconds=duration_seconds,
            once=once,
            pushgateway_url=pushgateway_url,
            runner=selected_runner,
            push_text=selected_push,
            sleep=sleep,
            monotonic=monotonic,
        )
        failed = [name for name, row in data["results"].items() if row["error"]]
        ok = data["samples"] > 0 and data["pushes"] > 0 and not failed
        severity = "ok" if ok else ("warn" if data["pushes"] > 0 else "fail")
        payload = {
            "ok": ok,
            "severity": severity,
            "data": data,
            "message": "NPU telemetry monitor complete" if lang == "en" else "NPU telemetry monitor 完成",
            "error": "; ".join(failed) if failed and not ok else None,
        }
        exit_code = 0 if ok else (1 if severity == "fail" else 0)
    except ConfigError as exc:
        payload = {
            "ok": False,
            "severity": "fail",
            "data": {"server": server, "all": all_servers},
            "message": "Config error" if lang == "en" else "配置错误",
            "error": str(exc),
        }
        exit_code = 2
    except Exception as exc:
        payload = {
            "ok": False,
            "severity": "fail",
            "data": {"server": server, "all": all_servers},
            "message": "NPU telemetry monitor failed" if lang == "en" else "NPU telemetry monitor 失败",
            "error": str(exc),
        }
        exit_code = 1
    if payload["error"]:
        print(f"{payload['message']}: {payload['error']}", file=sys.stderr)
    emit_progress(
        "hw.monitor.result",
        level="info" if payload["ok"] else "error",
        severity=payload["severity"],
    )
    print(json.dumps(payload, ensure_ascii=False))
    return exit_code


def _monitor_loop(
    servers: list[ServerSpec],
    *,
    interval_seconds: float,
    duration_seconds: float | None,
    once: bool,
    pushgateway_url: str,
    runner: RunInEnv,
    push_text: PushText,
    sleep: Callable[[float], None],
    monotonic: Callable[[], float],
) -> dict[str, Any]:
    started = monotonic()
    iterations = 0
    total_samples = 0
    total_pushes = 0
    results = {
        spec.name: {
            "samples": 0,
            "pushes": 0,
            "last_device_count": 0,
            "error": None,
        }
        for spec in servers
    }
    while True:
        iterations += 1
        for spec in servers:
            row = results[spec.name]
            emit_progress("hw.monitor.sample", server=spec.name, iteration=iterations)
            try:
                samples = _sample_server(spec, runner=runner)
                exposition = build_machine_latest_telemetry_exposition(samples)
                pushed = bool(exposition.strip()) and push_text(
                    _machine_endpoint(pushgateway_url, spec.name),
                    exposition,
                )
                row["samples"] += len(samples)
                row["pushes"] += 1 if pushed else 0
                row["last_device_count"] = len({_sample_identity(sample) for sample in samples})
                row["error"] = None if pushed else "no telemetry pushed"
                total_samples += len(samples)
                total_pushes += 1 if pushed else 0
            except Exception as exc:
                row["error"] = str(exc)
        if once:
            break
        if duration_seconds is not None and monotonic() - started >= duration_seconds:
            break
        sleep(max(0.0, interval_seconds))
    return {
        "servers": [spec.name for spec in servers],
        "interval_seconds": interval_seconds,
        "duration_seconds": duration_seconds,
        "iterations": iterations,
        "samples": total_samples,
        "pushes": total_pushes,
        "pushgateway_url": pushgateway_url,
        "results": results,
    }


def _sample_server(spec: ServerSpec, *, runner: RunInEnv) -> list[Any]:
    code, stdout, stderr = runner(spec, NPU_SMI_ONCE_COMMAND, 15.0)
    if code != 0:
        detail = (stderr or stdout or "").strip()[:240] or f"exit={code}"
        raise RuntimeError(f"npu-smi failed: {detail}")
    samples = parse_npu_smi_watch_output(
        stdout,
        run_id="machine-monitor",
        case_id="machine-monitor",
        server=spec.name,
        source="machine-monitor",
    )
    if not samples:
        samples = _samples_from_hw_parser(stdout, server=spec.name)
    if not samples:
        raise RuntimeError("npu-smi output contained no telemetry samples")
    return samples


def _run_command(spec: ServerSpec, command: str, timeout: float) -> tuple[int, str, str]:
    identity_file = (
        Path(spec.identity_file).expanduser()
        if getattr(spec, "identity_file", None)
        else None
    )
    host = HostSpec(
        alias=spec.name,
        host=spec.host,
        port=int(spec.port),
        user=spec.user,
        identity_file=identity_file,
    )
    client = SSHClient(host, bootstrap_password=spec.bootstrap_password_secret)
    client.connect(connect_timeout=5.0, retries=0)
    try:
        return client.exec(command, timeout=timeout)
    finally:
        client.close()


def _samples_from_hw_parser(text: str, *, server: str) -> list[Any]:
    parsed = parse_npu_smi_info(text)
    samples: list[Any] = []
    for index, device in enumerate(parsed["devices"]):
        device_id = device.get("id")
        if device_id is None:
            device_id = index
        samples.append(
            {
                "run_id": "machine-monitor",
                "case_id": "machine-monitor",
                "server": server,
                "device_id": int(device_id),
                "chip_id": device.get("chip_id") if device.get("chip_id") is not None else 0,
                "sample_index": len(samples),
                "source": "machine-monitor",
                "hbm_used_mib": device.get("memory_used_mib"),
                "hbm_total_mib": device.get("memory_total_mib"),
                "ai_core_utilization_percent": device.get("utilization_pct"),
                "npu_utilization_percent": device.get("utilization_pct"),
            }
        )
    return samples


def _sample_identity(sample: Any) -> tuple[Any, Any]:
    if isinstance(sample, dict):
        return sample.get("device_id"), sample.get("chip_id", 0)
    return getattr(sample, "device_id", None), getattr(sample, "chip_id", 0)


def _push_text(endpoint: str, body: str) -> bool:
    req = urllib.request.Request(endpoint, data=body.encode("utf-8"), method="PUT")
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        return 200 <= resp.status < 300


def _machine_endpoint(pushgateway_url: str, server_name: str) -> str:
    return f"{pushgateway_url.rstrip('/')}/metrics/job/autoresearch_machine/server/{_job_suffix(server_name)}"


def _job_suffix(value: str) -> str:
    import re

    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_")
    return cleaned or "unknown"


def _select_servers(
    *,
    server: str | None,
    all_servers: bool,
    config: str | Path | None,
) -> list[ServerSpec]:
    if bool(server) == all_servers:
        raise ConfigError("必须且只能提供 --server NAME 或 --all")
    cfg = from_path(config)
    if all_servers:
        if not cfg.servers:
            raise ConfigError("config.servers 为空")
        return list(cfg.servers)
    for item in cfg.servers:
        if item.name == server:
            return [item]
    raise ConfigError(f"未找到服务器: {server}")

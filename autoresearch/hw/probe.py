"""Single-server Ascend hardware probe orchestration."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
from typing import Callable

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.layout import LOGS_DIR
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import HostSpec, SSHClient, SSHError, resolve_host

from .models import CommandRecord, DriverVersions, HardwareData, NPUProcess
from .parser import (
    core_field_errors,
    parse_driver_version_info,
    parse_lspci_devices,
    parse_npu_smi_info,
    parse_ps_output,
    parse_typed_metric_output,
)


NPU_SMI_INFO_COMMAND = "npu-smi info"
DRIVER_VERSION_COMMAND = "cat /usr/local/Ascend/driver/version.info"
LSPCI_COMMAND = "lspci -Dnn"
TYPED_QUERY_TYPES = ("memory", "temp", "usages")
SSHClientFactory = Callable[..., SSHClient]
ProbeFunction = Callable[[str, str | Path | None], CheckResult]


def typed_query_command(metric_type: str, device_id: int) -> str:
    """Build one allowlisted typed command from a parsed integer id."""
    if metric_type not in TYPED_QUERY_TYPES:
        raise ValueError(f"unsupported typed query type: {metric_type}")
    if (
        not isinstance(device_id, int)
        or isinstance(device_id, bool)
        or device_id < 0
    ):
        raise ValueError("device_id must be a non-negative integer")
    return f"npu-smi info -t {metric_type} -i {device_id}"


def enrich_processes(
    client: SSHClient,
    processes: list[NPUProcess],
    command_records: list[CommandRecord] | None = None,
) -> list[str]:
    """Enrich parsed numeric PIDs with user and executable basename."""
    pids = sorted(
        {
            process["pid"]
            for process in processes
            if isinstance(process["pid"], int)
            and not isinstance(process["pid"], bool)
            and process["pid"] >= 0
        }
    )
    if not pids:
        return []

    command = (
        "ps -o pid=,user=,comm= -p "
        + ",".join(str(pid) for pid in pids)
    )
    try:
        if command_records is None:
            exit_code, stdout, stderr = client.exec(command)
        else:
            exit_code, stdout, stderr = _exec_recorded(
                client,
                command,
                command_records,
            )
    except Exception as exc:
        return [f"process enrichment failed: {exc}"]

    if exit_code != 0:
        detail = stderr.strip() or "no stderr"
        return [
            f"process enrichment failed with exit code {exit_code}: {detail}"
        ]

    details = parse_ps_output(stdout)
    warnings: list[str] = []
    for process in processes:
        detail = details.get(process["pid"])
        if detail is None:
            warnings.append(
                f"process {process['pid']} exited or could not be inspected"
            )
            continue
        process["user"], process["process_name"] = detail
    return warnings


def _missing_query_types(device) -> list[str]:
    query_types: list[str] = []
    if (
        device["memory_used_mib"] is None
        or device["memory_total_mib"] is None
    ):
        query_types.append("memory")
    if device["temperature_c"] is None:
        query_types.append("temp")
    if device["utilization_pct"] is None:
        query_types.append("usages")
    return query_types


def _exec_recorded(
    client: SSHClient,
    command: str,
    command_records: list[CommandRecord],
) -> tuple[int, str, str]:
    exit_code, stdout, stderr = client.exec(command)
    command_records.append(
        CommandRecord(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
        )
    )
    return exit_code, stdout, stderr


def _supplement_typed_metrics(
    client: SSHClient,
    data: HardwareData,
    command_records: list[CommandRecord],
) -> None:
    used_supplement = False
    for device in data["devices"]:
        device_id = device["id"]
        if not isinstance(device_id, int) or isinstance(device_id, bool):
            data["warnings"].append(
                "typed query skipped: parsed device id is not an integer"
            )
            continue
        for metric_type in _missing_query_types(device):
            command = typed_query_command(metric_type, device_id)
            exit_code, stdout, stderr = _exec_recorded(
                client,
                command,
                command_records,
            )
            if exit_code != 0:
                detail = stderr.strip() or "no stderr"
                data["warnings"].append(
                    f"typed query {metric_type} for device {device_id} "
                    f"failed with exit code {exit_code}: {detail}"
                )
                continue
            values = parse_typed_metric_output(stdout, metric_type, device_id)
            if not values:
                data["warnings"].append(
                    f"typed query {metric_type} for device {device_id} "
                    "returned an unknown format"
                )
                continue
            for field, value in values.items():
                current = device[field]
                if current is None:
                    device[field] = value
                    used_supplement = True
                elif current != value:
                    data["warnings"].append(
                        f"typed query {metric_type} conflict for device "
                        f"{device_id} field {field}: kept primary value {current}"
                    )
    if used_supplement:
        data["warnings"].append("typed supplement used for missing core metrics")
    data["field_errors"] = core_field_errors(data["devices"])


def _collect_driver_versions(
    client: SSHClient,
    data: HardwareData,
    command_records: list[CommandRecord],
) -> None:
    exit_code, stdout, stderr = _exec_recorded(
        client,
        DRIVER_VERSION_COMMAND,
        command_records,
    )
    if exit_code != 0:
        detail = stderr.strip() or "file unavailable"
        data["warnings"].append(
            f"driver version.info unavailable (exit code {exit_code}): {detail}"
        )
        return

    versions = parse_driver_version_info(stdout)
    if versions["driver"] is None and versions["package"] is None:
        data["warnings"].append(
            "driver version.info contained no recognized version fields"
        )
        return
    data["driver_versions"]["driver"] = versions["driver"]
    data["driver_versions"]["package"] = versions["package"]


def write_raw_failure_log(
    server_name: str,
    command_records: list[CommandRecord],
) -> Path:
    """Write failed command output under the local hardware log directory."""
    safe_server = re.sub(r"[^A-Za-z0-9_.-]", "_", server_name) or "unknown"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = LOGS_DIR / f"hw-{safe_server}-{timestamp}.log"
    path.parent.mkdir(parents=True, exist_ok=True)

    sections: list[str] = []
    for record in command_records:
        sections.extend(
            [
                f"$ {record['command']}",
                f"exit_code={record['exit_code']}",
                "--- stdout ---",
                record["stdout"],
                "--- stderr ---",
                record["stderr"],
                "",
            ]
        )
    path.write_text("\n".join(sections), encoding="utf-8")
    return path


def _raw_output_summary(command_records: list[CommandRecord]) -> str:
    parts: list[str] = []
    for record in command_records:
        if record["command"] == DRIVER_VERSION_COMMAND:
            parts.append(
                f"{record['command']}: exit code {record['exit_code']}"
            )
            continue
        output = "\n".join(
            value for value in (record["stdout"], record["stderr"]) if value
        )
        if output:
            parts.append(f"{record['command']}: {output}")
        else:
            parts.append(
                f"{record['command']}: exit code {record['exit_code']}"
            )
    return " ".join(" ".join(parts).split())[:512]


def _attach_failure_diagnostics(
    data: HardwareData,
    server_name: str,
    command_records: list[CommandRecord],
) -> None:
    if not command_records:
        return
    data["raw_output_summary"] = _raw_output_summary(command_records)
    try:
        data["raw_log_path"] = str(
            write_raw_failure_log(server_name, command_records)
        )
    except OSError as exc:
        data["warnings"].append(f"failed to write local raw log: {exc}")


def resolve_server_host(
    server_name: str,
    config_path: str | Path | None = None,
) -> tuple[ServerSpec, HostSpec]:
    """Resolve an exact configured server name to a public SSH host spec."""
    config = from_path(config_path)
    server = next(
        (item for item in config.servers if item.name == server_name),
        None,
    )
    if server is None:
        available = [item.name for item in config.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{server_name}'; 当前已配: {available}"
        )

    host = resolve_host(f"{server.user}@{server.host}:{server.port}")
    host = HostSpec(
        alias=server.name,
        host=host.host,
        port=host.port,
        user=host.user,
        identity_file=(
            Path(server.identity_file).expanduser()
            if server.identity_file
            else None
        ),
    )
    return server, host


def _empty_data(server: ServerSpec) -> HardwareData:
    return HardwareData(
        server={
            "name": server.name,
            "host": server.host,
            "port": server.port,
        },
        devices=[],
        processes=[],
        driver_versions=DriverVersions(
            npu_smi=None,
            driver=None,
            package=None,
        ),
        warnings=[],
        field_errors=[],
        fallback=None,
        raw_log_path=None,
        raw_output_summary=None,
    )


def _result(
    *,
    ok: bool,
    severity: CheckSeverity,
    data: HardwareData,
    message: str,
    error: str | None,
) -> CheckResult:
    return CheckResult(
        ok=ok,
        severity=severity,
        data=dict(data),
        message=message,
        error=error,
    )


def probe_server(
    server_name: str,
    config_path: str | Path | None = None,
    ssh_client_factory: SSHClientFactory = SSHClient,
) -> CheckResult:
    """Run the fixed NPU command and preserve partial parser output on failure."""
    server, host = resolve_server_host(server_name, config_path)
    data = _empty_data(server)
    client: SSHClient | None = None
    command_records: list[CommandRecord] = []
    stage = "connect"

    try:
        client = ssh_client_factory(
            host,
            bootstrap_password=server.bootstrap_password_secret,
        )
        emit_progress("hw.connect", server=server.name)
        client.connect(connect_timeout=5.0)

        stage = "command"
        emit_progress(
            "hw.command",
            server=server.name,
            command=NPU_SMI_INFO_COMMAND,
        )
        exit_code, stdout, stderr = _exec_recorded(
            client,
            NPU_SMI_INFO_COMMAND,
            command_records,
        )

        stage = "parse"
        emit_progress("hw.parse", server=server.name)
        parsed = parse_npu_smi_info(stdout)
        data["devices"] = parsed["devices"]
        data["processes"] = parsed["processes"]
        data["driver_versions"] = parsed["driver_versions"]
        data["warnings"] = list(parsed["warnings"])
        data["field_errors"] = parsed["field_errors"]

        if parsed["error"] is None and data["field_errors"]:
            _supplement_typed_metrics(client, data, command_records)
        if parsed["error"] is None:
            data["warnings"].extend(
                enrich_processes(client, data["processes"], command_records)
            )

        _collect_driver_versions(client, data, command_records)

        if parsed["error"] is not None:
            lspci_exit, lspci_stdout, lspci_stderr = _exec_recorded(
                client,
                LSPCI_COMMAND,
                command_records,
            )
            fallback_devices = (
                parse_lspci_devices(lspci_stdout)
                if lspci_exit == 0
                else []
            )
            data["devices"] = fallback_devices
            data["field_errors"] = core_field_errors(fallback_devices)
            data["fallback"] = "lspci"
            if lspci_exit != 0:
                detail = lspci_stderr.strip() or "no stderr"
                data["warnings"].append(
                    f"lspci fallback failed with exit code "
                    f"{lspci_exit}: {detail}"
                )
            elif not fallback_devices:
                data["warnings"].append(
                    "lspci fallback found no supported Ascend accelerators"
                )
            else:
                data["warnings"].append(
                    "lspci fallback proves device presence only; "
                    "dynamic metrics are unavailable"
                )
            _attach_failure_diagnostics(data, server.name, command_records)
            emit_progress(
                "hw.fail",
                level="error",
                server=server.name,
                failed_stage=stage,
            )
            return _result(
                ok=False,
                severity=CheckSeverity.FAIL,
                data=data,
                message="NPU 输出解析失败，已执行 lspci 降级",
                error=f"npu-smi parse failed: {parsed['error']}",
            )

        if exit_code != 0:
            detail = stderr.strip() or "no stderr"
            error = f"npu-smi command failed with exit code {exit_code}: {detail}"
            emit_progress(
                "hw.fail",
                level="error",
                server=server.name,
                failed_stage=stage,
            )
            _attach_failure_diagnostics(data, server.name, command_records)
            return _result(
                ok=False,
                severity=CheckSeverity.FAIL,
                data=data,
                message="NPU 命令执行失败",
                error=error,
            )

        if data["field_errors"]:
            emit_progress(
                "hw.fail",
                level="error",
                server=server.name,
                failed_stage=stage,
            )
            _attach_failure_diagnostics(data, server.name, command_records)
            return _result(
                ok=False,
                severity=CheckSeverity.FAIL,
                data=data,
                message="NPU 核心指标不完整",
                error="one or more core NPU metrics could not be parsed",
            )

        if stderr.strip():
            data["warnings"].append(f"npu-smi stderr: {stderr.strip()}")

        severity = (
            CheckSeverity.WARN if data["warnings"] else CheckSeverity.OK
        )
        emit_progress(
            "hw.complete",
            level="warn" if severity == CheckSeverity.WARN else "info",
            server=server.name,
            devices=len(data["devices"]),
        )
        return _result(
            ok=True,
            severity=severity,
            data=data,
            message="NPU 核心指标探测完成",
            error=None,
        )
    except SSHError as exc:
        error_kind = "connection" if stage == "connect" else "command"
        emit_progress(
            "hw.fail",
            level="error",
            server=server.name,
            failed_stage=stage,
        )
        _attach_failure_diagnostics(data, server.name, command_records)
        return _result(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message="SSH 连接失败" if stage == "connect" else "SSH 命令失败",
            error=f"SSH {error_kind} failed: {exc}",
        )
    except Exception as exc:
        emit_progress(
            "hw.fail",
            level="error",
            server=server.name,
            failed_stage=stage,
        )
        _attach_failure_diagnostics(data, server.name, command_records)
        return _result(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message="硬件探测失败",
            error=f"{stage} failed: {exc}",
        )
    finally:
        if client is not None:
            client.close()


def _cli_failure(server_name: str | None, message: str, error: str) -> CheckResult:
    data = HardwareData(
        server={"name": server_name} if server_name else {},
        devices=[],
        processes=[],
        driver_versions=DriverVersions(
            npu_smi=None,
            driver=None,
            package=None,
        ),
        warnings=[],
        field_errors=[],
        fallback=None,
        raw_log_path=None,
        raw_output_summary=None,
    )
    return _result(
        ok=False,
        severity=CheckSeverity.FAIL,
        data=data,
        message=message,
        error=error,
    )


def probe_all(
    config_path: str | Path | None = None,
    max_workers: int = 3,
    probe_fn: ProbeFunction = probe_server,
) -> CheckResult:
    """Probe every configured server with bounded, failure-isolated workers."""
    config = from_path(config_path)
    server_names = [server.name for server in config.servers]
    if not server_names:
        raise ConfigError("config.servers 不能为空")
    if max_workers < 1:
        raise ConfigError("max_workers 必须大于等于 1")

    results_by_name: dict[str, CheckResult] = {}
    worker_count = min(3, max_workers, len(server_names))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {}
        for server_name in server_names:
            emit_progress("hw.all.begin", server=server_name)
            future = executor.submit(probe_fn, server_name, config_path)
            futures[future] = server_name

        for future in as_completed(futures):
            server_name = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = _cli_failure(
                    server_name,
                    "硬件探测失败",
                    f"worker failed: {exc}",
                )
            results_by_name[server_name] = result
            emit_progress(
                "hw.all.complete" if result["ok"] else "hw.all.fail",
                level="info" if result["ok"] else "error",
                server=server_name,
                severity=result["severity"].value,
            )

    ordered_results = {
        server_name: results_by_name[server_name]
        for server_name in server_names
    }
    passed_servers = [
        name for name, result in ordered_results.items() if result["ok"]
    ]
    failed_servers = [
        name for name, result in ordered_results.items() if not result["ok"]
    ]
    warned = sum(
        result["severity"] == CheckSeverity.WARN
        for result in ordered_results.values()
    )
    if failed_servers:
        severity = CheckSeverity.FAIL
        ok = False
        message = "部分服务器硬件探测失败"
        error = "; ".join(
            f"{name}: {ordered_results[name]['error'] or 'probe failed'}"
            for name in failed_servers
        )
    else:
        severity = CheckSeverity.WARN if warned else CheckSeverity.OK
        ok = True
        message = "全部服务器硬件探测完成"
        error = None

    return CheckResult(
        ok=ok,
        severity=severity,
        data={
            "results": ordered_results,
            "total": len(server_names),
            "passed": len(passed_servers),
            "failed": len(failed_servers),
            "warned": warned,
            "passed_servers": passed_servers,
            "failed_servers": failed_servers,
        },
        message=message,
        error=error,
    )


def run_probe(
    server: str | None,
    all_servers: bool = False,
    config: str | Path | None = None,
    lang: str = "zh",
) -> int:
    """CLI boundary: print exactly one CheckResult JSON and return 0/1/2."""
    result: CheckResult
    exit_code: int
    emit_progress("hw.probe.start", server=server)

    try:
        if bool(server) == all_servers:
            raise ConfigError("必须且只能提供 --server NAME 或 --all")
        if all_servers:
            result = probe_all(config_path=config)
        else:
            result = probe_server(server, config_path=config)
        exit_code = 0 if result["ok"] else 1
    except ConfigError as exc:
        label = "配置错误" if lang == "zh" else "Config error"
        result = _cli_failure(server, label, str(exc))
        exit_code = 2
    except Exception as exc:
        label = "硬件探测失败" if lang == "zh" else "Hardware probe failed"
        result = _cli_failure(server, label, str(exc))
        exit_code = 1

    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    emit_progress(
        "hw.probe.result",
        level="info" if result["ok"] else "error",
        server=server,
        severity=result["severity"].value,
    )
    print(json.dumps(result, ensure_ascii=False))
    return exit_code

"""Single-server Ascend hardware probe orchestration."""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Callable

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import HostSpec, SSHClient, SSHError, resolve_host

from .models import DriverVersions, HardwareData
from .parser import parse_npu_smi_info


NPU_SMI_INFO_COMMAND = "npu-smi info"
SSHClientFactory = Callable[[HostSpec], SSHClient]


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
    if server.identity_file:
        host = HostSpec(
            alias=host.alias,
            host=host.host,
            port=host.port,
            user=host.user,
            identity_file=Path(server.identity_file).expanduser(),
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
    stage = "connect"

    try:
        client = ssh_client_factory(host)
        emit_progress("hw.connect", server=server.name)
        client.connect(connect_timeout=5.0)

        stage = "command"
        emit_progress(
            "hw.command",
            server=server.name,
            command=NPU_SMI_INFO_COMMAND,
        )
        exit_code, stdout, stderr = client.exec(NPU_SMI_INFO_COMMAND)

        stage = "parse"
        emit_progress("hw.parse", server=server.name)
        parsed = parse_npu_smi_info(stdout)
        data["devices"] = parsed["devices"]
        data["processes"] = parsed["processes"]
        data["driver_versions"] = parsed["driver_versions"]
        data["warnings"] = list(parsed["warnings"])
        data["field_errors"] = parsed["field_errors"]

        if exit_code != 0:
            detail = stderr.strip() or "no stderr"
            error = f"npu-smi command failed with exit code {exit_code}: {detail}"
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
                message="NPU 命令执行失败",
                error=error,
            )

        if parsed["error"] is not None:
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
                message="NPU 输出解析失败",
                error=f"npu-smi parse failed: {parsed['error']}",
            )

        if data["field_errors"]:
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
    )
    return _result(
        ok=False,
        severity=CheckSeverity.FAIL,
        data=data,
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
        if all_servers:
            raise ConfigError("--all 将在 Plan 04-03 开放")
        if not server:
            raise ConfigError("必须提供 --server NAME")
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

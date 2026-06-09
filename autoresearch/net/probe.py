"""Local and remote network probe orchestration."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import re
import shlex
import subprocess
import sys
from typing import Callable, Iterable

from workspace_core.config import ConfigError, ServerSpec, from_path
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import HostSpec, SSHClient, SSHError, resolve_host

from .curl import (
    build_curl_command,
    parse_curl_result,
    target_label,
    validate_target_url,
)
from .tunnel import (
    DEFAULT_LOCAL_PROXY_URL,
    DEFAULT_REMOTE_PROXY_PORT,
    ensure_tunnel,
    redact_proxy_url,
)
from .models import CurlAttempt, NetworkGroupSummary, NetworkRow, NetworkSummary


RunCommand = Callable[..., subprocess.CompletedProcess[str]]
SSHClientFactory = Callable[..., SSHClient]
RemoteProbeFunction = Callable[..., list[NetworkRow]]
PROXY_ELIGIBLE_LABELS = {"huggingface", "github"}


def probe_local(
    targets: Iterable[str],
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    run_cmd: RunCommand = subprocess.run,
) -> list[NetworkRow]:
    """Probe configured targets from the local Mac with direct-first semantics."""
    rows: list[NetworkRow] = []
    for url in _validated_targets(targets):
        label = target_label(url)
        direct = _run_local_curl(url, "direct", None, run_cmd)
        attempts = [direct]
        if (
            not direct["ok"]
            and label in PROXY_ELIGIBLE_LABELS
            and local_proxy_url
        ):
            attempts.append(
                _run_local_curl(url, "proxy", local_proxy_url, run_cmd)
            )
        rows.append(_row_from_attempts("local", None, label, url, attempts))
    return rows


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


def probe_remote_direct(
    server_name: str,
    targets: Iterable[str],
    config_path: str | Path | None = None,
    ssh_client_factory: SSHClientFactory = SSHClient,
) -> list[NetworkRow]:
    """Probe configured targets from one remote server through SSH direct curl."""
    clean_targets = _validated_targets(targets)
    server, host = resolve_server_host(server_name, config_path)
    client: SSHClient | None = None
    try:
        client = ssh_client_factory(
            host,
            bootstrap_password=server.bootstrap_password_secret,
        )
        client.connect(connect_timeout=5.0)
        rows: list[NetworkRow] = []
        for url in clean_targets:
            label = target_label(url)
            command = _remote_shell_command(url)
            exit_code, stdout, stderr = client.exec(command)
            attempt = parse_curl_result(
                exit_code,
                stdout,
                stderr,
                "direct",
                url,
            )
            rows.append(
                _row_from_attempts(
                    "remote",
                    server.name,
                    label,
                    url,
                    [attempt],
                    remote_direct=True,
                )
            )
        return rows
    except SSHError as exc:
        return _failure_rows(
            "remote",
            server.name,
            clean_targets,
            f"SSH failed: {exc}",
        )
    except Exception as exc:
        return _failure_rows(
            "remote",
            server.name,
            clean_targets,
            f"remote probe failed: {exc}",
        )
    finally:
        if client is not None:
            client.close()


def probe_remote_with_proxy_fallback(
    server_name: str,
    targets: Iterable[str],
    config_path: str | Path | None = None,
    *,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    ssh_client_factory: SSHClientFactory = SSHClient,
    ensure_tunnel_fn=ensure_tunnel,
) -> list[NetworkRow]:
    """Probe one remote server; retry failed targets through ssh -R proxy."""
    clean_targets = _validated_targets(targets)
    server, host = resolve_server_host(server_name, config_path)
    client: SSHClient | None = None
    remote_proxy_url: str | None = None
    try:
        client = ssh_client_factory(
            host,
            bootstrap_password=server.bootstrap_password_secret,
        )
        client.connect(connect_timeout=5.0)
        rows: list[NetworkRow] = []
        for url in clean_targets:
            label = target_label(url)
            exit_code, stdout, stderr = client.exec(_remote_shell_command(url))
            direct = parse_curl_result(
                exit_code,
                stdout,
                stderr,
                "direct",
                url,
            )
            attempts = [direct]
            if not direct["ok"]:
                if remote_proxy_url is None:
                    try:
                        state = ensure_tunnel_fn(
                            server_name,
                            config_path=config_path,
                            local_proxy_url=local_proxy_url,
                            remote_proxy_port=remote_proxy_port,
                        )
                        remote_proxy_url = state["remote_proxy_url"]
                    except Exception as exc:
                        attempts.append(
                            _proxy_unavailable_attempt(
                                url,
                                "proxy_unavailable: "
                                + _sanitize_proxy_error(
                                    str(exc),
                                    local_proxy_url,
                                ),
                            )
                        )
                        rows.append(
                            _row_from_attempts(
                                "remote",
                                server.name,
                                label,
                                url,
                                attempts,
                                remote_direct=True,
                            )
                        )
                        continue

                px_exit, px_stdout, px_stderr = client.exec(
                    _remote_shell_command(url, remote_proxy_url)
                )
                attempts.append(
                    parse_curl_result(
                        px_exit,
                        px_stdout,
                        px_stderr,
                        "proxy",
                        url,
                        proxy_url=remote_proxy_url,
                    )
                )
            rows.append(
                _row_from_attempts(
                    "remote",
                    server.name,
                    label,
                    url,
                    attempts,
                    remote_direct=True,
                )
            )
        return rows
    except SSHError as exc:
        return _failure_rows(
            "remote",
            server.name,
            clean_targets,
            f"SSH failed: {exc}",
        )
    except Exception as exc:
        return _failure_rows(
            "remote",
            server.name,
            clean_targets,
            f"remote probe failed: {exc}",
        )
    finally:
        if client is not None:
            client.close()


def probe_all_remotes(
    config_path: str | Path | None,
    targets: Iterable[str],
    probe_fn: RemoteProbeFunction = probe_remote_with_proxy_fallback,
    max_workers: int = 3,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
) -> list[NetworkRow]:
    """Probe every configured server with bounded, failure-isolated workers."""
    config = from_path(config_path)
    server_names = [server.name for server in config.servers]
    clean_targets = _validated_targets(targets)
    if max_workers < 1:
        raise ConfigError("max_workers 必须大于等于 1")
    if not server_names:
        return []

    rows_by_name: dict[str, list[NetworkRow]] = {}
    worker_count = min(3, max_workers, len(server_names))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {}
        for server_name in server_names:
            emit_progress("net.remote.begin", server=server_name)
            if probe_fn is probe_remote_with_proxy_fallback:
                future = executor.submit(
                    probe_fn,
                    server_name,
                    clean_targets,
                    config_path,
                    local_proxy_url=local_proxy_url,
                    remote_proxy_port=remote_proxy_port,
                )
            else:
                future = executor.submit(
                    probe_fn,
                    server_name,
                    clean_targets,
                    config_path,
                )
            futures[future] = server_name

        for future in as_completed(futures):
            server_name = futures[future]
            try:
                rows = future.result()
            except Exception as exc:
                rows = _failure_rows(
                    "remote",
                    server_name,
                    clean_targets,
                    f"worker failed: {exc}",
                )
            rows_by_name[server_name] = rows
            has_fail = any(row["status"] == "fail" for row in rows)
            emit_progress(
                "net.remote.fail" if has_fail else "net.remote.complete",
                level="error" if has_fail else "info",
                server=server_name,
            )

    ordered: list[NetworkRow] = []
    for server_name in server_names:
        ordered.extend(rows_by_name[server_name])
    return ordered


def summarize_rows(rows: list[NetworkRow]) -> NetworkSummary:
    """Build total, local, remote, and named group summaries."""
    local_rows = [row for row in rows if row["location"] == "local"]
    remote_names = sorted(
        {row["server"] for row in rows if row["location"] == "remote" and row["server"]}
    )
    remotes = {
        name: _summarize_group(
            [row for row in rows if row["location"] == "remote" and row["server"] == name]
        )
        for name in remote_names
    }
    groups = {"local": _summarize_group(local_rows), **remotes}
    total = _summarize_group(rows)
    return NetworkSummary(
        total=total["total"],
        passed=total["passed"],
        warned=total["warned"],
        failed=total["failed"],
        needs_proxy=total["needs_proxy"],
        proxy_used=total["proxy_used"],
        proxy_failed=total["proxy_failed"],
        failed_targets=total["failed_targets"],
        local=groups["local"],
        remotes=remotes,
        groups=groups,
    )


def run_probe(
    server: str | None = None,
    local_only: bool = False,
    config: str | Path | None = None,
    local_proxy_url: str = DEFAULT_LOCAL_PROXY_URL,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    lang: str = "zh",
) -> int:
    """CLI boundary: print exactly one CheckResult JSON and return 0/1/2."""
    emit_progress(
        "net.probe.start",
        server=server,
        local_only=local_only,
    )
    result: CheckResult
    exit_code: int
    try:
        if server and local_only:
            raise ConfigError("不能同时提供 --server 和 --local-only")
        cfg = from_path(config)
        targets = _validated_targets(cfg.network.targets)

        emit_progress("net.local.begin")
        rows = probe_local(targets, local_proxy_url=local_proxy_url)
        emit_progress("net.local.complete", targets=len(targets))

        if not local_only:
            if server:
                emit_progress("net.remote.begin", server=server)
                remote_rows = probe_remote_with_proxy_fallback(
                    server,
                    targets,
                    config,
                    local_proxy_url=local_proxy_url,
                    remote_proxy_port=remote_proxy_port,
                )
                emit_progress("net.remote.complete", server=server)
            else:
                remote_rows = probe_all_remotes(
                    config,
                    targets,
                    local_proxy_url=local_proxy_url,
                    remote_proxy_port=remote_proxy_port,
                )
            rows.extend(remote_rows)

        summary = summarize_rows(rows)
        severity = _severity_from_summary(summary)
        result = CheckResult(
            ok=severity != CheckSeverity.FAIL,
            severity=severity,
            data={
                "rows": rows,
                "summary": summary,
                "warnings": _warnings_from_rows(rows),
                "metadata": {
                    "target_count": len(targets),
                    "remote_scope": (
                        "none" if local_only else (server or "all")
                    ),
                },
            },
            message=_message(severity, lang),
            error=_error_from_rows(rows),
        )
        exit_code = 1 if severity == CheckSeverity.FAIL else 0
    except (ConfigError, ValueError) as exc:
        result = _cli_failure(
            "配置错误" if lang == "zh" else "Config error",
            str(exc),
        )
        exit_code = 2
    except Exception as exc:
        result = _cli_failure(
            "网络探测失败" if lang == "zh" else "Network probe failed",
            str(exc),
        )
        exit_code = 1

    if result["error"]:
        print(f"{result['message']}: {result['error']}", file=sys.stderr)
    emit_progress(
        "net.probe.result",
        level="error" if result["severity"] == CheckSeverity.FAIL else "info",
        server=server,
        severity=result["severity"].value,
    )
    print(json.dumps(result, ensure_ascii=False))
    return exit_code


def _validated_targets(targets: Iterable[str]) -> list[str]:
    values = list(targets)
    if not values:
        raise ConfigError("config.network.targets 不能为空")
    return [validate_target_url(url) for url in values]


def _run_local_curl(
    url: str,
    mode: str,
    proxy_url: str | None,
    run_cmd: RunCommand,
) -> CurlAttempt:
    command = build_curl_command(url, proxy_url=proxy_url)
    completed = run_cmd(
        command,
        capture_output=True,
        text=True,
        timeout=12,
    )
    return parse_curl_result(
        int(completed.returncode),
        completed.stdout or "",
        completed.stderr or "",
        mode,  # type: ignore[arg-type]
        url,
        proxy_url=redact_proxy_url(proxy_url) if proxy_url else None,
    )


def _row_from_attempts(
    location: str,
    server: str | None,
    label: str,
    url: str,
    attempts: list[CurlAttempt],
    *,
    remote_direct: bool = False,
) -> NetworkRow:
    final = attempts[-1]
    if final["ok"] and len(attempts) == 1:
        status = "ok"
    elif final["ok"] and final["mode"] == "proxy":
        status = "warn"
    elif remote_direct:
        status = "fail"
    elif label in PROXY_ELIGIBLE_LABELS and len(attempts) == 1:
        status = "warn"
    else:
        status = "fail"

    return NetworkRow(
        location=location,  # type: ignore[typeddict-item]
        server=server,
        target_label=label,
        target_url=url,
        effective_mode=final["mode"] if final["ok"] else None,
        status=status,  # type: ignore[typeddict-item]
        http_code=final["http_code"],
        latency_ms=final["latency_ms"],
        speed_download_bps=final["speed_download_bps"],
        attempts=attempts,
        error=None if status in {"ok", "warn"} and final["ok"] else final["error"],
    )


def _remote_shell_command(url: str, proxy_url: str | None = None) -> str:
    command = build_curl_command(url)
    shell_command = " ".join(shlex.quote(part) for part in command)
    if proxy_url:
        proxy = shlex.quote(proxy_url)
        return f"ALL_PROXY={proxy} HTTPS_PROXY={proxy} {shell_command}"
    return shell_command


def _proxy_unavailable_attempt(url: str, error: str) -> CurlAttempt:
    return CurlAttempt(
        mode="proxy",
        target_url=url,
        proxy_url=None,
        exit_code=1,
        ok=False,
        status="fail",
        http_code=None,
        latency_ms=None,
        speed_download_bps=None,
        error=error,
    )


def _sanitize_proxy_error(error: str, local_proxy_url: str) -> str:
    text = error.replace(local_proxy_url, redact_proxy_url(local_proxy_url))
    return re.sub(r"(https?://)[^/\s:@]+:[^/\s@]+@", r"\1***:***@", text)


def _failure_rows(
    location: str,
    server: str | None,
    targets: Iterable[str],
    error: str,
) -> list[NetworkRow]:
    rows: list[NetworkRow] = []
    for url in _validated_targets(targets):
        label = target_label(url)
        attempt = CurlAttempt(
            mode="direct",
            target_url=url,
            proxy_url=None,
            exit_code=1,
            ok=False,
            status="fail",
            http_code=None,
            latency_ms=None,
            speed_download_bps=None,
            error=error,
        )
        rows.append(
            NetworkRow(
                location=location,  # type: ignore[typeddict-item]
                server=server,
                target_label=label,
                target_url=url,
                effective_mode=None,
                status="fail",
                http_code=None,
                latency_ms=None,
                speed_download_bps=None,
                attempts=[attempt],
                error=error,
            )
        )
    return rows


def _summarize_group(rows: list[NetworkRow]) -> NetworkGroupSummary:
    return NetworkGroupSummary(
        total=len(rows),
        passed=sum(row["status"] == "ok" for row in rows),
        warned=sum(row["status"] == "warn" for row in rows),
        failed=sum(row["status"] == "fail" for row in rows),
        needs_proxy=any(row["effective_mode"] == "proxy" for row in rows),
        proxy_used=sum(row["effective_mode"] == "proxy" for row in rows),
        proxy_failed=sum(
            row["status"] == "fail"
            and any(attempt["mode"] == "proxy" for attempt in row["attempts"])
            for row in rows
        ),
        failed_targets=[
            row["target_label"]
            for row in rows
            if row["status"] == "fail"
        ],
    )


def _severity_from_summary(summary: NetworkSummary) -> CheckSeverity:
    if summary["failed"]:
        return CheckSeverity.FAIL
    if summary["warned"]:
        return CheckSeverity.WARN
    return CheckSeverity.OK


def _warnings_from_rows(rows: list[NetworkRow]) -> list[str]:
    warnings: list[str] = []
    for row in rows:
        if row["status"] == "warn":
            scope = row["server"] or "local"
            warnings.append(
                f"{scope}/{row['target_label']} required proxy fallback"
            )
    return warnings


def _error_from_rows(rows: list[NetworkRow]) -> str | None:
    errors = [
        f"{row['server'] or 'local'}/{row['target_label']}: {row['error']}"
        for row in rows
        if row["status"] == "fail" and row["error"]
    ]
    return "; ".join(errors) if errors else None


def _message(severity: CheckSeverity, lang: str) -> str:
    if severity == CheckSeverity.FAIL:
        return "网络探测发现失败" if lang == "zh" else "Network probe failed"
    if severity == CheckSeverity.WARN:
        return "网络探测完成，存在告警" if lang == "zh" else "Network probe completed with warnings"
    return "网络探测完成" if lang == "zh" else "Network probe completed"


def _cli_failure(message: str, error: str) -> CheckResult:
    return CheckResult(
        ok=False,
        severity=CheckSeverity.FAIL,
        data={
            "rows": [],
            "summary": summarize_rows([]),
            "warnings": [],
            "metadata": {},
        },
        message=message,
        error=error,
    )

"""Implementation for `autoresearch check all`."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
from typing import Any, Callable

from workspace_core.config import ConfigError, from_path
from workspace_core.progress import emit_progress

from autoresearch.config import run_validate
from autoresearch.hw.probe import run_probe as run_hw_probe
from autoresearch.net.probe import run_probe as run_net_probe
from autoresearch.reach.tester import run_reach_test
from autoresearch.services.status import run_status
from autoresearch.stack.checker import run_stack_check

from .models import StepResult, ready_step, skipped_step, step_result, summarize_steps


DEFAULT_CONFIG_PATH = "config/config.yaml"
DEFAULT_REMOTE_PROXY_PORT = 17892
DEFAULT_STACK_LIBS = ("verl",)


def run_check_all(
    *,
    server: str | None = None,
    config: str | None = None,
    stack_libs: tuple[str, ...] | None = None,
    remote_proxy_port: int = DEFAULT_REMOTE_PROXY_PORT,
    lang: str = "zh",
) -> tuple[int, dict[str, Any]]:
    """Run M1 readiness checks and return ``(exit_code, payload)``."""
    cfg_path = config or DEFAULT_CONFIG_PATH
    libs = stack_libs or DEFAULT_STACK_LIBS
    emit_progress("orch.check.start", server=server, config=cfg_path)

    steps: list[StepResult] = []

    config_step = _run_step(
        "config",
        "customer-config",
        lambda: _capture_json_stdout(run_validate, config=cfg_path, lang=lang, as_json=True),
    )
    steps.append(config_step)
    if not config_step["ok"]:
        steps.extend(_skipped_after("配置校验失败，无法解析后续服务器。"))
        return _finish("check", steps, server, cfg_path)

    try:
        server_name = server or _first_server_name(cfg_path)
    except Exception as exc:
        steps.append(
            step_result(
                step_id="server",
                label="server-selection",
                exit_code=2,
                payload={"ok": False, "error": str(exc)},
            )
        )
        steps.extend(_skipped_after("服务器选择失败。"))
        return _finish("check", steps, server, cfg_path)

    steps.append(
        _run_step(
            "services",
            "local-services-health",
            lambda: _capture_json_stdout(run_status, as_json=True, lang=lang),
        )
    )
    steps.append(
        _run_step(
            "hw",
            "server-hardware-probe",
            lambda: _capture_json_stdout(
                run_hw_probe,
                server=server_name,
                all_servers=False,
                config=cfg_path,
                lang=lang,
            ),
        )
    )
    steps.append(
        _run_step(
            "net",
            "network-check",
            lambda: _capture_json_stdout(
                run_net_probe,
                server=server_name,
                local_only=False,
                config=cfg_path,
                remote_proxy_port=remote_proxy_port,
                lang=lang,
            ),
        )
    )
    steps.append(
        _run_step(
            "reach",
            "service-reachability",
            lambda: _capture_json_stdout(
                run_reach_test,
                server=server_name,
                config=cfg_path,
                lang=lang,
            ),
        )
    )
    steps.append(
        _run_step(
            "stack",
            "train-stack-health",
            lambda: _capture_json_stdout(
                run_stack_check,
                server=server_name,
                config=cfg_path,
                libs=libs,
                lang=lang,
            ),
        )
    )

    if any(step["status"] == "fail" for step in steps):
        reason = "前置 readiness check 存在失败，未进入 collect/report readiness。"
        steps.append(skipped_step("collect", "data-collection", reason))
        steps.append(skipped_step("report", "experiment-report", reason))
    else:
        steps.append(
            ready_step(
                "collect",
                "data-collection",
                "`run smoke` will execute the data collection step.",
            )
        )
        steps.append(
            ready_step(
                "report",
                "experiment-report",
                "`run smoke` will render a report from the collected run.",
            )
        )

    return _finish("check", steps, server_name, cfg_path)


def _run_step(
    step_id: str,
    label: str,
    fn: Callable[[], tuple[int, dict[str, Any]]],
) -> StepResult:
    emit_progress("orch.check.step.start", step=step_id)
    try:
        exit_code, payload = fn()
    except Exception as exc:
        exit_code, payload = 2, {"ok": False, "error": str(exc)}
    step = step_result(
        step_id=step_id,
        label=label,
        exit_code=exit_code,
        payload=payload,
    )
    emit_progress(
        "orch.check.step.result",
        level="error" if step["status"] == "fail" else "info",
        step=step_id,
        status=step["status"],
    )
    return step


def _capture_json_stdout(fn: Callable[..., int], *args: Any, **kwargs: Any) -> tuple[int, dict[str, Any]]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exit_code = fn(*args, **kwargs)
    text = buffer.getvalue().strip()
    if not text:
        return exit_code, {"ok": exit_code == 0}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {"ok": exit_code == 0, "stdout": text}
    return exit_code, payload


def _first_server_name(config_path: str | Path) -> str:
    cfg = from_path(config_path)
    if not cfg.servers:
        raise ConfigError("config.servers 为空，无法选择默认服务器")
    return cfg.servers[0].name


def _skipped_after(reason: str) -> list[StepResult]:
    return [
        skipped_step("services", "local-services-health", reason),
        skipped_step("hw", "server-hardware-probe", reason),
        skipped_step("net", "network-check", reason),
        skipped_step("reach", "service-reachability", reason),
        skipped_step("stack", "train-stack-health", reason),
        skipped_step("collect", "data-collection", reason),
        skipped_step("report", "experiment-report", reason),
    ]


def _finish(
    command: str,
    steps: list[StepResult],
    server: str | None,
    config: str,
) -> tuple[int, dict[str, Any]]:
    summary = summarize_steps(steps)
    ok = summary["failed"] == 0
    payload = {
        "ok": ok,
        "command": command,
        "server": server,
        "config": config,
        "failed_step": summary["failed_step"],
        "summary": summary,
        "steps": steps,
    }
    emit_progress(
        "orch.check.result",
        level="info" if ok else "error",
        ok=ok,
        failed_step=summary["failed_step"],
    )
    return (0 if ok else 1), payload

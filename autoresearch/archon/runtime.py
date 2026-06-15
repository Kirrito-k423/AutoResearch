"""Deterministic runtime helpers used by repo-local Archon workflows."""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from workspace_core.config import ConfigError, from_path


DEFAULT_CONFIG_PATH = "config/config.yaml"
DEFAULT_LIB = "verl"
DEFAULT_TIMEOUT = 60.0
DEFAULT_PUSHGATEWAY_URL = "http://127.0.0.1:17891"
DEFAULT_REMOTE_PROXY_PORT = 17890
DEFAULT_ARTIFACTS_DIR = ".archon/artifacts/local"


@dataclass(frozen=True)
class ArchonRuntimeEnv:
    """Environment values shared by all Archon adapter scripts."""

    config_path: str
    server: str
    lib: str
    timeout: float
    pushgateway_url: str
    run_id: str | None
    artifacts_dir: Path
    remote_proxy_port: int


def build_env() -> ArchonRuntimeEnv:
    """Resolve Archon environment variables into typed runtime settings."""
    config_path = os.environ.get("AR_CONFIG_PATH", DEFAULT_CONFIG_PATH)
    return ArchonRuntimeEnv(
        config_path=config_path,
        server=os.environ.get("AR_SERVER") or _first_server_name(config_path),
        lib=os.environ.get("AR_LIB", DEFAULT_LIB),
        timeout=_float_env("AR_TIMEOUT", DEFAULT_TIMEOUT),
        pushgateway_url=os.environ.get("AR_PUSHGATEWAY_URL", DEFAULT_PUSHGATEWAY_URL),
        run_id=os.environ.get("AR_RUN_ID") or None,
        artifacts_dir=_artifacts_dir(),
        remote_proxy_port=_int_env("AR_REMOTE_PROXY_PORT", DEFAULT_REMOTE_PROXY_PORT),
    )


def _first_server_name(config_path: str) -> str:
    cfg = from_path(config_path)
    if not cfg.servers:
        raise ConfigError("config.servers 为空，无法为 Archon workflow 选择默认服务器")
    return cfg.servers[0].name


def _float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} 必须是数字，收到: {raw}") from exc


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} 必须是整数，收到: {raw}") from exc


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _artifacts_dir() -> Path:
    path = Path(os.environ.get("ARTIFACTS_DIR", DEFAULT_ARTIFACTS_DIR)).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_artifact(name: str, payload: dict[str, Any], env: ArchonRuntimeEnv | None = None) -> Path:
    runtime_env = env or build_env()
    path = runtime_env.artifacts_dir / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_artifact(name: str, env: ArchonRuntimeEnv | None = None) -> dict[str, Any]:
    runtime_env = env or build_env()
    path = runtime_env.artifacts_dir / name
    return json.loads(path.read_text(encoding="utf-8"))


def _json_default(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def _capture_json_stdout(fn: Callable[..., int], *args: Any, **kwargs: Any) -> tuple[int, dict[str, Any]]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exit_code = fn(*args, **kwargs)
    text = buffer.getvalue().strip()
    if not text:
        return exit_code, {"ok": exit_code == 0, "stdout": ""}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {"ok": exit_code == 0, "stdout": text}
    return exit_code, payload


def _result(skill: str, exit_code: int, payload: dict[str, Any], env: ArchonRuntimeEnv) -> dict[str, Any]:
    return {
        "ok": exit_code == 0,
        "skill": skill,
        "exit_code": exit_code,
        "server": env.server,
        "config": env.config_path,
        "artifacts_dir": str(env.artifacts_dir),
        "payload": payload,
    }


def run_skill_01(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 01: customer config validation."""
    from autoresearch.config.validate import run_validate

    runtime_env = env or build_env()
    exit_code, payload = _capture_json_stdout(
        run_validate,
        config=runtime_env.config_path,
        lang="zh",
        as_json=True,
    )
    result = _result("ar-skill-01", exit_code, payload, runtime_env)
    _write_artifact("skill-01-result.json", result, runtime_env)
    return exit_code, result


def run_skill_02(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 02: local services start and health status."""
    from autoresearch.services.start import run_start
    from autoresearch.services.status import run_status

    runtime_env = env or build_env()
    start_exit = run_start(lang="zh")
    status_exit, status_payload = _capture_json_stdout(run_status, as_json=True, lang="zh")
    exit_code = 0 if start_exit == 0 and status_exit == 0 else 1
    payload = {
        "start_exit_code": start_exit,
        "status_exit_code": status_exit,
        "status": status_payload,
    }
    result = _result("ar-skill-02", exit_code, payload, runtime_env)
    _write_artifact("skill-02-result.json", result, runtime_env)
    return exit_code, result


def run_skill_03(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 03: remote hardware probe."""
    from autoresearch.hw.probe import run_probe

    runtime_env = env or build_env()
    exit_code, payload = _capture_json_stdout(
        run_probe,
        server=runtime_env.server,
        all_servers=False,
        config=runtime_env.config_path,
        lang="zh",
    )
    result = _result("ar-skill-03", exit_code, payload, runtime_env)
    _write_artifact("skill-03-result.json", result, runtime_env)
    return exit_code, result


def run_skill_04(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 04: local and remote network probe."""
    from autoresearch.net.probe import run_probe

    runtime_env = env or build_env()
    exit_code, payload = _capture_json_stdout(
        run_probe,
        server=runtime_env.server,
        local_only=False,
        config=runtime_env.config_path,
        remote_proxy_port=runtime_env.remote_proxy_port,
        lang="zh",
    )
    result = _result("ar-skill-04", exit_code, payload, runtime_env)
    _write_artifact("skill-04-result.json", result, runtime_env)
    return exit_code, result


def run_skill_05(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 05: remote reachability to local wandb and pushgateway."""
    from autoresearch.reach.tester import run_reach_test

    runtime_env = env or build_env()
    exit_code, payload = _capture_json_stdout(
        run_reach_test,
        server=runtime_env.server,
        config=runtime_env.config_path,
        lang="zh",
    )
    result = _result("ar-skill-05", exit_code, payload, runtime_env)
    _write_artifact("skill-05-result.json", result, runtime_env)
    return exit_code, result


def _stack_libs(env: ArchonRuntimeEnv) -> list[str]:
    raw = os.environ.get("AR_STACK_LIBS")
    if raw:
        libs = [item.strip() for item in raw.split(",") if item.strip()]
        if libs:
            return libs
    return ["verl", "veomni"]


def _stack_state_path(env: ArchonRuntimeEnv) -> Path:
    return env.artifacts_dir / "stack-state.json"


def setup_stack_state(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    runtime_env = env or build_env()
    state = {
        "libs": _stack_libs(runtime_env),
        "index": 0,
        "complete": False,
        "results": [],
    }
    _write_artifact("stack-state.json", state, runtime_env)
    return 0, _result("ar-skill-06-setup", 0, state, runtime_env)


def run_stack_step(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    from autoresearch.stack.checker import run_stack_check

    runtime_env = env or build_env()
    state = _read_artifact("stack-state.json", runtime_env)
    libs = list(state.get("libs") or [])
    index = int(state.get("index") or 0)
    if index >= len(libs):
        state["complete"] = True
        _write_artifact("stack-state.json", state, runtime_env)
        return 0, _result("ar-skill-06-step", 0, {"skipped": True, "state": state}, runtime_env)

    lib = str(libs[index])
    exit_code, payload = _capture_json_stdout(
        run_stack_check,
        server=runtime_env.server,
        config=runtime_env.config_path,
        libs=(lib,),
        lang="zh",
    )
    state.setdefault("results", []).append(
        {"lib": lib, "exit_code": exit_code, "ok": exit_code == 0, "payload": payload}
    )
    state["index"] = index + 1
    state["complete"] = state["index"] >= len(libs)
    _write_artifact("stack-state.json", state, runtime_env)
    step_payload = {"lib": lib, "exit_code": exit_code, "state": state}
    # The loop step exits 0 so Archon can continue to the next lib; the summary
    # node turns accumulated failures into the final non-zero status.
    return 0, _result("ar-skill-06-step", 0, step_payload, runtime_env)


def summarize_stack_state(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    runtime_env = env or build_env()
    state = _read_artifact("stack-state.json", runtime_env)
    failures = [item for item in state.get("results", []) if not item.get("ok")]
    exit_code = 0 if not failures and state.get("complete") else 1
    payload = {"ok": exit_code == 0, "failures": failures, "state": state}
    result = _result("ar-skill-06", exit_code, payload, runtime_env)
    _write_artifact("skill-06-result.json", result, runtime_env)
    return exit_code, result


def run_skill_06(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 06: stack check, sequential over configured libs."""
    runtime_env = env or build_env()
    setup_stack_state(runtime_env)
    while True:
        state = _read_artifact("stack-state.json", runtime_env)
        if state.get("complete"):
            break
        run_stack_step(runtime_env)
    return summarize_stack_state(runtime_env)


def _collect_state_path(env: ArchonRuntimeEnv) -> Path:
    return env.artifacts_dir / "collect-state.json"


def _collect_max_attempts() -> int:
    return max(1, _int_env("AR_COLLECT_MAX_ATTEMPTS", 2))


def setup_collect_state(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    runtime_env = env or build_env()
    state = {
        "attempt": 0,
        "max_attempts": _collect_max_attempts(),
        "done": False,
        "results": [],
    }
    _write_artifact("collect-state.json", state, runtime_env)
    return 0, _result("ar-skill-07-setup", 0, state, runtime_env)


def run_collect_step(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    from autoresearch.collect.cli import run_collect

    runtime_env = env or build_env()
    state = _read_artifact("collect-state.json", runtime_env)
    if state.get("done"):
        return 0, _result("ar-skill-07-step", 0, {"skipped": True, "state": state}, runtime_env)

    attempt = int(state.get("attempt") or 0) + 1
    exit_code, payload = run_collect(
        server=runtime_env.server,
        lib=runtime_env.lib,
        config=runtime_env.config_path,
        workdir=os.environ.get("AR_WORKDIR"),
        timeout=runtime_env.timeout,
        run_id=runtime_env.run_id,
        pushgateway_url=runtime_env.pushgateway_url,
    )
    attempt_result = {"attempt": attempt, "exit_code": exit_code, "ok": exit_code == 0, "payload": payload}
    state.setdefault("results", []).append(attempt_result)
    state["attempt"] = attempt
    state["done"] = exit_code == 0 or attempt >= int(state.get("max_attempts") or 1)
    _write_artifact("collect-state.json", state, runtime_env)
    _write_artifact("collect-result.json", {"ok": exit_code == 0, **payload}, runtime_env)
    # The loop step exits 0 so failures can be retried until max_attempts.
    return 0, _result("ar-skill-07-step", 0, {"attempt": attempt, "state": state}, runtime_env)


def summarize_collect_state(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    runtime_env = env or build_env()
    state = _read_artifact("collect-state.json", runtime_env)
    latest = (state.get("results") or [{}])[-1]
    raw_exit_code = latest.get("exit_code")
    exit_code = int(raw_exit_code) if raw_exit_code is not None else 1
    payload = {"ok": exit_code == 0, "latest": latest, "state": state}
    result = _result("ar-skill-07", exit_code, payload, runtime_env)
    _write_artifact("skill-07-result.json", result, runtime_env)
    return exit_code, result


def run_skill_07(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 07: collect data with bounded retry."""
    runtime_env = env or build_env()
    setup_collect_state(runtime_env)
    while True:
        state = _read_artifact("collect-state.json", runtime_env)
        if state.get("done"):
            break
        run_collect_step(runtime_env)
    return summarize_collect_state(runtime_env)


def _resolve_report_run_id(env: ArchonRuntimeEnv) -> str:
    if env.run_id:
        return env.run_id
    collect_path = env.artifacts_dir / "collect-result.json"
    if collect_path.exists():
        collect = json.loads(collect_path.read_text(encoding="utf-8"))
        run_id = collect.get("run_id") or collect.get("payload", {}).get("run_id")
        if run_id:
            return str(run_id)
    raise ValueError("缺少 run_id: 设置 AR_RUN_ID，或先运行 collect workflow 生成 collect-result.json")


def run_skill_08(env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    """Skill 08: render experiment report from a run id."""
    from autoresearch.report.cli import run_render

    runtime_env = env or build_env()
    run_id = _resolve_report_run_id(runtime_env)
    exit_code, payload = run_render(
        run_id=run_id,
        open_report=_bool_env("AR_OPEN_REPORT", False),
    )
    result = _result("ar-skill-08", exit_code, payload, runtime_env)
    _write_artifact("report-result.json", result, runtime_env)
    return exit_code, result


def run_by_skill(skill: str, env: ArchonRuntimeEnv | None = None) -> tuple[int, dict[str, Any]]:
    runtime_env = env or build_env()
    mode = os.environ.get("AR_ARCHON_MODE", "").strip().lower()
    if skill == "01":
        return run_skill_01(runtime_env)
    if skill == "02":
        return run_skill_02(runtime_env)
    if skill == "03":
        return run_skill_03(runtime_env)
    if skill == "04":
        return run_skill_04(runtime_env)
    if skill == "05":
        return run_skill_05(runtime_env)
    if skill == "06":
        if mode == "stack-setup":
            return setup_stack_state(runtime_env)
        if mode == "stack-step":
            return run_stack_step(runtime_env)
        if mode == "stack-summary":
            return summarize_stack_state(runtime_env)
        return run_skill_06(runtime_env)
    if skill == "07":
        if mode == "collect-setup":
            return setup_collect_state(runtime_env)
        if mode == "collect-step":
            return run_collect_step(runtime_env)
        if mode == "collect-summary":
            return summarize_collect_state(runtime_env)
        return run_skill_07(runtime_env)
    if skill == "08":
        return run_skill_08(runtime_env)
    raise ValueError(f"unknown Archon skill id: {skill}")


def main(skill: str) -> int:
    try:
        exit_code, payload = run_by_skill(skill)
    except Exception as exc:
        exit_code = 1
        payload = {"ok": False, "skill": f"ar-skill-{skill}", "error": str(exc)}
    print(json.dumps(payload, ensure_ascii=False, default=_json_default))
    return exit_code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m autoresearch.archon.runtime <skill-id>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))

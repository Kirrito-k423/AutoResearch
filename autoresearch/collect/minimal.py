"""autoresearch.collect.minimal — minimal-runner 编排 (D-44, Phase 08-01).

`collect_minimal(server, lib, ...)` 读 config → 找 spec → 派发到对应 runner
(verl → verl-workspace-adapter.verl.minimal_runner,
 veomni → verl-workspace-adapter.veomni.minimal_runner).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from workspace_core.config import ConfigError, ServerSpec, from_path


# === Lib dispatch (D-44: verl / veomni 对称) ===

_LIB_TO_RUNNER = {
    "verl": "verl_workspace_adapter.verl.minimal_runner",
    "veomni": "verl_workspace_adapter.veomni.minimal_runner",
}


def _resolve_spec(server_name: str, config_path: str | Path | None) -> ServerSpec:
    cfg = from_path(str(config_path) if config_path else None)
    for s in cfg.servers:
        if s.name == server_name:
            return s
    raise ConfigError(f"config 中找不到 server={server_name}; 现有: {[s.name for s in cfg.servers]}")


def _resolve_workdir(spec: ServerSpec, workdir_override: str | None) -> str:
    """D-46 workdir 字段; 08-03 才加 schema, 这里先 getattr 兜底 ('/root' 缺省).

    override 是空字符串也 fall back (None 跟 "" 都视为未指定).
    """
    if workdir_override:
        return workdir_override
    return getattr(spec, "workdir", "/root") or "/root"


def collect_minimal(
    server: str,
    lib: str = "verl",
    config_path: str | Path | None = None,
    workdir_override: str | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """跑一次 1-step 干跑, 返回 MinimalResult dict (D-44).

    Args:
        server: config 中服务器名 (e.g. "A2-AK-225")
        lib: 库名, "verl" / "veomni" (D-43 决策: 不支持其他)
        config_path: config yaml 路径, 缺省 None 走 from_path 兜底
        workdir_override: 覆盖 spec.workdir (测试用)
        timeout: SSH exec timeout, 默认 30s (D-41)

    Returns:
        MinimalResult dict, 含 lib / sum_value / npu_count / elapsed_ms / exit_code / stdout / stderr / error
    """
    if lib not in _LIB_TO_RUNNER:
        raise ValueError(
            f"lib={lib!r} 不支持; 仅支持 {list(_LIB_TO_RUNNER.keys())} (D-43 决策)"
        )

    spec = _resolve_spec(server, config_path)
    workdir = _resolve_workdir(spec, workdir_override)
    conda_env = getattr(spec, "conda_env", "") or ""

    # 动态 import runner (verl / veomni), 避免 hard dep
    import importlib
    module_path = _LIB_TO_RUNNER[lib]
    runner = importlib.import_module(module_path)
    return runner.run_minimal(
        spec=spec, conda_env=conda_env, workdir=workdir, lib=lib, timeout=timeout,
    )

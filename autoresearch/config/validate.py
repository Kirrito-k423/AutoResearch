"""autoresearch config validate — 校验 config/config.yaml (CFG-VAL-01..02).

设计 (D-04/D-07):
- 复用 workspace_core.config.from_path() (Phase 2 沉淀)
- 中文错误已有 (from_path 内部 _format_validation_error)
- 成功: 打印 '✅ 校验通过' + 摘要
- 失败: 抛 ConfigError, 中文含字段路径 + 原因 + 期望
- --json 返 JSON {ok, summary: {...}}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click

from workspace_core.config import from_path, ConfigError
from ._common import resolve_config_path


def _summarize(cfg) -> dict[str, Any]:
    """从 Config 对象抽简短摘要 (不打印完整配置 — 留 show)."""
    return {
        "version": cfg.version,
        "servers_count": len(cfg.servers),
        "servers": [s.name for s in cfg.servers],
        "network_enabled": cfg.network.enabled,
        "network_targets_count": len(cfg.network.targets),
        "log_level": cfg.log.level,
        "wandb_enabled": cfg.wandb.enabled,
        "wandb_project": cfg.wandb.project,
    }


def run_validate(
    *, config: str | None = None, lang: str = "zh", as_json: bool = False
) -> int:
    """Validate 子命令主入口.

    Returns:
        exit code: 0 = pass, 1 = fail (校验错误)
    """
    target = resolve_config_path(config)
    try:
        cfg = from_path(target)
    except ConfigError as e:
        if as_json:
            payload = {"ok": False, "path": str(target), "error": str(e)}
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            msg = (
                f"❌ 校验失败: {target}"
                if lang == "zh"
                else f"❌ Validation failed: {target}"
            )
            print(msg, file=sys.stderr)
            print(str(e), file=sys.stderr)
        return 1

    summary = _summarize(cfg)
    if as_json:
        payload = {"ok": True, "path": str(target), "summary": summary}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if lang == "zh":
            print(f"✅ {target} 校验通过")
            print(f"   version: {summary['version']}")
            print(
                f"   servers: {summary['servers_count']} "
                f"({', '.join(summary['servers']) or '无'})"
            )
            print(
                f"   network: enabled={summary['network_enabled']}, "
                f"{summary['network_targets_count']} targets"
            )
            print(f"   log: level={summary['log_level']}")
            print(
                f"   wandb: enabled={summary['wandb_enabled']}, "
                f"project={summary['wandb_project']}"
            )
        else:
            print(f"✅ {target} validated")
            print(f"   version: {summary['version']}")
            print(f"   servers: {summary['servers_count']}")
            print(f"   network: enabled={summary['network_enabled']}")
    return 0

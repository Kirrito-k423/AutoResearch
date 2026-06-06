"""~/.autoresearch/ 固定目录 (D-17, CORE-LAYOUT-01).

惰性创建: 调 ensure_* 才建.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Final


# === 根目录常量 ===
ROOT_DIR: Final[Path] = Path.home() / ".autoresearch"
RUNS_DIR: Final[Path] = ROOT_DIR / "runs"
LOGS_DIR: Final[Path] = ROOT_DIR / "logs"
CACHE_DIR: Final[Path] = ROOT_DIR / "cache"
SSH_KEYS_DIR: Final[Path] = ROOT_DIR / "ssh_keys"


# === run-id 校验 ===
# 允许: 日期前缀 + 自由名 (e.g. 2026-06-06-smoke-001, my-exp-v2)
DEFAULT_RUN_ID_RE: Final[re.Pattern] = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_\-\.]{0,127}$"
)


class RunIDError(ValueError):
    """run-id 非法 (含路径分隔符 / 太长 / 起始字符异常)."""


def _validate_run_id(run_id: str) -> str:
    if not isinstance(run_id, str) or not DEFAULT_RUN_ID_RE.match(run_id):
        raise RunIDError(
            f"run-id 非法 '{run_id}'; 须匹配 {DEFAULT_RUN_ID_RE.pattern}"
        )
    return run_id


@dataclass(frozen=True)
class RunPaths:
    """单次 run 的所有路径, 一次解析免得后面散落 Path 拼接."""

    run_id: str
    root: Path          # ~/.autoresearch/runs/<id>/
    logs: Path          # <root>/logs/
    wandb: Path         # <root>/wandb/
    prom: Path          # <root>/prom/
    manifest: Path      # <root>/manifest.json


def run_dir(run_id: str, *, create: bool = True) -> RunPaths:
    """获取 run 目录结构. create=True 时自动建 logs/wandb/prom."""
    rid = _validate_run_id(run_id)
    root = RUNS_DIR / rid
    paths = RunPaths(
        run_id=rid,
        root=root,
        logs=root / "logs",
        wandb=root / "wandb",
        prom=root / "prom",
        manifest=root / "manifest.json",
    )
    if create:
        for p in (paths.logs, paths.wandb, paths.prom):
            p.mkdir(parents=True, exist_ok=True)
    return paths


def ensure_run_dir(run_id: str) -> RunPaths:
    """ensure + create. run-id 冲突时硬失败 (D-17)."""
    rid = _validate_run_id(run_id)
    target = RUNS_DIR / rid
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(
            f"run-id '{rid}' 目录已存在且非空 ({target}); "
            f"换 --run-id 或先删. 已存在: {list(target.iterdir())[:3]}"
        )
    return run_dir(rid, create=True)


def ensure_root() -> Path:
    """确保 ~/.autoresearch/{runs,logs,cache,ssh_keys}/ 4 个目录都建."""
    for d in (RUNS_DIR, LOGS_DIR, CACHE_DIR, SSH_KEYS_DIR):
        d.mkdir(parents=True, exist_ok=True)
    return ROOT_DIR


def clean_run(run_id: str) -> None:
    """强制删一个 run 目录 (D-17 cleanup helper, 不在 M1 强制要求)."""
    rid = _validate_run_id(run_id)
    target = RUNS_DIR / rid
    if target.exists():
        shutil.rmtree(target)

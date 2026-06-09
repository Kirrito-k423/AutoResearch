"""workspace-core.layout — ~/.autoresearch/ 固定目录约定 (D-17, CORE-LAYOUT-01).

8 skill 走 ensure_run_dir / run_dir 拿本次 run 的所有路径, 不自己拼接.
"""
from .paths import (
    ROOT_DIR,
    RUNS_DIR,
    LOGS_DIR,
    CACHE_DIR,
    SSH_KEYS_DIR,
    TUNNELS_DIR,
    run_dir,
    ensure_run_dir,
    ensure_root,
    clean_run,
    RunPaths,
    RunIDError,
    DEFAULT_RUN_ID_RE,
)

__all__ = [
    "ROOT_DIR",
    "RUNS_DIR",
    "LOGS_DIR",
    "CACHE_DIR",
    "SSH_KEYS_DIR",
    "TUNNELS_DIR",
    "run_dir",
    "ensure_run_dir",
    "ensure_root",
    "clean_run",
    "RunPaths",
    "RunIDError",
    "DEFAULT_RUN_ID_RE",
]

"""autoresearch services stop — 串行调 3 个 docker compose down。

实现 SVC-CHK-STOP-01。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSE_DIR = ROOT / "services"

# 与 start.py 对称；Archon 仍由 `archon serve` 管理
COMPOSE_SERVICES = ["wandb", "prometheus", "grafana"]


def _check_docker() -> str | None:
    """检查 docker CLI 是否可用。"""
    if shutil.which("docker") is None:
        return "错误：找不到 `docker` 命令。"
    return None


def _run_compose_down(svc: str, lang: str) -> bool:
    """对单个服务执行 `docker compose -f <path> down`。"""
    compose_file = COMPOSE_DIR / svc / "compose.yml"
    if not compose_file.exists():
        msg = (
            f"错误：找不到 compose 文件 {compose_file}"
            if lang == "zh"
            else f"Error: compose file not found: {compose_file}"
        )
        print(msg, file=sys.stderr)
        return False

    info = f"[{svc}] docker compose -f {compose_file} down"
    print(info, file=sys.stderr)

    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "down"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("错误：找不到 docker 命令。", file=sys.stderr)
        return False

    if result.returncode != 0:
        print(f"[{svc}] FAILED (exit={result.returncode}):", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False

    print(f"[{svc}] OK", file=sys.stderr)
    return True


def run_stop(*, lang: str) -> int:
    """Stop 子命令主入口。

    Returns exit code: 0 = all stopped, 1 = any failed, 2 = docker missing.
    """
    err = _check_docker()
    if err is not None:
        print(err, file=sys.stderr)
        return 2

    all_ok = True
    for svc in COMPOSE_SERVICES:
        if not _run_compose_down(svc, lang):
            all_ok = False
            break

    if lang == "zh":
        print(
            "Archon：由 `archon serve` 自行管理；autoresearch services stop 不影响 Archon。",
            file=sys.stderr,
        )
    else:
        print(
            "Archon: managed by `archon serve`; autoresearch services stop does not affect it.",
            file=sys.stderr,
        )

    return 0 if all_ok else 1

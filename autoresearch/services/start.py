"""autoresearch services start — 串行调 3 个 docker compose up。

实现 SVC-CHK-START-01 (调 docker compose up) + SVC-CHK-DEPS-01 (缺 docker 可读错误)。

D-05/D-05c: Archon 不在我们的 compose 里；输出明确提示用户用 `archon serve`。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSE_DIR = ROOT / "services"

# Archon 由 `archon serve` 管理；不列在这里
COMPOSE_SERVICES = ["wandb", "prometheus", "grafana"]


def _check_docker() -> str | None:
    """检查 docker CLI 是否可用；返回错误消息或 None。"""
    if shutil.which("docker") is None:
        return "错误：找不到 `docker` 命令。请先安装 Docker Desktop（macOS）。"
    return None


def _run_compose_up(svc: str, lang: str) -> bool:
    """对单个服务执行 `docker compose -f <path> up -d`；失败返回 False。"""
    compose_file = COMPOSE_DIR / svc / "compose.yml"
    if not compose_file.exists():
        msg = (
            f"错误：找不到 compose 文件 {compose_file}"
            if lang == "zh"
            else f"Error: compose file not found: {compose_file}"
        )
        print(msg, file=sys.stderr)
        return False

    info = f"[{svc}] docker compose -f {compose_file} up -d"
    print(info, file=sys.stderr)

    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
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


def run_start(*, lang: str) -> int:
    """Start 子命令主入口。

    Returns exit code: 0 = all started, 1 = any failed, 2 = docker missing.
    """
    err = _check_docker()
    if err is not None:
        print(err, file=sys.stderr)
        return 2

    all_ok = True
    for svc in COMPOSE_SERVICES:
        if not _run_compose_up(svc, lang):
            all_ok = False
            break  # 串行：失败则停，避免错误叠加

    # D-05c: Archon 不在范围
    if lang == "zh":
        print(
            "Archon：由 `archon serve` 自行管理，不在 autoresearch 范围（D-05）。",
            file=sys.stderr,
        )
    else:
        print(
            "Archon: managed by `archon serve`, not by autoresearch (D-05).",
            file=sys.stderr,
        )

    return 0 if all_ok else 1

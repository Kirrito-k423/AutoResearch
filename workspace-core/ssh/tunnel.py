"""反向代理封装 (D-02): 系统 ssh -R + ServerAliveInterval + 进程由 Popen 管."""
from __future__ import annotations

import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .exceptions import TunnelError
from .host import HostSpec


@dataclass
class ReverseTunnel:
    """ssh -R 反向代理的运行实例."""

    proc: subprocess.Popen
    pid: int
    host_alias: str
    remote_port: int
    local_port: int
    log_path: Path

    def stop(self, timeout_s: float = 5.0) -> None:
        """优雅停止 tunnel 进程 (SIGTERM -> SIGKILL)."""
        try:
            self.proc.wait(timeout_s)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            try:
                self.proc.wait(timeout_s)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def open_reverse_tunnel(
    host: HostSpec,
    *,
    remote_port: int,
    local_port: int,
    identity_file: Path | None = None,
    log_dir: Path | None = None,
) -> ReverseTunnel:
    """起一条 ssh -R 反向代理, 返回 ReverseTunnel 实例.

    命令模板:
        ssh -N -R <remote_port>:localhost:<local_port> \\
           -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \\
           -o ExitOnForwardFailure=yes \\
           -o ControlMaster=no -o ControlPath=none \\
           [-i <identity_file>] \\
           <user>@<host>
    """
    if log_dir is None:
        log_dir = Path.home() / ".autoresearch" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"tunnel-{host.alias or host.host}.log"

    cmd = [
        "ssh", "-N",
        "-R", f"{remote_port}:localhost:{local_port}",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3",
        "-o", "ExitOnForwardFailure=yes",
        "-o", "ControlMaster=no",
        "-o", "ControlPath=none",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", f"UserKnownHostsFile={Path.home() / '.ssh' / 'known_hosts'}",
    ]
    if identity_file:
        cmd += ["-i", str(identity_file)]
    cmd += [f"{host.user}@{host.host}"]

    try:
        log_file = open(log_path, "a")
        proc = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,  # 独立进程组, 避免 SIGINT 串到子进程
        )
    except FileNotFoundError:
        raise TunnelError("找不到 ssh 命令; 请确认 PATH 含 /usr/bin/ssh")
    except OSError as e:
        raise TunnelError(f"无法启动 ssh tunnel: {e}") from e

    # 短延迟看是否立即死 (ExitOnForwardFailure=yes 时, 失败立即退出)
    time.sleep(0.5)
    if proc.poll() is not None:
        try:
            log_tail = log_path.read_text(errors="ignore")[-500:]
        except OSError:
            log_tail = "(log 无法读取)"
        raise TunnelError(
            f"ssh tunnel 启动后立即退出 (rc={proc.returncode}); log tail:\n{log_tail}"
        )

    return ReverseTunnel(
        proc=proc,
        pid=proc.pid,
        host_alias=host.alias or host.host,
        remote_port=remote_port,
        local_port=local_port,
        log_path=log_path,
    )

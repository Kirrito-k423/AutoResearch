"""autoresearch ping — SSH 端到端冒烟 (D-18, D-19, D-20).

M1 阶段 02 范围; phase 11 + 12 起会被更深 check 取代.

设计:
- 无 --server: 走 paramiko dummy server, 验证 SSH 代码路径 (无外部依赖)
- 有 --server: 走真 SSH + 反向代理通断
- 成功: stdout 唯一 JSON {ssh, reverse_tunnel, latency_ms, mode, ...}
- 失败: 中文错误到 stderr, exit 1 (D-20 硬失败) / 2 (配置错)
"""
from __future__ import annotations

import json
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

import click
import paramiko

from workspace_core.ssh.client import SSHClient
from workspace_core.ssh.exceptions import SSHError
from workspace_core.ssh.host import HostSpec, resolve_host
from workspace_core.ssh.tunnel import ReverseTunnel, open_reverse_tunnel
from workspace_core.config import from_path, ConfigError
from workspace_core.progress import emit_progress


# === paramiko dummy server (D-18 / D-04c) ===

def _free_port() -> int:
    """找 OS 分配的空闲端口."""
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
    finally:
        s.close()


class _DummySSHServer:
    """paramiko 自带 server, 接受任何密码/key, 跑 echo 'ok' 命令.

    用法::

        with _DummySSHServer() as (host, stop):
            with SSHClient(host) as c:
                c.exec("echo ok")  # → 返回 "ok\\n", exit_code=0

    关键设计 (paramiko 3.x):
    - `check_channel_exec_request` 钩子**不能**同步 close channel; 那样 client
      端的 `chan.exec_command` 会 raise "Channel closed" 因为它还在等响应.
    - 正确做法: 启一个 daemon thread 在 channel 上 sendall + send_exit_status,
      主钩子 return True. client 读完自动 close (eof).
    """

    def __init__(self) -> None:
        self.host_key = paramiko.RSAKey.generate(2048)
        self.port = _free_port()
        self._server_sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._transport: paramiko.Transport | None = None
        self._stop = False

    def __enter__(self) -> tuple[HostSpec, "callable"]:
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind(("127.0.0.1", self.port))
        self._server_sock.listen(1)
        self._server_sock.settimeout(10.0)

        def serve() -> None:
            class _Srv(paramiko.ServerInterface):
                def check_auth_password(self, username, password):
                    return paramiko.AUTH_SUCCESSFUL

                def check_auth_publickey(self, username, key):
                    return paramiko.AUTH_SUCCESSFUL

                def check_channel_request(self, kind, chanid):
                    # 允许 session (PTY, exec, shell, subsystem)
                    if kind == "session":
                        return paramiko.OPEN_SUCCEEDED
                    return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

                def check_channel_exec_request(self, channel, command):
                    # 启后台 thread 处理 channel, 不在主钩子里 close
                    cmd = (
                        command.decode("utf-8", errors="replace")
                        if isinstance(command, bytes)
                        else command
                    )

                    def handle() -> None:
                        try:
                            if "echo ok" in cmd:
                                channel.sendall(b"ok\n")
                                channel.send_exit_status(0)
                                time.sleep(0.05)
                                channel.shutdown_read()
                                channel.shutdown_write()
                            else:
                                channel.sendall(f"unknown: {cmd}\n".encode())
                                channel.send_exit_status(1)
                                time.sleep(0.05)
                                channel.shutdown_read()
                                channel.shutdown_write()
                            # 不 close: client 读完自动 EOF
                        except Exception:
                            pass

                    threading.Thread(target=handle, daemon=True).start()
                    return True

            try:
                conn, _ = self._server_sock.accept()
                if self._stop:
                    conn.close()
                    return
                self._transport = paramiko.Transport(conn)
                self._transport.add_server_key(self.host_key)
                self._transport.start_server(server=_Srv())
                # 让 server 保持运行; transport 在 stop() 时被关
                while not self._stop:
                    time.sleep(0.1)
            except Exception:
                pass  # dummy server 容忍异常退出

        self._thread = threading.Thread(target=serve, daemon=True)
        self._thread.start()
        time.sleep(0.3)  # 让 server socket 处于 accept 状态

        host_spec = HostSpec(
            alias="dummy",
            host="127.0.0.1",
            port=self.port,
            user="dummy",
            identity_file=None,
        )

        def stop() -> None:
            self._stop = True
            try:
                if self._transport is not None:
                    self._transport.close()
            except Exception:
                pass
            try:
                if self._server_sock is not None:
                    self._server_sock.close()
            except Exception:
                pass

        return host_spec, stop

    def __exit__(self, *exc: Any) -> None:
        self._stop = True
        if self._transport is not None:
            try:
                self._transport.close()
            except Exception:
                pass
        if self._server_sock is not None:
            try:
                self._server_sock.close()
            except Exception:
                pass


# === helper: 把 server 规格组装成 HostSpec (合并 config.identity_file) ===

def _resolve_server_host(server_name: str) -> HostSpec:
    """从 config 找 server, 组装 HostSpec (identity_file 优先用 config 里的)."""
    cfg = from_path()
    server = next((s for s in cfg.servers if s.name == server_name), None)
    if server is None:
        raise click.UsageError(
            f"config.servers 中找不到 '{server_name}'; "
            f"当前已配: {[s.name for s in cfg.servers]}"
        )
    target = f"{server.user}@{server.host}:{server.port}"
    host = resolve_host(target)
    if server.identity_file:
        host = HostSpec(
            alias=host.alias,
            host=host.host,
            port=host.port,
            user=host.user,
            identity_file=Path(server.identity_file),
        )
    return host


# === 两条 ping 路径 ===

def _ping_via_dummy() -> dict[str, Any]:
    """D-18: paramiko dummy server 验证 SSH 代码路径."""
    with _DummySSHServer() as (host, _stop):
        t0 = time.perf_counter()
        emit_progress("ping.ssh.connect", host=host.host, port=host.port, mode="dummy")
        with SSHClient(host) as c:
            c.connect()  # dummy 接受任何密码/key
            exit_code, out, err = c.exec("echo ok", timeout=5.0)
        ssh_ok = exit_code == 0 and "ok" in out
        emit_progress(
            "ping.ssh.echo",
            ssh=ssh_ok,
            exit_code=exit_code,
            stdout=out.strip()[:80],
        )
        # dummy server 不能验证反向代理 (ssh -R 走外部 ssh, dummy 仅本地)
        emit_progress(
            "ping.tunnel.skipped",
            level="warn",
            reason="dummy server 不支持反向代理端到端",
        )
        latency_ms = int((time.perf_counter() - t0) * 1000)
    return {
        "ssh": ssh_ok,
        "reverse_tunnel": None,  # None = skipped
        "latency_ms": latency_ms,
        "mode": "dummy",
    }


def _ping_via_real_server(server_name: str) -> dict[str, Any]:
    """D-19: 真 server 走 SSH + 反向代理通断."""
    host = _resolve_server_host(server_name)
    tunnel: ReverseTunnel | None = None
    t0 = time.perf_counter()
    try:
        with SSHClient(host) as c:
            emit_progress(
                "ping.ssh.connect", host=host.host, port=host.port, mode="real"
            )
            c.connect()
            exit_code, out, err = c.exec("echo ok", timeout=10.0)
            ssh_ok = exit_code == 0 and "ok" in out
            emit_progress(
                "ping.ssh.echo",
                ssh=ssh_ok,
                exit_code=exit_code,
                stdout=out.strip()[:80],
            )

            # 反向代理: remote 8080 → local 8080
            emit_progress("ping.tunnel.open", remote_port=8080, local_port=8080)
            tunnel = open_reverse_tunnel(
                host, remote_port=8080, local_port=8080
            )
            time.sleep(1.0)  # 让 ssh -R 完全建立
            rt_ok = True  # 起得来就算通 (D-19: 不假设远端有 web server)
            emit_progress("ping.tunnel.ok", remote_port=8080, local_port=8080)
    finally:
        if tunnel is not None:
            try:
                tunnel.stop()
                emit_progress("ping.tunnel.stopped", remote_port=tunnel.remote_port)
            except Exception:
                pass

    latency_ms = int((time.perf_counter() - t0) * 1000)
    return {
        "ssh": ssh_ok,
        "reverse_tunnel": rt_ok,
        "latency_ms": latency_ms,
        "mode": "real",
        "server": server_name,
    }


# === 主入口 ===

def run_ping(*, server: str | None, lang: str) -> int:
    """autoresearch ping 主入口.

    Args:
        server: 可选, server alias 走真 SSH; 不传走 dummy
        lang: zh/en (与 phase 1 D-04 一致)

    Returns:
        exit code: 0 = ok, 1 = any check fail, 2 = config error
    """
    try:
        if server is None:
            result = _ping_via_dummy()
        else:
            result = _ping_via_real_server(server)
    except ConfigError as e:
        msg = f"配置错误: {e}" if lang == "zh" else f"Config error: {e}"
        print(msg, file=sys.stderr)
        return 2
    except click.UsageError as e:
        msg = str(e)
        print(msg, file=sys.stderr)
        return 2
    except SSHError as e:
        msg = f"SSH 错误: {e}" if lang == "zh" else f"SSH error: {e}"
        print(msg, file=sys.stderr)
        return 1
    except Exception as e:
        msg = f"未知错误: {e}" if lang == "zh" else f"Unknown error: {e}"
        print(msg, file=sys.stderr)
        return 1

    # D-04e: stdout 唯一 JSON 对象
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 成功判定: ssh 必须 True; reverse_tunnel True 或 None (skipped) 算通过
    ok = result["ssh"] and (result["reverse_tunnel"] is not False)
    return 0 if ok else 1

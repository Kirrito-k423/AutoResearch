"""SSHClient 抽象接口 (D-01 抹平 paramiko) + Bootstrap 编排 (D-03)."""
from __future__ import annotations

import os
import time

import paramiko

from .exceptions import AuthError, CommandTimeoutError, ConnectError, SSHError
from .host import HostSpec, resolve_host
from . import keys as ssh_keys


DEFAULT_CONNECT_TIMEOUT_S = 5.0
DEFAULT_CMD_TIMEOUT_S = 30.0
DEFAULT_RETRIES = 3
BACKOFF_BASE_S = 1.0


class SSHClient:
    """paramiko 抹平抽象 (D-01).

    8 skill 只用本接口, 不直接 import paramiko.
    """

    def __init__(
        self,
        host: HostSpec,
        *,
        bootstrap_password: str | None = None,
        force_password: bool = False,
    ) -> None:
        """force_password: bootstrap 阶段强制走 password, 不试 key.

        True 时 connect 临时把 look_for_keys/allow_agent 关掉,
        强制 paramiko 只用 password 认证 (跳过 key 试错).
        完成后第二次 connect() 不传此参, 走正常 key 认证.
        """
        self.host = host
        self._configured_password = bootstrap_password
        self._force_password = force_password
        self._client: paramiko.SSHClient | None = None

    # ===== 登录 / 注销 =====

    def connect(
        self,
        *,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT_S,
        retries: int = DEFAULT_RETRIES,
    ) -> None:
        """连接 + 认证. 支持 3 阶段凭据解析 (D-03):
        1. ssh-agent (key, 系统自动尝试 allow_agent=True)
        2. IdentityFile (key) — 从 ssh_config 或显式传
        3. password (env SSH_PASSWORD_<ALIAS>) — 仅 bootstrap 用
        """
        if self._client is not None:
            return  # 幂等

        bootstrap_password = self._bootstrap_password()

        last_err: Exception | None = None
        for attempt in range(retries + 1):
            if attempt > 0:
                time.sleep(BACKOFF_BASE_S * (2 ** (attempt - 1)))
            try:
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                # 缺 host key 时警告 (CI / 临时 server 常见)
                client.set_missing_host_key_policy(paramiko.WarningPolicy)

                connect_kwargs: dict = {
                    "hostname": self.host.host,
                    "port": self.host.port,
                    "username": self.host.user,
                    "timeout": connect_timeout,
                    "allow_agent": not self._force_password,
                    "look_for_keys": not self._force_password,
                }
                if self.host.identity_file:
                    connect_kwargs["key_filename"] = str(self.host.identity_file)

                if bootstrap_password:
                    connect_kwargs["password"] = bootstrap_password

                client.connect(**connect_kwargs)
                self._client = client
                return
            except paramiko.AuthenticationException as e:
                # Auth 失败 = 立刻报错, 不重试
                raise AuthError(
                    f"认证失败 host={self.host.host}:{self.host.port} user={self.host.user}; "
                    f"如需密码引导, 设置 env SSH_PASSWORD_{self._alias_key()}"
                ) from e
            except (paramiko.SSHException, OSError) as e:
                last_err = ConnectError(
                    f"连接失败 host={self.host.host}:{self.host.port} "
                    f"(attempt={attempt + 1}/{retries + 1}): {e}"
                )

        raise last_err or ConnectError(
            f"连接失败 host={self.host.host}:{self.host.port}"
        )

    def _alias_key(self) -> str:
        """env var 名: 用 alias.upper() 或 user@host."""
        if self.host.alias:
            return self.host.alias.upper()
        return f"{self.host.user}@{self.host.host}".upper().replace(".", "_").replace("-", "_")

    def _bootstrap_password(self) -> str | None:
        """优先使用配置已解析的密码，否则读兼容环境变量."""
        return self._configured_password or os.environ.get(
            f"SSH_PASSWORD_{self._alias_key()}"
        )

    def close(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

    def __enter__(self) -> "SSHClient":
        self.connect()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ===== 命令执行 =====

    def exec(
        self,
        command: str,
        *,
        timeout: float = DEFAULT_CMD_TIMEOUT_S,
    ) -> tuple[int, str, str]:
        """执行命令, 返回 (exit_code, stdout, stderr)."""
        if self._client is None:
            raise SSHError(f"未连接; 先调 connect() — host={self.host.host}")
        _, stdout, _ = self._client.exec_command(command, timeout=timeout)
        return self._consume_exec_output(
            command=command,
            stdout_stream=stdout,
            timeout=timeout,
        )

    def exec_until_marker(
        self,
        command: str,
        *,
        marker: str,
        timeout: float = DEFAULT_CMD_TIMEOUT_S,
        grace_period: float = 0.2,
    ) -> tuple[int, str, str]:
        """执行命令; 一旦 stdout/stderr 出现 marker 就主动收口 channel.

        适用于远端已产出最终结果, 但 SSH 会话回收可能继续悬挂的场景.
        返回值保持与 exec 一致; 若因 marker 提前结束, exit_code 固定为 0.
        """
        if self._client is None:
            raise SSHError(f"未连接; 先调 connect() — host={self.host.host}")
        _, stdout, _ = self._client.exec_command(command, timeout=timeout)
        return self._consume_exec_output(
            command=command,
            stdout_stream=stdout,
            timeout=timeout,
            marker=marker,
            grace_period=grace_period,
        )

    def _consume_exec_output(
        self,
        *,
        command: str,
        stdout_stream,
        timeout: float,
        marker: str | None = None,
        grace_period: float = 0.0,
    ) -> tuple[int, str, str]:
        channel = stdout_stream.channel
        deadline = time.monotonic() + timeout
        stdout_bytes = bytearray()
        stderr_bytes = bytearray()
        marker_seen_at: float | None = None
        while True:
            while channel.recv_ready():
                stdout_bytes.extend(channel.recv(32768))
            while channel.recv_stderr_ready():
                stderr_bytes.extend(channel.recv_stderr(32768))
            if marker and marker_seen_at is None:
                marker_bytes = marker.encode("utf-8")
                if marker_bytes in stdout_bytes or marker_bytes in stderr_bytes:
                    marker_seen_at = time.monotonic()
            if marker_seen_at is not None and time.monotonic() - marker_seen_at >= grace_period:
                channel.close()
                return (
                    0,
                    stdout_bytes.decode("utf-8", errors="replace"),
                    stderr_bytes.decode("utf-8", errors="replace"),
                )
            if channel.exit_status_ready():
                while channel.recv_ready():
                    stdout_bytes.extend(channel.recv(32768))
                while channel.recv_stderr_ready():
                    stderr_bytes.extend(channel.recv_stderr(32768))
                break
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                channel.close()
                raise CommandTimeoutError(
                    f"命令超时 host={self.host.host}:{self.host.port} "
                    f"timeout={timeout}s command={command!r}"
                )
            time.sleep(min(0.05, remaining))
        exit_code = channel.recv_exit_status()
        return (
            exit_code,
            stdout_bytes.decode("utf-8", errors="replace"),
            stderr_bytes.decode("utf-8", errors="replace"),
        )

    # ===== SFTP =====

    def sftp(self) -> paramiko.SFTPClient:
        if self._client is None:
            raise SSHError(f"未连接; 先调 connect() — host={self.host.host}")
        return self._client.open_sftp()

    # ===== Bootstrap helper =====

    def bootstrap(self) -> bool:
        """Bootstrap-then-Key 模式 (D-03): 密码登录 → 部署公钥 → 标完成.

        Returns:
            True  - 这次部署了新公钥
            False - 已部署过

        Raises:
            SSHError: 未用 alias 形式 (user@host 直连无法标记)
            ConnectError / AuthError: 连接或认证失败
        """
        if not self.host.alias:
            raise SSHError(
                "bootstrap 仅适用于 alias 形式 (有 ~/.ssh/config 条目); "
                f"user@host 直连无法标记 — target={self.host.user}@{self.host.host}"
            )

        # 必须先 connect (可能用密码)
        if self._client is None:
            self.connect()

        password = self._bootstrap_password()
        if not password:
            raise SSHError(
                f"需要 env SSH_PASSWORD_{self._alias_key()} 提供一次性密码"
            )

        return ssh_keys.deploy_public_key(self, self.host.alias, password)

"""autoresearch.ssh_bootstrap.deploy — 部署本机公钥到远端 authorized_keys.

流程 (D-34):
  1. ensure_local_keypair()  — 确保本机有 ~/.autoresearch/ssh_keys/id_ed25519
  2. SSH 远端, force_password=True, 用 config.bootstrap_password_secret 认证
  3. 读远端 ~/.ssh/authorized_keys (无则创建)
  4. 检查本机 pub 指纹是否已存在; 不存在则追加
  5. chmod 700 ~/.ssh, 600 authorized_keys
  6. 写本地 marker (~/.autoresearch/ssh_keys/<host>.deployed)
  7. (verify) 第二次 connect 用 key 认证, 验证部署成功

--apply 默认 False (dry-run).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from workspace_core.config import ServerSpec, from_path, ConfigError
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import (
    AuthError,
    BootstrapFailed,
    HostSpec,
    SSHClient,
    SSHError,
    keys as ssh_keys,
)


def _resolve_server(name: str, config_path: str | None) -> ServerSpec:
    cfg = from_path(config_path)
    spec = next((s for s in cfg.servers if s.name == name), None)
    if spec is None:
        avail = [s.name for s in cfg.servers]
        raise ConfigError(
            f"config.servers 中找不到 '{name}'; 已配: {avail}"
        )
    return spec


def _build_host(spec: ServerSpec) -> HostSpec:
    return HostSpec(
        alias=spec.name,
        host=spec.host,
        port=spec.port,
        user=spec.user,
        identity_file=(
            Path(spec.identity_file).expanduser()
            if spec.identity_file
            else None
        ),
    )


def _exec(client: SSHClient, command: str, timeout: float = 15.0) -> tuple[int, str, str]:
    """统一包 exec 返回值. 兼容真 paramiko (stdout/stderr 有 .channel/.read())
    和 mock (直接返回元组)."""
    result = client.exec(command, timeout=timeout)
    if isinstance(result, tuple) and len(result) == 3:
        return result  # 已是 (exit_code, stdout, stderr) 形式
    si, so, se = result
    # 真 paramiko: so.channel.recv_exit_status + so.read()
    try:
        exit_code = so.channel.recv_exit_status
    except AttributeError:
        exit_code = 0
    try:
        out = so.read().decode("utf-8", "replace")
    except (AttributeError, TypeError):
        out = str(so.read()) if hasattr(so, "read") else ""
    try:
        err = se.read().decode("utf-8", "replace")
    except (AttributeError, TypeError):
        err = str(se.read()) if hasattr(se, "read") else ""
    return exit_code, out, err


def run_deploy_key(
    server_name: str,
    config_path: str | None = None,
    apply: bool = False,
    lang: str = "zh",
) -> CheckResult:
    """deploy-key CLI 入口."""
    data: dict[str, Any] = {
        "server": server_name,
        "apply_requested": apply,
    }
    warnings: list[str] = []

    try:
        spec = _resolve_server(server_name, config_path)
    except ConfigError as exc:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="配置错误", error=str(exc),
        )

    data["host"] = spec.host
    data["port"] = spec.port
    data["user"] = spec.user
    data["identity_file"] = spec.identity_file

    if not spec.bootstrap_password_secret:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data,
            message=(
                "config.bootstrap_password_secret 为空; "
                "deploy-key 需要一次性密码走 SSH 密码认证"
            ),
            error="missing bootstrap_password_secret",
        )

    # 1. 确保本机 keypair
    try:
        priv, pub = ssh_keys.ensure_local_keypair()
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="本机 keypair 准备失败", error=str(exc),
        )
    pub_text = pub.read_text(encoding="utf-8").strip()
    pub_fp = ssh_keys.public_key_fingerprint(pub)
    data["public_key_fingerprint"] = pub_fp
    data["public_key_path"] = str(pub)

    if not apply:
        return CheckResult(
            ok=True, severity=CheckSeverity.OK,
            data={**data, "would_deploy_pub": pub_text[:80] + "..."},
            message=(
                f"DRY-RUN: would append {pub_fp} to "
                f"{spec.user}@{spec.host}:~/.ssh/authorized_keys "
                "(use --apply to execute)"
            ),
            error=None,
        )

    # 2. SSH 远端, force_password 走密码认证
    host = _build_host(spec)
    client = SSHClient(
        host,
        bootstrap_password=spec.bootstrap_password_secret,
        force_password=True,
    )
    try:
        emit_progress("ssh.deploy.connect", server=spec.name, host=spec.host)
        client.connect(connect_timeout=8.0)
    except (AuthError, SSHError) as exc:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="SSH 密码认证失败", error=str(exc),
        )

    try:
        # 3. 读现有 authorized_keys
        _, home_dir_out, _ = _exec(client, "echo $HOME")
        home = home_dir_out.strip()
        if not home:
            home = "/root" if spec.user == "root" else f"/home/{spec.user}"
        ak_remote = f"{home}/.ssh/authorized_keys"
        ssh_dir = f"{home}/.ssh"
        data["remote_authorized_keys"] = ak_remote

        mkdir_code, _, mkdir_err = _exec(
            client, f"mkdir -p {ssh_dir} && chmod 700 {ssh_dir}"
        )
        if mkdir_code != 0:
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data,
                message="远端 ~/.ssh 目录创建失败",
                error=mkdir_err.strip() or f"exit={mkdir_code}",
            )

        # 读现有
        cat_code, existing, _ = _exec(client, f"cat {ak_remote} 2>/dev/null || true")
        if cat_code != 0:
            existing = ""

        # 4. 检查指纹是否已存在
        if pub_fp in existing or pub_text in existing:
            data["already_deployed"] = True
            warnings.append("公钥指纹或全文已存在于 authorized_keys")
        else:
            data["already_deployed"] = False
            # 用 heredoc 追加, 同时 chmod 600
            # 远端用 '>>' 追加, 用 sudo (如果 user 不是 root)
            # 安全: heredoc 用 'EOF_AR_KEY' 标识符, 避免命令注入
            append_cmd = (
                f"cat >> {ak_remote} << 'EOF_AR_KEY'\n"
                f"{pub_text}\n"
                f"EOF_AR_KEY\n"
            )
            sudo_prefix = spec.sudo_command.strip()
            if sudo_prefix:
                # 非 root 用户: 仍以该用户写 authorized_keys
                # (一般用户能写自己的 ~/.ssh, 不需要 sudo)
                pass
            chmod_cmd = f"chmod 600 {ak_remote}"
            full_cmd = append_cmd + chmod_cmd
            ap_code, ap_out, ap_err = _exec(client, full_cmd)
            if ap_code != 0:
                return CheckResult(
                    ok=False, severity=CheckSeverity.FAIL,
                    data=data,
                    message="authorized_keys 追加失败",
                    error=ap_err.strip() or f"exit={ap_code}",
                )

        # 5. 写本地 marker
        ssh_keys.mark_key_deployed(spec.name, pub)
        data["marker_path"] = str(ssh_keys._deployed_marker_path(spec.name))

        # 6. verify: 第二次 connect 走 key
        verify_client = SSHClient(host, bootstrap_password=None, force_password=False)
        try:
            emit_progress("ssh.deploy.verify", server=spec.name)
            verify_client.connect(connect_timeout=8.0)
            verify_client.close()
            data["key_auth_verified"] = True
        except (AuthError, SSHError) as exc:
            data["key_auth_verified"] = False
            warnings.append(
                f"key 部署后 key 认证未通过: {exc}; "
                "可能是 server sshd 仍拒绝 key, 需查 /var/log/auth.log"
            )

        return CheckResult(
            ok=True,
            severity=CheckSeverity.WARN if warnings else CheckSeverity.OK,
            data=data,
            message=(
                f"公钥已部署到 {spec.user}@{spec.host} (fp={pub_fp[:24]}...)"
                + (" | key 认证已验证" if data.get("key_auth_verified") else " | key 认证未验证, 见 warnings")
            ),
            error=None,
        )
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="deploy-key 执行失败", error=str(exc),
        )
    finally:
        client.close()

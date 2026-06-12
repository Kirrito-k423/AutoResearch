"""autoresearch.ssh_bootstrap.sudo — 给远端 user 装 NOPASSWD sudo (D-34).

策略 (安全优先):
  1. 写 /etc/sudoers.d/<user>-nopasswd, 0440 权限
  2. 写前备份 /etc/sudoers 到 /etc/sudoers.bak.<ts>
  3. 写完跑 visudo -c 校验
  4. 校验失败: rm /etc/sudoers.d/<user>-nopasswd, 报错
  5. 就地验证: sudo -n whoami 应返回 root

--apply 默认 False (dry-run).
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

from workspace_core.config import ServerSpec, from_path, ConfigError
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import (
    AuthError,
    HostSpec,
    SSHClient,
    SSHError,
)

from .deploy import _build_host, _exec, _resolve_server


SUDOERS_D_PATH = "/etc/sudoers.d/{user}-nopasswd"
SUDOERS_D_RULE = '{user} ALL=(ALL) NOPASSWD: ALL\n'


def _sudo_prefix_or_self(spec: ServerSpec) -> str:
    """返回能写 /etc 的命令前缀.

    user=root: 直接执行 (无前缀).
    其他: 用 config.sudo_command 拼前缀 (假设该 user 已有 sudo 权限 — NOPASSWD 在跑).
    """
    if spec.user == "root":
        return ""
    sudo = spec.sudo_command.strip()
    if not sudo:
        raise ConfigError(
            f"非 root user ({spec.user}) 需要 sudo_command 字段; "
            "装 NOPASSWD sudo 规则需要先有 sudo 权限, "
            "请先在远端手动配一次, 再用本工具自动部署"
        )
    return sudo


def run_install_nopasswd_sudo(
    server_name: str,
    config_path: str | None = None,
    apply: bool = False,
    lang: str = "zh",
) -> CheckResult:
    data: dict[str, Any] = {"server": server_name, "apply_requested": apply}
    try:
        spec = _resolve_server(server_name, config_path)
    except ConfigError as exc:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="配置错误", error=str(exc),
        )

    data["user"] = spec.user
    data["host"] = spec.host
    sudoers_file = SUDOERS_D_PATH.format(user=spec.user)
    data["sudoers_file"] = sudoers_file
    data["rule"] = SUDOERS_D_RULE.format(user=spec.user).strip()

    if not apply:
        return CheckResult(
            ok=True, severity=CheckSeverity.OK,
            data={**data, "would_write": SUDOERS_D_RULE.format(user=spec.user)},
            message=(
                f"DRY-RUN: would write to {sudoers_file} "
                f"on {spec.user}@{spec.host} (use --apply to execute)"
            ),
            error=None,
        )

    # 0. 先做 sudo_command 校验 — 早失败, 不浪费 SSH
    try:
        sudo_prefix = _sudo_prefix_or_self(spec)
    except ConfigError as exc:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="配置校验失败", error=str(exc),
        )

    # 1. SSH 远端
    host = _build_host(spec)
    client = SSHClient(
        host,
        bootstrap_password=spec.bootstrap_password_secret,
        force_password=True,
    )
    try:
        try:
            client.connect(connect_timeout=8.0)
        except (AuthError, SSHError) as exc:
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data, message="SSH 认证失败", error=str(exc),
            )
        ts = _dt.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        backup_path = f"/etc/sudoers.bak.{ts}"
        data["backup_path"] = backup_path

        # 2. 备份 /etc/sudoers
        bk_cmd = f"{sudo_prefix} cp -p /etc/sudoers {backup_path}".strip()
        bk_code, _, bk_err = _exec(client, bk_cmd)
        if bk_code != 0:
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data, message="备份 /etc/sudoers 失败",
                error=bk_err.strip() or f"exit={bk_code}",
            )

        # 3. 写 sudoers.d 文件
        rule = SUDOERS_D_RULE.format(user=spec.user)
        # 用 echo + sudo tee 写入, 避免 heredoc + sudo 的转义
        # 单引号转义: 规则不含单引号, 安全
        write_cmd = (
            f"{sudo_prefix} tee {sudoers_file} > /dev/null << 'EOF_AR_SUDO'\n"
            f"{rule}"
            f"EOF_AR_SUDO\n"
            f"{sudo_prefix} chmod 0440 {sudoers_file}\n"
            f"{sudo_prefix} chown root:root {sudoers_file}\n"
        ).strip()
        w_code, _, w_err = _exec(client, write_cmd)
        if w_code != 0:
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data, message=f"写 {sudoers_file} 失败",
                error=w_err.strip() or f"exit={w_code}",
            )

        # 4. visudo -c 校验
        chk_cmd = f"{sudo_prefix} visudo -c -f {sudoers_file}".strip()
        chk_code, chk_out, chk_err = _exec(client, chk_cmd)
        data["visudo_check"] = chk_out.strip() or chk_err.strip()
        if chk_code != 0:
            # 回滚
            rm_cmd = f"{sudo_prefix} rm -f {sudoers_file}".strip()
            _exec(client, rm_cmd)
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data,
                message="visudo 校验失败, 已回滚",
                error=chk_err.strip() or f"exit={chk_code}",
            )

        # 5. 验证: root 直接 whoami; 非 root 走 sudo -n whoami
        if spec.user == "root":
            v_cmd = "whoami"
        else:
            v_cmd = f"{sudo_prefix} sudo -n whoami".strip()
        v_code, v_out, v_err = _exec(client, v_cmd)
        data["verify_output"] = v_out.strip() or v_err.strip()
        if v_code != 0 or v_out.strip() != "root":
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data=data,
                message="NOPASSWD sudo 验证失败 (sudo -n whoami 非 root)",
                error=v_err.strip() or f"exit={v_code} output={v_out!r}",
            )

        emit_progress("ssh.sudo.nopasswd.applied", server=spec.name, user=spec.user)
        return CheckResult(
            ok=True, severity=CheckSeverity.OK,
            data=data,
            message=(
                f"NOPASSWD sudo 已装到 {spec.user}@{spec.host}:"
                f"{sudoers_file} (验证: sudo -n whoami → root)"
            ),
            error=None,
        )
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data=data, message="install-nopasswd-sudo 失败", error=str(exc),
        )
    finally:
        client.close()

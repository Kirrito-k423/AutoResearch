"""autoresearch.ssh_bootstrap — deploy-key / install-nopasswd-sudo / status 单测 (mock SSHClient)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
import yaml
import tempfile
from pathlib import Path

import pytest

from autoresearch.ssh_bootstrap import (
    run_deploy_key,
    run_install_nopasswd_sudo,
    run_ssh_status,
)
from workspace_core.config import from_yaml


# === helpers ===

def _config(servers_yaml: str) -> str:
    """写一份 config 到 tmp, 返回 path."""
    tmp = Path(tempfile.mkdtemp())
    path = tmp / "config.yaml"
    path.write_text(yaml.safe_dump({
        "version": 1,
        "servers": yaml.safe_load(servers_yaml)["servers"],
    }))
    return str(path)


def _ssh_mock_client():
    """构造假 SSHClient: connect/exec/close 全 fake."""
    c = MagicMock()
    c.connect.return_value = None
    c.close.return_value = None
    # exec 返回 (exit_code, stdout, stderr) — 通过 _exec 包装返回三元组
    return c


# === deploy-key ===

def test_deploy_key_dry_run_returns_intent():
    cfg = _config("""
servers:
  - name: ax-test
    host: 192.0.2.10
    user: root
    bootstrap_password_secret: secret-pwd
""")
    result = run_deploy_key("ax-test", config_path=cfg, apply=False)
    assert result["ok"] is True
    assert "DRY-RUN" in result["message"]
    assert "would_deploy_pub" in result["data"]
    assert result["data"]["apply_requested"] is False


def test_deploy_key_apply_uses_force_password_and_appends_pub():
    cfg = _config("""
servers:
  - name: ax-test
    host: 192.0.2.10
    user: root
    bootstrap_password_secret: secret-pwd
""")
    fake_client = _ssh_mock_client()
    # 第一次 exec: echo $HOME → /root
    # 第二次 exec: mkdir + chmod → 0
    # 第三次 exec: cat authorized_keys → 空
    # 第四次 exec: 追加 heredoc + chmod → 0
    fake_client.exec.return_value = (0, "/root\n", "")
    # mock SSHClient 类
    with patch("autoresearch.ssh_bootstrap.deploy.SSHClient") as mc:
        mc.return_value = fake_client
        with patch(
            "autoresearch.ssh_bootstrap.deploy.ssh_keys.mark_key_deployed"
        ) as mk:
            with patch(
                "autoresearch.ssh_bootstrap.deploy.ssh_keys.is_key_deployed",
                return_value=True,  # 跳过 verify 路径
            ):
                result = run_deploy_key("ax-test", config_path=cfg, apply=True)
    assert result["ok"] is True
    # 第一次 SSHClient 调用: 必须 force_password=True
    first_call = mc.call_args_list[0]
    assert first_call.kwargs.get("force_password") is True
    assert first_call.kwargs.get("bootstrap_password") == "secret-pwd"
    # 第二次 SSHClient 调用: 走 verify, force_password=False
    assert len(mc.call_args_list) >= 2
    verify_call = mc.call_args_list[1]
    assert verify_call.kwargs.get("force_password") is False
    # mark_key_deployed 至少被调一次
    assert mk.called


def test_deploy_key_already_deployed_skips_append():
    """远端 authorized_keys 已含本机公钥, 不重复追加."""
    cfg = _config("""
servers:
  - name: ax-test
    host: 192.0.2.10
    user: root
    bootstrap_password_secret: secret-pwd
""")
    fake_client = _ssh_mock_client()
    fake_client.exec.return_value = (0, "/root\n", "")
    with patch("autoresearch.ssh_bootstrap.deploy.SSHClient") as mc:
        mc.return_value = fake_client
        # mock public_key_fingerprint 直接返回固定值
        with patch(
            "autoresearch.ssh_bootstrap.deploy.ssh_keys.public_key_fingerprint",
            return_value="SHA256:fakefp",
        ):
            with patch(
                "autoresearch.ssh_bootstrap.deploy.ssh_keys.is_key_deployed",
                return_value=True,
            ):
                # 让 cat authorized_keys 返回含 fakefp 的内容
                def fake_exec(cmd, timeout=15.0):
                    if "cat /root/.ssh/authorized_keys" in cmd:
                        return (0, "ssh-ed25519 ... SHA256:fakefp user@host\n", "")
                    return (0, "/root\n", "")
                fake_client.exec.side_effect = fake_exec
                result = run_deploy_key("ax-test", config_path=cfg, apply=True)
    assert result["ok"] is True
    assert result["data"]["already_deployed"] is True


def test_deploy_key_ssh_auth_failure_returns_fail():
    cfg = _config("""
servers:
  - name: ax-test
    host: 192.0.2.10
    user: root
    bootstrap_password_secret: wrong-pwd
""")
    from workspace_core.ssh import AuthError
    with patch("autoresearch.ssh_bootstrap.deploy.SSHClient") as mc:
        c = MagicMock()
        c.connect.side_effect = AuthError("bad password")
        mc.return_value = c
        result = run_deploy_key("ax-test", config_path=cfg, apply=True)
    assert result["ok"] is False
    assert "认证失败" in result["message"] or "Auth" in result["error"]


# === install-nopasswd-sudo ===

def test_install_nopasswd_sudo_dry_run():
    cfg = _config("""
servers:
  - name: ax-180
    host: 192.0.2.10
    user: admin123
    bootstrap_password_secret: secret
    sudo_command: ""
""")
    result = run_install_nopasswd_sudo("ax-180", config_path=cfg, apply=False)
    assert result["ok"] is True
    assert "DRY-RUN" in result["message"]
    assert "admin123 ALL=(ALL) NOPASSWD: ALL" in result["data"]["rule"]


def test_install_nopasswd_sudo_apply_writes_sudoers_d_and_verifies():
    cfg = _config("""
servers:
  - name: ax-180
    host: 192.0.2.10
    user: admin123
    bootstrap_password_secret: secret
    sudo_command: "sudo -i"
""")
    fake_client = _ssh_mock_client()
    # 第一次 exec: cp /etc/sudoers → 0
    # 第二次 exec: heredoc + chmod + chown → 0
    # 第三次 exec: visudo -c → 0 + "OK"
    # 第四次 exec: sudo -n whoami → 0 + "root"
    fake_client.exec.return_value = (0, "OK\n", "")
    with patch("autoresearch.ssh_bootstrap.sudo.SSHClient") as mc:
        mc.return_value = fake_client
        def fake_exec(cmd, timeout=15.0):
            if "visudo" in cmd:
                return (0, "/etc/sudoers.d/admin123-nopasswd: parsed OK\n", "")
            if "sudo -n whoami" in cmd:
                return (0, "root\n", "")
            return (0, "", "")
        fake_client.exec.side_effect = fake_exec
        result = run_install_nopasswd_sudo("ax-180", config_path=cfg, apply=True)
    assert result["ok"] is True, result
    assert "NOPASSWD sudo 已装" in result["message"]


def test_install_nopasswd_sudo_visudo_failure_rolls_back():
    cfg = _config("""
servers:
  - name: ax-180
    host: 192.0.2.10
    user: admin123
    bootstrap_password_secret: secret
    sudo_command: "sudo -i"
""")
    fake_client = _ssh_mock_client()
    fake_client.exec.return_value = (0, "", "")
    with patch("autoresearch.ssh_bootstrap.sudo.SSHClient") as mc:
        mc.return_value = fake_client
        def fake_exec(cmd, timeout=15.0):
            if "visudo" in cmd:
                return (1, "", "syntax error\n")
            return (0, "", "")
        fake_client.exec.side_effect = fake_exec
        result = run_install_nopasswd_sudo("ax-180", config_path=cfg, apply=True)
    assert result["ok"] is False
    assert "visudo" in result["message"] or "visudo" in result["error"]
    # 应有 rm -f 回滚
    rm_calls = [c for c in fake_client.exec.call_args_list if "rm -f" in c.args[0]]
    assert rm_calls, "expected rollback rm -f after visudo failure"


def test_install_nopasswd_sudo_non_root_without_sudo_command_fails():
    """非 root user 没 sudo_command 字段, 应当报错 (不偷偷加 sudo)."""
    cfg = _config("""
servers:
  - name: ax-180
    host: 192.0.2.10
    user: admin123
    bootstrap_password_secret: secret
    sudo_command: ""
""")
    result = run_install_nopasswd_sudo("ax-180", config_path=cfg, apply=True)
    assert result["ok"] is False
    assert "sudo_command" in result["error"]


def test_install_nopasswd_sudo_root_user_skips_sudo_prefix():
    """root user 安装 NOPASSWD 不需要 sudo 前缀."""
    cfg = _config("""
servers:
  - name: ax-225
    host: 192.0.2.10
    user: root
    bootstrap_password_secret: secret
    sudo_command: ""
""")
    fake_client = _ssh_mock_client()
    fake_client.exec.return_value = (0, "", "")
    with patch("autoresearch.ssh_bootstrap.sudo.SSHClient") as mc:
        mc.return_value = fake_client
        def fake_exec(cmd, timeout=15.0):
            if "visudo" in cmd:
                return (0, "OK\n", "")
            if "sudo -n whoami" in cmd:
                return (0, "root\n", "")
            return (0, "", "")
        fake_client.exec.side_effect = fake_exec
        result = run_install_nopasswd_sudo("ax-225", config_path=cfg, apply=True)
    assert result["ok"] is True
    # 检查所有 exec 命令不含 "sudo " 前缀
    for call in fake_client.exec.call_args_list:
        cmd = call.args[0]
        assert not cmd.startswith("sudo"), f"root user should not use sudo prefix: {cmd[:60]}"


# === status ===

def test_ssh_status_returns_one_row_per_server():
    cfg = _config("""
servers:
  - name: ax-225
    host: 192.0.2.10
    user: root
  - name: ax-180
    host: 192.0.2.11
    user: admin123
""")
    fake_client = _ssh_mock_client()
    with patch("autoresearch.ssh_bootstrap.status.SSHClient") as mc:
        mc.return_value = fake_client
        result = run_ssh_status(server_name=None, config_path=cfg)
    assert result["data"]["total"] == 2
    servers = result["data"]["servers"]
    assert {s["server"] for s in servers} == {"ax-225", "ax-180"}
    for s in servers:
        assert "keypair_local" in s
        assert "key_deployed" in s
        assert "nopasswd_sudo" in s
        assert "ready_for_probe" in s
        assert "ssh_reachable" in s


def test_ssh_status_specific_server_not_found():
    cfg = _config("""
servers:
  - name: ax-225
    host: 192.0.2.10
    user: root
""")
    fake_client = _ssh_mock_client()
    with patch("autoresearch.ssh_bootstrap.status.SSHClient") as mc:
        mc.return_value = fake_client
        result = run_ssh_status(server_name="nonexistent", config_path=cfg)
    assert result["ok"] is False
    assert "未找到" in result["message"]


# === force_password in workspace-core.ssh.SSHClient ===

def test_ssh_client_force_password_disables_key_lookup():
    """SSHClient(force_password=True) 时 connect kwargs 关掉 key 试错."""
    from workspace_core.ssh.client import SSHClient
    from workspace_core.ssh.host import HostSpec
    import paramiko

    c = SSHClient(
        HostSpec(alias="t", host="192.0.2.1", port=22, user="u", identity_file=None),
        bootstrap_password="pwd",
        force_password=True,
    )
    with patch.object(paramiko.SSHClient, "connect") as gconnect:
        gconnect.return_value = None
        c.connect(connect_timeout=2.0)
    kw = gconnect.call_args.kwargs
    assert kw["look_for_keys"] is False
    assert kw["allow_agent"] is False
    assert kw["password"] == "pwd"

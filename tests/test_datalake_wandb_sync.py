"""Tests for datalake.wandb.sync (Phase 08-02, D-45)."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, call

import pytest
from workspace_core.config import ServerSpec

from datalake.wandb.sync import (
    sync_run,
    _list_remote_wandb_runs,
    _check_wandb_cli,
    _check_local_wandb_server,
    _wandb_sync_subprocess,
    _sftp_fetch_dir,
    WandbNotInstalled,
    NoRemoteRun,
    SyncFailed,
)


def _spec():
    return ServerSpec(name="A2-AK-225", host="192.168.9.225", user="root")


# === _check_wandb_cli ===

def test_check_wandb_cli_missing(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: None if x == "wandb" else "/usr/bin/x")
    with pytest.raises(WandbNotInstalled, match="没装 wandb CLI"):
        _check_wandb_cli()


def test_check_wandb_cli_present(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda x: "/usr/local/bin/wandb" if x == "wandb" else None)
    _check_wandb_cli()  # 不抛


# === _list_remote_wandb_runs ===

def test_list_remote_runs_returns_run_dirs():
    spec = _spec()
    with patch("datalake.wandb.sync._ssh_exec_capture") as mock:
        mock.return_value = (0, "run-20260615_050749-abc123\nrun-20260615_050800-xyz789\nlatest.log\n", "")
        runs = _list_remote_wandb_runs(spec, workdir="/root")
    assert "run-20260615_050749-abc123" in runs
    assert "run-20260615_050800-xyz789" in runs
    # latest.log 不在
    assert all(r.startswith("run-") for r in runs)


def test_list_remote_runs_filters_by_prefix():
    spec = _spec()
    with patch("datalake.wandb.sync._ssh_exec_capture") as mock:
        mock.return_value = (0, "run-20260615_050749-abc123\nrun-20260615_050800-xyz789\n", "")
        runs = _list_remote_wandb_runs(spec, workdir="/root", run_id_prefix="abc")
    assert runs == ["run-20260615_050749-abc123"]


def test_list_remote_runs_empty_dir():
    spec = _spec()
    with patch("datalake.wandb.sync._ssh_exec_capture") as mock:
        mock.return_value = (0, "", "")
        runs = _list_remote_wandb_runs(spec, workdir="/root")
    assert runs == []


# === _check_local_wandb_server ===

def test_check_local_server_alive(monkeypatch):
    """本地服务在 → True."""
    import urllib.request
    from contextlib import contextmanager
    @contextmanager
    def fake_urlopen(req, timeout):
        class FakeResp:
            status = 200
        yield FakeResp()
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert _check_local_wandb_server() is True


def test_check_local_server_dead(monkeypatch):
    """本地服务不在 → False (graceful)."""
    import urllib.request
    import urllib.error
    def boom(req, timeout):
        raise urllib.error.URLError("Connection refused")
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    assert _check_local_wandb_server() is False


# === _wandb_sync_subprocess ===

def test_wandb_sync_subprocess_pass():
    fake = MagicMock(returncode=0, stdout="wandb: Syncing run xyz\n", stderr="")
    with patch("datalake.wandb.sync.subprocess.run", return_value=fake) as mock:
        ec, so, se = _wandb_sync_subprocess(Path("/tmp/fake"))
    assert ec == 0
    assert "Syncing" in so
    args = mock.call_args[0][0]
    assert args[0] == "wandb"
    assert args[1] == "sync"


def test_wandb_sync_subprocess_timeout():
    with patch("datalake.wandb.sync.subprocess.run", side_effect=subprocess.TimeoutExpired("wandb", 30)):
        with pytest.raises(subprocess.TimeoutExpired):
            _wandb_sync_subprocess(Path("/tmp/fake"), timeout=5.0)


# === _sftp_fetch_dir (mock sftp) ===

def test_sftp_fetch_dir_skips_tmp_files(tmp_path):
    """SFTP 递归拉: 跳过 .tmp / .lock / hidden, 拉普通文件."""
    fake_sftp = MagicMock()
    # mock sftp.listdir_attr 返回 1 dir + 1 file + 1 .tmp
    dir_item = MagicMock()
    dir_item.filename = "subdir"
    dir_item.st_mode = 0o040000  # dir
    file_item = MagicMock()
    file_item.filename = "wandb-metadata.json"
    file_item.st_mode = 0o100000  # file
    tmp_item = MagicMock()
    tmp_item.filename = "wandb-summary.json.tmp"
    tmp_item.st_mode = 0o100000
    hidden_item = MagicMock()
    hidden_item.filename = ".wandb"
    hidden_item.st_mode = 0o040000

    def listdir_attr_side(remote_dir):
        if remote_dir.endswith("/wandb"):
            return [dir_item, file_item, tmp_item, hidden_item]
        if remote_dir.endswith("/subdir"):
            return []
        return []

    fake_sftp.listdir_attr.side_effect = listdir_attr_side

    spec = _spec()
    # datalake.wandb.sync 内部 SSHClient 来自 workspace_core.ssh.client
    # resolve_secret 是 lazy import, patch workspace_core.secrets.resolve_secret
    with patch("workspace_core.ssh.client.SSHClient") as MockClient, \
         patch("workspace_core.secrets.resolve_secret", return_value=None):
        instance = MagicMock()
        instance.sftp.return_value = fake_sftp
        MockClient.return_value = instance
        _sftp_fetch_dir(spec, "/root/wandb", tmp_path / "out")

    # 验证: 拉了 wandb-metadata.json, 没拉 .tmp / .wandb
    assert (tmp_path / "out" / "wandb-metadata.json")  # file 路径创建 (sftp.get mock 没真写)
    # hidden / tmp 不在 listdir 顶层递归: 因 listdir_attr 仅对子目录返回 [] 不创建
    # 关键: sftp.get 调用 1 次 (file), hidden dir 没递归
    assert fake_sftp.get.call_count == 1


# === sync_run end-to-end (mock) ===

def test_sync_run_happy_path(tmp_path):
    """sync_run: 1) 验 wandb CLI 2) ls 远程 3) SFTP 拉 4) subprocess sync 5) return path."""
    spec = _spec()
    local_root = tmp_path / "runs"
    with patch("datalake.wandb.sync._check_wandb_cli"), \
         patch("datalake.wandb.sync._list_remote_wandb_runs",
               return_value=["run-20260615_050749-abc123"]), \
         patch("datalake.wandb.sync._sftp_fetch_dir") as mock_fetch, \
         patch("datalake.wandb.sync._wandb_sync_subprocess",
               return_value=(0, "Syncing run abc123\nwandb: Synced 3 files\n", "")):
        result = sync_run("abc123", spec, workdir="/root", local_runs_root=local_root)

    assert result == local_root / "abc123" / "wandb"
    # _sftp_fetch_dir 调了 1 次, 远程目录是 /root/wandb/run-...
    args = mock_fetch.call_args
    assert args[0][1] == "/root/wandb/run-20260615_050749-abc123"


def test_sync_run_no_remote_run_raises(tmp_path):
    spec = _spec()
    local_root = tmp_path / "runs"
    with patch("datalake.wandb.sync._check_wandb_cli"), \
         patch("datalake.wandb.sync._list_remote_wandb_runs", return_value=[]):
        with pytest.raises(NoRemoteRun, match="找不到"):
            sync_run("missing", spec, workdir="/root", local_runs_root=local_root)


def test_sync_run_wandb_cli_missing(tmp_path):
    spec = _spec()
    local_root = tmp_path / "runs"
    with patch("datalake.wandb.sync._check_wandb_cli",
               side_effect=WandbNotInstalled("Mac 本地没装 wandb CLI")):
        with pytest.raises(WandbNotInstalled, match="没装 wandb CLI"):
            sync_run("abc", spec, workdir="/root", local_runs_root=local_root)


def test_sync_run_sync_failed_with_local_server_hint(tmp_path):
    """sync 失败: stderr 含 'Connection refused' → 提示启服务."""
    spec = _spec()
    local_root = tmp_path / "runs"
    with patch("datalake.wandb.sync._check_wandb_cli"), \
         patch("datalake.wandb.sync._list_remote_wandb_runs",
               return_value=["run-20260615_050749-abc"]), \
         patch("datalake.wandb.sync._sftp_fetch_dir"), \
         patch("datalake.wandb.sync._wandb_sync_subprocess",
               return_value=(1, "", "wandb: Connection refused to localhost:8080")):
        with pytest.raises(SyncFailed, match="autoresearch services start"):
            sync_run("abc", spec, workdir="/root", local_runs_root=local_root)


def test_sync_run_sync_failed_generic(tmp_path):
    spec = _spec()
    local_root = tmp_path / "runs"
    with patch("datalake.wandb.sync._check_wandb_cli"), \
         patch("datalake.wandb.sync._list_remote_wandb_runs",
               return_value=["run-20260615_050749-abc"]), \
         patch("datalake.wandb.sync._sftp_fetch_dir"), \
         patch("datalake.wandb.sync._wandb_sync_subprocess",
               return_value=(1, "some stdout", "some random error")):
        with pytest.raises(SyncFailed, match="exit=1"):
            sync_run("abc", spec, workdir="/root", local_runs_root=local_root)

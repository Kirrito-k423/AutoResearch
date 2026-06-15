"""Tests for datalake.logs.collector (Phase 08-03, D-46/D-47)."""
from __future__ import annotations

from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from workspace_core.config import ServerSpec

from datalake.logs.collector import LogFetchError, collect_log, tail_remote_log


def _spec() -> ServerSpec:
    return ServerSpec(name="A2-AK-225", host="192.168.9.225", user="root")


def _patch_client(remote_file):
    return patch("datalake.logs.collector.SSHClient", autospec=True)


def test_collect_log_happy_path(tmp_path):
    remote_file = BytesIO(b"SUM= 5.29\nNPU_COUNT= 8\n")
    remote_file.prefetch = MagicMock()
    remote_file.close = MagicMock()

    with _patch_client(remote_file) as MockClient:
        instance = MockClient.return_value
        instance.sftp.return_value.open.return_value = remote_file
        path = collect_log("run123", _spec(), local_runs_root=tmp_path)

    assert path == tmp_path / "run123" / "log.txt"
    assert path.read_text() == "SUM= 5.29\nNPU_COUNT= 8\n"
    remote_file.prefetch.assert_called_once()
    instance.sftp.return_value.open.assert_called_once_with("/root/runs/run123.log", "rb")
    instance.close.assert_called_once()


def test_collect_log_uses_workdir_override(tmp_path):
    remote_file = BytesIO(b"ok\n")
    remote_file.prefetch = MagicMock()
    remote_file.close = MagicMock()

    with _patch_client(remote_file) as MockClient:
        instance = MockClient.return_value
        instance.sftp.return_value.open.return_value = remote_file
        collect_log("run123", _spec(), workdir_override="/home/t00906153", local_runs_root=tmp_path)

    instance.sftp.return_value.open.assert_called_once_with(
        "/home/t00906153/runs/run123.log", "rb"
    )


def test_collect_log_not_found_is_readable(tmp_path):
    with _patch_client(None) as MockClient:
        instance = MockClient.return_value
        instance.sftp.return_value.open.side_effect = FileNotFoundError("missing")
        with pytest.raises(LogFetchError, match="远程日志不存在"):
            collect_log("missing", _spec(), local_runs_root=tmp_path)
    instance.close.assert_called_once()


def test_collect_log_permission_error_is_readable(tmp_path):
    with _patch_client(None) as MockClient:
        instance = MockClient.return_value
        instance.sftp.return_value.open.side_effect = PermissionError("denied")
        with pytest.raises(LogFetchError, match="无权限"):
            collect_log("denied", _spec(), local_runs_root=tmp_path)
    instance.close.assert_called_once()


def test_tail_remote_log_uses_remote_path_stem(tmp_path):
    remote_file = BytesIO(b"hello\n")
    remote_file.prefetch = MagicMock()
    remote_file.close = MagicMock()

    with _patch_client(remote_file) as MockClient:
        instance = MockClient.return_value
        instance.sftp.return_value.open.return_value = remote_file
        path = tail_remote_log(_spec(), "/tmp/custom.log", local_runs_root=tmp_path)

    assert path == tmp_path / "custom" / "log.txt"
    instance.sftp.return_value.open.assert_called_once_with("/tmp/custom.log", "rb")

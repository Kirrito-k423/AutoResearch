"""Tests for reverse tunnel (mock ssh binary)."""
from pathlib import Path
from unittest.mock import patch, MagicMock

from workspace_core.ssh.tunnel import open_reverse_tunnel, ReverseTunnel
from workspace_core.ssh.host import HostSpec
from workspace_core.ssh.exceptions import TunnelError


def test_open_reverse_tunnel_constructs_correct_ssh_command(tmp_path):
    """Verify ssh -R command is constructed correctly (no real process)."""
    h = HostSpec(alias="test-host", host="example.com", port=22, user="u", identity_file=Path("/tmp/key"))
    mock_proc = MagicMock()
    mock_proc.poll.return_value = None  # pretend process still running
    mock_proc.pid = 12345
    mock_proc.wait = MagicMock()

    with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
        tunnel = open_reverse_tunnel(h, remote_port=8080, local_port=9090, identity_file=Path("/tmp/key"), log_dir=tmp_path)

    call_args = mock_popen.call_args
    cmd = call_args[0][0]
    assert "ssh" in cmd
    assert "-N" in cmd
    assert "-R" in cmd
    # -R 参数: 8080:localhost:9090
    idx = cmd.index("-R")
    assert cmd[idx + 1] == "8080:localhost:9090"
    assert "ServerAliveInterval=30" in cmd
    assert "ServerAliveCountMax=3" in cmd
    assert "ExitOnForwardFailure=yes" in cmd
    assert "-i" in cmd
    assert "/tmp/key" in cmd
    assert cmd[-1] == "u@example.com"
    # start_new_session=True (independent process group)
    assert call_args[1].get("start_new_session") is True

    assert tunnel.pid == 12345
    assert tunnel.remote_port == 8080
    assert tunnel.local_port == 9090
    assert "test-host" in str(tunnel.log_path)


def test_open_reverse_tunnel_fails_immediately():
    """If ExitOnForwardFailure triggers, Popen.poll() returns code → raise TunnelError."""
    h = HostSpec(alias="fail-host", host="invalid", port=22, user="u", identity_file=None)
    mock_proc = MagicMock()
    mock_proc.poll.return_value = 1  # 进程已退出
    mock_proc.returncode = 1

    with patch("subprocess.Popen", return_value=mock_proc):
        with patch("pathlib.Path.mkdir"):  # 不真建 log_dir
            with patch("pathlib.Path.read_text", return_value="connection refused"):
                with patch("builtins.open", MagicMock()):
                    with patch("time.sleep"):  # skip 0.5s
                        with patch("workspace_core.ssh.tunnel.open", MagicMock()):  # log file
                            with patch.object(Path, "read_text", return_value="connection refused"):
                                with patch("os.path.exists", return_value=True):
                                    with patch("pathlib.Path.home", return_value=Path("/tmp")):
                                        import pytest
                                        with pytest.raises(TunnelError) as exc:
                                            open_reverse_tunnel(h, remote_port=8080, local_port=9090)
        assert "立即退出" in str(exc.value)

"""Tests for ssh key management (D-03)."""
import pytest
from pathlib import Path

from workspace_core.ssh import keys
from workspace_core.ssh.keys import (
    is_key_deployed,
    mark_key_deployed,
    public_key_fingerprint,
)


def test_ensure_local_keypair(tmp_path, monkeypatch):
    """Generate ed25519 keypair on first call, idempotent on second."""
    monkeypatch.setattr(keys, "_ssh_keys_dir", lambda: tmp_path)
    priv, pub = keys.ensure_local_keypair()
    assert priv.exists()
    assert pub.exists()
    assert priv.read_text().startswith("-----BEGIN OPENSSH PRIVATE KEY-----")
    # pub 内容: ssh-ed25519 <base64> autoresearch
    pub_content = pub.read_text()
    assert pub_content.startswith("ssh-ed25519")
    assert "autoresearch" in pub_content

    # 幂等: 第二次不重新生成
    priv2, pub2 = keys.ensure_local_keypair()
    assert priv == priv2
    assert pub == pub2


def test_is_key_deployed_false_initially(tmp_path, monkeypatch):
    monkeypatch.setattr(keys, "_ssh_keys_dir", lambda: tmp_path)
    _, pub = keys.ensure_local_keypair()
    assert is_key_deployed("test-host", pub, key_dir=tmp_path) is False


def test_mark_and_check_key_deployed(tmp_path, monkeypatch):
    monkeypatch.setattr(keys, "_ssh_keys_dir", lambda: tmp_path)
    _, pub = keys.ensure_local_keypair()
    assert is_key_deployed("test-host", pub, key_dir=tmp_path) is False
    mark_key_deployed("test-host", pub, key_dir=tmp_path)
    assert is_key_deployed("test-host", pub, key_dir=tmp_path) is True

    # 不同 host 不同标记
    assert is_key_deployed("other-host", pub, key_dir=tmp_path) is False


def test_public_key_fingerprint_format(tmp_path, monkeypatch):
    monkeypatch.setattr(keys, "_ssh_keys_dir", lambda: tmp_path)
    _, pub = keys.ensure_local_keypair()
    fp = public_key_fingerprint(pub)
    assert fp.startswith("SHA256:")
    assert len(fp) > 20

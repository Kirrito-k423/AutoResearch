"""SSH key 管理: 本地 keypair + 部署公钥 + 缓存 (D-03 Bootstrap-then-Key)."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .exceptions import KeyDeployError


SSH_KEYS_DIR = Path.home() / ".autoresearch" / "ssh_keys"


def _ssh_keys_dir() -> Path:
    """解析时的 SSH_KEYS_DIR (供测试 monkeypatch)."""
    return SSH_KEYS_DIR


def ensure_local_keypair(key_dir: Path | None = None) -> tuple[Path, Path]:
    """确保本机有 ed25519 keypair; 没有就生成.

    Args:
        key_dir: 私钥目录 (默认 ~/.autoresearch/ssh_keys)

    Returns (private_key_path, public_key_path).
    """
    if key_dir is None:
        key_dir = _ssh_keys_dir()
    key_dir.mkdir(parents=True, exist_ok=True)
    priv = key_dir / "id_ed25519"
    pub = key_dir / "id_ed25519.pub"

    if not priv.exists():
        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-N", "", "-f", str(priv), "-C", "autoresearch"],
            check=True,
            capture_output=True,
        )
    return priv, pub


def public_key_fingerprint(pub_path: Path) -> str:
    """算公钥 fingerprint (用作已部署标记).

    格式: 'SHA256:base64...' (ssh-keygen -lf 默认输出)
    """
    result = subprocess.run(
        ["ssh-keygen", "-lf", str(pub_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    parts = result.stdout.split()
    # 输出: "256 SHA256:xxx user@host (ED25519)"
    if len(parts) < 2:
        raise KeyDeployError(f"无法解析 ssh-keygen 输出: {result.stdout!r}")
    return parts[1]


def _deployed_marker_path(host_alias: str, key_dir: Path | None = None) -> Path:
    """~/.autoresearch/ssh_keys/<host>.deployed 标记文件路径."""
    if key_dir is None:
        key_dir = _ssh_keys_dir()
    safe = host_alias.replace("/", "_").replace("@", "_")
    return key_dir / f"{safe}.deployed"


def is_key_deployed(host_alias: str, pub_path: Path, key_dir: Path | None = None) -> bool:
    """检查本机公钥是否已部署到 <host_alias> (依据标记文件)."""
    marker = _deployed_marker_path(host_alias, key_dir)
    if not marker.exists():
        return False
    return marker.read_text().strip() == public_key_fingerprint(pub_path)


def mark_key_deployed(host_alias: str, pub_path: Path, key_dir: Path | None = None) -> None:
    """标记 <host_alias> 已部署本机公钥."""
    marker = _deployed_marker_path(host_alias, key_dir)
    marker.write_text(public_key_fingerprint(pub_path))


def deploy_public_key(
    client: SSHClient, host_alias: str, password: str, key_dir: Path | None = None
) -> bool:
    """Bootstrap 阶段: 用密码登录后部署本机公钥到远端.

    Returns:
        True  - 这次部署了新公钥
        False - 已部署过 (跳过)

    Raises:
        KeyDeployError: 部署失败
    """
    _, pub_path = ensure_local_keypair(key_dir)

    if is_key_deployed(host_alias, pub_path, key_dir):
        return False  # 之前已部署, 跳过

    pub_key_content = pub_path.read_text().strip()
    sftp = client.sftp()
    try:
        # 读远端 authorized_keys, 追加, 写回
        remote_ak = ".ssh/authorized_keys"
        try:
            existing = sftp.open(remote_ak, "r").read().decode("utf-8", errors="ignore")
        except IOError:
            existing = ""

        if pub_key_content in existing:
            # 远端已有 (但本机标记丢了), 仅补标记
            mark_key_deployed(host_alias, pub_path, key_dir)
            return False

        # 确保 .ssh 目录存在
        try:
            sftp.mkdir(".ssh")
        except IOError:
            pass  # 已存在

        with sftp.open(remote_ak, "a") as f:
            f.write(pub_key_content + "\n")

        # 权限收尾
        sftp.chmod(remote_ak, 0o600)
        try:
            sftp.chmod(".ssh", 0o700)
        except IOError:
            pass
    except Exception as e:
        raise KeyDeployError(
            f"无法部署公钥到 {host_alias}: {e}"
        ) from e
    finally:
        try:
            sftp.close()
        except Exception:
            pass

    mark_key_deployed(host_alias, pub_path, key_dir)
    return True

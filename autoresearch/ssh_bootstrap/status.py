"""autoresearch.ssh_bootstrap.status — 一眼看每台 server 的 key + sudo 就绪状态.

每台 server 输出 4 个布尔:
  - keypair_local: 本机 ~/.autoresearch/ssh_keys/id_ed25519 是否存在
  - key_deployed:  本机公钥指纹是否在远端 authorized_keys
  - nopasswd_sudo: 远端 /etc/sudoers.d/<user>-nopasswd 是否存在 + 有效
  - ready_for_probe: 满足 (root user) OR (key_deployed AND nopasswd_sudo)
"""
from __future__ import annotations

from typing import Any

from workspace_core.config import from_path, ConfigError
from workspace_core.result import CheckResult, CheckSeverity
from workspace_core.ssh import AuthError, HostSpec, SSHClient, SSHError, keys as ssh_keys


def _check_one(server_name: str, spec, config_path: str | None) -> dict[str, Any]:
    """对一台 server 做 4 项检查. 不连远端, 全部本地判定 + 1 次 SSH 探活 (optional)."""
    info: dict[str, Any] = {
        "server": server_name,
        "host": spec.host,
        "port": spec.port,
        "user": spec.user,
    }
    # 1. 本地 keypair
    keypair_local = False
    pub = None
    try:
        priv, pub = ssh_keys.ensure_local_keypair()
        keypair_local = priv.exists() and pub.exists()
    except Exception:  # noqa: BLE001
        pass
    info["keypair_local"] = keypair_local

    # 2. key deployed (按本地 marker)
    key_deployed = False
    if pub is not None and pub.exists():
        key_deployed = ssh_keys.is_key_deployed(server_name, pub)
    info["key_deployed"] = key_deployed

    # 3. nopasswd sudo: 本地无法直接判断, 标 "unknown" (除非 user=root)
    if spec.user == "root":
        info["nopasswd_sudo"] = "n/a (root user)"
    else:
        info["nopasswd_sudo"] = "unknown (run install-nopasswd-sudo to set)"

    # 4. ready_for_probe
    if spec.user == "root":
        info["ready_for_probe"] = key_deployed  # root 只需 key 部署
    else:
        info["ready_for_probe"] = key_deployed and (
            info["nopasswd_sudo"] != "unknown (run install-nopasswd-sudo to set)"
        )

    # 5. SSH 探活 (用 key 优先; 失败不报错, 只是标不可达)
    try:
        host = HostSpec(
            alias=spec.name, host=spec.host, port=spec.port, user=spec.user,
            identity_file=__import__("pathlib").Path(spec.identity_file).expanduser() if spec.identity_file else None,
        )
        c = SSHClient(host, bootstrap_password=spec.bootstrap_password_secret, force_password=True)
        c.connect(connect_timeout=4.0)
        c.close()
        info["ssh_reachable"] = True
    except (AuthError, SSHError, OSError) as exc:
        info["ssh_reachable"] = False
        info["ssh_error"] = str(exc)[:120]

    return info


def run_ssh_status(
    server_name: str | None = None,
    config_path: str | None = None,
) -> CheckResult:
    """CLI 入口. server_name=None 走全部 config.servers."""
    try:
        cfg = from_path(config_path)
    except ConfigError as exc:
        return CheckResult(
            ok=False, severity=CheckSeverity.FAIL,
            data={}, message="配置错误", error=str(exc),
        )

    if server_name:
        servers = [s for s in cfg.servers if s.name == server_name]
        if not servers:
            avail = [s.name for s in cfg.servers]
            return CheckResult(
                ok=False, severity=CheckSeverity.FAIL,
                data={"available": avail},
                message=f"未找到 server: {server_name}",
                error=f"available: {avail}",
            )
    else:
        servers = list(cfg.servers)

    rows = [_check_one(s.name, s, config_path) for s in servers]
    ready = [r["server"] for r in rows if r.get("ready_for_probe") and r.get("ssh_reachable")]
    not_ready = [r["server"] for r in rows if r["server"] not in ready]

    return CheckResult(
        ok=len(not_ready) == 0,
        severity=CheckSeverity.OK if not not_ready else CheckSeverity.WARN,
        data={
            "servers": rows,
            "ready": ready,
            "not_ready": not_ready,
            "total": len(rows),
        },
        message=(
            f"全部 {len(rows)} 台 ready"
            if not not_ready
            else f"{len(ready)}/{len(rows)} ready, 待补: {', '.join(not_ready)}"
        ),
        error=None,
    )

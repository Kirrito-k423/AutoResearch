"""workspace-core.ssh — SSH 客户端抽象 + Bootstrap-then-Key + 反向代理 (D-01..05)."""
from .client import SSHClient
from .host import HostSpec, resolve_host
from .tunnel import open_reverse_tunnel, ReverseTunnel
from . import keys
from .exceptions import (
    SSHError,
    HostResolveError,
    ConnectError,
    AuthError,
    BootstrapFailed,
    KeyDeployError,
    TunnelError,
)

__all__ = [
    "SSHClient",
    "HostSpec",
    "resolve_host",
    "open_reverse_tunnel",
    "ReverseTunnel",
    "keys",
    "SSHError",
    "HostResolveError",
    "ConnectError",
    "AuthError",
    "BootstrapFailed",
    "KeyDeployError",
    "TunnelError",
]

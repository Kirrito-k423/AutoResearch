"""autoresearch.bmc — 带外管理 (BMC) skill.

支持 Redfish 协议 (iBMC 等), 走 HTTPS + Basic Auth.
默认 power off/on/cycle 是 dry-run; 须加 --apply 才执行真实下电上电.
"""
from .client import (
    BMCClient,
    BMCError,
    BMCPowerState,
    BMCSystemInfo,
    build_bmc_client,
)
from .identify import identify_server
from .power import power_status, power_off, power_on, power_cycle

__all__ = [
    "BMCClient",
    "BMCError",
    "BMCPowerState",
    "BMCSystemInfo",
    "build_bmc_client",
    "identify_server",
    "power_status",
    "power_off",
    "power_on",
    "power_cycle",
]

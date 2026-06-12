"""Redfish BMC 客户端 (D-32).

设计原则:
- 走标准 Redfish REST API + HTTPS Basic Auth
- 不引第三方依赖, 纯 requests
- 不静默吞错; 任何 HTTP / JSON 错误抛 BMCError (含 status + body 摘要)
- SSL verify 默认 False (内网 BMC 普遍自签证书), 提供 verify 参数
- 不带 session 持久化 (CLI 单次调用就够)
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from enum import Enum
from typing import Any
import json

import requests

from workspace_core.config import BMCSpec
from workspace_core.progress import emit_progress


class BMCError(Exception):
    """BMC 调用失败. 包含 status + body 摘要."""


class BMCPowerState(str, Enum):
    """Redfish PowerState 枚举 (我们关心的子集)."""

    ON = "On"
    OFF = "Off"
    POWERING_ON = "PoweringOn"
    POWERING_OFF = "PoweringOff"
    UNKNOWN = "Unknown"

    @classmethod
    def from_redfish(cls, value: str | None) -> "BMCPowerState":
        if not value:
            return cls.UNKNOWN
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN


@dataclass
class BMCSystemInfo:
    """BMC 拿到的机器唯一识别信息 (D-32 双源)."""

    bmc_uuid: str | None
    bmc_hostname: str | None
    system_serial: str | None
    system_sku: str | None
    system_model: str | None
    system_manufacturer: str | None
    power_state: BMCPowerState
    raw_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "bmc_uuid": self.bmc_uuid,
            "bmc_hostname": self.bmc_hostname,
            "system_serial": self.system_serial,
            "system_sku": self.system_sku,
            "system_model": self.system_model,
            "system_manufacturer": self.system_manufacturer,
            "power_state": self.power_state.value,
            "raw_summary": self.raw_summary,
        }


class BMCClient:
    """单次会话的 Redfish 客户端."""

    def __init__(
        self,
        spec: BMCSpec,
        *,
        verify_ssl: bool = False,
        timeout: float = 8.0,
    ) -> None:
        self.spec = spec
        self.base_url = f"https://{spec.host}:{spec.port}"
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._session = requests.Session()
        token = base64.b64encode(
            f"{spec.user}:{spec.password}".encode("utf-8")
        ).decode("ascii")
        self._session.headers.update(
            {
                "Authorization": f"Basic {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "OData-Version": "4.0",
            }
        )

    def _get(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            resp = self._session.get(
                url, timeout=self.timeout, verify=self.verify_ssl
            )
        except requests.RequestException as exc:
            raise BMCError(f"BMC GET {url} 网络错误: {exc}") from exc
        if resp.status_code != 200:
            raise BMCError(
                f"BMC GET {url} HTTP {resp.status_code}: "
                f"{resp.text.strip()[:200]}"
            )
        try:
            return resp.json()
        except json.JSONDecodeError as exc:
            raise BMCError(f"BMC GET {url} 响应非 JSON: {exc}") from exc

    def _post(self, path: str, body: dict[str, Any]) -> tuple[int, str]:
        url = f"{self.base_url}{path}"
        try:
            resp = self._session.post(
                url,
                json=body,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
        except requests.RequestException as exc:
            raise BMCError(f"BMC POST {url} 网络错误: {exc}") from exc
        return resp.status_code, resp.text.strip()[:200]

    # === Redfish 公开 API ===

    def get_service_root(self) -> dict[str, Any]:
        """GET /redfish/v1 — 探活 + 拿版本信息."""
        return self._get("/redfish/v1")

    def get_managers(self) -> list[dict[str, Any]]:
        """返回所有 manager 的 OdataId 列表."""
        data = self._get("/redfish/v1/Managers")
        members = data.get("Members", [])
        return [
            m.get("@odata.id")
            for m in members
            if isinstance(m, dict) and m.get("@odata.id")
        ]

    def get_manager_info(self, manager_id: str = "1") -> dict[str, Any]:
        """GET /redfish/v1/Managers/{id} — 含 FirmwareVersion, UUID."""
        return self._get(f"/redfish/v1/Managers/{manager_id}")

    def get_systems(self) -> list[dict[str, Any]]:
        """返回所有 system 的 OdataId 列表."""
        data = self._get("/redfish/v1/Systems")
        members = data.get("Members", [])
        return [
            m.get("@odata.id")
            for m in members
            if isinstance(m, dict) and m.get("@odata.id")
        ]

    def get_system_info(self, system_id: str = "1") -> dict[str, Any]:
        """GET /redfish/v1/Systems/{id} — 含 SerialNumber, SKU, PowerState."""
        return self._get(f"/redfish/v1/Systems/{system_id}")

    def get_power_state(self, system_id: str = "1") -> BMCPowerState:
        """直接读 PowerState 字段."""
        info = self.get_system_info(system_id)
        return BMCPowerState.from_redfish(info.get("PowerState"))

    def reset_system(
        self,
        reset_type: str,
        system_id: str = "1",
    ) -> tuple[int, str]:
        """POST /redfish/v1/Systems/{id}/Actions/ComputerSystem.Reset.

        reset_type: "On" | "ForceOff" | "GracefulShutdown" | "PowerCycle" |
                    "GracefulRestart" | "ForceRestart"
        """
        path = (
            f"/redfish/v1/Systems/{system_id}/"
            "Actions/ComputerSystem.Reset"
        )
        return self._post(path, {"ResetType": reset_type})

    def close(self) -> None:
        self._session.close()


def build_bmc_client(spec: BMCSpec, *, verify_ssl: bool = False) -> BMCClient:
    """从 BMCSpec 构造客户端 (CLI 入口统一用这个)."""
    emit_progress("bmc.connect", host=spec.host, port=spec.port)
    return BMCClient(spec, verify_ssl=verify_ssl)

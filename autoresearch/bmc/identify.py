"""BMC identify: 拿机器唯一硬件编码 (D-32).

来源 (优先级):
  1. /redfish/v1/Systems/{id}.SerialNumber
  2. /redfish/v1/Systems/{id}.SKU
  3. /redfish/v1/Managers/{id}.UUID (BMC UUID)
  4. /redfish/v1/Managers/{id}.HostName

最终 result.bmc_identifier = 第一个非空值 (UUID > Serial > SKU).
"""
from __future__ import annotations

from typing import Any

from workspace_core.config import BMCSpec
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity

from .client import BMCClient, BMCError, BMCPowerState, BMCSystemInfo, build_bmc_client


def _first_nonempty(*values: str | None) -> str | None:
    for v in values:
        if v and v.strip():
            return v.strip()
    return None


def identify_server(
    spec: BMCSpec,
    *,
    verify_ssl: bool = False,
) -> CheckResult:
    """走 Redfish 拉机器标识; 任何子查询失败都记录 warning, 不整体 fail."""
    data: dict[str, Any] = {"bmc_host": spec.host, "bmc_port": spec.port}
    warnings: list[str] = []
    try:
        client = build_bmc_client(spec, verify_ssl=verify_ssl)
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message="BMC 客户端构造失败",
            error=str(exc),
        )

    try:
        bmc_uuid: str | None = None
        bmc_hostname: str | None = None
        system_serial: str | None = None
        system_sku: str | None = None
        system_model: str | None = None
        system_manufacturer: str | None = None
        power_state = None
        try:
            managers = client.get_managers()
            if managers:
                manager_info = client.get_manager_info()
                bmc_uuid = manager_info.get("UUID")
                bmc_hostname = manager_info.get("HostName")
            else:
                warnings.append("BMC 无 manager 成员")
        except BMCError as exc:
            warnings.append(f"manager 字段拉取失败: {exc}")

        try:
            systems = client.get_systems()
            if systems:
                sys_info = client.get_system_info()
                system_serial = sys_info.get("SerialNumber")
                system_sku = sys_info.get("SKU")
                system_model = sys_info.get("Model")
                system_manufacturer = sys_info.get("Manufacturer")
                ps = sys_info.get("PowerState")
                power_state = BMCPowerState.from_redfish(ps)
            else:
                warnings.append("BMC 无 system 成员")
        except BMCError as exc:
            warnings.append(f"system 字段拉取失败: {exc}")

        identifier = _first_nonempty(
            bmc_uuid,
            system_serial,
            system_sku,
        )
        info = BMCSystemInfo(
            bmc_uuid=bmc_uuid,
            bmc_hostname=bmc_hostname,
            system_serial=system_serial,
            system_sku=system_sku,
            system_model=system_model,
            system_manufacturer=system_manufacturer,
            power_state=power_state
            if power_state is not None
            else BMCPowerState.UNKNOWN,
            raw_summary=identifier or "(no identifier)",
        )
        data.update(info.to_dict())
        data["bmc_identifier"] = identifier

        if identifier is None:
            return CheckResult(
                ok=False,
                severity=CheckSeverity.FAIL,
                data=data,
                message="BMC 未返回任何唯一编码 (UUID/Serial/SKU 全空)",
                error="; ".join(warnings) or "no identifier",
            )

        emit_progress("bmc.identify", host=spec.host, identifier=identifier)
        return CheckResult(
            ok=True,
            severity=CheckSeverity.WARN if warnings else CheckSeverity.OK,
            data=data,
            message=(
                f"BMC 唯一编码已记录: {identifier[:24]}"
                + ("..." if identifier and len(identifier) > 24 else "")
            ),
            error=None,
        )
    except BMCError as exc:
        return CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message="BMC 标识拉取失败",
            error=str(exc),
        )
    finally:
        client.close()

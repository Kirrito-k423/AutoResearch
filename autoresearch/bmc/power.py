"""BMC 电源控制 (D-32).

默认 DRY-RUN: --apply 不传, 仅打印意图.
传 --apply 才真正下 POST Reset.

安全门 (D-32):
  1. config.bmc.power_operations_allowed = false → 任何 --apply 都拒绝
  2. 默认无 --apply → 只返回 'would do X'
  3. 操作类型白名单: On / ForceOff / PowerCycle
"""
from __future__ import annotations

from typing import Literal

from workspace_core.config import BMCSpec
from workspace_core.progress import emit_progress
from workspace_core.result import CheckResult, CheckSeverity

from .client import BMCClient, BMCError, BMCPowerState, build_bmc_client


PowerOp = Literal["off", "on", "cycle", "status"]


_RESET_TYPE_MAP: dict[str, str] = {
    "off": "ForceOff",
    "on": "On",
    "cycle": "PowerCycle",
}


def _power_op(
    spec: BMCSpec,
    *,
    op: PowerOp,
    apply: bool = False,
    verify_ssl: bool = False,
) -> CheckResult:
    """统一电源操作入口."""
    data: dict = {
        "bmc_host": spec.host,
        "bmc_port": spec.port,
        "operation": op,
        "apply_requested": apply,
    }
    if op == "status":
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
            state = client.get_power_state()
            data["power_state"] = state.value
            return CheckResult(
                ok=True,
                severity=CheckSeverity.OK,
                data=data,
                message=f"BMC 电源状态: {state.value}",
                error=None,
            )
        except BMCError as exc:
            return CheckResult(
                ok=False,
                severity=CheckSeverity.FAIL,
                data=data,
                message="BMC 电源状态拉取失败",
                error=str(exc),
            )
        finally:
            client.close()

    reset_type = _RESET_TYPE_MAP[op]

    # 双重保险: config 未授权, 任何 apply 都拒绝
    if apply and not spec.power_operations_allowed:
        return CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message=(
                f"refuse to {op} (ResetType={reset_type}): "
                "config bmc.power_operations_allowed=false (默认安全)"
            ),
            error="power_operations_allowed=false",
        )

    if not apply:
        return CheckResult(
            ok=True,
            severity=CheckSeverity.OK,
            data={**data, "would_send": reset_type},
            message=(
                f"DRY-RUN: would POST ResetType={reset_type} to "
                f"{spec.host}:{spec.port} (use --apply to execute)"
            ),
            error=None,
        )

    # apply + 授权 → 真打
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
        emit_progress("bmc.power.apply", host=spec.host, op=op, reset_type=reset_type)
        status_code, body = client.reset_system(reset_type)
        data["http_status"] = status_code
        data["response_body"] = body
        if status_code in (200, 202, 204):
            return CheckResult(
                ok=True,
                severity=CheckSeverity.OK,
                data=data,
                message=f"BMC 已接受 {op} (ResetType={reset_type})",
                error=None,
            )
        return CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message=f"BMC 拒绝 {op} (HTTP {status_code})",
            error=body,
        )
    except BMCError as exc:
        return CheckResult(
            ok=False,
            severity=CheckSeverity.FAIL,
            data=data,
            message=f"BMC {op} 失败",
            error=str(exc),
        )
    finally:
        client.close()


def power_status(spec: BMCSpec, **kw) -> CheckResult:
    return _power_op(spec, op="status", **kw)


def power_off(spec: BMCSpec, **kw) -> CheckResult:
    return _power_op(spec, op="off", **kw)


def power_on(spec: BMCSpec, **kw) -> CheckResult:
    return _power_op(spec, op="on", **kw)


def power_cycle(spec: BMCSpec, **kw) -> CheckResult:
    return _power_op(spec, op="cycle", **kw)

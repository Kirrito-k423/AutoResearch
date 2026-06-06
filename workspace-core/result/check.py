"""统一 skill/check 返回结构 (D-21)."""
from __future__ import annotations

from enum import Enum
from typing import Any, TypedDict


class CheckSeverity(str, Enum):
    """check 严重度三档."""

    OK = "ok"
    WARN = "warn"
    FAIL = "fail"


# 显式 priority (越大越严重), 避免依赖字符串字母序
_SEVERITY_PRIORITY: dict[CheckSeverity, int] = {
    CheckSeverity.OK: 0,
    CheckSeverity.WARN: 1,
    CheckSeverity.FAIL: 2,
}


class CheckResult(TypedDict):
    """单次 check 的返回结构.

    字段语义:
    - ok:      True/False, 整体成功/失败 (binary); severity 反映细分等级
    - severity: OK/WARN/FAIL, 用于"硬失败"vs"告警继续"分层
    - data:    结构化结果 (e.g. {"latency_ms": 42, "host": "nvidia-01"})
    - message: 一行中文/英文描述
    - error:   失败时的技术细节 (None 表示无错)
    """

    ok: bool
    severity: CheckSeverity
    data: dict[str, Any]
    message: str
    error: str | None


def ok(data: dict[str, Any] | None = None, message: str = "ok") -> CheckResult:
    """构造一个成功的 CheckResult."""
    return CheckResult(
        ok=True,
        severity=CheckSeverity.OK,
        data=data or {},
        message=message,
        error=None,
    )


def fail(
    error: str,
    data: dict[str, Any] | None = None,
    message: str = "fail",
    severity: CheckSeverity = CheckSeverity.FAIL,
) -> CheckResult:
    """构造一个失败的 CheckResult (默认 FAIL, 也可传 WARN 降级)."""
    return CheckResult(
        ok=False,
        severity=severity,
        data=data or {},
        message=message,
        error=error,
    )


def merge(results: list[CheckResult]) -> CheckResult:
    """合并多个 check 结果. 严重度取最高档: FAIL > WARN > OK.

    注: 不能用 max(..., key=lambda r: r["severity"].value), 因为字符串字母序
    与语义顺序不一致 (ASCII 里 'o' > 'f', "ok" > "fail"), 用 _SEVERITY_PRIORITY
    显式映射.
    """
    if not results:
        return CheckResult(
            ok=True,
            severity=CheckSeverity.OK,
            data={"count": 0, "failed": 0, "warned": 0},
            message="no checks run",
            error=None,
        )
    severity = max(results, key=lambda r: _SEVERITY_PRIORITY[r["severity"]])[
        "severity"
    ]
    overall_ok = severity == CheckSeverity.OK
    errors = [r["error"] for r in results if r["error"]]
    return CheckResult(
        ok=overall_ok,
        severity=severity,
        data={
            "count": len(results),
            "failed": sum(1 for r in results if r["severity"] == CheckSeverity.FAIL),
            "warned": sum(1 for r in results if r["severity"] == CheckSeverity.WARN),
        },
        message=f"merged {len(results)} checks",
        error="; ".join(errors) if errors else None,
    )

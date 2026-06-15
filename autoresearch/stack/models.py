"""autoresearch.stack.models — TypedDict definitions for stack check results."""
from __future__ import annotations

from typing import TypedDict


class LibraryCheck(TypedDict):
    """单 library 检测结果."""

    library: str                  # "verl" / "veomni" / "torch" / "torch_npu"
    version: str | None           # 库版本, e.g. "0.2.0"
    ok: bool
    detail: str | None            # 错误信息 or extra context
    warning: str | None           # best-effort warn (D-41.C6)


class CondaEnvProbe(TypedDict):
    """conda env 探测结果."""

    name: str                     # 期望 env 名
    exists: bool
    python_version: str | None    # env 内 python 版本
    detail: str | None


class OneStepResult(TypedDict):
    """1-step 干跑结果 (D-41, NPU 适配)."""

    ok: bool
    npu_device_count: int | None
    sum_value: float | None        # SUM=<float> 透出
    elapsed_ms: int | None
    detail: str | None
    warning: str | None


class StackResult(TypedDict):
    """单 server stack check 汇总."""

    server: str
    ok: bool
    severity: str                 # "ok" / "warn" / "fail"
    conda_env: CondaEnvProbe
    libraries: dict[str, LibraryCheck]   # library -> check
    one_step: OneStepResult | None
    error: str | None


class StackSummary(TypedDict):
    """Aggregate --all 结果."""

    total: int
    passed: int
    failed: int
    warned: int
    passed_servers: list[str]
    failed_servers: list[str]
    results: dict[str, StackResult]

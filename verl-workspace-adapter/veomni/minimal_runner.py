"""verl-workspace-adapter.veomni.minimal_runner — veomni 1-step 干跑 (D-44).

复用 Phase 7 D-41 1-step 脚本 (torch_npu + lib).
不引 veomni SDK / 训练脚本, 走 `python -c "..."` 单进程.
"""
from __future__ import annotations

import time
from typing import TypedDict

from workspace_core.config import ServerSpec
from workspace_core.ssh import CommandTimeoutError

from ..common.conda_utils import run_in_env
from ..verl.minimal_runner import (
    ONE_STEP_SCRIPT_TMPL,
    MinimalResult,
    _parse_one_step_output,
)


def run_minimal(
    spec: ServerSpec,
    conda_env: str = "",
    workdir: str = "",
    lib: str = "veomni",
    timeout: float = 30.0,
) -> MinimalResult:
    """远程跑 1-step 干跑 (veomni), 返回 MinimalResult (D-44).

    跟 verl runner 同结构, lib 默认 veomni.
    """
    # 用 {lib} 替换 lib 占位; 模板默认 verl, 替换第一次出现
    script = ONE_STEP_SCRIPT_TMPL.replace("verl", lib, 1)
    safe_script = script.replace('"', '\\"').replace("\n", "; ")
    command = f'python -c "{safe_script}"'

    t0 = time.perf_counter()
    try:
        ec, so, se = run_in_env(spec, command, conda_env=conda_env, workdir=workdir, timeout=timeout)
    except CommandTimeoutError as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=True,
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        return MinimalResult(
            lib=lib, sum_value=None, npu_count=None, elapsed_ms=elapsed,
            exit_code=-1, stdout="", stderr="", error=str(e), timeout=False,
        )
    elapsed = int((time.perf_counter() - t0) * 1000)
    sum_val, npu_count = _parse_one_step_output(so)
    return MinimalResult(
        lib=lib, sum_value=sum_val, npu_count=npu_count, elapsed_ms=elapsed,
        exit_code=ec, stdout=so, stderr=se, error=None, timeout=False,
    )

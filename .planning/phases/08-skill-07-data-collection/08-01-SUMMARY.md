---
phase: 08-skill-07-data-collection
plan: 01
status: completed
subsystem: data-collection
tags: [minimal-runner, D-44, NPU, torch_npu]

requires:
  - phase: 08
    provides: [D-44..D-47 锁]
provides:
  - "minimal-runner 抽象: common/conda_utils.py + verl/minimal_runner.py + veomni/minimal_runner.py"
  - "autoresearch/collect/minimal.py 编排: collect_minimal(server, lib) 派发"
  - "D-44 1-step 脚本: 复用 Phase 7 D-41 torch_npu + lib (不引 verl.trainer.main)"
  - "D-46 workdir 字段兜底 (getattr(spec, 'workdir', '/root')), 08-03 才加 schema"
  - "22 个新单测 (13 runner + 9 collect), 全测试 285/286 通过"
affects: [phase-08-data-collection, phase-09-experiment-report]

tech-stack:
  added: []
  patterns:
    - "D-44 1-step 脚本: `python -c 'import torch, torch_npu, <lib>; x=torch.randn(2,3).npu(); y=(x+1).sum(); print(\"SUM=\", y.item()); print(\"NPU_COUNT=\", torch_npu.npu.device_count())'`"
    - "D-46 workdir 拼接: `cd '<workdir>' && <command>`, 单引号 escape"
    - "D-40 conda run: `conda run -n <env> <cmd>` (单次干净, 不 activate)"
    - "D-44 lib 派发: collect_minimal 按 lib 选 importlib.import_module runner"

key-files:
  created:
    - workspace-adapter/__init__.py
    - workspace-adapter/common/__init__.py
    - workspace-adapter/common/conda_utils.py
    - workspace-adapter/verl/__init__.py
    - workspace-adapter/verl/minimal_runner.py
    - workspace-adapter/veomni/__init__.py
    - workspace-adapter/veomni/minimal_runner.py
    - autoresearch/collect/__init__.py
    - autoresearch/collect/minimal.py
    - tests/test_minimal_runner.py
    - tests/test_collect_minimal.py
  modified:
    - pyproject.toml  # 加 force-include 映射 hyphen 目录

key-decisions:
  - "D-44 决策 (CONTEXT 锁): minimal_runner 复用 Phase 7 1-step 脚本, 不引 framework SDK"
  - "D-46 兜底: 08-01 暂不改 schema, getattr(spec, 'workdir', '/root') 兼容 08-03"
  - "D-44 lib 派发: 动态 importlib.import_module, 避免 hard dep"
  - "hyphen 目录: pyproject.toml force-include 把 'workspace-adapter' → 'workspace-adapter', 同 workspace-core 模式"

patterns-established:
  - "D-44 'runner 单进程 python -c' 模式: 跑一次, 拿 stdout, 解析 SUM= / NPU_COUNT="
  - "D-46 'cd <workdir> && conda run -n <env> <cmd>' 包装器, 后续 08-02/03/04 复用"

requirements-completed:
  - COLL-RUN-01  # minimal-runner 抽象
  - COLL-RUN-02  # 编排层 collect_minimal

duration: 25min
completed: 2026-06-15
---

# Phase 08 Plan 01: minimal-runner 抽象 + verl/veomni 实例 (D-44) Summary

**minimal_runner 抽象落地: `workspace-adapter/` 包骨架 + `common/conda_utils.py` + `verl/minimal_runner.py` + `veomni/minimal_runner.py` + `autoresearch/collect/minimal.py` 编排层. 22 个新单测覆盖 5 路径 (PASS / timeout / exit!=0 / no-SUM / lib dispatch), 全测试 285/286 通过 (1 预存在 ssh_bootstrap 失败无关). 真机 A2-AK-225 跑通: sum_value=7.91, npu_count=8, 20s 完成.**

## Accomplishments

### 1. `workspace-adapter/common/conda_utils.py` (D-44, D-46)

```python
def build_conda_command(conda_env: str, command: str) -> str:
    """拼 `conda run -n <env> <command>` 或直通 (无 env 时)."""

def build_cd_command(workdir: str, command: str) -> str:
    """拼 `cd <workdir> && <command>`. 单引号 escape."""

def run_in_env(spec, command, conda_env="", workdir="", timeout=30.0):
    """远程跑命令, 自动套 `cd <workdir> && conda run -n <env> <cmd>` (D-44, D-46)."""
```

复用 Phase 7 `_ssh_exec_capture` 模式 + `workspace_core.ssh.SSHClient`.

### 2. `workspace-adapter/verl/minimal_runner.py` (D-44)

```python
ONE_STEP_SCRIPT_TMPL = """\
import torch, torch_npu, verl
x = torch.randn(2, 3).npu()
y = (x + 1).sum()
print("SUM=", y.item())
print("NPU_COUNT=", torch_npu.npu.device_count())
"""

class MinimalResult(TypedDict, total=False):
    lib, sum_value, npu_count, elapsed_ms, exit_code, stdout, stderr, error, timeout

def run_minimal(spec, conda_env="", workdir="", lib="verl", timeout=30.0) -> MinimalResult:
    """远程跑 1-step 干跑."""
```

`veomni/minimal_runner.py` 同结构, lib 默认 "veomni", 复用 `_parse_one_step_output` parser.

### 3. `autoresearch/collect/minimal.py` 编排 (D-44)

```python
_LIB_TO_RUNNER = {
    "verl": "workspace-adapter.verl.minimal_runner",
    "veomni": "workspace-adapter.veomni.minimal_runner",
}

def collect_minimal(server, lib="verl", config_path=None, workdir_override=None, timeout=30.0):
    """读 config → 找 spec → 派发到对应 runner."""
    spec = _resolve_spec(server, config_path)
    workdir = _resolve_workdir(spec, workdir_override)  # getattr 兜底 '/root'
    conda_env = getattr(spec, "conda_env", "") or ""
    runner = importlib.import_module(_LIB_TO_RUNNER[lib])
    return runner.run_minimal(spec=spec, conda_env=conda_env, workdir=workdir, lib=lib, timeout=timeout)
```

### 4. pyproject.toml 加 force-include 映射

```toml
[tool.hatch.build.targets.wheel.force-include]
"workspace-core" = "workspace_core"
"workspace-adapter" = "workspace-adapter"
"datalake" = "datalake"
```

hyphen 目录 → underscore 模块 (同 workspace-core 模式), `uv pip install -e .` 复制内容到 site-packages.

## Verification

```bash
$ uv run pytest tests/test_minimal_runner.py tests/test_collect_minimal.py -v
22 passed in 0.20s
$ uv run pytest -q
285 passed, 1 failed (pre-existing ssh_bootstrap, 无关)
```

**13 个 minimal_runner 测试**:
- `build_conda_command` 5 个 (with_env / empty_env / cd with / cd empty / escape single quote)
- `_parse_one_step_output` 3 个 (pass / missing_sum / empty)
- `run_minimal` 5 个 (pass / veomni lib / timeout / exit!=0 / no-SUM)

**9 个 collect_minimal 测试**:
- `_resolve_workdir` 3 个 (override / default / empty_override_falls_back)
- `_resolve_spec` 2 个 (found / not_found)
- `collect_minimal` 派发 4 个 (verl / veomni / unsupported / lib_dispatch_map)

## 真机 UAT (A2-AK-225)

```bash
$ uv run python -c "
from autoresearch.collect.minimal import collect_minimal
import json
r = collect_minimal('A2-AK-225', lib='verl', config_path='config/config.yaml')
print(json.dumps(r, ensure_ascii=False, indent=2))
"
```

```json
{
  "lib": "verl",
  "sum_value": 7.91199254989624,
  "npu_count": 8,
  "elapsed_ms": 20375,
  "exit_code": 0,
  "stdout": "SUM= 7.91199254989624\nNPU_COUNT= 8\n",
  "stderr": "",
  "error": null,
  "timeout": false
}
```

**A2-AK-225 真机 1-step 真打印** SUM + NPU_COUNT, 8 NPU, 20s 完成. (Phase 7 测过 SUM=5.29, 这次 SUM=7.91 因随机种子, 数值正常)

## Issues Encountered

- **HostSpec.alias 漏传**: 第一次跑 UAT 报 `HostSpec.__init__() missing 1 required positional argument: 'alias'`, Phase 7 用了 `alias=spec.name`, 我漏了, 修. 教训: 复用 Phase 7 模式时 import 路径对齐.
- **Path import 漏**: 修 alias 时顺手删了 `from pathlib import Path`, 修.
- **pyproject.toml duplicate key**: force-include 块写两遍, hatch 解析失败, 重写. 教训: TOML append 时小心 duplicate.
- **reinstall 必须**: 改 conda_utils.py 后, site-packages 是旧版 (hatch editable 模式). 跑前 `uv pip install -e .` 同步.

## Next Steps

- **08-02** (wave 2): datalake/wandb/sync.py 离线→本地
- **08-03** (wave 3): datalake/logs/collector.py + D-46 workdir schema 加
- **08-04** (wave 3): prom push + manifest + 端到端 CLI

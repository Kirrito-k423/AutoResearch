---
phase: 07-skill-06-train-stack-health
plan: 01
status: completed
subsystem: train-stack-health
tags: [conda, verl, veomni, library-detect, D-39, D-40, D-42]

requires: []
provides:
  - `ServerSpec.conda_env` 字段 (D-40.B1, 默认空字符串)
  - `autoresearch/stack/` 模块: 库检测 + conda env 探测 + 1-step 干跑 (D-41 NPU 适配预留)
  - `autoresearch stack check --server X` CLI
affects: [phase-07-train-stack-health, phase-08-data-collection]

tech-stack:
  added: []
  patterns:
    - "D-39: 库检测走 `python -c 'import <lib>; print(<lib>.__version__)'` (单 import 验证)"
    - "D-40: conda env 探测走 `conda env list | grep <env>`"
    - "D-40: 有 env 时 `conda run -n <env> python -c ...`; 无 env 走系统 python"
    - "D-42 失败诊断 3 类: env 缺失 / import 失败 / 1-step 超时"

key-files:
  created:
    - autoresearch/stack/__init__.py
    - autoresearch/stack/models.py
    - autoresearch/stack/checker.py
    - tests/test_stack_checker.py
    - tests/test_stack_cli.py
  modified:
    - workspace-core/config/schema.py
    - autoresearch/cli.py

key-decisions:
  - "D-40.B1: ServerSpec.conda_env 默认空字符串, 留空 = 走系统 python"
  - "D-40.B5: config.example.yaml 4 台 server 配 `conda_env: verl-env` (用户实际配时按 conda env 实际名)"
  - "D-39 走 `conda run -n <env>` (不 activate, 单次干净), timeout 12s 默认"
  - "D-42 诊断含 env 名 + lib 名 + 命令 (e.g. `conda env create -f <env>.yml`)"

patterns-established:
  - "07-01 库检测模板: `_check_library_command` 拼 `conda run -n <env> python -c "import <lib>; print(<lib>.__version__)"`
  - "07-01 conda env 探测模板: 解析 `conda env list` 输出, 匹配 `^<env>\\s+(\\S+)`"

requirements-completed:
  - STACK-VERL-01   # verl 库检测
  - STACK-VEOMNI-01 # veomni 库检测

duration: 25min
completed: 2026-06-12
---

# Phase 07 Plan 01: conda_env 字段 + 库检测 Summary

**`ServerSpec.conda_env` 字段就绪 + 库检测实现 + CLI 接入. 21 个新单测全绿, 260/261 全测试通过.**

## Accomplishments

- **D-40 conda_env 字段**: `ServerSpec.conda_env: str = ""` (默认空), 走 `conda run -n <env>` 或系统 python
- **D-39 库检测**: 远程 `python -c "import <lib>; print(<lib>.__version__)"`
- **D-40 conda env 探测**: 远程 `conda env list` 解析, 匹配 env 名存在性
- **D-42 失败诊断**: 3 类 (env 缺失 → `conda env create` 提示; import 失败 → `pip install` 提示; 1-step 超时预留)
- **CLI**: `autoresearch stack check --server X` 接 `--all` (互斥) + `--lib` (多次叠加)
- **21 个新单测**:
  - D-41 脚本用 torch_npu (不是 CUDA) — `test_one_step_script_uses_torch_npu_not_cuda`
  - D-42 env 缺失诊断含 env 名
  - ConfigError -> fail
  - 库检测 PASS / FAIL (ImportError 诊断)
  - 1-step 干跑 4 路径 (PASS / timeout / exit!=0 / no-SUM)
  - top-level 汇总 (happy / env_missing / one_step_timeout)
  - CLI 5 路径 (help / missing / both / forwarding)

## Verification

- `uv run pytest tests/test_stack_checker.py tests/test_stack_cli.py -v` → **21 passed**
- `uv run pytest -q` → **260 passed, 1 failed (pre-existing ssh_bootstrap)**
- `uv run autoresearch stack --help` → ✅
- `uv run autoresearch stack check --help` → ✅
- **真机 UAT** (A2-AK-225, config 没配 conda_env 走系统 python):
  - **verl import OK** — version=0.8.0.dev ✅
  - **veomni import FAIL** — `ModuleNotFoundError: No module named 'veomni'` (用户未装, 符合预期)
  - 1-step 跳过 (env 没配)
  - **诊断链路完整**, 错误信息含 traceback

## Issues Encountered

- **预存在失败** `test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix`: 跟 04-04 一起存在, 与本 plan 无关.
- **workspace-core editable install**: 改 `workspace-core/config/schema.py` 后 venv 不自动更新, 需要 `uv pip install -e .` (已执行).
- **pytest 把 `test_server_reach` 当 test**: Phase 6 reach 用了 `as _tester` alias 防 pick-up, Phase 7 stack 同样模式.

## Next Steps

- Wave 2 (07-02): 1-step 干跑 NPU 适配已完成 (D-41 脚本就位), 只差 run_one_step_dryrun 单元测试覆盖 (test_one_step_* 已在 07-01 写完). 07-02 计划实为 07-01 的延伸, 但 07-02 PLAN.md 仍按原计划跑 UAT 验证 1-step 真机端到端.
- Wave 3 (07-03): `ar-stack check --all` 并发 + 4 台真机 UAT
- 用户后续: 装 veomni (如需要) 或在 config 配 `conda_env: verl-env` 触发 1-step 干跑


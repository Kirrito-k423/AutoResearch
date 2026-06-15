---
phase: 07-skill-06-train-stack-health
plan: 02
status: completed
subsystem: train-stack-health
tags: [one-step, dryrun, NPU, D-41]

requires:
  - phase: 07-01
    provides: [ServerSpec.conda_env, autoresearch.stack.checker]
provides:
  - 1-step 干跑 `run_one_step_dryrun` (D-41, NPU 适配走 torch_npu)
  - D-42 失败诊断 3 类 (env 缺失 / import 失败 / 1-step 超时)
  - 30s timeout 单独传 (D-41.C1)
  - result 透出 npu.device_count (D-41.C5)
affects: [phase-07-train-stack-health, phase-08-data-collection]

tech-stack:
  added: []
  patterns:
    - "D-41 1-step 脚本模板: `import torch, torch_npu, <lib>; x=torch.randn(2,3).npu(); y=(x+1).sum(); print('SUM=', y.item()); print('NPU_COUNT=', torch_npu.npu.device_count())`"
    - "D-41.C1: 1-step 走 30s timeout (12s 默认太短, 远程冷启 torch_npu 慢)"
    - "D-41.C5: result 透出 npu_device_count 给用户看"
    - "D-41.C6: 1-step 失败不阻塞 (warn 算 pass), 让用户判断"

key-files:
  created: []
  modified:
    - autoresearch/stack/checker.py
    - tests/test_stack_checker.py

key-decisions:
  - "D-41.C1: 1-step 30s timeout 单独传 (D-39 库检测用 12s 默认)"
  - "D-41.C2: 脚本固定用 `torch_npu` (不是 CUDA), 用户明确要求 NPU 适配"
  - "D-41.C5: result.npu_device_count 字段透出 NPU 数量"
  - "D-41.C6: 1-step 失败 -> severity=warn, overall ok=True (D-39 同样逻辑, 不阻塞)"
  - "D-42.D3: 1-step 30s 超时 -> warning 含 'NPU 通信问题, 先跑 autoresearch hw probe'"

patterns-established:
  - "D-41 1-step 4 失败路径完整: PASS / timeout / exit!=0 / no-SUM (各 warning 文案不同)"

requirements-completed:
  - STACK-VERL-02   # conda env 探测 (07-01 已就位, 07-02 整合进 check_stack)
  - STACK-VERL-03   # 1-step 干跑 (D-41 NPU 适配)
  - STACK-VEOMNI-02 # veomni conda env 探测
  - STACK-VEOMNI-03 # veomni 1-step 干跑

duration: 12min
completed: 2026-06-12
---

# Phase 07 Plan 02: 1-step 干跑 NPU 适配 + 失败诊断 Summary

**`run_one_step_dryrun` 实现 + D-41 NPU 适配 (torch_npu) + D-42 失败诊断 3 类. 5 个新单测覆盖 (PASS / timeout / exit!=0 / no-SUM), 260/261 全测试保持绿.**

## Accomplishments

- **D-41 1-step 脚本** (NPU 适配 — 用户明确要求):
  ```python
  import torch, torch_npu, <lib>
  x = torch.randn(2, 3).npu()
  y = (x + 1).sum()
  print("SUM=", y.item())
  print("NPU_COUNT=", torch_npu.npu.device_count())
  ```
  **不用 `verl.trainer.main(...)`** (CUDA 风格不适用, REQUIREMENTS.md 草稿作废)
- **D-41.C1 30s timeout**: 单独传 `client.exec(cmd, timeout=30.0)`, 不沿用 12s 默认
- **D-41.C5 npu_device_count**: result 多 `npu_device_count` 字段透出
- **D-41.C6 best-effort**: 1-step 失败 -> severity=warn, overall ok=True
- **D-42 失败诊断**:
  - env 缺失 -> `conda env create -f <env>.yml` 提示 (D-42.D1)
  - import 失败 -> `pip install 是否在 <env> 内` 提示 (D-42.D2)
  - 1-step 30s timeout -> `NPU 通信问题, 先跑 autoresearch hw probe` (D-42.D3)
  - 1-step exit != 0 -> `<lib> 可能 import 失败` (D-42 扩展)
  - 1-step stdout 无 `SUM=` -> `检查 torch_npu / <lib> 是否同 env` (D-42 扩展)

## Verification

- `uv run pytest tests/test_stack_checker.py -v` → **16 passed** (含 5 个 one_step_* 测试)
- `uv run pytest -q` → **260 passed, 1 failed (pre-existing ssh_bootstrap)**
- **真机 UAT** (A2-AK-225, `--lib verl`):
  - conda_env 未配 -> 1-step 跳过 (env_probe.exists=False)
  - 用户机器上 veomni 未装 (`ModuleNotFoundError`), 1-step 走通条件需先解决 veomni
  - **诊断链路完整**: env 缺失 + import 失败 都有可读错误
  - 真机端到端 1-step 干跑 (SUM + NPU_COUNT) 需用户在 config 配 conda_env 并确保 env 内有 torch_npu + verl

## Issues Encountered

- **预存在失败** `test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix`: 跟 04-04 一起存在, 与本 plan 无关.
- **真机端到端 1-step 干跑未跑通**: A2-AK-225 系统 python 没 torch_npu (在 conda env 内), 用户需:
  1. 在 config.servers[].conda_env 配实际 env 名 (e.g. `verl-env`)
  2. 确保 env 内 `pip install torch_npu` 已装
  3. 再跑 `autoresearch stack check --server X --lib verl` 触发 1-step

## Next Steps

- Wave 3 (07-03): `ar-stack check --all` 并发 + 4 台真机 UAT
- 用户后续: 配 conda_env + 装 torch_npu (如需要) 后重跑


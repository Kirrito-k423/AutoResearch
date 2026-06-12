# Phase 7: Skill 06 — train-stack-health - Context

**Gathered:** 2026-06-12
**Status:** Ready for planning
**Discussion mode:** user-approved defaults + 1 override (C, NPU 适配)

<domain>
## Phase Boundary

验证远程服务器 verl + veomni 各自的 conda env 健康, 能跑 1-step 干跑 (NPU 算子).
本 phase 是 "训练栈就绪" 验证, 不实际跑训练; 训练由 Phase 8 data-collection 接力.

**硬件前提: 服务器是 Ascend NPU (910B3 等), 不是 CUDA.** REQUIREMENTS.md
原 STACK-VERL-03 / STACK-VEOMNI-03 草稿写的 `verl.trainer.main(...)` 是 CUDA 风格,
本 phase 实施时按 NPU 适配 (torch_npu, 走 NPU 算子).

</domain>

<decisions>
## Implementation Decisions

### A. 库检测策略 (D-39, 默认)
- **D-39.A1:** `python -c "import <lib>; print(<lib>.__version__)"` (单 import 验可加载 + 拿版本)
- **D-39.A2:** 检测到 import OK + 输出版本号 -> PASS; ImportError -> FAIL
- **D-39.A3:** 不跑 `which verl` 之类 (conda env 里 exec 可能在 PATH 但 import 失败, 反之亦然)
- **D-39.A4:** 远程命令走 `conda run -n <env> python -c "..."` (不走 activate, conda run 是单次干净)

### B. conda env 探测 (D-40, 默认)
- **D-40.B1:** config.servers[].conda_env 加可选字段, 默认空字符串
- **D-40.B2:** 远程 `conda env list` 解析; 找不到 env 名 -> FAIL + 提示
- **D-40.B3:** config 有显式 conda_env 时, 走 `conda run -n <env>`; 没配时走 `python` (system)
- **D-40.B4:** 探到 env 但 import 失败, 提示"env 存在但 <lib> 不在, 检查 pip install"
- **D-40.B5:** 仓库内每台 server 配 verl-env / veomni-env (config.example.yaml 加示例)

### C. 1-step 干跑 (D-41, **NPU 适配 — 用户明确要求**)
- **D-41.C1:** 远程 `python -c "..."` 跑 NPU 张量 + verl/veomni 1-step, 30s timeout
- **D-41.C2 (NPU 适配核心):** 1-step 脚本走 `torch_npu` (不是 torch.cuda):
  ```python
  import torch, torch_npu
  import verl  # 或 veomni
  x = torch.randn(2, 3).npu()       # 走 NPU
  y = (x + 1).sum()
  print("SUM=", y.item())           # 触发 NPU 算子
  ```
  不再走 `verl.trainer.main(...)` (CUDA 风格不适用)
- **D-41.C3:** 1-step exit 0 + stdout 含 `SUM=`<数字> -> PASS
- **D-41.C4:** 1-step 30s timeout 触发 -> FAIL + 提示"driver/CUDA-NPU 通信问题, 跑 Phase 4 hw probe"
- **D-41.C5:** 输出 `npu.device_count()` 也读一下, 写到 result (透出 NPU 数量)
- **D-41.C6:** 1-step 失败不阻塞, 但需明确标 fail (D-39 同样逻辑)

### D. 失败诊断 (D-42, 默认)
- **D-42.D1:** env 缺失 (`conda env list` 无此 env) -> error 含 "请跑 `conda env create -f <env>.yml`"
- **D-42.D2:** import 失败 (env 存在但 lib 没装) -> error 含 "检查 pip install 是否在 <env> 内"
- **D-42.D3:** 1-step 超时 -> error 含 "NPU 通信问题, 先跑 autoresearch hw probe --server X"
- **D-42.D4:** 不做自动 conda env 修复 (用户决定装什么)

### 计划范围 (Wave 建议)
- **07-01 (Wave 1):** config 加 `conda_env` 字段 + 改 example.yaml 加 `verl-env` / `veomni-env`; `ar-stack` CLI group + 库检测 (D-39) + conda env 探测 (D-40)
- **07-02 (Wave 2):** 1-step 干跑 (D-41, NPU 适配) 远程执行; 单机 `ar-stack check --server X`; fail 诊断 (D-42)
- **07-03 (Wave 3, 选做):** `ar-stack check --all` 并发 + 4 台真机 UAT

### the agent's Discretion
- torch_npu 在 conda env 内的 import 失败处理 (重试 vs 直接 fail)
- result JSON 字段排序
- CLI `--json` 机读输出 (如需)

</decisions>

<canonical_refs>
## Canonical References

Downstream agents MUST read these before planning or implementing:

### SSH / 远程命令
- `workspace-core/ssh/client.py` — SSHClient.exec 走远程命令, 默认 timeout 12s (Phase 7 1-step 需 30s 单独传)
- `autoresearch/reach/tester.py` — Phase 6 reach tester 是 Phase 7 的最近邻, 复用 `_ssh_exec_capture` 模式
- `autoresearch/hw/probe.py` — `probe_server` 返回 HardwareData 模式, Phase 7 stack check 类似

### 服务 / 决策
- `autoresearch/bmc/identify.py` — Phase 4 BMC identify 跟 Phase 7 1-step 都属"远程走命令验某事", 模式可借鉴
- `.planning/phases/06-skill-05-service-reachability/06-CONTEXT.md` — 最近邻 phase, 风格/模板对齐
- `.planning/phases/05-skill-04-network-check/05-03-SUMMARY.md` — `net.tunnel.ensure_tunnel` 已为 Phase 6+ 暴露

### NPU 适配 (D-41 关键)
- 远程 Ascend 服务器标准库: `torch_npu` (Huawei 官方, 走 NPU 算子)
- `verl` / `veomni` 走 HuggingFace 风格, 底层兼容 torch + torch_npu (无需改)
- 1-step 验算子: `(torch.randn(2, 3).npu() + 1).sum().item()`

### 项目约定
- `AGENTS.md` §"进度协议模板" — 所有 CLI 子命令走 `__AR_PROGRESS__=` stderr
- `AGENTS.md` §"测试规范" — click.testing.CliRunner 测 CLI, pytest, 业务逻辑必须有断言

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `autoresearch.reach.tester._ssh_exec_capture` — 跑远程命令 + 返 (exit, stdout, stderr), Phase 7 1-step 复用
- `workspace_core.config.ServerSpec` — 已支持 identity_file / sudo_command / bmc, 加 conda_env 字段是 1 行
- `workspace_core.ssh.SSHClient.exec(command, timeout=...)` — timeout 可调, 1-step 30s 直接传

### Established Patterns
- CLI group: `@main.group(name="stack")` 类似 `@main.group(name="reach")` Phase 6
- 单机: `ar-stack check --server X`; 并发: `--all` (Phase 4 模式)
- CheckResult 模式: ok/severity/data/message/error 五字段

### Integration Points
- Phase 7 stack check -> 调 Phase 6 reach (但 Phase 7 范围是 env 验证, 不强制调 reach)
- Phase 7 stack check -> 调 Phase 4 hw probe 数据 (npu 数量参考, best-effort)
- Phase 7 stack check -> 为 Phase 8 data-collection 铺路 (1-step 真跑训练前先验 stack)

</code_context>

<specifics>
## Specific Ideas

- **NPU 适配是用户明确要求** — 不是默认, 写进 D-41 锁决策
- REQUIREMENTS.md STACK-VERL-03 / STACK-VEOMNI-03 原写 `verl.trainer.main(...)` 是 CUDA 风格, 实施时按 D-41 改 NPU
- torch_npu 在 conda env 内的可用性是 1-step 干跑的前置 (verl 可能没装 torch_npu, 这种 stack 标 WARN 而非 FAIL — 留给用户判断)

## Deferred Ideas

- 远程 conda env 创建 / pip install 自动修复 — 用户决定装什么 (D-42.D4)
- 多 framework (deepspeed / megatron) 检测 — Phase 7 范围只 verl + veomni
- CUDA-only fallback 模式 — 服务器是 NPU, 不需要

</specifics>

---

*Phase: 07-skill-06-train-stack-health*
*Context gathered: 2026-06-12*

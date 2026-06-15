---
phase: 11-orchestration
status: active
updated: 2026-06-15T15:35:00Z
---

# Phase 11: 顶层 CLI 编排 - Context

## Goal

交付两个面向用户的顶层命令：

- `autoresearch check all`：串跑 M1 最小循环的 readiness/check 部分，输出统一 step 报告。
- `autoresearch run smoke --server X`：执行 collect -> report，失败时指出挂在哪一步和原因。

## In Scope

- 新增顶层 CLI groups：`check` 与 `run`
- 新增 orchestration runtime/helper，复用现有 skill 的 Python `run_*` 入口
- 统一 step result JSON schema
- 进度事件走 `__AR_PROGRESS__=...` stderr
- 单测覆盖 happy path 和失败诊断

## Out of Scope

- 不新增新服务
- 不把 Archon 再包一层
- 不自动安装远程 `veomni`
- 不解决历史 Phase 4 BMC partial UAT

## Decisions

### A. 复用入口，不 shell 拼命令 (D-63)

- `check all` 与 `run smoke` 都直接调用现有 Python 函数，如 `run_validate`、`run_status`、`run_probe`、`run_reach_test`、`run_stack_check`、`run_collect`、`run_render`。
- 这样保留唯一 JSON stdout 和进度协议，不重复业务逻辑。

### B. `check all` 的 skill 7/8 语义 (D-64)

- `check all` 是 readiness check，不应该偷偷启动完整实验。
- Skill 7 data-collection readiness 通过输入解析、远程工作目录/训练栈前置检查结果间接覆盖，并输出 `skipped`/`ready` 状态。
- Skill 8 report readiness 检查本地 run/report 运行时能力是否可调用；实际 report 生成属于 `run smoke`。
- 真正 collect/report 闭环由 `run smoke` 覆盖。

### C. `run smoke` 是 Phase 11 的用户入口 (D-65)

- `run smoke` 串 `run_collect` -> `run_render`。
- 若 collect 失败，report step 标记 skipped，并在 summary 中给出 `failed_step=collect`。
- 若 report 失败，summary 给出 `failed_step=report`。
- 成功时输出 `run_id`、`manifest`、`report`、`warnings`。

### D. 真实服务器默认与可覆盖 (D-66)

- `--server` 对 `run smoke` 必填；`check all` 可以从 config 第一台服务器推断，也允许 `--server` 指定。
- `--lib` 默认 `verl`，因为当前真实服务器 `veomni` 未安装；用户可多次传 `--stack-lib` 给 `check all` 覆盖 stack check。
- `--remote-proxy-port` 默认 `17892` 给 `check all` 的 net step，避免与 reach/wandb 的 `17890` 冲突。

## Canonical References

- `.planning/ROADMAP.md` Phase 11
- `.planning/REQUIREMENTS.md` ORCH-*
- `autoresearch/archon/runtime.py`：Phase 10 已验证的编排映射
- `autoresearch/collect/cli.py`
- `autoresearch/report/cli.py`
- `workspace-core/progress/emitter.py`


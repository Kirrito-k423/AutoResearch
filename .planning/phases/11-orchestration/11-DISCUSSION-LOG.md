---
phase: 11-orchestration
status: discussed
updated: 2026-06-15T15:35:00Z
---

# Phase 11: 顶层 CLI 编排 - Discussion Log

## Discussion Pass 1: 用户入口边界

| Option | Outcome |
|---|---|
| 新增 `autoresearch check all` 和 `autoresearch run smoke` | ✓ |
| 只复用 `archon workflow run ar-min-loop` | |
| 把所有 orchestration 放到 shell 脚本 | |

**Decision:** 用户需要不依赖 Archon UI 的本地 CLI 入口；Phase 11 直接落到 `autoresearch` 单二进制。

## Discussion Pass 2: check 与 smoke 分工

| Option | Outcome |
|---|---|
| `check all` 做 readiness，不启动完整实验 | ✓ |
| `check all` 也执行 collect/report | |
| 只做服务健康检查 | |

**Decision:** `check all` 汇总前置健康；真正跑实验和报告由 `run smoke` 负责。

## Execution Notes

- 需要保证 stdout 是唯一 JSON 对象。
- 进度必须用 `emit_progress`。
- 单测先 mock 下游 skill 函数，真实 UAT 再用 A2-AK-225 + `verl` 跑。
- 当前真实环境 `veomni` 未安装，默认 smoke 使用 `verl`。


# Phase 10: Archon 适配层 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-15
**Phase:** 10-archon
**Areas discussed:** workflow asset layout, skill mapping, runtime contract, iterative execution, validation path

---

## Workflow asset layout

| Option | Description | Selected |
|--------|-------------|----------|
| Repo-local `.archon/workflows/` + `.archon/scripts/` | Workflow YAML 和 deterministic adapter 都跟仓走，最适合版本控制与 PR 审阅 | ✓ |
| 只写 YAML，节点里直接堆长 bash | 最少文件数，但参数解析和复用会迅速变脆 | |
| 依赖用户全局 `~/.archon/` 资产 | 可跨 repo 共享，但仓库内不可见、不可审计 | |

**User's choice:** auto-selected recommended default
**Notes:** 为了让 Phase 10 交付物跟仓库一起 ship，决定把资产都放在 repo-local `.archon/` 下。

---

## Skill mapping

| Option | Description | Selected |
|--------|-------------|----------|
| 包 happy path 主命令 | `config validate` / `services start+status` / `hw probe` / `collect run` / `report render` 这些真实运行路径进入 workflow | ✓ |
| 每个 workflow 覆盖整组 CLI | 把 init/show/debug 子命令也都包进去，范围更大 | |
| 只做一个总 workflow，不做 8 个 skill workflow | 实现更快，但不满足 `ARCH-WF-01` | |

**User's choice:** auto-selected recommended default
**Notes:** Phase 10 的重点是“能跑起来”，不是把全部维护命令都搬进 Archon。

---

## Runtime contract

| Option | Description | Selected |
|--------|-------------|----------|
| 环境变量 + `$ARTIFACTS_DIR` 文件交接 | `AR_SERVER` / `AR_LIB` 等输入覆盖，`collect-result.json` 之类文件在 workflow 内传递状态 | ✓ |
| 完全依赖 prompt 文本传参 | 实现轻，但 `run_id` / JSON handoff 很脆 | |
| 新增仓库级数据库或服务做状态中转 | 能力更强，但明显超出本 phase | |

**User's choice:** auto-selected recommended default
**Notes:** `collect -> report` 的 `run_id` 传递是关键风险，所以明确选择 artifact 文件交接。

---

## Iterative execution

| Option | Description | Selected |
|--------|-------------|----------|
| 真实 `loop:` 节点仅用于 STACK / COLL | STACK 做逐库处理，COLL 做有限重试，其他步骤保持 deterministic | ✓ |
| 所有 skill 都做 loop | 形式统一，但简单步骤被过度复杂化 | |
| 完全不用 `loop:`，只用 shell 重试 | 实现最省事，但不满足 `ARCH-WF-03` | |

**User's choice:** auto-selected recommended default
**Notes:** 只在确实有“迭代”含义的地方引入 `loop:`，既满足需求，也控制复杂度。

---

## Validation path

| Option | Description | Selected |
|--------|-------------|----------|
| 实装后补装/启用本机 Archon CLI，做 validate + run + Web UI 验证 | 覆盖 `ARCH-RUN-01/02` 的真实验收 | ✓ |
| 只交付 YAML，不做本机验证 | 风险低，但不能宣称 phase 完成 | |
| 把 Archon 改进 compose 再验证 | 会突破项目既有边界 | |

**User's choice:** auto-selected recommended default
**Notes:** 当前本机 `archon` 还没起，Phase 10 将顺手把这件事补上并纳入真实验证。

---

## the agent's Discretion

- `.archon/scripts/` 内部的 helper 拆分粒度
- `services` workflow 里 start/status 的具体组织方式
- artifact/state 文件的命名细节

## Deferred Ideas

- 基于 Archon 的顶层 `autoresearch check all` / `run smoke` 封装（Phase 11）
- provider/model profile 的 repo-level 预设
- Archon 调度、后台队列、云部署

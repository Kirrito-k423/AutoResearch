---
phase: 10-archon
type: context
status: locked
locked_at: 2026-06-15
discussion_mode: auto
locks:
  - D-56
  - D-57
  - D-58
  - D-59
  - D-60
---

# Phase 10: Archon 适配层 - Context

**Gathered:** 2026-06-15
**Status:** Ready for planning
**Discussion mode:** auto (user requested autonomous progression)

<domain>
## Phase Boundary

把已经完成的 8 个 AutoResearch skill 包装成 repo-local Archon workflow 资产，让用户既能单独触发每个 skill workflow，也能用一个主 workflow 从 config 校验一路串到 report 生成。

本 phase 的交付物是：

- `.archon/workflows/` 下的 8 个 skill workflow
- 主 workflow `ar-min-loop.yaml`
- 为这些 workflow 服务的 repo-local Archon script/runtime 资产
- 一套基于本机 Archon CLI / Web UI 的验证路径

本 phase **不**新增新的业务能力，不改 8 个 skill 的产品语义；它只把已经 ship 的 CLI 能力接进 Archon。

</domain>

<decisions>
## Implementation Decisions

### A. Archon 资产布局与入口复用 (D-56)
- **D-56.A1:** 所有 Phase 10 资产都落在 repo-local `.archon/` 下：workflow YAML 放 `.archon/workflows/`，可复用的 deterministic runtime 放 `.archon/scripts/`。
- **D-56.A2:** workflow 节点优先复用现有 Python 入口，不复制业务逻辑。具体做法是：Archon script node 调 repo-local Python 脚本，而这些脚本再调用现有 `run_*` 函数或稳定 CLI 入口。
- **D-56.A3:** 除了 `STACK` / `COLL` 的显式 loop 节点外，其余 skill 默认使用 deterministic script / bash node；不把简单串接问题重新做成 AI 推理问题。
- **D-56.A4:** repo 内 workflow **不硬编码 provider/model**；脚本节点本身不需要 AI，loop 节点继承用户本机 Archon 的默认 provider 配置，避免把仓库绑死到单一模型供应商。

### B. 8 个 skill 的 workflow 映射是“运行 happy path”，不是全 CLI 镜像 (D-57)
- **D-57.B1:** `ar-skill-01` 对应 `autoresearch config validate`，目标是验证已有配置，而不是在 workflow 里生成/覆写 config。
- **D-57.B2:** `ar-skill-02` 先确保本地 compose 服务启动，再做健康检查；也就是把 `services start` + `services status` 作为一个运维 happy path 包起来，而不是只查状态。
- **D-57.B3:** `ar-skill-03`..`ar-skill-08` 分别映射到现有主线命令：`hw probe`、`net probe`、`reach test`、`stack check`、`collect run`、`report render`。
- **D-57.B4:** 主 workflow 以“能从 config 一路跑到 report”为目标，因此复用这些 happy-path 节点，不额外引入 Phase 11 的 `check all` / `run smoke` 新编排能力。

### C. Workflow 运行参数与节点间交接契约 (D-58)
- **D-58.C1:** Phase 10 统一使用 Archon 运行环境变量作为输入覆盖层：`AR_CONFIG_PATH`、`AR_SERVER`、`AR_LIB`、`AR_TIMEOUT`、`AR_PUSHGATEWAY_URL`、`AR_RUN_ID`。
- **D-58.C2:** 默认值遵循“真实 UAT 优先”：
  - `AR_CONFIG_PATH` 默认 `config/config.yaml`
  - `AR_SERVER` 默认取 config 中第一台 server
  - `AR_LIB` 默认 `verl`
  - `AR_TIMEOUT` 默认 `60`
  - `AR_PUSHGATEWAY_URL` 默认 `http://127.0.0.1:17891`（复用 reach/tunnel 约定）
- **D-58.C3:** 节点间传递运行时数据（尤其 `collect` 产出的 `run_id`）不靠脆弱的 prompt 文本拼接，而是写到 Archon run 的 `$ARTIFACTS_DIR` 里，例如 `collect-result.json`、`stack-state.json` 这类显式文件。
- **D-58.C4:** `report` skill workflow 在 `AR_RUN_ID` 缺失时，优先读取同一次 Archon run 的 `collect-result.json`；这样主 workflow 不需要额外人工抄 run_id。

### D. `loop:` 只用于 STACK / COLL 的真实迭代场景 (D-59)
- **D-59.D1:** `ARCH-WF-03` 用真实的 Archon `loop:` 节点满足，而不是用 shell `for` 假装“迭代”。
- **D-59.D2:** `STACK` 的 loop 语义是“逐个库完成检查”：对 `verl` 和 `veomni` 分别执行 stack check，循环状态写入 artifact/state 文件，直到两者都处理完，再由后置总结节点给出整体 pass/fail。
- **D-59.D3:** `COLL` 的 loop 语义是“带上限的自动重试”：首次失败后允许有限次数重试，并把每次 attempt 的 payload、错误与最终 `run_id` 记录到 artifact/state 文件；停止条件由 `until_bash` 读取状态文件判定。
- **D-59.D4:** `ar-skill-06` / `ar-skill-07` 两个 standalone workflow 采用 Archon `loop:` 表达循环/重试语义；主 workflow 为保证在无 provider auth 的本机也能完成端到端 smoke run，调用这两个 skill 的 deterministic script 入口，由 runtime 内部执行同一套有界循环。

### E. 验证路径必须覆盖本地 CLI 与 Web UI 可观察性 (D-60)
- **D-60.E1:** Archon 仍按项目既有决策作为外部 CLI 安装，不放进 `autoresearch services start`；Phase 10 的实现和文档都要保持这一边界。
- **D-60.E2:** Phase 10 完成标准不是“YAML 文件存在”就算了，至少要过 `archon validate workflows`，并对主 workflow 做一次真实 `workflow run` 级验证。
- **D-60.E3:** `ARCH-RUN-02` 的验收依赖 Archon Web UI 的原生 progress / result cards，因此本 phase 的验证要确认本机 `archon serve` 可起、workflow run 能在 UI 中看到进度。
- **D-60.E4:** 若本机尚未安装 Archon CLI，本 phase 允许直接补装并完成验证；这是实现本 phase success criteria 的一部分，不视为额外需求。

### F. 主 workflow 端口隔离 (D-61)
- **D-61.F1:** `ar-min-loop` 中的网络代理节点默认使用 `AR_REMOTE_PROXY_PORT=${AR_REMOTE_PROXY_PORT:-17892}`，避免和 Phase 6 reach/wandb 固定的远端 `17890` 隧道互相抢端口。
- **D-61.F2:** 单独运行 `ar-skill-04` 时仍沿用网络 skill 的默认 `17890`，保持 Phase 5 CLI 行为不变；只有主闭环为了顺序组合安全改用 `17892`。

### G. Provider auth 与主闭环可运行性 (D-62)
- **D-62.G1:** 本机 Archon CLI 可以运行 script/bash 节点，但当前 Claude provider 在 loop 节点返回 401；Phase 10 不把外部 provider 重新认证作为代码完成前置条件。
- **D-62.G2:** `ar-min-loop` 必须优先保证真实端到端可执行，因此主 workflow 使用 8 个 deterministic skill 节点；`ARCH-WF-03` 的 Archon loop 表达由 `ar-skill-06` / `ar-skill-07` 单独 workflow 覆盖并通过 `archon validate`。
- **D-62.G3:** loop workflow 的 `until_bash` 使用 `uv run python`，避免 macOS 环境中没有 `python` 可执行文件导致 loop 判定失败。

### the agent's Discretion
- `.archon/scripts/` 内部是一个脚本对应一个 skill，还是拆出少量共享 helper，由实现阶段按最少重复原则决定。
- `services` workflow 用纯 script node 还是 `bash` + script 混合，只要能稳定返回 JSON 并符合现有服务边界即可。
- artifact/state 文件的具体命名、字段排序和日志颗粒度由实现阶段决定；前提是主 workflow 能可靠消费。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase boundary / requirements
- `.planning/ROADMAP.md` — Phase 10 goal、3 个 plans、success criteria
- `.planning/REQUIREMENTS.md` — `ARCH-WF-01..03`, `ARCH-WF-MAIN-01..02`, `ARCH-RUN-01..02`
- `.planning/STATE.md` — 当前已完成到 Phase 9，Phase 10 是下一步
- `.planning/phases/09-skill-08-experiment-report/09-CONTEXT.md` — 最近邻上游 phase，定义了 report 的 local-first / run_id / report 产物语义

### Existing CLI surface to wrap
- `autoresearch/cli.py` — 全部 skill group 的稳定命令名与子命令边界
- `autoresearch/config/validate.py` — Skill 01 的 `run_validate()` 入口
- `autoresearch/services/start.py` — Skill 02 的服务启动边界（只管 wandb/prometheus/grafana）
- `autoresearch/services/status.py` — Skill 02 的健康检查输出形态
- `autoresearch/hw/probe.py` — Skill 03 的 `run_probe()` 入口
- `autoresearch/net/probe.py` — Skill 04 的 `run_probe()` 入口
- `autoresearch/reach/tester.py` — Skill 05 的 `run_reach_test()` / `run_reach_test_all()` 入口
- `autoresearch/stack/checker.py` — Skill 06 的 `run_stack_check()` / `run_stack_check_all()` 入口
- `autoresearch/collect/cli.py` — Skill 07 的 `run_collect()` 入口与 `run_id` / manifest payload
- `autoresearch/report/cli.py` — Skill 08 的 `run_render()` 入口

### Service and environment boundaries
- `README.md` — quickstart 中对 `archon serve` 与 `autoresearch services start` 的关系说明
- `services/README.md` — Archon 不在 compose、其他 3 个服务走 compose 的边界
- `services/archon/README.md` — Archon 安装 / 启动 / 健康检查方式
- `autoresearch/services/_common.py` — Archon / wandb / prometheus / grafana / pushgateway 的 health endpoint 固定值

### Archon official behavior
- `https://archon.diy/guides/authoring-workflows/` — `.archon/workflows/` 目录、DAG 基础字段
- `https://archon.diy/guides/script-nodes/` — script node 通过 `uv` 运行 repo-local Python 脚本，`stdout` 作为节点输出
- `https://archon.diy/guides/loop-nodes/` — `loop:` / `until_bash` / `fresh_context` 的正式语义
- `https://archon.diy/book/quick-reference/` — `archon workflow run`、`archon validate workflows`、变量与 YAML schema
- `https://archon.diy/adapters/web/` — Web UI 的 progress cards / result cards / execution detail 页面

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `run_*` Python 入口已经覆盖 8 个 skill 的 happy path；Phase 10 只需要做 Archon 适配，不需要重新拼业务流程。
- `autoresearch/collect/cli.py` 已经稳定产出 `run_id`、`manifest`、`wandb_path`、`log_path` 等 JSON payload，适合写入 Archon artifact 做下游交接。
- `autoresearch/report/cli.py` 已经接受单个 `run_id` 并生成本地 HTML，天然适合当主 workflow 的最后一跳。
- `autoresearch/services/start.py` / `status.py` 已明确把 Archon 排除在 compose 之外，这个边界必须沿用。

### Established Patterns
- 项目所有主命令都追求“最终 stdout 是唯一 JSON 对象”；Archon 适配层应保留这个 contract，避免额外解析噪音。
- Local-first 是全项目硬约束：workflow 触发远程检查或最小实验，但状态与最终产物都回到本机。
- 最近两 phase 的真实 UAT 都以 `A2-AK-225 + verl` 跑通，因此 Phase 10 默认值应优先贴近这条已验证路径，而不是引入新的默认试验面。

### Integration Points
- `.archon/workflows/` 是 repo-local workflow 注册位置；这里将成为新的入口面。
- `.archon/scripts/` 适合作为 deterministic adapter 层，把 Archon 运行时环境映射到项目现有 `run_*` 入口。
- `$ARTIFACTS_DIR` 是主 workflow 内部 handoff 的天然落点，尤其适合 `collect -> report`、`stack loop -> summary` 这类跨节点交接。

</code_context>

<specifics>
## Specific Ideas

- 当前本机真实服务状态是：`wandb` / `prometheus` / `pushgateway` healthy，`archon` / `grafana` unhealthy；这意味着 Phase 10 的验证顺手会把 Archon 实际拉起。
- 当前最强真实样本仍是 `01KV5MV7N5A3RBZ6388E5HCYAP`，它已经过 Phase 8 collect 与 Phase 9 report 的真实 UAT，可作为 `report` workflow 的现成回归锚点。
- Archon 官方文档已经明确：
  - workflow 文件位置是 `.archon/workflows/`
  - script node 可用 `runtime: uv`
  - loop node 支持 `until_bash`
  - Web UI 会展示 progress / result cards
- 本 phase 最容易踩坑的点不是 YAML 数量，而是“如何把 collect 的 `run_id` 稳定传给 report”，所以交接契约被提升为锁决策。

</specifics>

<deferred>
## Deferred Ideas

- 把 Archon workflow 再上提成 Phase 11 的 `autoresearch check all` / `autoresearch run smoke` CLI 封装
- Archon provider / model 的仓库级显式 profile（例如专门的 Codex / Claude preset）
- 基于 Archon 的定时调度、后台队列或云端部署
- 把更多失败诊断和自动修复逻辑嵌进 workflow loop（Phase 10 先满足最小可跑与可观察）

</deferred>

---

*Phase: 10-archon*
*Context gathered: 2026-06-15*

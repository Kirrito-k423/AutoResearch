---
phase: 09-skill-08-experiment-report
type: context
status: locked
locked_at: 2026-06-15
discussion_mode: auto
locks:
  - D-51
  - D-52
  - D-53
  - D-54
  - D-55
---

# Phase 9: Skill 08 — experiment-report - Context

**Gathered:** 2026-06-15
**Status:** Ready for planning
**Discussion mode:** auto (user requested autonomous progression)

<domain>
## Phase Boundary

给定一个 Phase 8 产生的 `run_id`，在本地生成单页 HTML 报告，固定写到 `~/.autoresearch/runs/<run_id>/report.html`，并把这一轮实验的三路结果以“可读摘要 + 可点击原始入口”的方式串起来：

- log 摘要
- wandb 指标视图
- Prometheus 资源视图

本 phase 的目标是“**单个 run 的本地静态报告**”，不是多 run dashboard，也不是新的长驻 Web 服务。

</domain>

<decisions>
## Implementation Decisions

### A. 报告入口与真相源 (D-51)
- **D-51.A1:** 报告入口固定为 `autoresearch report render --run-id X`。
- **D-51.A2:** `manifest.json` 是报告重建的真相源；实现从 `~/.autoresearch/runs/<run_id>/manifest.json` 起步，而不是从 wandb / Prometheus 反向猜 run。
- **D-51.A3:** 如果 `manifest.json` 缺失或不可解析，CLI 直接失败；如果 manifest 存在但某一路下游数据缺失，仍生成 partial HTML，并在对应区块明确标注缺口。
- **D-51.A4:** 默认输出路径固定为 `~/.autoresearch/runs/<run_id>/report.html`，先满足 REQUIREMENTS 的固定产物约束，不在本 phase 额外扩展 `--output` 自定义路径。

### B. 数据读取策略 = 本地优先，不依赖云端 API (D-52)
- **D-52.B1:** log 视图只读本地 artifact：`manifest.log_files[]` 指向的本地 `log.txt`。
- **D-52.B2:** wandb 视图优先读本地同步产物：`manifest.wandb_path/files/wandb-summary.json`；不依赖 wandb cloud，不要求外网。
- **D-52.B3:** Prometheus 视图优先走本地 `http://localhost:9090/api/v1/query` / `query_range` 按 `run_id` 查询；如果本地 Prometheus 暂不可达，则报告保留 “prom 已推送/未推送” 状态和跳转链接，但不阻塞 HTML 生成。
- **D-52.B4:** Phase 9 不额外回远程服务器取数；所有读取都应来自本机现成 artifact 或本机本地服务。

### C. M1 指标展示语义 = snapshot-style，而非长时训练曲线 (D-53)
- **D-53.C1:** Phase 8 的最小实验只产生单次 wandb log 和单次 pushgateway metric，因此本 phase 默认展示“**单点/快照型图表**”，而不是假设存在多 step 训练曲线。
- **D-53.C2:** wandb 面板至少展示 `sum`、`npu_count`、`lib` 以及单点图/迷你图；Prometheus 面板至少展示 `autoresearch_npu_count{run_id=...}` 的当前值以及单点图/迷你图。
- **D-53.C3:** 报告文案要诚实表达数据粒度：M1 是 minimal run snapshot，不伪装成多 epoch 训练历史。
- **D-53.C4:** log 面板展示“摘要 + 原始片段入口”，默认给出关键行提炼（如 `SUM=...`、`NPU_COUNT=...`、`WANDB_RUN_ID=...`）和末尾片段，而不是整页塞满原始日志。

### D. 页面结构与 `--open` 行为 (D-54)
- **D-54.D1:** 页面首屏先给运行摘要：`run_id`、server、lib、conda_env、elapsed、exit_code、started_at/finished_at、error。
- **D-54.D2:** 页面主体固定三块：`log`、`wandb`、`prometheus`，每块同时有“摘要/图表”和“原始入口链接”。
- **D-54.D3:** `--open` 只负责在本地默认浏览器打开已生成的 `report.html`；如果打开失败，不影响 render 本身成功。
- **D-54.D4:** 报告是单文件静态 HTML，可带少量内联 CSS/JS，但不引入新的本地 Web 服务器。

### E. 链接策略 (D-55)
- **D-55.E1:** 报告中必须嵌入 raw artifact 链接：`manifest.json`、`log.txt`、`wandb` 本地目录。
- **D-55.E2:** wandb 链接采用“尽力 deep-link，保底 service root”的策略：若实现时能稳定构造本地 wandb run URL，则直达 run；否则至少提供 `http://localhost:8080/` 和 `wandb_run_id` 明示，不能留空。
- **D-55.E3:** Prometheus 链接使用按 `run_id` 固定查询的 graph URL，便于用户跳到本地 Prometheus 继续看：
  - 查询核心：`autoresearch_npu_count{run_id="<run_id>"}`
- **D-55.E4:** 即便本地服务暂时不在线，链接也照样写进报告；服务可用性由页面状态提示，不由链接存在与否决定。

### the agent's Discretion
- 报告采用模板字符串、Jinja2 风格拼装，还是轻量组件化渲染，由实现阶段决定。
- 图表用内联 SVG、极轻量前端库，还是纯 HTML 指标卡，由实现阶段决定；前提是单文件静态 HTML、默认离线可打开。
- log 摘要算法（关键行提取优先，还是头尾截断优先）可由实现阶段决定，只要最终页面既有摘要也能追到原始日志。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase boundary / requirements
- `.planning/ROADMAP.md` — Phase 9 goal、success criteria、plan 拆分
- `.planning/REQUIREMENTS.md` — `RPT-MANIFEST-01`, `RPT-PAGE-01..03`, `RPT-LINK-01`
- `.planning/STATE.md` — 当前 Phase 8 已 ship、Phase 9 是紧接的下一步

### Upstream collection truth
- `.planning/phases/08-skill-07-data-collection/08-CONTEXT.md` — Phase 8 锁定的 local-first / manifest / wandb / prom 决策
- `.planning/phases/08-skill-07-data-collection/08-VERIFICATION.md` — 真机验证证据与真实 run id
- `autoresearch/collect/cli.py` — `run_collect()` 最终 payload、产物路径与错误语义
- `autoresearch/collect/manifest.py` — manifest 构造入口
- `datalake/manifest/schema.py` — `RunManifest` 字段边界
- `datalake/manifest/writer.py` — manifest 落盘位置

### Local artifact and path conventions
- `workspace-core/layout/paths.py` — `~/.autoresearch/runs/<id>/` 目录约定
- `datalake/wandb/sync.py` — 本地 wandb 目录结构与 `wandb-summary.json` 位置
- `datalake/prometheus/push_gateway.py` — Prometheus metric 名称与 `run_id` 标签格式

### Test anchors
- `tests/test_collect_cli.py` — collect 输出 payload 与 manifest 保留约束
- `tests/test_collect_manifest.py` — manifest 字段映射约束
- `tests/test_datalake_manifest.py` — manifest JSON 序列化约束

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `datalake.manifest.RunManifest` — 已把报告所需主键字段集中起来，Phase 9 直接复用，不重建 schema
- `workspace_core.layout.paths.run_dir()` — 可统一解析 `~/.autoresearch/runs/<id>/` 下的目标路径
- `autoresearch.collect.cli.run_collect()` — 已定义 run 完成后本地产物最小集合：manifest / log / wandb / prom 状态

### Established Patterns
- CLI 最终 stdout 输出唯一 JSON；报告子命令也应延续这个机读约定
- 本地优先（local-first）是全项目硬约束：报告读取本机产物，不回远端、不依赖云
- 错误允许 partial：Phase 8 已允许下游失败但 manifest 保留，Phase 9 报告也应沿用 partial-friendly 语义

### Integration Points
- `autoresearch/cli.py` 需要新增 `report` group / `render` subcommand
- 新代码大概率落在 `autoresearch/report/`，围绕 `loader` / `renderer` / `open` 组织
- Phase 9 直接消费 Phase 8 的真实 run artifact，不需要再改 collect 主链路

</code_context>

<specifics>
## Specific Ideas

- 当前最强的真实样本是 `01KV5MV7N5A3RBZ6388E5HCYAP`：
  - `server=A2-AK-225`
  - `lib=verl`
  - `wandb_run_id=dzeibhga`
  - `log.txt` 含 `SUM=...`、`NPU_COUNT=...`、`WANDB_RUN_ID=...`
- 本地 wandb summary 目前已有足够的最小字段：`sum`、`npu_count`、`lib`、`_step`
- 页面首屏应该把“这是不是一次成功采集”说得很直白：成功/失败状态、错误信息、三路数据是否齐全
- 报告应优先帮助用户复盘一次最小实验，而不是追求通用 BI 工具感

</specifics>

<deferred>
## Deferred Ideas

- 多 run 对比报告 / 历史列表页
- 自动刷新 / live report
- 自建本地 report web 服务
- 解析 `.wandb` 二进制以支持未来多 step 详细曲线（如果 Phase 8 以后采集粒度升级，再单开 phase）

</deferred>

---

*Phase: 09-skill-08-experiment-report*
*Context gathered: 2026-06-15*

# Roadmap: AutoResearch

## Milestones

- ✅ **v1.0 MinViable Loop** — Phases 1-13, shipped 2026-06-15. Archive: `.planning/milestones/v1.0/`
- ✅ **v1.1 Formal Verl** — Phase 14, shipped 2026-06-18. Archive: `.planning/milestones/v1.1-ROADMAP.md`
- 📋 **v2.0 Distribute** — multi-node scheduling and broader infrastructure support (planned)

## Phases

<details>
<summary>✅ v1.0 MinViable Loop (Phases 1-13) — SHIPPED 2026-06-15</summary>

- [x] Phase 1: 仓骨架与本地服务栈 (4/4 plans) — completed 2026-06-09
- [x] Phase 2: workspace-core 沉淀 (4/4 plans) — completed 2026-06-09
- [x] Phase 3: Skill 01 — customer-config (2/2 plans) — completed 2026-06-09
- [x] Phase 4: Skill 03 — server-hardware-probe (4/3 plans) — completed 2026-06-12
- [x] Phase 5: Skill 04 — network-check (3/3 plans) — completed 2026-06-12
- [x] Phase 6: Skill 05 — service-reachability (3/3 plans) — completed 2026-06-12
- [x] Phase 7: Skill 06 — train-stack-health (3/3 plans) — completed 2026-06-15
- [x] Phase 8: Skill 07 — data-collection (4/4 plans) — completed 2026-06-15
- [x] Phase 9: Skill 08 — experiment-report (2/2 plans) — completed 2026-06-15
- [x] Phase 10: Archon 适配层 (3/3 plans) — completed 2026-06-15
- [x] Phase 11: 顶层 CLI 编排 (2/2 plans) — completed 2026-06-15
- [x] Phase 12: E2E 端到端 smoke (2/2 plans) — completed 2026-06-15
- [x] Phase 13: M1 归档 (1/1 plan) — completed 2026-06-15

</details>

<details>
<summary>✅ v1.1 Formal Verl (Phase 14) — SHIPPED 2026-06-18</summary>

- [x] Phase 14: 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环 (5/5 plans) — completed 2026-06-18

**Final artifact:** `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1`

**Delivered:** `autoresearch run verl-case`, Qwen3.5-2B + geometry3k formal execution on Ascend, 8/8 sync/async matrix rows, immutable config snapshots, local W&B/Prometheus/log/report artifacts, and multi-repo provenance.

</details>

## Progress

| Milestone | Phases | Plans Complete | Status | Completed |
|---|---:|---:|---|---|
| v1.0 MinViable Loop | 13/13 | 37/37 | Shipped | 2026-06-15 |
| v1.1 Formal Verl | 1/1 | 5/5 | Shipped | 2026-06-18 |
| v2.0 Distribute | TBD | 0/0 | Not started | - |

## Next

No active milestone is defined. Start the next milestone with `$gsd-new-milestone` when ready to choose the next scope.

### Phase 15: 补齐 Verl 正式实验 NPU HBM/Core 指标与 Qwen3.5 GRPO 真实脚本阶段耗时

**Goal:** 让 Verl 正式 case 从可跑通升级为可观测、可复盘的真实 GRPO 实验：运行期间采集 NPU HBM/Core 曲线，并从 Qwen3.5 GRPO 真实脚本中沉淀各阶段耗时、吞吐和精度指标。
**Requirements**:

- Prometheus 接入运行时 NPU HBM/Core 采样指标，报告能按 run 展示显存占用和 core 利用率曲线。
- `autoresearch run verl-case` 使用 Qwen3.5-2B GRPO 真实脚本路径，不以 demo 或 validation-only 替代正式训练/推理流程。
- 数据仓保存 Verl 推理、logp、update 等阶段耗时，总吞吐、精度指标、W&B 原始数据和不可变配置快照，能通过 run 命名和 git provenance 对应到具体代码版本。

**Depends on:** Phase 14
**Plans:** 1/4 plans executed

Plans:

- [x] 15-01 Runtime NPU HBM/Core Telemetry And Prometheus Evidence
- [ ] 15-02 Real Qwen3.5-2B GRPO Training Tuning Matrix
- [ ] 15-03 Verl Stage Timing Extraction From W&B And Raw Logs
- [ ] 15-04 Numbered Data Repository Bundle And Rebuildable Visualizations

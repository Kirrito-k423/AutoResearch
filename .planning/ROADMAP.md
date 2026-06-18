# Roadmap: AutoResearch

## Milestones

- ✅ **v1.0 MinViable Loop** — Phases 1-13, shipped 2026-06-15. Archive: `.planning/milestones/v1.0/`
- ✅ **v1.1 Stable** — Phase 14 formal Verl case loop completed 2026-06-18; later hardening may start a new milestone
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

## Progress

| Milestone | Phases | Plans Complete | Status | Completed |
|---|---:|---:|---|---|
| v1.0 MinViable Loop | 13/13 | 37/37 | Shipped | 2026-06-15 |
| v1.1 Stable | 1/1 | 5/5 | Completed | 2026-06-18 |
| v2.0 Distribute | TBD | 0/0 | Not started | - |

## Next

Phase 14 is complete. The final formal-case artifact bundle is `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1`.

### Phase 14: 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环

**Goal:** Add `autoresearch run verl-case` and a local-first Verl formal-case loop for Qwen3.5-2B + geometry3k on Ascend, including strict sync/async length matrix execution, immutable config snapshots, multi-repo provenance, observability artifacts, and reportable performance/accuracy results.
**Requirements**: TBD
**Depends on:** Phase 13
**Plans:** 5 plans

Plans:

**Wave 1**

- [x] 14-01: Formal Case Config, Matrix, Evaluation, And Provenance Models

**Wave 2 *(blocked on Wave 1 completion)***

- [x] 14-02: Verl Docker, Data Prep, Provenance, And Remote Formal Runner

**Wave 3 *(blocked on Wave 2 completion)***

- [x] 14-03: `autoresearch run verl-case` Orchestration And Local Artifacts

**Wave 4 *(blocked on Wave 3 completion)***

- [x] 14-04: Formal Case Report, Verification, And UAT Closure

**Wave 5 *(blocked on Wave 4 real-UAT evidence)***

- [x] 14-05: Real Formal Runtime Completion And Artifact Closure

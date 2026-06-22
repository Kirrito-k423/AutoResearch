# Phase 15: verl-npu-hbm-core-qwen3-5-grpo - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-22T11:53:31Z
**Phase:** 15-verl-npu-hbm-core-qwen3-5-grpo
**Areas discussed:** NPU sampling contract, real GRPO training closure, Verl stage timing source, artifact organization and rebuildability

---

## NPU Sampling Contract

| Option | Description | Selected |
|--------|-------------|----------|
| Python 0.5s loop | Python sampler calls `npu-smi info -t memory/usages` every 0.5s, normalizes JSONL, and pushes Prometheus. | |
| Native watch | Use `npu-smi info watch -d 1 -s amn`; command help shows `-d` range is 1-100 seconds. | yes |
| Hybrid | Use Python 0.5s structured sampler plus 1s native watch raw-log backup. | |

**User's choice:** `1.2`
**Notes:** User first suggested 0.5s continuous runtime sampling. After A2-AK-225 showed `npu-smi info watch` exists and `-d` minimum is 1s, user selected the native watch route.

---

## Real GRPO Training Closure

| Option | Description | Selected |
|--------|-------------|----------|
| Single-card first, then 8-card | Start with single-card BS=1, increase batch knobs to fit HBM, then promote stable candidates to single-node 8-card throughput. | yes |
| Full single-card and 8-card sweep | Sweep both scales completely; most data, highest cost. | |
| 8-card only | Skip single-card search and tune directly for single-node throughput. | |

**User's choice:** `2.1`
**Notes:** User added that every case should run 3 training steps. The performance goal is to fill HBM and maximize single-card and full-machine throughput.

---

## Verl Stage Timing Source

| Option | Description | Selected |
|--------|-------------|----------|
| W&B native first | Use Verl's W&B logger for native stage metrics where available. | yes |
| Log parsing fallback | Parse console/raw logs for rollout, logp, update, and related stages. | yes |
| Patch Verl if needed | Add light instrumentation only if W&B and logs cannot expose required stage timings. | conditional |

**User's choice:** Free-text: "verl应该支持wandb的接口吧，也可以日志解析。"
**Notes:** Locked as W&B first, logs second, Verl patch only if needed and provenance-tracked.

---

## Artifact Organization And Rebuildability

| Option | Description | Selected |
|--------|-------------|----------|
| Numbered full bundle | `0-report/`, `1-wandb/`, `2-prometheus/`, `3-raw-logs/`, `4-config/`, `5-provenance/`, `6-rows/`, `restore/`. | yes |
| Number first four only | Number report/W&B/Prometheus/logs and keep config/provenance/rows unnumbered. | |
| Custom layout | User supplies another directory convention. | |

**User's choice:** `3.1`
**Notes:** User specified customer reading priority: `0-总report`, `1-wandb`, `2-普罗米修斯数据`, `3-原始数据log`; W&B and Prometheus visualizations must be rebuildable.

---

## the agent's Discretion

- Exact module names and internal data classes for telemetry, stage timing, and report extensions.
- Exact batch-size growth rule after BS=1, as long as each case runs 3 steps and failures are recorded.
- Exact mechanism for rebuilding Prometheus visualizations from saved data, as long as curves can be recreated from the data bundle.

## Deferred Ideas

- Revisit 0.5s telemetry through a custom sampler or lower-level API if native 1s `npu-smi watch` is insufficient.
- General scheduling, multi-node tuning, and broad benchmark suites remain out of scope for this phase.

# Phase 14: 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-16T15:11:56Z
**Phase:** 14-跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环
**Areas discussed:** Formal entry and container boundary, model/data cache policy, experiment matrix, code provenance, case type, geometry3k modality, completion standard, accuracy standard

---

## Formal Entry And Container Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Add `autoresearch run verl-case` | Create a separate formal case entrypoint so smoke remains minimal. | ✓ |
| Extend existing smoke/collect path only | Faster wiring, but risks changing existing smoke semantics. | |

**User's choice:** Add `autoresearch run verl-case`.
**Notes:** User said Docker usage should follow `build_a2_docker.md` from VeOmni AscendDockerUsage. Initial image target remains `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`.

---

## Model/Data Cache Policy

| Option | Description | Selected |
|--------|-------------|----------|
| Configurable local cache under `/Users/Zhuanz/autoResearchData` | Keep <=5GB assets locally and allow path override. | ✓ |
| Remote-only cache | Avoid local disk use but weaker local reproducibility. | |

**User's choice:** Keep container/model/data assets within 5GB locally when possible.
**Notes:** User specified model `Qwen/Qwen3.5-2B`, dataset `hiyouga/geometry3k`, and local cache root `/Users/Zhuanz/autoResearchData`; paths should be configurable.

---

## Experiment Matrix

| Option | Description | Selected |
|--------|-------------|----------|
| Strict full matrix through 16k | Run every length and sync/async combination; any failure blocks completion. | ✓ |
| Core matrix with 16k as resource boundary | Let 16k OOM/timeout be reported as a boundary. | |
| Single point first | Only prove 1k/2k first, defer full matrix. | |

**User's choice:** Strict full matrix through 16k.
**Notes:** User specified `1k input / 2k output`, `ignore_eos` disabled, output/inference length doubles until `16k`, and all synchronous/asynchronous combinations must complete.

---

## Code Provenance

| Option | Description | Selected |
|--------|-------------|----------|
| Auto fork/commit/push allowed | Use `Kirrito-k423` forks and experiment branches for official repos. | ✓ |
| Local-only provenance | Avoid GitHub writes, but weaker experiment-to-code linkage. | |

**User's choice:** Auto fork/commit/push is allowed.
**Notes:** User wants experiment data tied to code changes across AutoResearch and modified dependencies such as Verl, vLLM, Transformers, and MindSpeed. Each experiment needs a full immutable config snapshot; second-level timestamps are acceptable for correspondence.

---

## Case Type

| Option | Description | Selected |
|--------|-------------|----------|
| GRPO/RL math reasoning case | Best fit for geometry3k and async inference evaluation. | ✓ |
| SFT case | Easier supervised loop, weaker async inference signal. | |
| Let researcher decide | Defer case type to research. | |

**User's choice:** GRPO/RL math reasoning case.
**Notes:** User selected option 1.

---

## geometry3k Modality

| Option | Description | Selected |
|--------|-------------|----------|
| Raw multimodal `image + problem` | Preserves geometry3k task semantics. | ✓ |
| Text-only problem | Easier to run, but loses visual information. | |
| Dual track | Start text-only, then add image+problem. | |

**User's choice:** Raw multimodal `image + problem`.
**Notes:** User selected option 1. Research/planning must verify Qwen3.5-2B + Verl + Ascend multimodal GRPO support instead of silently dropping images.

---

## Completion Standard

| Option | Description | Selected |
|--------|-------------|----------|
| Complete matrix strictly passes | Every length and sync/async combination must finish with artifacts. | ✓ |
| Core matrix passes, 16k can be resource boundary | Useful for risk control but weaker than formal case. | |
| Single point then expand later | Safer but too demo-like. | |

**User's choice:** Complete matrix strictly passes.
**Notes:** User selected option 1.

---

## Accuracy Standard

| Option | Description | Selected |
|--------|-------------|----------|
| Sync vs async consistency only | Compare paired outputs between modes. | |
| Ground truth only | Evaluate each mode against geometry3k answer field. | |
| Dual standard | Require both ground-truth accuracy and sync/async consistency reporting. | ✓ |

**User's choice:** Dual standard.
**Notes:** User selected option 3.

---

## the agent's Discretion

- Define exact Python module names, dataclass names, and report layout while preserving existing layer boundaries.
- Research current Verl GRPO/async argument names and Ascend support before writing the execution plan.
- Pick exact accuracy normalization and drift thresholds if no official project threshold exists, but do not weaken full-matrix completion.

## Deferred Ideas

- Text-only geometry3k fallback.
- General experiment scheduler / web UI.
- Multi-node scheduling beyond the first formal case.

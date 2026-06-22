---
status: partial
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
source:
  - 15-01-SUMMARY.md
  - 15-02-SUMMARY.md
  - 15-03-SUMMARY.md
  - 15-04-SUMMARY.md
started: 2026-06-22T18:14:14Z
updated: 2026-06-22T18:24:30Z
---

## Current Test

[testing paused - 2 items blocked by remote NPU availability / image compatibility]

## Tests

### 1. Runtime HBM/Core telemetry evidence
expected: Formal Verl rows collect runtime `npu-smi info watch` evidence, normalize HBM/Core/NPU utilization rows, and preserve Prometheus-compatible telemetry artifacts for report curves.
result: pass
evidence:
  - 15-01-SUMMARY.md
  - `uv run pytest -q tests/test_verl_telemetry.py tests/test_verl_case_runner.py tests/test_datalake_prometheus_push.py tests/test_report_prometheus.py tests/test_report_render.py`

### 2. Real Qwen3.5-2B GRPO three-step training case
expected: At least one single-card Qwen3.5-2B + geometry3k GRPO case completes `completed_training_steps=3` with `target_training_steps=3`; fewer steps are retained as failed data points.
result: blocked
blocked_by: server
reason: "2026-06-23 02:20-02:24 Asia/Shanghai recheck: A2-AK-225 still has an existing `Qwen3.5-2B-GRPO-video` Ray/Verl `main_ppo` process inside `verl-8.5.2-a2`; the exact target-image smoke still fails before the case can run. A3-AX-180 and A3-AK-182 still fail minimal NPU smoke with `OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed`. A2-AK-102 is not a safe fallback because the target image is absent and all 8 NPUs are occupied by vLLM services."
evidence:
  - 15-02-SUMMARY.md
  - A2-AK-225 `autoresearch hw probe --all`: 8 x 910B2, HBM about 4.6-5.0GiB used per device, but the GRPO-video process remains present.
  - A2-AK-225 active process: `python3 -m verl.trainer.main_ppo ... trainer.project_name=GRPO-video trainer.experiment_name=Qwen3.5-2B-GRPO-video`
  - A2-AK-225 qualification: `exact image NPU smoke failed: The argument is invalid.Reason: rtGetDevMsg execution failed, the feature is not supported.`
  - A3-AX-180 qualification: `exact image NPU smoke failed: OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed.`
  - A3-AK-182 qualification: `exact image NPU smoke failed: OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed.`
  - A2-AK-102 lightweight inventory: target image absent; two vLLM services occupy all 8 NPUs with about 59-60GiB HBM each.

### 3. Verl stage timing extraction
expected: W&B offline files and raw Verl logs can produce durable per-case and run-level `stage-timings.jsonl` rows covering rollout/logp/reward/update/validation/checkpoint/data-loading stages when present.
result: pass
evidence:
  - 15-03-SUMMARY.md
  - `uv run pytest -q tests/test_verl_stage_timing.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py tests/test_report_render.py tests/test_report_wandb.py`

### 4. Numbered data repository bundle
expected: Formal Verl artifacts are organized under `0-report/`, `1-wandb/`, `2-prometheus/`, `3-raw-logs/`, `4-config/`, `5-provenance/`, `6-rows/`, and `restore/`, with report loaders remaining backward compatible.
result: pass
evidence:
  - 15-04-SUMMARY.md
  - `uv run pytest -q tests/test_report_cli.py tests/test_datalake_wandb_sync.py tests/test_orchestrator_verl_case.py tests/test_report_loader.py tests/test_report_wandb.py tests/test_report_prometheus.py tests/test_report_render.py tests/test_datalake_manifest.py`

### 5. Final successful training evidence bundle
expected: A copied `autoresearch-log` bundle from a successful three-step training run contains W&B raw data, Prometheus/OpenMetrics resource curves, raw logs, immutable config/provenance, rows, stage timings, and report links tied to the code commit.
result: blocked
blocked_by: server
reason: "Blocked by the same real-run gate as Test 2. The bundle layout and loaders are implemented, but the final successful three-step training bundle cannot be produced until a host passes the exact target-image NPU smoke and completes a 3-step GRPO row."

## Summary

total: 5
passed: 3
issues: 0
pending: 0
skipped: 0
blocked: 2

## Gaps

[none - blocked items are external execution prerequisites, not diagnosed code defects]

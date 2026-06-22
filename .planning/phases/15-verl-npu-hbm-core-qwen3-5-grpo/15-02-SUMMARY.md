---
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
plan: 02
subsystem: verl-training
tags: [verl, grpo, qwen35, geometry3k, tuning, three-steps]
status: implementation-complete-uat-blocked
completed: 2026-06-22
blocking_uat:
  reason: A2-AK-225 NPU devices were occupied by existing python/ray workers, so a successful real 3-step formal training case could not be honestly produced in this pass.
  required_next_action: rerun autoresearch run verl-case on a free A2 host and require at least one single-card case with completed_training_steps=3.
provides:
  - True GRPO training config defaults with trainer_val_only=false and training_steps=3
  - Single-card BS=1 tuning matrix and single-node promotion path
  - Row-level completed_training_steps, target_training_steps, failure_class, device_count, and batch knobs
  - Resource-busy/OOM/timeout/incomplete-step failure classification
key-files:
  modified:
    - workspace-adapter/verl/case_config.py
    - workspace-adapter/verl/case_runner.py
    - autoresearch/orchestrator/verl_case.py
    - tests/test_verl_case_config.py
    - tests/test_verl_case_runner.py
    - tests/test_orchestrator_verl_case.py
commits:
  - 0d9608d feat(15-02): add verl training tuning config
  - 19c08e1 feat(15-02): run verl grpo training cases
  - 0b529b3 feat(15-02): orchestrate verl training tuning matrix
  - a939395 feat(15-02): promote stable verl cases to single node
  - 676ff93 fix(15-02): let skip readiness bypass host smoke
  - ea35488 fix(15-02): classify resource busy and use npu-smi fallback
  - 63e6e15 fix(15-02): sample hbm telemetry with npu-smi info
---

# Phase 15 Plan 02 Summary: Real GRPO Training Tuning Matrix

Implementation is complete for the true Qwen3.5-2B + geometry3k GRPO training path. The runner now defaults to training mode, starts tuning from one visible NPU with batch size 1, promotes stable candidates to 8-card single-node cases, and records failed attempts instead of dropping them.

## What Changed

- Added Phase 15 tuning fields, including `training_steps=3`, single-card devices, single-node devices, tuning batch sizes, and GRPO training defaults.
- Generated Verl commands now set `trainer.val_only=False`, `trainer.total_training_steps=3`, `trainer.val_before_train=False`, and `trainer.logger=[console,wandb]`.
- Row results include `completed_training_steps`, `target_training_steps`, device visibility, batch knobs, throughput, and `failure_class`.
- Rows with fewer than 3 completed training steps are classified as `incomplete_training_steps`, not passed throughput data.
- Orchestration runs single-card tuning first, then promotes stable candidates to a single-node candidate.

## Verification

```bash
uv run pytest -q tests/test_verl_case_config.py tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py
```

Covered again in the full regression on 2026-06-22:

```bash
uv run pytest -q
```

Result: `467 passed, 6 warnings`.

## UAT Status

The real remote training UAT is still pending because A2-AK-225 was resource-busy during the execution window. This is not counted as a successful training result. The next valid UAT must produce a bundle where at least one single-card case has `completed_training_steps=3` and `target_training_steps=3`.


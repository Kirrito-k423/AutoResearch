---
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
plan: 02
subsystem: verl-training
tags: [verl, grpo, qwen35, geometry3k, tuning, three-steps]
status: implementation-complete-uat-blocked
completed: 2026-06-22
blocking_uat:
  reason: A2-AK-225 NPU devices were occupied by existing Verl/Ray/VLLM workers, so a successful real 3-step formal training case could not be honestly produced in this pass.
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
data_commits:
  - e574359 data: add verl qualification failure 20260622
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

### Follow-up on 2026-06-23 02:08 Asia/Shanghai

Additional diagnostics found two separate host constraints:

- A3-AK-182 and A3-AX-180 both report `acl.get_soc_name() == Ascend910_9382`; the current `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5` image fails a minimal `torch.ones + torch.cat + torch.npu.synchronize()` smoke with `OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed`. A3 hosts should not be selected for this 910B image unless a compatible A3 image/kernel package is introduced.
- A2-AK-225 has the correct arm64 image and 910B2 hardware, but NPU resources are currently held by an existing `Qwen3.5-2B-GRPO-video` Ray/Verl run inside the long-lived `verl-8.5.2-a2` container. It must not be counted as available until that workload finishes or is explicitly cleared.

Code was hardened so formal host qualification now runs real NPU ops (`ones`, `zeros`, `cat`, synchronize) instead of only copying a CPU tensor to NPU, and single-card cases mount the configured full-machine NPU device set while preserving `ASCEND_RT_VISIBLE_DEVICES=[0]` for actual training isolation.

### Attempt on 2026-06-22 22:26:19 Asia/Shanghai

Command:

```bash
uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --timeout 7200
```

Result: failed at `prepare` before matrix execution. The exact Verl container smoke could not acquire NPU devices. Follow-up probes showed the container saw `torch_npu.device_count=0` and `npu-smi` returned `dcmi model initialized failed, because the device is used. ret is -8020`.

Blocking workload observed on A2-AK-225:

- `python3 -m verl.trainer.main_ppo ... Qwen3-VL-8B-Instruct ... trainer.total_training_steps=3`, PID `243179`, started around 2026-06-22 22:25 Asia/Shanghai.
- `VLLMWorker_TP` workers on all 8 NPUs, about 25.5GB per NPU.
- `rayWorkerDict` workers on all 8 NPUs.

Evidence bundle:

- `/Users/Zhuanz/autoResearchData/autoresearch-log/experiments/verl/Qwen35-2B/GRPO/20260622/Qwen35-2B-GRPO-1Kto16K-260622d-222619s-train-modes-sync-async-noignoreeos/RUN.md`
- `/Users/Zhuanz/autoResearchData/autoresearch-log/experiments/verl/Qwen35-2B/GRPO/20260622/Qwen35-2B-GRPO-1Kto16K-260622d-222619s-train-modes-sync-async-noignoreeos/3-raw-logs/qualification-failure.json`

Data repo commit: `e574359`.

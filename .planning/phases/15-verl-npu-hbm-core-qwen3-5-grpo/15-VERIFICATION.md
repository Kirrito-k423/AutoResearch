---
status: human_needed
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
verified_at: 2026-06-22T18:24:30Z
automated_tests: passed
uat: partial
ship_ready: false
---

# Phase 15 Verification

## Verdict

Phase 15 implementation is verified at the code/test level, but the phase is not shippable as a completed experiment milestone because the real Qwen3.5-2B GRPO three-step UAT is still blocked by external NPU host state.

## Automated Checks

```bash
uv run pytest -q
```

Result observed during the 2026-06-23 02:17 CST close-out check: `469 passed, 6 warnings`.

Focused Phase 15 checks also passed:

```bash
uv run pytest -q tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_verl_case_config.py tests/test_verl_stage_timing.py
```

Result: `77 passed`.

## Remote UAT Evidence

Non-destructive qualification was re-run on 2026-06-23 02:20-02:24 Asia/Shanghai.

| Host | Hardware / image state | Qualification result |
|---|---|---|
| A2-AK-225 | 910B2, arm64 image present (`sha256:fd53bed...`), HBM mostly free but an existing GRPO-video `main_ppo` process remains | Blocked: exact image smoke still fails with `rtGetDevMsg execution failed`; active process includes `trainer.project_name=GRPO-video trainer.experiment_name=Qwen3.5-2B-GRPO-video`. |
| A3-AX-180 | x86_64 image present (`sha256:0effe...`), NPUs otherwise free | Incompatible: exact image smoke fails with `OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed`. |
| A3-AK-182 | arm64 image present (`sha256:fd53bed...`), no Verl target-image container running during recheck | Incompatible: exact image smoke fails with `OnesLike ADD_TO_LAUNCHER_LIST_AICORE failed`. |
| A2-AK-102 | 910B3, target image absent, 8 NPUs occupied by long-running vLLM services | Not selected: the required image is not present and HBM is already heavily consumed by two vLLM deployments. |

## Blocked Criteria

- No current artifact proves `completed_training_steps=3` and `target_training_steps=3` for a Qwen3.5-2B + geometry3k GRPO training row.
- No final successful three-step `autoresearch-log` bundle can be produced until A2-AK-225 is free/cleared or another host passes the exact image NPU smoke.
- A3 hosts should not be selected for this exact 910B image unless a compatible image/kernel package is introduced.
- A2-AK-102 should not be selected while the vLLM services own the 8-card HBM budget.

## Ship Gate

`$gsd-ship` must not proceed for Phase 15 while this file has `status: human_needed` and `ship_ready: false`.

## Next Valid Verification Command

After A2-AK-225 is free or explicitly cleared:

```bash
uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --timeout 7200
```

The run is valid only if at least one row records:

```json
{"completed_training_steps": 3, "target_training_steps": 3, "status": "passed"}
```

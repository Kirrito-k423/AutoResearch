---
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
plan: 03
subsystem: verl-stage-timing
tags: [verl, grpo, wandb, raw-logs, timing, report]
status: complete
completed: 2026-06-22
provides:
  - W&B history/summary extraction for timing-like Verl metrics
  - Raw Verl log extraction for timing dictionaries and key-value timing lines
  - Training step counter shared by UAT/failure reasoning
  - Per-case and run-level stage-timings.jsonl artifacts
  - Report section for Verl stage timing summaries and details
key-files:
  created:
    - workspace-adapter/verl/stage_timing.py
  modified:
    - autoresearch/orchestrator/verl_case.py
    - autoresearch/report/models.py
    - autoresearch/report/render.py
    - autoresearch/report/verl_case.py
    - autoresearch/report/wandb.py
    - tests/test_verl_stage_timing.py
    - tests/test_report_verl_case.py
    - tests/test_report_wandb.py
    - tests/test_orchestrator_verl_case.py
commits:
  - c66c7ee feat(15-03): extract verl stage timings
  - ed22bf0 feat(15): persist verl timings and numbered artifacts
---

# Phase 15 Plan 03 Summary: Verl Stage Timing Extraction

Verl stage timing extraction now has two evidence paths: W&B offline history/summary files and raw console logs. The local data bundle no longer depends on the live W&B UI to explain rollout, logp, reward, update, validation, checkpoint, or data-loading time when those metrics are present.

## What Changed

- Added `VerlStageTiming` and W&B metric normalization in `workspace-adapter/verl/stage_timing.py`.
- Added raw log parsing for timing dictionaries and `key=value`/`key: value` timing lines.
- Added `count_completed_training_steps()` so logs can distinguish 0/1/2/3 completed training steps.
- Orchestration now scans `6-rows/cases/*/*.log`, writes per-case `stage-timings.jsonl`, and writes run-level `6-rows/stage-timings.jsonl`.
- Manifest `formal_case.stage_timings` points to the run-level stage timing artifact.
- Report rendering now includes a `Verl 阶段耗时` section with stage/source summaries and detail rows.

## Verification

```bash
uv run pytest -q tests/test_verl_stage_timing.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py tests/test_report_render.py tests/test_report_wandb.py
```

Result: `33 passed`.

Full regression on 2026-06-22:

```bash
uv run pytest -q
```

Result: `467 passed, 6 warnings`.

## Notes

No Verl dependency repo patch was required. If a future real run shows the native logs omit target stages, the next step should patch Verl itself and capture that dependency commit in `5-provenance/`.


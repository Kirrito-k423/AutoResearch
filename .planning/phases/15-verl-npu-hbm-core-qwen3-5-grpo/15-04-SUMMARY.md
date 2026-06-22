---
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
plan: 04
subsystem: data-bundle
tags: [autoresearch-log, artifacts, wandb, prometheus, manifest, report]
status: complete
completed: 2026-06-22
provides:
  - Numbered formal bundle layout under configured artifact_root
  - 0-report/report.html as customer entry point
  - 1-wandb raw offline data and rebuild script location
  - 2-prometheus telemetry/OpenMetrics evidence location
  - 3-raw-logs, 4-config, 5-provenance, 6-rows, and restore layout
  - Manifest artifact_layout metadata and backward-compatible report loading
key-files:
  modified:
    - autoresearch/orchestrator/verl_case.py
    - autoresearch/report/cli.py
    - autoresearch/report/logs.py
    - autoresearch/report/prometheus.py
    - autoresearch/report/verl_case.py
    - autoresearch/report/wandb.py
    - datalake/manifest/schema.py
    - datalake/wandb/sync.py
    - workspace-adapter/verl/SKILL.md
    - tests/test_orchestrator_verl_case.py
    - tests/test_report_cli.py
    - tests/test_datalake_wandb_sync.py
commits:
  - ed22bf0 feat(15): persist verl timings and numbered artifacts
---

# Phase 15 Plan 04 Summary: Numbered Data Repository Bundle

Formal Verl bundles now use the customer-reading order requested for the separate `autoresearch-log` data repository. The code repository owns logic; the data repository owns immutable configs, provenance, logs, W&B, Prometheus evidence, rows, stage timings, and reports.

## What Changed

- New runs create:
  - `0-report/`
  - `1-wandb/`
  - `2-prometheus/`
  - `3-raw-logs/`
  - `4-config/`
  - `5-provenance/`
  - `6-rows/`
  - `restore/`
- `manifest.json` records `artifact_layout.version` and section names.
- `autoresearch report render` writes `0-report/report.html` for numbered formal bundles while preserving old flat bundle behavior.
- W&B sync accepts `local_wandb_dir`, so formal runs store W&B artifacts directly in `1-wandb/`.
- Report loaders resolve both new and old paths for matrix, logs, W&B, Prometheus, config, and provenance.
- Root `RUN.md` explains the numbered bundle; root `README.md` points users to `RUN.md` and `0-report/report.html`.
- `workspace-adapter/verl/SKILL.md` now documents the true GRPO/3-step and numbered-bundle workflow.

## Verification

```bash
uv run pytest -q tests/test_report_cli.py tests/test_datalake_wandb_sync.py tests/test_orchestrator_verl_case.py tests/test_report_loader.py tests/test_report_wandb.py tests/test_report_prometheus.py tests/test_report_render.py tests/test_datalake_manifest.py
```

Result: `54 passed`.

Full regression on 2026-06-22:

```bash
uv run pytest -q
```

Result: `467 passed, 6 warnings`.

## Remaining Operational Step

Once a free A2 host is available, rerun the real formal GRPO case. The resulting `autoresearch-log` bundle should be pushed with the same numbered layout and must include the code commit id `ed22bf0` or a later successor.


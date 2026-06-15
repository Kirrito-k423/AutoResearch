---
phase: 12-e2e-smoke
plan: 02
status: completed
completed_at: "2026-06-15"
requirements:
  - E2E-02
---

# Phase 12 Plan 02 Summary: Report completeness check

## What changed

- Added `autoresearch.e2e.report_check.check_report_completeness(...)`.
- The completeness oracle loads the report bundle from the run manifest and checks four required surfaces:
  - generated `report.html`
  - local log artifact
  - local wandb artifact
  - Prometheus query availability
- Wired the oracle into `run_e2e_smoke` after the smoke run and before Archon/duration gates.
- Missing report views now fail E2E with `failed_step=report` and a compact `missing` list.

## Verification

- `uv run pytest tests/test_e2e_smoke.py tests/test_report_loader.py tests/test_cli.py -q` -> 14 passed
- `uv run pytest -q` -> 361 passed, 6 warnings
- Real E2E report completeness for run `01KV62JVH0N3ZRVRMH4PYWF1VB` passed with no missing views.

## UAT evidence

Report completeness payload:

- `html.ok=true`
- `log.ok=true`
- `wandb.ok=true`
- `prometheus.ok=true`
- `missing=[]`
- `warnings=[]`


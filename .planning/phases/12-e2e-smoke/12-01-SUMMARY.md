---
phase: 12-e2e-smoke
plan: 01
status: completed
completed_at: "2026-06-15"
requirements:
  - E2E-01
  - E2E-03
  - E2E-04
---

# Phase 12 Plan 01 Summary: E2E smoke CLI

## What changed

- Added the `autoresearch e2e smoke` command as the Phase 12 E2E entrypoint.
- Implemented `autoresearch.e2e.smoke.run_e2e_smoke(...)` to run readiness, smoke, report completeness, Archon observability, and duration gates.
- Added step-normalized JSON output with `failed_step`, `elapsed_seconds`, nested step payloads, and progress events.
- Added CLI options for server/lib selection, config/workdir overrides, run id, Pushgateway/Prometheus URLs, Archon URL, max duration, and remote proxy port.

## Verification

- `uv run pytest tests/test_e2e_smoke.py tests/test_report_loader.py tests/test_cli.py -q` -> 14 passed
- `uv run autoresearch e2e smoke --help` -> help lists `--server`, `--max-duration`, and `--archon-url`
- `uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` -> `ok=true`

## UAT evidence

- Run id: `01KV62JVH0N3ZRVRMH4PYWF1VB`
- Report: `/Users/Zhuanz/.autoresearch/runs/01KV62JVH0N3ZRVRMH4PYWF1VB/report.html`
- Duration: `146.673` seconds, under the 30 minute gate
- Archon observable: `http://localhost:8088/healthz` returned 200 and `.archon/workflows/ar-min-loop.yaml` existed


---
phase: 11-orchestration
plan: 02
status: completed
subsystem: orchestrator
tags: [cli, orchestration, collect, report, prometheus]

requirements-completed:
  - ORCH-RUN-01
  - ORCH-RUN-02
  - ORCH-LOG-01

completed: 2026-06-15
---

# Phase 11 Plan 02: `autoresearch run smoke` Summary

Plan 02 added the top-level smoke run orchestrator.

## Accomplishments

- Added `autoresearch/orchestrator/smoke.py` to run `collect -> report` and return one unified step report.
- Added failure routing with `failed_step`, per-step diagnostics, and skipped report behavior when collect fails.
- Added `autoresearch run smoke` CLI with server, lib, config, workdir, timeout, run id, Pushgateway, Prometheus, and report-open options.
- Added a Prometheus scrape wait before report rendering so freshly pushed Pushgateway metrics appear in the generated report.
- Preserved stdout as a single JSON object and emitted progress via `orch.smoke.*` `__AR_PROGRESS__=` stages.

## Verification

```bash
uv run pytest tests/test_orchestrator_smoke.py tests/test_cli.py -q
```

Result: covered by the final full suite in `11-VERIFICATION.md`.

```bash
uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891
```

Result: `ok=true`, collect and report passed.

## Real Run Output

- run id: `01KV60QS8PMSEG02MQEB0Z27FT`
- manifest: `/Users/Zhuanz/.autoresearch/runs/01KV60QS8PMSEG02MQEB0Z27FT/manifest.json`
- report: `/Users/Zhuanz/.autoresearch/runs/01KV60QS8PMSEG02MQEB0Z27FT/report.html`
- Prometheus: `prometheus_ready=true`; report warnings `[]`

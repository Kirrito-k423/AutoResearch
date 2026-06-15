---
status: partial
phase: 08-skill-07-data-collection
source: 08-01-SUMMARY.md, 08-02-SUMMARY.md, 08-03-SUMMARY.md, 08-04-SUMMARY.md
started: 2026-06-15T10:28:47Z
updated: 2026-06-15T10:28:47Z
---

## Current Test

[testing paused - 2 runtime items blocked by local Docker/wandb services]

## Tests

### 1. Minimal Runner With Remote Log Path
expected: `collect_minimal(..., run_id=...)` passes run_id to the selected runner, runner writes `<workdir>/runs/<run_id>.log`, and returns `remote_log_path`.
result: pass
evidence: `uv run pytest tests/test_minimal_runner.py tests/test_collect_minimal.py -q`

### 2. Local Log Collection
expected: `collect_log()` pulls the remote run log into `~/.autoresearch/runs/<run-id>/log.txt` and reports readable errors for missing/permission failures.
result: pass
evidence: `uv run pytest tests/test_datalake_logs_collector.py -q`

### 3. Manifest And Collect CLI
expected: `autoresearch collect run` orchestrates minimal, wandb sync, log collect, prom push, manifest write, and prints exactly one JSON object.
result: pass
evidence: `uv run pytest tests/test_collect_cli.py tests/test_collect_manifest.py tests/test_datalake_manifest.py -q`

### 4. Local wandb Sync Visible In UI
expected: A real run can sync into local wandb and be visible through the local wandb service.
result: blocked
blocked_by: third-party
reason: Local Docker Desktop backend is not responding; `autoresearch services status --json` reports wandb unhealthy and Docker socket `_ping` times out.

### 5. Prometheus Pushgateway Visible Metric
expected: A real run pushes `autoresearch_npu_count` through pushgateway and local Prometheus can query it.
result: blocked
blocked_by: third-party
reason: Local pushgateway/prometheus services are unhealthy and ports 9091/9090 have no listeners while Docker socket `_ping` times out.

## Summary

total: 5
passed: 3
issues: 0
pending: 0
skipped: 0
blocked: 2

## Gaps

- truth: "Local wandb service accepts synced offline runs and shows them in UI"
  status: blocked
  reason: "Docker Desktop backend/socket does not respond; wandb service is unhealthy."
  severity: blocker
  test: 4
  root_cause: "External local runtime failure, not Phase 8 code path."
  artifacts:
    - path: "services/wandb/compose.yml"
      issue: "Cannot start or verify while Docker socket _ping times out."
  missing:
    - "Restore Docker Desktop backend, then run `autoresearch services start` and repeat real collect UAT."
  debug_session: ""
- truth: "Local Prometheus can see a metric pushed through pushgateway"
  status: blocked
  reason: "pushgateway/prometheus services are unhealthy because Docker backend is unavailable."
  severity: blocker
  test: 5
  root_cause: "External local runtime failure, not Phase 8 code path."
  artifacts:
    - path: "services/prometheus/compose.yml"
      issue: "Cannot start or verify while Docker socket _ping times out."
  missing:
    - "Restore Docker Desktop backend, start pushgateway/prometheus, and repeat prom metric UAT."
  debug_session: ""

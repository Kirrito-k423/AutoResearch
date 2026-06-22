---
phase: 15-verl-npu-hbm-core-qwen3-5-grpo
plan: 01
subsystem: observability
tags: [verl, npu-smi, prometheus, telemetry, report]
requires:
  - phase: 14-verl-workspace-adapter-verl
    provides: formal Verl case runner, local artifact collection, Prometheus/W&B/report surfaces
provides:
  - Runtime npu-smi watch telemetry command/parser for formal Verl cases
  - Per-row telemetry raw log, normalized JSONL, and row summary fields
  - Prometheus text exposition for HBM/Core/NPU resource metrics
  - Report fallback that renders saved resource curves without live Prometheus
affects: [15-02, 15-03, 15-04, autoresearch run verl-case, experiment-report]
tech-stack:
  added: []
  patterns:
    - Save raw evidence and normalized rows before pushing to live services
    - Keep Prometheus live push best-effort while making local evidence authoritative
key-files:
  created:
    - workspace-adapter/verl/telemetry.py
    - tests/test_verl_telemetry.py
  modified:
    - workspace-adapter/verl/case_config.py
    - workspace-adapter/verl/case_runner.py
    - datalake/prometheus/push_gateway.py
    - datalake/prometheus/__init__.py
    - autoresearch/orchestrator/verl_case.py
    - autoresearch/report/models.py
    - autoresearch/report/prometheus.py
    - autoresearch/report/render.py
    - tests/test_verl_case_runner.py
    - tests/test_datalake_prometheus_push.py
    - tests/test_orchestrator_verl_case.py
    - tests/test_report_prometheus.py
    - tests/test_report_render.py
key-decisions:
  - "Use native npu-smi info watch -d 1 -s amn and reject 0.5s native sampling claims."
  - "Persist OpenMetrics text exposition so Prometheus-style curves rebuild from the data bundle."
  - "Report live Prometheus failures as non-fatal when local telemetry evidence exists."
patterns-established:
  - "Telemetry parser is pure and separately tested before being embedded in remote row execution."
  - "Prometheus resource metrics use labels run_id, case_id, server, device_id, and source."
requirements-completed: []
duration: 20 min
completed: 2026-06-22
---

# Phase 15 Plan 01: Runtime NPU HBM/Core Telemetry And Prometheus Evidence Summary

**Native `npu-smi watch` telemetry now produces per-case raw logs, normalized rows, Prometheus resource evidence, and offline report curves.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-22T12:04:32Z
- **Completed:** 2026-06-22T12:24:27Z
- **Tasks:** 4
- **Files modified:** 13

## Accomplishments

- Added `workspace-adapter/verl/telemetry.py` with command construction, parser, and summary helpers for native 1s `npu-smi info watch -d 1 -s amn`.
- Wrapped each generated formal Verl row command with a best-effort sampler that writes `npu-smi-watch.raw.log`, `npu-telemetry.jsonl`, and result-level telemetry metadata without masking the Verl exit status.
- Added Prometheus/OpenMetrics evidence for HBM used, HBM total, AI Core utilization, and NPU utilization with run/case/server/device/source labels.
- Extended the report loader and renderer so HBM/Core/NPU curves render from saved local evidence when live Prometheus has no matching data or is down.

## Task Commits

Each task was committed atomically:

1. **Task 15-01-01: Add typed NPU telemetry parser and command builder** - `a76e3c6` (`feat(15-01): add npu telemetry parser`)
2. **Task 15-01-02: Run telemetry sampler around every Verl case** - `cead0a1` (`feat(15-01): collect npu telemetry per verl case`)
3. **Task 15-01-03: Export telemetry as Prometheus-compatible evidence** - `71c4b61` (`feat(15-01): export npu telemetry prometheus evidence`)
4. **Task 15-01-04: Load saved telemetry curves in reports when live Prometheus is unavailable** - `aa2ace6` (`feat(15-01): render telemetry resource curves`)

## Files Created/Modified

- `workspace-adapter/verl/telemetry.py` - Pure telemetry command, parser, and summary helpers.
- `workspace-adapter/verl/case_runner.py` - Starts/stops sampler around each remote row command and writes telemetry artifacts.
- `workspace-adapter/verl/case_config.py` - Adds optional telemetry fields to `VerlCaseResultRow`.
- `datalake/prometheus/push_gateway.py` - Builds and pushes resource OpenMetrics exposition.
- `autoresearch/orchestrator/verl_case.py` - Reads row telemetry JSONL, saves OpenMetrics evidence, and pushes telemetry metrics.
- `autoresearch/report/prometheus.py` - Loads saved resource curves as live Prometheus fallback.
- `autoresearch/report/render.py` - Renders HBM/Core/NPU resource charts.

## Decisions Made

- Native watch remains 1s because A2-AK-225 reports `npu-smi info watch -d` supports only `[1~100]`.
- Empty telemetry samples now produce no OpenMetrics payload, preventing false claims that resource metrics exist.
- Live Prometheus is optional for report curves once local telemetry evidence exists.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added telemetry fields to the result row model**
- **Found during:** Task 15-01-02 (Run telemetry sampler around every Verl case)
- **Issue:** The plan asked for row results to include telemetry paths and summary, but `VerlCaseResultRow` would otherwise drop those fields.
- **Fix:** Added `telemetry_raw_path`, `telemetry_jsonl_path`, and `telemetry_summary`.
- **Files modified:** `workspace-adapter/verl/case_config.py`
- **Verification:** `uv run pytest -q tests/test_verl_case_runner.py -k "row_command or run_verl_case"` passed.
- **Committed in:** `cead0a1`

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** Required for correctness; no scope creep beyond preserving planned telemetry evidence.

## Issues Encountered

- Empty telemetry rows initially generated a header-only OpenMetrics payload, which made orchestration think resource metrics existed. Fixed by returning an empty exposition when no metric samples are emitted and added regression coverage.

## Verification

```bash
uv run pytest -q tests/test_verl_telemetry.py tests/test_verl_case_runner.py tests/test_datalake_prometheus_push.py tests/test_report_prometheus.py tests/test_report_render.py
```

Result: `59 passed`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 15-02 can now rely on per-case NPU telemetry artifacts and reportable resource curves while adding real three-step GRPO training cases. Plan 15-04 can reuse the saved OpenMetrics file under the numbered `2-prometheus/` bundle.

## Self-Check: PASSED

- All four planned tasks completed.
- All task-level and plan-level verification commands passed.
- SUMMARY includes the required deviation and task commit mapping.

---
*Phase: 15-verl-npu-hbm-core-qwen3-5-grpo*
*Completed: 2026-06-22*

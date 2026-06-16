---
phase: 14-verl-workspace-adapter-verl
plan: 03
subsystem: autoresearch-run
tags: [verl-case, cli, orchestration, local-artifacts, provenance]
requires:
  - phase: 14-01
    provides: formal-case config and manifest schema
  - phase: 14-02
    provides: Docker/data/provenance/remote-runner boundaries
provides:
  - `autoresearch run verl-case` CLI command
  - Formal-case orchestration over skills 1-6 readiness
  - Local run directory artifacts for config, provenance, matrix, log, Prometheus evidence, manifest, and report
  - Configurable dependency repository provenance paths
affects: [autoresearch, workspace-core, workspace-adapter, datalake, tests]
tech-stack:
  added: []
  patterns: [click-command, local-first-run-artifacts, mockable-orchestrator]
key-files:
  created:
    - autoresearch/orchestrator/verl_case.py
    - tests/test_orchestrator_verl_case.py
  modified:
    - autoresearch/cli.py
    - autoresearch/orchestrator/__init__.py
    - workspace-core/config/schema.py
    - workspace-adapter/verl/case_config.py
    - config/config.example.yaml
    - datalake/prometheus/push_gateway.py
    - datalake/wandb/sync.py
    - tests/workspace-core/test_config.py
key-decisions:
  - "Default `autoresearch run verl-case` runs skills 1-6 readiness; `--skip-readiness` is explicit."
  - "Server selection is config-driven: `--server` overrides, otherwise the first configured server is used."
  - "Top-level `ok=true` requires local matrix, manifest, config snapshot, provenance, log, and report artifacts to exist."
  - "Dependency repo paths are configurable under `verl_case.dependency_repo_paths`; missing paths warn instead of failing."
patterns-established:
  - "Formal-case orchestration mirrors smoke/check payloads and final stdout JSON protocol."
  - "Hyphenated `workspace-adapter` runtime imports use `importlib` in normal Python modules."
requirements-completed: []
duration: 20min
completed: 2026-06-16
---

# Phase 14 Plan 03: `autoresearch run verl-case` Orchestration And Local Artifacts Summary

**A user-facing formal-case command now wires readiness, immutable config, provenance, remote matrix execution, and local-first artifacts into one JSON-result workflow**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-16T15:36:56Z
- **Completed:** 2026-06-16T15:56:09Z
- **Tasks:** 4 completed
- **Files modified:** 10

## Accomplishments

- Added `run_verl_case_orchestration(...)` with progress stages for start, readiness, prepare, run, collect, report, and result.
- Added `autoresearch run verl-case` with options for server/config/workdir/timeout/run-id/cache/proxy/readiness/Git push/report opening.
- Persisted local formal-case artifacts under the run directory: immutable config snapshot, `provenance.json`, `matrix-results.jsonl`, `verl-case.log`, Prometheus evidence JSON, W&B artifact directory, `manifest.json`, and `report.html`.
- Added dependency provenance configuration for `verl`, `vllm`, `transformers`, and `mindspeed`; missing configured paths are warnings, not failures.
- Preserved existing `run smoke` behavior and CLI JSON protocol.

## Task Commits

1. **Task 14-03: Verl case orchestration and CLI artifacts** - `e8cdfde` (feat)

## Files Created/Modified

- `autoresearch/orchestrator/verl_case.py` - Formal-case orchestration, artifact persistence, manifest writing, and provenance wiring.
- `tests/test_orchestrator_verl_case.py` - Readiness, success artifact, matrix failure, provenance warning, and CLI JSON tests.
- `autoresearch/cli.py` - Added `run verl-case` command.
- `autoresearch/orchestrator/__init__.py` - Exported `run_verl_case_orchestration`.
- `workspace-core/config/schema.py` - Added `verl_case.dependency_repo_paths`.
- `workspace-adapter/verl/case_config.py` - Mirrored dependency path field in serializable formal-case config.
- `config/config.example.yaml` - Documented configurable dependency repo paths.
- `tests/workspace-core/test_config.py` - Covered dependency path config parsing.
- `datalake/prometheus/push_gateway.py` and `datalake/wandb/sync.py` - Replaced invalid hyphen imports with `importlib`.

## Decisions Made

- Kept real remote execution behind the Phase 14 runner; 14-03 verifies orchestration boundaries with mocks and local files.
- Kept automatic Git mutation behind `--allow-git-push`; provenance capture runs without mutation by default.
- Let existing report rendering produce the initial `report.html`; formal performance/accuracy-specific report polish is reserved for 14-04.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed existing datalake imports from hyphenated package names**
- **Found during:** 14-03 implementation scan
- **Issue:** `datalake/prometheus/push_gateway.py` and `datalake/wandb/sync.py` used `from workspace-adapter...` import syntax, which is invalid Python and would break CLI import paths touched by this plan.
- **Fix:** Switched both modules to `importlib.import_module("workspace-adapter...")` while preserving module-level names for existing tests.
- **Files modified:** `datalake/prometheus/push_gateway.py`, `datalake/wandb/sync.py`
- **Verification:** Included in the 65-test focused suite.
- **Committed in:** `e8cdfde`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Required to keep formal-case orchestration and existing collect/report helpers importable.

## Issues Encountered

- `workspace_core` is copied into the active `.venv`; after adding `verl_case.dependency_repo_paths`, ran `uv pip install -e .` before tests.

## Verification

```bash
uv pip install -e .
uv run pytest -q tests/test_orchestrator_verl_case.py tests/test_cli.py tests/test_orchestrator_smoke.py tests/test_verl_case_runner.py tests/test_verl_case_config.py tests/test_datalake_manifest.py tests/test_report_loader.py tests/test_report_render.py tests/test_report_cli.py tests/workspace-core/test_config.py tests/test_datalake_prometheus_push.py tests/test_datalake_wandb_sync.py
uv run autoresearch run verl-case --help
```

Result: 65 passed; CLI help displayed `run verl-case` options.

## User Setup Required

Real execution still needs the remote machine/Docker/image/model/data path readiness and local observability services. The command supports `--skip-readiness` for controlled debugging, but default execution runs the readiness gates.

## Next Phase Readiness

Ready for 14-04: formal report/verification can consume the local run directory and real or mocked matrix artifacts produced by `autoresearch run verl-case`.

---
*Phase: 14-verl-workspace-adapter-verl*
*Completed: 2026-06-16*

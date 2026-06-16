---
phase: 14-verl-workspace-adapter-verl
plan: 02
subsystem: workspace-adapter-verl
tags: [verl, docker, geometry3k, provenance, remote-runner]
requires:
  - phase: 14-01
    provides: formal-case config, strict matrix, result models, and manifest fields
provides:
  - Ascend Docker command builder for Verl formal cases
  - geometry3k local preparation boundary preserving image/problem/answer rows
  - multi-repo Git provenance capture with explicit commit/push gate
  - remote Verl formal-case runner boundary over the strict sync/async matrix
affects: [workspace-adapter, tests]
tech-stack:
  added: []
  patterns: [ascend-docker-command-builder, local-cache-data-prep, mockable-remote-runner]
key-files:
  created:
    - workspace-adapter/verl/docker.py
    - workspace-adapter/verl/data_prep.py
    - workspace-adapter/verl/provenance.py
    - workspace-adapter/verl/case_runner.py
    - tests/test_verl_case_runner.py
  modified: []
key-decisions:
  - "Keep remote commit/push behind allow_commit_push so experiment repos can be made immutable only when explicitly requested."
  - "Preserve geometry3k multimodal rows and fail fast when image/problem/answer fields are missing."
  - "Use a runner injection point for remote execution so Docker/provenance behavior is unit-testable without Ascend hardware."
patterns-established:
  - "Docker command construction is centralized under workspace-adapter/verl/docker.py instead of inline shell fragments."
  - "Remote formal-case runs parse row-level VERL_CASE_RESULT payloads and mark top-level failure when any row fails."
requirements-completed: []
duration: 6min
completed: 2026-06-16
---

# Phase 14 Plan 02: Verl Docker, Data Prep, Provenance, And Remote Formal Runner Summary

**A testable remote execution boundary for the formal Verl case, covering Ascend Docker launch shape, geometry3k prep, Git provenance, and strict matrix failure semantics**

## Performance

- **Duration:** 6 min
- **Started:** 2026-06-16T15:30:49Z
- **Completed:** 2026-06-16T15:36:56Z
- **Tasks:** 4 completed
- **Files modified:** 5

## Accomplishments

- Added Ascend A2 Docker pull/run command builders using the target image, device flags, driver mounts, shared memory, proxy env vars, and model/dataset/output mounts.
- Added geometry3k preparation that writes Verl-ready JSONL while preserving `image`, `problem`, `answer`, and `sample_id`; missing multimodal fields raise `DataPrepError`.
- Added Git provenance capture for AutoResearch and dependency repositories, including fork/branch URL derivation and explicit optional commit/push behavior.
- Added a remote formal-case runner boundary that pulls the image, executes every sync/async length-matrix row, parses row metrics, and fails the top-level run if any matrix row fails.
- Added a local execution test for the generated row script after catching a quoting bug in the first implementation.

## Task Commits

1. **Task 14-02: Docker/data/provenance/runner boundaries** - `98db88a` (feat)

## Files Created/Modified

- `workspace-adapter/verl/docker.py` - Ascend-compatible Docker pull/run command builders.
- `workspace-adapter/verl/data_prep.py` - geometry3k local preparation boundary and typed data-prep error.
- `workspace-adapter/verl/provenance.py` - Git provenance capture and optional commit/push hook.
- `workspace-adapter/verl/case_runner.py` - Remote formal-case runner and row-level result parsing.
- `tests/test_verl_case_runner.py` - Unit coverage for Docker command shape, geometry3k prep, provenance, runner failure semantics, and generated row script execution.

## Decisions Made

- Kept actual Hugging Face downloads out of unit tests; the data-prep boundary accepts local cached fixtures now and can be wired to CLI orchestration in 14-03.
- Used `python3` plus a shell-quoted here-doc for generated remote row scripts because the Mac test environment has no bare `python`.
- Kept dependency-repo mutation explicit through `allow_commit_push`; provenance can be captured without pushing.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed generated remote row-script quoting**
- **Found during:** Focused 14-02 verification
- **Issue:** The first generated row command encoded the here-doc with escaped newlines and assigned JSON as a string, so shell/Python execution would fail before a real remote run.
- **Fix:** Switched to a real multiline script wrapped with `shlex.quote`, loaded config via `json.loads(...)`, and added a subprocess test for `_row_command`.
- **Files modified:** `workspace-adapter/verl/case_runner.py`, `tests/test_verl_case_runner.py`
- **Verification:** `uv run pytest -q tests/test_verl_case_runner.py tests/test_verl_case_config.py` passed.
- **Committed in:** `98db88a`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Improved remote-run reliability before integrating the CLI orchestration.

## Issues Encountered

- No real Ascend Docker run was attempted in 14-02; this plan intentionally establishes testable boundaries. Real server execution is deferred to 14-03/14-04.

## Verification

```bash
uv run pytest -q tests/test_verl_case_runner.py tests/test_verl_case_config.py
```

Result: 11 passed.

## User Setup Required

None for this plan. Real execution still depends on configured remote server access, Docker image availability, cached model/data, and local observability services in the next plans.

## Next Phase Readiness

Ready for 14-03: `autoresearch run verl-case` can wire config loading, local cache paths, immutable snapshots, provenance capture, and runner invocation into the CLI/artifact loop.

---
*Phase: 14-verl-workspace-adapter-verl*
*Completed: 2026-06-16*

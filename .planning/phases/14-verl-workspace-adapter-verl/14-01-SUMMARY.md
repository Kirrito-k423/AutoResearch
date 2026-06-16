---
phase: 14-verl-workspace-adapter-verl
plan: 01
subsystem: config
tags: [verl, config, manifest, provenance, evaluation]
requires:
  - phase: 13-m1-archive
    provides: v1.0 local-first baseline and planning archive
provides:
  - Formal Verl case config defaults
  - Strict sync/async length matrix helpers
  - Immutable config snapshot writer
  - Geometry answer evaluation helpers
  - Manifest fields for formal-case artifacts and provenance
affects: [workspace-core, workspace-adapter, datalake, tests]
tech-stack:
  added: []
  patterns: [pydantic-config, local-first-manifest, importlib-hyphen-package]
key-files:
  created:
    - workspace-adapter/verl/case_config.py
    - workspace-adapter/verl/evaluation.py
    - tests/test_verl_case_config.py
  modified:
    - workspace-core/config/schema.py
    - workspace-core/config/__init__.py
    - config/config.example.yaml
    - datalake/manifest/schema.py
    - tests/workspace-core/test_config.py
    - tests/test_datalake_manifest.py
    - tests/test_minimal_runner.py
key-decisions:
  - "Use Pydantic models for formal-case config and result rows so immutable snapshots serialize cleanly."
  - "Keep geometry answer scoring dependency-free and deterministic for unit tests."
  - "Fix existing hyphen-package test imports with importlib because Python import statements cannot parse workspace-adapter."
patterns-established:
  - "Formal case fields extend RunManifest without breaking minimal-run manifests."
  - "Workspace-adapter modules with a hyphenated top-level package are imported via importlib in tests."
requirements-completed: []
duration: 18min
completed: 2026-06-16
---

# Phase 14 Plan 01: Formal Case Config, Matrix, Evaluation, And Provenance Models Summary

**Typed Verl formal-case contract with strict matrix generation, immutable snapshots, answer scoring, and manifest provenance fields**

## Performance

- **Duration:** 18 min
- **Started:** 2026-06-16T15:12:00Z
- **Completed:** 2026-06-16T15:30:49Z
- **Tasks:** 4 completed
- **Files modified:** 10

## Accomplishments

- Added non-secret `verl_case` config defaults for cache root, Docker image, Qwen3.5-2B, geometry3k, strict output lengths, `ignore_eos=false`, modes, GitHub owner, and remote workdir.
- Added formal-case matrix/provenance/result models and immutable config snapshot writer under `workspace-adapter/verl`.
- Added deterministic answer extraction and scoring helpers for geometry ground truth and sync/async consistency.
- Extended `RunManifest` with optional `formal_case`, `config_snapshot`, and `provenance` fields while preserving existing minimal-run compatibility.
- Repaired the existing `tests/test_minimal_runner.py` import/patch syntax so the suite can collect tests that touch `workspace-adapter`.

## Task Commits

1. **Task 14-01: Config, matrix, evaluation, manifest contracts** - `adfc29c` (feat)

## Files Created/Modified

- `workspace-adapter/verl/case_config.py` - Verl formal-case config, matrix rows, provenance, result rows, and immutable snapshot writer.
- `workspace-adapter/verl/evaluation.py` - Deterministic geometry answer extraction and scoring helpers.
- `tests/test_verl_case_config.py` - Unit tests for strict matrix, immutable config, and answer scoring.
- `workspace-core/config/schema.py` - Added `VerlCaseConfig` and `Config.verl_case`.
- `workspace-core/config/__init__.py` - Exported `VerlCaseConfig`.
- `config/config.example.yaml` - Documented non-secret formal-case defaults.
- `datalake/manifest/schema.py` - Added formal-case manifest fields.
- `tests/workspace-core/test_config.py` - Covered defaults and override parsing.
- `tests/test_datalake_manifest.py` - Covered formal-case manifest serialization.
- `tests/test_minimal_runner.py` - Replaced invalid `workspace-adapter` import/patch syntax with `importlib` and `patch.object`.

## Decisions Made

- Kept token/secret handling out of config snapshots; only non-secret reproducibility fields are serialized.
- Used second-level UTC timestamps in immutable config filenames.
- Treated the invalid `workspace-adapter` test imports as a blocking deviation because they prevented Phase 14 test collection.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed existing `tests/test_minimal_runner.py` syntax and patch targets**
- **Found during:** Wave 1 focused verification
- **Issue:** The test file contained `from workspace-adapter...` import statements and `patch("workspace-adapter...")` targets. Python cannot parse the import syntax, and `unittest.mock.patch` rejects hyphenated module names.
- **Fix:** Replaced imports with `importlib.import_module("workspace-adapter...")` and replaced string patch targets with `patch.object(...)` on dynamically imported modules.
- **Files modified:** `tests/test_minimal_runner.py`
- **Verification:** `uv run pytest -q tests/workspace-core/test_config.py tests/test_datalake_manifest.py tests/test_verl_case_config.py tests/test_minimal_runner.py` passed.
- **Committed in:** `adfc29c`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Required for test collection and directly related to the `workspace-adapter/verl` execution surface. No product behavior changed.

## Issues Encountered

- `workspace_core` is installed into `.venv` as a package copy. Ran `uv pip install -e .` after source edits so the current test environment sees `workspace-core` changes.

## Verification

```bash
uv pip install -e .
uv run pytest -q tests/workspace-core/test_config.py tests/test_datalake_manifest.py tests/test_verl_case_config.py tests/test_minimal_runner.py
```

Result: 35 passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for 14-02: Docker command builder, geometry3k prep boundary, provenance capture, and remote formal runner can consume the config/matrix/provenance models.

---
*Phase: 14-verl-workspace-adapter-verl*
*Completed: 2026-06-16*

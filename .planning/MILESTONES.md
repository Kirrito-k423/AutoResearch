# Milestones

## v1.1 Formal Verl (Shipped: 2026-06-18)

**Status:** shipped
**Shipped:** 2026-06-18
**Phases:** 14
**Plans:** 5 summaries
**Requirements:** scoped by Phase 14 ROADMAP goal and `v1.1-MILESTONE-AUDIT.md`
**Final run:** `formal-20260618-a2ak225-combined-r1`
**Tag:** `v1.1`

### Delivered

AutoResearch v1.1 ships a formal, non-demo Verl case loop for Qwen3.5-2B + geometry3k on Ascend. The final combined artifact preserves immutable configs, local W&B/Prometheus/log data, multi-repo provenance, and sync/async sequence-length results through 16k output tokens.

### Key Accomplishments

1. Added typed formal-case configuration, strict sync/async matrix generation, scoring, and immutable manifest/provenance fields.
2. Added `autoresearch run verl-case` to orchestrate readiness checks, remote Docker execution, local artifact sync, and one final JSON result.
3. Prepared and ran Qwen3.5-2B + geometry3k formal rows on `A2-AK-225` with the official Ascend Verl image path recorded.
4. Completed the 8-row matrix: sync and async modes at 1024 input tokens with 2048, 4096, 8192, and 16384 output tokens.
5. Preserved final evidence under `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1`.
6. Recorded sequence-length and async-vs-sync observations in the Phase 14 summary and final HTML report.

### Verification

- `uv run pytest tests/test_verl_case_runner.py tests/test_minimal_runner.py -q` -> 58 passed
- `uv run pytest -q` -> 435 passed, 6 warnings
- `uv run autoresearch report render --run-id formal-20260618-a2ak225-combined-r1` -> ok
- Matrix result: 8/8 rows passed in `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/matrix-results.jsonl`

### Known Gaps

- Prometheus live query in the final report returned no current metric, but local Prometheus evidence is preserved at `prom/formal-case-prometheus.json`.
- Accuracy uses the configured two-sample geometry3k validation slice and is not a broad model-quality benchmark.
- Open artifact audit reported 4 UAT entries at close; all had 0 pending scenarios and were acknowledged in `STATE.md`.

### Archive

- `.planning/milestones/v1.1-ROADMAP.md`
- `.planning/milestones/v1.1-REQUIREMENTS.md`
- `.planning/milestones/v1.1-MILESTONE-AUDIT.md`

---

## v1.0 MinViable Loop

**Status:** shipped
**Shipped:** 2026-06-15
**Phases:** 1-13
**Plans:** 37 summaries after Phase 13
**Requirements:** 82/88 checked
**Branch:** `codex/phase-02-workspace-core`
**PR:** `https://github.com/Kirrito-k423/AutoResearch/pull/1`
**Tag:** `v1.0`

### Delivered

AutoResearch v1.0 ships the local-first M1 loop: configure, check services,
probe hardware/network/reachability/stack, run a minimal remote training smoke,
collect log/wandb/prometheus artifacts locally, render a report, and verify the
whole path through `autoresearch e2e smoke`.

### Key Accomplishments

1. Built the Python package, Click CLI, service compose files, and local-first workspace layout.
2. Added `workspace-core` for config, secrets, SSH, progress, logging, and run directory conventions.
3. Implemented the eight M1 skill groups from config through report rendering.
4. Added Archon workflow assets for each skill plus the main `ar-min-loop` workflow.
5. Added top-level orchestration commands: `autoresearch check all`, `autoresearch run smoke`, and `autoresearch e2e smoke`.
6. Passed real A2-AK-225 E2E smoke in 146.673 seconds with report html/log/wandb/prometheus all present.

### Verification

- `uv run pytest -q` -> 361 passed, 6 warnings
- `uv run autoresearch check all --server A2-AK-225 --stack-lib verl` -> ok
- `uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` -> ok
- `uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` -> ok, run `01KV62JVH0N3ZRVRMH4PYWF1VB`

### Known Gaps

- HW-CONN-01, HW-CONN-02, HW-OCC-01, HW-OCC-02, NET-TUNNEL-01, and NET-TUNNEL-02 remain archived as known follow-up gaps.
- Phase 04 UAT remains partial because several configured machines still have BMC, SSH, or driver-level blockers outside the code path.
- Open artifact audit reported 2 UAT items at close; both were acknowledged and deferred with zero pending scenarios.

### Archive

- `.planning/milestones/v1.0/ROADMAP.md`
- `.planning/milestones/v1.0/REQUIREMENTS.md`
- `.planning/milestones/v1.0/PROJECT.md`
- `.planning/milestones/v1.0/STATE.md`
- `.planning/milestones/v1.0/INDEX.md`

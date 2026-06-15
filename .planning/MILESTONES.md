# Milestones

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

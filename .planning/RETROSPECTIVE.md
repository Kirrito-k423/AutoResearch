# Retrospective

## Milestone: v1.0 — MinViable Loop

**Shipped:** 2026-06-15
**Phases:** 13
**Plans:** 37 summaries after Phase 13

### What Was Built

- Local service stack and health CLI.
- Shared workspace-core foundations for SSH, config, secrets, progress, logs, and run layout.
- Hardware, network, reachability, stack, collection, and report skill groups.
- Archon workflow assets for the eight skills and main minimum loop.
- Top-level CLI orchestration and E2E smoke validation.

### What Worked

- The local-first artifact model made verification repeatable: logs, wandb, Prometheus, manifests, and reports all resolved from the Mac.
- Reusing Python `run_*` entrypoints kept orchestration debuggable and avoided brittle shell stitching.
- The progress protocol made long-running real-server checks observable enough to diagnose transient failures.

### What Was Inefficient

- Real hardware and BMC variability forced several historical UAT gaps to remain as operational follow-up.
- Local services needed practical repair work before higher-level workflows could be trusted.
- Archon provider auth made script-node verification more reliable than provider-driven loop execution for v1.0.

### Patterns Established

- CLI commands print one final JSON object and progress only on stderr.
- Warnings are allowed for known operational degradation; failures stop orchestrators at the named step.
- Reports are reconstructed from manifests and local artifacts instead of remote state.
- Remote no-network cases use reverse proxy fallback through the Mac.

### Key Lessons

- The best acceptance test for this project is a real A2-AK-225 E2E smoke, not just unit tests.
- Prometheus needs scrape wait time after Pushgateway writes; otherwise reports can be falsely incomplete.
- Milestone archives should preserve known gaps honestly instead of checking them off cosmetically.

### Deferred Items

| Category | Item | Status |
|---|---|---|
| uat_gap | Phase 04 / 04-UAT.md | partial, 0 pending scenarios |
| uat_gap | Phase 12 / 12-UAT.md | passed, 0 pending scenarios |

## Cross-Milestone Trends

To be filled after v1.1 ships.

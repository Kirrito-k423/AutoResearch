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

## Milestone: v1.1 — Formal Verl

**Shipped:** 2026-06-18
**Phases:** 1
**Plans:** 5 summaries

### What Was Built

- Formal Verl case configuration, strict sync/async matrix generation, scoring, and immutable provenance fields.
- `autoresearch run verl-case` orchestration across readiness checks, remote Docker execution, local artifact sync, and final JSON output.
- Qwen3.5-2B + geometry3k formal execution on `A2-AK-225`.
- Final local-first artifact bundle with manifest, logs, W&B, Prometheus evidence, report, and multi-repo provenance.
- Sequence-length and async-vs-sync result reporting through 16k output tokens.

### What Worked

- Treating the formal case as a vertical slice exposed the real runner, report, provenance, and recovery contracts in one pass.
- Immutable timestamped run directories made retries and partial recovery auditable instead of mysterious.
- Keeping W&B/Prometheus/log/report artifacts local preserved the project invariant even while remote execution was long-running.
- The final combined run let the successful retry for sync 8k replace one transient KV-cache failure without hiding the original evidence.

### What Was Inefficient

- Long remote rows plus SSH stdout hangs made naive command completion unreliable.
- Early summary extraction mixed in stale blocker text until the milestone entry was manually corrected.
- Prometheus live query remains fragile for historical report rendering even when local evidence JSON exists.
- The two-sample validation slice is enough for pipeline proof, but too small for quality claims.

### Patterns Established

- Formal experiment data must carry immutable config snapshots and Git provenance for every modified repo.
- Matrix rows should be recoverable from remote log/validation artifacts without trusting the live SSH channel.
- Final reports should distinguish pipeline health from model-quality benchmark claims.
- vLLM/verl transient resource failures should be preserved as source-run evidence when a retry resolves the final matrix.

### Key Lessons

- The useful unit of completion for this repo is not "command returned"; it is "local artifact bundle proves the run and its code provenance."
- Async/sync comparisons need both performance metrics and output consistency checks to be interpretable.
- Long-context NPU runs need explicit recovery metadata because allocation and Ray/vLLM startup failures can be row-local.
- Milestone automation is helpful, but final archive text still needs factual review against the actual run evidence.

### Deferred Items

| Category | Item | Status |
|---|---|---|
| observability | Prometheus live historical query | warning only; local evidence preserved |
| evaluation | geometry3k validation sample size | deliberately tiny pipeline proof, not benchmark |
| uat_gap | Phase 04 / 04-UAT.md | carried known v1.0 gap, 0 pending scenarios |

## Cross-Milestone Trends

| Pattern | v1.0 | v1.1 | Trend |
|---|---|---|---|
| Local-first evidence | smoke report bundle | formal experiment bundle | stronger |
| Real hardware dependency | A2-AK-225 smoke | A2-AK-225 long Verl matrix | still central |
| Recovery needs | service/proxy readiness | SSH stdout and row-level recovery | broader |
| Remaining caveat style | hardware/network UAT gaps | Prometheus/query and tiny eval slice | documented, not hidden |

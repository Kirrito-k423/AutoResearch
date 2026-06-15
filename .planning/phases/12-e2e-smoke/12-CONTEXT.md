---
phase: 12-e2e-smoke
status: ready-for-planning
gathered: 2026-06-15T16:30:00Z
---

# Phase 12: E2E 端到端 smoke - Context

<domain>
## Phase Boundary

Phase 12 delivers one local CLI path that proves the M1 loop end to end:
readiness check, minimal experiment collection, report rendering, report
completeness validation, Archon observability check, and duration gate.

It does not add new training behavior, new dashboard UI, or new remote
provisioning. It scripts and validates the system built in Phases 1-11.
</domain>

<decisions>
## Implementation Decisions

### E2E Entry

- **D-68:** Use `autoresearch e2e smoke` as the user-facing E2E script instead of a standalone shell script.
- **D-69:** The E2E command reuses Phase 11 Python entrypoints: `run_check_all` then `run_smoke`.
- **D-70:** The default server/lib path remains `--server A2-AK-225 --lib verl`; `veomni` remains outside the required E2E until the remote env installs it.

### Report Completeness

- **D-71:** Report completeness means all three report views are available: local log, local wandb artifact summary, and local Prometheus metric series.
- **D-72:** Completeness is checked from the same `ReportBundle` used by the renderer, not by scraping HTML text.
- **D-73:** A missing view is an E2E failure with `failed_step=report`, even if the HTML file exists.

### Archon Observability

- **D-74:** Phase 12 checks Archon observability by verifying Archon health on `http://localhost:8088/healthz` and the repo-local `ar-min-loop` workflow file.
- **D-75:** The E2E CLI does not run another Archon workflow by default; Phase 10 already proved the Archon run path, while Phase 12 focuses on the local CLI loop.

### Duration Gate

- **D-76:** E2E has a configurable `--max-duration` gate, default `1800` seconds, matching the `< 30 min` requirement.

### the agent's Discretion

- Keep the payload compact but include nested readiness/smoke payloads for diagnosis.
- Prefer unit tests with mocks for failure routing; real UAT will run against A2-AK-225.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements and roadmap

- `.planning/ROADMAP.md` — Phase 12 goal and success criteria.
- `.planning/REQUIREMENTS.md` — `E2E-01` through `E2E-04`.
- `.planning/STATE.md` — latest validated run path and environment constraints.

### Existing implementation

- `autoresearch/orchestrator/checks.py` — readiness orchestration entrypoint.
- `autoresearch/orchestrator/smoke.py` — collect -> report orchestration entrypoint.
- `autoresearch/report/loader.py` — report bundle source of truth.
- `autoresearch/report/models.py` — log/wandb/prom availability fields.
- `autoresearch/archon/runtime.py` — Archon workflow handoff patterns.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `StepResult`, `step_result`, `skipped_step`, and `summarize_steps` already normalize orchestration steps.
- `run_check_all` already returns the 8-position readiness report.
- `run_smoke` already emits progress, waits for Prometheus scrape, and returns report path/run id.
- `load_report_bundle` already provides `log.available`, `wandb.available`, and `prometheus.available`.

### Established Patterns

- CLI commands print one final JSON object on stdout and use `__AR_PROGRESS__=` on stderr.
- Command wrappers catch exceptions and return exit code `2` for orchestration errors.
- Tests patch Python entrypoints instead of invoking Docker/SSH for unit coverage.

### Integration Points

- Add a new `autoresearch/e2e/` package.
- Add a new `autoresearch e2e smoke` group in `autoresearch/cli.py`.
- Add `tests/test_e2e_smoke.py`.
</code_context>

<specifics>
## Specific Ideas

- The real UAT should use `A2-AK-225`, `verl`, and `http://127.0.0.1:17891` Pushgateway URL.
- Use `run_id` from `run_smoke` to validate the rendered report bundle.
- Treat Archon UI observability as health + workflow availability, not a second full Archon execution.
</specifics>

<deferred>
## Deferred Ideas

- A fully isolated fresh clone workflow can be added in v1.1 if needed.
- CI execution is deferred because the real E2E depends on local Docker Desktop, local wandb, and a reachable remote Ascend server.
</deferred>

---

*Phase: 12-e2e-smoke*
*Context gathered: 2026-06-15*

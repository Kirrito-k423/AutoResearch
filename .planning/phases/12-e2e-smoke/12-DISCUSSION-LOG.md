---
phase: 12-e2e-smoke
status: complete
gathered: 2026-06-15T16:30:00Z
mode: auto
---

# Phase 12: E2E 端到端 smoke - Discussion Log

> Audit trail only. Decisions are captured in `12-CONTEXT.md`.

## Auto-selected Areas

| Area | Options considered | Selected |
|------|--------------------|----------|
| E2E entry | standalone shell script / top-level CLI / Archon-only workflow | top-level CLI |
| Report completeness | HTML text scrape / `ReportBundle` source of truth / browser screenshot | `ReportBundle` source of truth |
| Archon observability | rerun full Archon workflow / health + workflow presence / skip | health + workflow presence |
| Duration gate | no gate / hard-coded 30 min / configurable max duration | configurable max duration |

## Rationale

- The project standard is a single `autoresearch` binary, so E2E should be reachable there.
- Phase 11 already created robust Python orchestration entrypoints; Phase 12 should compose them.
- `ReportBundle` exposes the exact availability booleans for log/wandb/prom, making it the cleanest completeness oracle.
- Phase 10 already proved the Archon workflow run path; Phase 12 should only assert that the Web UI/workflow surface remains observable.

## Deferred Ideas

- Fully isolated fresh-clone smoke.
- CI-hosted E2E.

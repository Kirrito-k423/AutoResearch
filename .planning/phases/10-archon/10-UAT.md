---
phase: 10-archon
status: complete
updated: 2026-06-15T15:16:00Z
---

# Phase 10 UAT — Archon adapter

## Real run used

- Archon workflow: `ar-min-loop`
- Archon run id: `37dfb89e99e9a482e25fadaf3e5b7d0d`
- Command:
  ```bash
  CLAUDE_BIN_PATH=/opt/homebrew/bin/claude AR_STACK_LIBS=verl archon workflow run ar-min-loop --no-worktree ""
  ```
- collect run id: `01KV5XK74K7CHQ92GGZ6C1V92V`
- report: `/Users/Zhuanz/.autoresearch/runs/01KV5XK74K7CHQ92GGZ6C1V92V/report.html`

## Observed results

- 8-node main workflow completed successfully.
- Archon artifacts include `skill-01-result.json` .. `skill-07-result.json`, `collect-result.json`, and `report-result.json`.
- `collect-result.json` shows `ok=true`, `prom_pushed=true`, and no errors.
- `report-result.json` shows `ok=true` and points to the generated HTML report.
- Archon Web UI loads at `http://localhost:8088`; Workflows search finds `ar-min-loop`.

## Acceptance

- [x] `ARCH-WF-01` — 8 skill workflows exist.
- [x] `ARCH-WF-02` — workflow nodes call repo Python/script entrypoints.
- [x] `ARCH-WF-03` — STACK/COLL standalone workflows contain real `loop:` nodes and validate.
- [x] `ARCH-WF-MAIN-01` — `ar-min-loop.yaml` chains the 8 skill sequence.
- [x] `ARCH-WF-MAIN-02` — main workflow produced a report.
- [x] `ARCH-RUN-01` — main workflow completed in real Archon CLI with `AR_STACK_LIBS=verl`.
- [x] `ARCH-RUN-02` — Archon Web UI is visible and lists `ar-min-loop`.

## Residual environment notes

- The current remote env has `verl` installed and passing, but `veomni` is not importable from `verl-qwen3.5`; default two-lib stack verification fails there for environment reasons.
- The local Archon Claude provider returns 401 for AI loop execution; deterministic script nodes are used for the main smoke path.

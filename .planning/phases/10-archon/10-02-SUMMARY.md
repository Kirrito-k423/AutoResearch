---
phase: 10-archon
plan: 02
status: completed
subsystem: archon-main-loop
tags: [archon, main-workflow, artifacts]

requirements-completed:
  - ARCH-WF-MAIN-01
  - ARCH-WF-MAIN-02
  - ARCH-RUN-01

completed: 2026-06-15
---

# Phase 10 Plan 02: `ar-min-loop` Summary

Plan 02 created the main Archon workflow that chains the 8 AutoResearch skills from config validation through report rendering.

## Accomplishments

- Added `.archon/workflows/ar-min-loop.yaml`.
- Main workflow now runs 8 deterministic skill nodes:
  `config` -> `services` -> `hw` -> `net` -> `reach` -> `stack` -> `collect` -> `report`.
- The main workflow uses `AR_REMOTE_PROXY_PORT=${AR_REMOTE_PROXY_PORT:-17892}` for network proxy checks so reach/wandb can keep remote port `17890`.
- `collect` writes `collect-result.json`; `report` reads the same Archon artifact directory and renders the final HTML report.
- `ar-skill-06.yaml` and `ar-skill-07.yaml` retain real Archon `loop:` nodes for STACK/COLL loop expression; the main workflow uses deterministic script entrypoints to avoid provider-auth dependency during smoke runs.

## Real Run

```bash
CLAUDE_BIN_PATH=/opt/homebrew/bin/claude AR_STACK_LIBS=verl archon workflow run ar-min-loop --no-worktree ""
```

Result: workflow completed successfully.

- Archon run: `37dfb89e99e9a482e25fadaf3e5b7d0d`
- collect run: `01KV5XK74K7CHQ92GGZ6C1V92V`
- report: `/Users/Zhuanz/.autoresearch/runs/01KV5XK74K7CHQ92GGZ6C1V92V/report.html`

## Residual Notes

- Default stack check over `verl,veomni` reaches the stack node but fails on the current remote because `veomni` is not importable in env `verl-qwen3.5`.
- `verl` stack check passes, including one NPU dry run on 8 devices.

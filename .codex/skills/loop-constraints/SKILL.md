---
name: loop-constraints
description: Load and enforce AutoResearch loop constraints before triage, edits, remote work, or external writes.
user_invocable: true
---

# Loop Constraints Enforcer

Before any loop work:

1. Read `loop-constraints.md`, `docs/safety.md`, and `LOOP.md`.
2. If `.loop-paused` exists or `STATE.md` says `Status: paused`, exit without action.
3. Count and report the active human gates and denylist categories.
4. Apply those constraints to every following action; constraints override triage priority.

Before editing, remote execution, Git/GitHub writes, or connector writes, re-check the relevant role scope and denylist. If authority is missing, return `ESCALATE_HUMAN` with the blocked action and required approval.

Never auto-merge, weaken tests, expose credentials, or let a maker verify its own work.

---
name: loop-budget
description: Enforce AutoResearch loop cadence, attempt, token, time, sub-agent, remote-compute, and kill-switch limits.
user_invocable: true
---

# Loop Budget Guard

Run at the start and end of every loop iteration.

## Start

1. Read `loop-budget.md`, `STATE.md`, and the last 24 hours of `loop-run-log.md`.
2. Exit if `.loop-paused` exists or state is paused.
3. Stay report-only at 80% of the daily cap; exit at 100%.
4. If nothing is actionable, return a no-op in under 5k estimated tokens.
5. Enforce L1: one candidate, zero sub-agents, zero remote compute.

## End

Append a structured record to `loop-run-log.md` with timestamp, trigger, evidence/run id, candidate count, actions, attempts, escalations, duration, token estimate, verdict, and stop reason. Never rewrite previous entries.

For L2, stop after three attempts for a hypothesis or two identical failure signatures, even if time/token budget remains.

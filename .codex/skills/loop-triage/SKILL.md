---
name: loop-triage
description: Read AutoResearch run evidence and loop state, then propose one bounded next experiment or escalate. L1 is report-only.
user_invocable: true
---

# AutoResearch Loop Triage

Produce a concise, evidence-backed update for the AutoResearch experiment loop.

## Read first

1. `LOOP.md`, `loop-constraints.md`, `loop-budget.md`, and `STATE.md`.
2. `.planning/STATE.md` for project blockers.
3. The latest available local run manifest, logs, metrics, report, and Git provenance.

## Output

Return exactly these sections:

1. `High Priority` — at most one problem/opportunity and why it matters.
2. `Evidence` — run id, paths, metrics, failure signature, and confidence.
3. `Candidate Hypothesis` — one falsifiable hypothesis and smallest validation.
4. `Risk / Budget / Authority` — what is safe now and what needs approval.
5. `Verdict` — `KEEP`, `REJECT`, or `ESCALATE_HUMAN`.
6. `State Updates` — exact proposed edits for `STATE.md` and an append-only log entry.

## Rules

- L1 is report-only: never modify source, run remote training, or write to external systems.
- Separate model/data/system/hardware/environment failure layers before proposing code work.
- Do not infer success from a single log line; prefer the immutable run bundle.
- Stop after two identical failure signatures or when evidence is not comparable.
- Never propose an architectural overhaul during triage.
- When escalating, include evidence, attempted actions, options, recommendation, and estimated cost.

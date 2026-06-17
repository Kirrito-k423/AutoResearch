---
status: partial
phase: 14-verl-workspace-adapter-verl
source: 14-03-SUMMARY.md, 14-04-SUMMARY.md
started: 2026-06-17T13:44:47Z
updated: 2026-06-17T15:02:00Z
server: A3-AX-180
model: Qwen/Qwen3.5-2B
dataset: hiyouga/geometry3k
---

## Current Test

[testing paused - 2 items outstanding]

## Tests

### 1. Start The Formal Command
expected: `uv run autoresearch run verl-case --server A3-AX-180 --config config/config.yaml --local-proxy-url http://127.0.0.1:7890 --remote-proxy-port 17894` should pass readiness far enough to enter formal-case preparation on the selected host.
result: pass

### 2. Accept Qwen3.5 Local Cache Layout
expected: The local cache under `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B` should accept Hugging Face `model.safetensors.index.json` plus sharded safetensors layout without requiring manual rename or ad hoc file surgery.
result: pass

### 3. Render Formal Report Sections
expected: Formal-case report loading and rendering should expose matrix, sequence-length impact, sync-vs-async impact, accuracy, consistency, and provenance sections, while strict completeness checks fail closed on missing matrix rows.
result: pass

### 4. Complete The Real 8-Row Matrix
expected: A real formal run on the selected qualifying host should finish all sync/async rows through `16384` output tokens and produce `matrix-results.jsonl` with 8 passed rows.
result: blocked
blocked_by: local_cache
reason: `A2-AK-225` was ruled out for fresh formal containers because new namespaces still hit `aclInit 507899 / Resource_Busy`. We switched to `A3-AX-180`, where the exact `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5` image passes the fresh-container NPU smoke test and formal readiness can enter `prepare`. However the real run is still waiting on the local `Qwen3.5-2B` shard download to finish; after the latest resume fixes, the largest `.incomplete` shard reached `114294784` bytes, crossing the earlier `107668954`-byte disconnect point, but the full `4.55GB` weight is not complete yet.

### 5. Produce The Final Artifact Bundle
expected: A successful real run should emit immutable config, provenance, matrix results, local log, W&B, Prometheus evidence, manifest, and final `report.html`, all tied to shipped commit SHAs and GitHub links.
result: blocked
blocked_by: prior-phase
reason: This artifact bundle depends on Test 4 succeeding first; no successful real 8-row matrix run exists yet.

## Summary

total: 5
passed: 3
issues: 0
pending: 0
skipped: 0
blocked: 2

## Gaps

- truth: "A2-AK-225 finishes all sync/async formal-case rows through 16k and writes 8 passed matrix rows."
  status: blocked
  reason: "A2 fresh-container namespace contention was isolated, and A3-AX-180 is now the active exact-image host; the remaining blocker is finishing the local Qwen3.5-2B weight cache before the 8-row real run can start."
  severity: blocker
  test: 4
  root_cause: "The old A2 blocker is understood, but the current blocking path is local asset completion: the exact-image run on A3-AX-180 can reach `prepare`, and the repaired resume path is still warming the `4.55GB` model shard."
  artifacts:
    - path: ".planning/phases/14-verl-workspace-adapter-verl/14-04-SUMMARY.md"
      issue: "Summary records both the A2 namespace blocker and the later A3-AX-180 exact-image + resume-validation evidence."
    - path: ".planning/phases/14-verl-workspace-adapter-verl/14-VERIFICATION.md"
      issue: "Verification records the A3-AX-180 selection and the `114294784`-byte resume checkpoint."
  missing:
    - "Finish warming the local Qwen3.5-2B cache or provide a faster authenticated HF path."
    - "Resume the real formal run on A3-AX-180 after the local shard is complete."
    - "Collect the final 8-row matrix and downstream artifact bundle."
  debug_session: ""

- truth: "The successful formal run emits manifest, report, provenance, W&B, and Prometheus evidence tied to shipped AutoResearch and verl commits."
  status: blocked
  reason: "Downstream artifact verification depends on a successful real matrix run."
  severity: blocker
  test: 5
  root_cause: "Final artifact generation is downstream of the blocked real formal-case execution."
  artifacts:
    - path: ".planning/phases/14-verl-workspace-adapter-verl/14-04-SUMMARY.md"
      issue: "Phase summary records shipped commit links but no successful real artifact bundle yet."
    - path: "autoresearch/orchestrator/verl_case.py"
      issue: "Artifact persistence path is implemented, but it has not been exercised by a successful real formal run."
  missing:
    - "A completed real 8-row matrix run."
    - "A real manifest/report pair generated from that successful run."
  debug_session: ""

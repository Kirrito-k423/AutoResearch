---
status: partial
phase: 14-verl-workspace-adapter-verl
source: 14-03-SUMMARY.md, 14-04-SUMMARY.md
started: 2026-06-17T13:44:47Z
updated: 2026-06-17T13:59:37Z
server: A2-AK-225
model: Qwen/Qwen3.5-2B
dataset: hiyouga/geometry3k
---

## Current Test

[testing paused - 2 items outstanding]

## Tests

### 1. Start The Formal Command
expected: `uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --local-proxy-url http://127.0.0.1:7890 --remote-proxy-port 17892` should pass readiness far enough to enter formal-case preparation on the selected host.
result: pass

### 2. Accept Qwen3.5 Local Cache Layout
expected: The local cache under `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B` should accept Hugging Face `model.safetensors.index.json` plus sharded safetensors layout without requiring manual rename or ad hoc file surgery.
result: pass

### 3. Render Formal Report Sections
expected: Formal-case report loading and rendering should expose matrix, sequence-length impact, sync-vs-async impact, accuracy, consistency, and provenance sections, while strict completeness checks fail closed on missing matrix rows.
result: pass

### 4. Complete The Real 8-Row Matrix
expected: A real formal run on `A2-AK-225` should finish all sync/async rows through `16384` output tokens and produce `matrix-results.jsonl` with 8 passed rows.
result: blocked
blocked_by: server
reason: Host-level `torch_npu` works and `docker exec` into long-lived `/verl-8.5.2-a2` works, but a fresh `docker run --rm` on the same image still fails with `aclInit` / `torch_npu.set_device()` error `507899` (`Resource_Busy`); `dmesg` reports `uda_occupy_dev_by_ns ... Conflict open udevid`, and old `asc_dumper` processes inside `/verl-8.5.2-a2` still hold Ascend device handles.

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
  reason: "Fresh containers on A2 still hit aclInit / Resource_Busy 507899 while the host env and the long-lived /verl-8.5.2-a2 container can allocate NPU normally."
  severity: blocker
  test: 4
  root_cause: "A stale container namespace on A2-AK-225 appears to retain Ascend device ownership (`uda_occupy_dev_by_ns` conflict), so new containers cannot acquire the NPU cleanly."
  artifacts:
    - path: ".planning/phases/14-verl-workspace-adapter-verl/14-04-SUMMARY.md"
      issue: "Summary records host-pass / old-container-pass / fresh-container-fail evidence and `uda_occupy_dev_by_ns` kernel errors."
    - path: ".planning/phases/14-verl-workspace-adapter-verl/14-VERIFICATION.md"
      issue: "Verification records the fresh-container namespace/device contention finding."
  missing:
    - "Finish warming the local Qwen3.5-2B cache or provide a faster authenticated HF path."
    - "Decide whether AutoResearch may reuse or reset the existing `/verl-8.5.2-a2` container."
    - "Clear stale Ascend device-holding processes/namespace on A2-AK-225, or choose a different host."
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

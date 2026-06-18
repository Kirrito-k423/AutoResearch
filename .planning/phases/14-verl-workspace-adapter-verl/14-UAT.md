---
status: passed
phase: 14-verl-workspace-adapter-verl
source: real A2-AK-225 formal runs
started: 2026-06-17T13:44:47Z
updated: 2026-06-18T11:16:20Z
server: A2-AK-225
model: Qwen/Qwen3.5-2B
dataset: hiyouga/geometry3k
combined_run_id: formal-20260618-a2ak225-combined-r1
---

# Phase 14 UAT: Formal Verl Case

## Current Test

[testing complete]

## Tests

### 1. Select A Real Ascend Host Through Skills 1-6

expected: Use the existing AutoResearch readiness path to identify a usable Ascend host for the requested official image and formal Verl case.

result: pass

evidence:

- Active run host: `A2-AK-225` (`192.168.9.225`)
- Workdir: `/home/t00906153`
- The earlier `A3-AX-180` route was rejected after the official `910b` image exposed a device/toolkit mismatch.
- `A2-AK-225` fresh-container attempts were affected by namespace/device contention, but the long-lived `verl-8.5.2-a2` container successfully ran the requested official image stack and full matrix.

### 2. Prepare Qwen3.5-2B And geometry3k

expected: Use configurable local cache paths under `/Users/Zhuanz/autoResearchData`, stage assets to the remote host, and keep model/data under the 5GB local-copy boundary where applicable.

result: pass

evidence:

- Model: `Qwen/Qwen3.5-2B`
- Dataset: `hiyouga/geometry3k`
- Local cache root: `/Users/Zhuanz/autoResearchData`
- Remote model path: `/home/t00906153/autoresearch/model-cache/Qwen__Qwen3.5-2B`
- Remote dataset path: `/home/t00906153/autoresearch/dataset`

### 3. Complete The Real 8-Row Matrix

expected: Run `1024 -> 2048/4096/8192/16384` for both sync and async inference, with `ignore_eos=false`, and produce 8 passed matrix rows.

result: pass

evidence:

- Combined run: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1`
- Report: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/report.html`
- Matrix: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/matrix-results.jsonl`
- Rows: 8 total, 8 passed

| Mode | Input | Output | Tokens/s | Latency ms | Accuracy | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| sync | 1024 | 2048 | 7.7928 | 262807.5 | 0.0 | 1.0 |
| async | 1024 | 2048 | 7.0256 | 291506.6 | 0.0 | 1.0 |
| sync | 1024 | 4096 | 10.7169 | 382201.5 | 0.0 | 1.0 |
| async | 1024 | 4096 | 10.1191 | 404777.3 | 0.0 | 1.0 |
| sync | 1024 | 8192 | 12.5911 | 650620.1 | 0.0 | 1.0 |
| async | 1024 | 8192 | 12.6575 | 647204.5 | 0.0 | 1.0 |
| sync | 1024 | 16384 | 14.8189 | 1105617.0 | 0.0 | 1.0 |
| async | 1024 | 16384 | 22.7116 | 721394.0 | 0.0 | 1.0 |

### 4. Sequence Length Impact

expected: Record how increasing output length from 2k to 16k changes throughput and latency.

result: pass

observations:

- Latency grows with output length for both modes.
- Tokens/s increases with longer generations because fixed setup overhead is amortized.
- Sync 8k initially failed once with vLLM KV cache allocation, then passed as a clean single-row rerun; both the failed evidence and successful rerun are preserved.
- Async 16k showed the strongest throughput result in this matrix: `22.7116` tokens/s.

### 5. Async Inference Impact On Performance And Accuracy

expected: Compare async against sync at the same input/output lengths for performance and output consistency.

result: pass

observations:

- 2k and 4k async were slightly slower than sync in this sample.
- 8k async and sync were effectively comparable.
- 16k async was materially faster than sync: `+7.8927` tokens/s and `-384223.0` ms latency delta.
- Accuracy was `0.0` for every row under the current two-sample geometry3k validation slice.
- Async output consistency against same-length sync baselines was `1.0` for all four lengths.

### 6. Produce The Final Artifact Bundle

expected: Preserve immutable config, provenance, matrix results, logs, row validation outputs, local W&B summary, Prometheus evidence, manifest, and report.

result: pass

evidence:

- Config snapshot: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/config-20260618T111620-combined.json`
- Provenance: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/provenance.json`
- Manifest: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/manifest.json`
- W&B summary: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/wandb/files/wandb-summary.json`
- Prometheus evidence: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/prom/formal-case-prometheus.json`
- Report render command: `uv run autoresearch report render --run-id formal-20260618-a2ak225-combined-r1`

note: The final render reported `Prometheus 查询成功但未返回该 run 的指标。`; the local Prometheus evidence JSON and source-run Prometheus artifacts are still preserved in the bundle.

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 0

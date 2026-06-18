---
phase: 14-verl-workspace-adapter-verl
plan: 05
status: completed
subsystem: formal-runtime-closure
tags: [verl-case, qwen3.5, geometry3k, ascend, formal-run]
completed: 2026-06-18
combined_run_id: formal-20260618-a2ak225-combined-r1
---

# Phase 14 Plan 05: Real Formal Runtime Completion Summary

## Outcome

Phase 14 is complete. We ran the formal Verl case on `A2-AK-225` with `Qwen/Qwen3.5-2B`, `hiyouga/geometry3k`, `ignore_eos=false`, and the requested official Ascend Verl image stack. The final combined artifact contains all 8 sync/async sequence-length rows and every row passed.

Final artifact bundle:

- Run id: `formal-20260618-a2ak225-combined-r1`
- Run directory: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1`
- Report: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/report.html`
- Matrix: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/matrix-results.jsonl`
- Manifest: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/manifest.json`

## Runtime Route

- `A3-AX-180` was rejected for this exact formal image path after the run exposed a host/toolkit/device mismatch.
- `A2-AK-225` became the active formal host because its long-lived `verl-8.5.2-a2` container could run the official image stack against all 8 NPUs.
- Fresh-container `A2-AK-225` allocation remains a known namespace/device-handle caveat, but the formal case itself is complete on the long-lived container route.
- `A2-AK-102` was not disturbed because its existing vLLM containers occupied all 8 cards and stopping them needed explicit approval.

## Matrix Results

| Mode | Input | Output | Tokens/s | Latency ms | Accuracy | Consistency | Source run |
|---|---:|---:|---:|---:|---:|---:|---|
| sync | 1024 | 2048 | 7.7928 | 262807.5 | 0.0 | 1.0 | `formal-20260618-a2ak225-sync-r3` |
| async | 1024 | 2048 | 7.0256 | 291506.6 | 0.0 | 1.0 | `formal-20260618-a2ak225-async-r4` |
| sync | 1024 | 4096 | 10.7169 | 382201.5 | 0.0 | 1.0 | `formal-20260618-a2ak225-sync-r3` |
| async | 1024 | 4096 | 10.1191 | 404777.3 | 0.0 | 1.0 | `formal-20260618-a2ak225-async-r4` |
| sync | 1024 | 8192 | 12.5911 | 650620.1 | 0.0 | 1.0 | `formal-20260618-a2ak225-sync8192-r1` |
| async | 1024 | 8192 | 12.6575 | 647204.5 | 0.0 | 1.0 | `formal-20260618-a2ak225-async-r4` |
| sync | 1024 | 16384 | 14.8189 | 1105617.0 | 0.0 | 1.0 | `formal-20260618-a2ak225-sync-r3` |
| async | 1024 | 16384 | 22.7116 | 721394.0 | 0.0 | 1.0 | `formal-20260618-a2ak225-async16384-r1` |

## Experiment 1: Sequence Length Impact

- Longer outputs increased latency in both sync and async modes.
- Tokens/s improved as output length increased, mostly because fixed setup overhead was amortized over more generated tokens.
- The initial sync 8k row failed once with vLLM KV cache allocation, then passed as an isolated rerun. Both the failure and the replacement successful run are preserved in source artifacts.
- The strongest throughput row was async 16k at `22.7116` tokens/s.

## Experiment 2: Async Inference Impact

- Async was slower than sync at 2k and 4k in this two-sample validation slice.
- Async and sync were effectively tied at 8k.
- Async was materially faster at 16k: `+7.8927` tokens/s and about `384223` ms lower latency than sync.
- Accuracy stayed `0.0` across all rows under the current geometry3k two-sample slice.
- Async output consistency against same-length sync baselines was `1.0` for 2k, 4k, 8k, and 16k.

## Code And Artifact Changes

- `workspace-adapter/verl/case_runner.py` now writes a remote row-level `result.json` before stdout marker output and supports local polling recovery.
- Default row execution now backgrounds the row command on the remote host and polls `rows/<key>/result.json`, avoiding SSH stdout/channel hangs after long Verl jobs.
- `tests/test_verl_case_runner.py` covers remote result recovery and the background polling runner path.
- Final artifacts are local-first and live under `~/.autoresearch/runs/`.

## Verification

- `uv run pytest tests/test_verl_case_runner.py tests/test_minimal_runner.py -q` -> `58 passed`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/verl-case-async-16384.local.yaml --timeout 20000 --run-id formal-20260618-a2ak225-async16384-r1 --allow-git-push --skip-readiness` -> `ok=true`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/verl-case-sync-8192.local.yaml --timeout 12000 --run-id formal-20260618-a2ak225-sync8192-r1 --allow-git-push --skip-readiness` -> `ok=true`
- `uv run autoresearch report render --run-id formal-20260618-a2ak225-combined-r1` -> `ok=true`

## Runtime Provenance

| Repo | Commit | Branch URL |
|---|---|---|
| AutoResearch | `f1047ca1b3c046e3905a54c40f0390017d891c11` | `https://github.com/Kirrito-k423/AutoResearch/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-phase-02-workspace-core` |
| verl | `76d341aa15e72d126005e105a679e6e22b394bbb` | `https://github.com/Kirrito-k423/verl/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-main` |
| vllm | `b8b302cde434df8c9289a2b465406b47ebab1c2d` | `https://github.com/Kirrito-k423/vllm/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-detached-b8b302cde` |

Transformers and MindSpeed were not modified as local dependency repositories in this formal case.

## Residual Caveats

- The final combined report warns that the live Prometheus query returned no metric for the combined run. The local evidence file is present at `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/prom/formal-case-prometheus.json`, and source-run Prometheus evidence is preserved.
- Accuracy is based on a deliberately small two-sample validation slice and is not a model-quality benchmark.

## Self-Check: PASSED

- PASS: Formal case is real hardware execution, not a demo.
- PASS: 8-row sync/async matrix completed and all rows passed.
- PASS: Sequence-length and async-vs-sync experiment conclusions are recorded.
- PASS: Config, provenance, rows, logs, W&B, Prometheus evidence, manifest, and report are local.
- PASS: Runtime provenance ties experiment data to AutoResearch, Verl, and vLLM commits/branches.

---
phase: 11-orchestration
status: complete
updated: 2026-06-15T16:11:00Z
---

# Phase 11 UAT — Top-level CLI orchestration

## Real check used

```bash
uv run autoresearch check all --server A2-AK-225 --stack-lib verl
```

Observed result:

- `ok=true`
- `summary.total=8`
- `passed=6`, `warned=2`, `failed=0`, `skipped=0`
- Services were `5/5` healthy, including wandb at `http://localhost:8080/ready`.
- `reach` passed for both local wandb and pushgateway from the remote server.
- `stack` passed for `verl` in `verl-qwen3.5` with 8 NPU devices observed in the one-step dry run.

Expected warnings:

- `hw` warned because BMC `192.168.12.225` is still unreachable; the NPU probe itself succeeded.
- `net` warned because remote HuggingFace/GitHub direct access failed and proxy fallback through `127.0.0.1:17892` succeeded.

## Real smoke used

```bash
uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891
```

Observed result:

- `ok=true`
- `summary.total=2`
- collect step passed
- report step passed
- `failed_step=null`
- `prometheus_ready=true`
- report warnings `[]`

Real run outputs:

- run id: `01KV60QS8PMSEG02MQEB0Z27FT`
- manifest: `/Users/Zhuanz/.autoresearch/runs/01KV60QS8PMSEG02MQEB0Z27FT/manifest.json`
- report: `/Users/Zhuanz/.autoresearch/runs/01KV60QS8PMSEG02MQEB0Z27FT/report.html`

## Acceptance

- [x] `ORCH-CHECK-01` — `autoresearch check all` reports all 8 skill positions.
- [x] `ORCH-CHECK-02` — each step includes status, exit code, diagnosis, and payload.
- [x] `ORCH-RUN-01` — `autoresearch run smoke --server X` ran collect + report.
- [x] `ORCH-RUN-02` — failure diagnostics are covered by orchestrator tests for collect/report/check failures.
- [x] `ORCH-LOG-01` — check and smoke emit `__AR_PROGRESS__=` stages and keep stdout as the final JSON object.

---
phase: 14-verl-workspace-adapter-verl
status: blocked
updated: 2026-06-17T14:15:00Z
server: A2-AK-225
model: Qwen/Qwen3.5-2B
dataset: hiyouga/geometry3k
---

# Phase 14 UAT — formal Verl case

## Commands

```bash
uv run autoresearch run verl-case \
  --server A2-AK-225 \
  --config config/config.yaml \
  --local-proxy-url http://127.0.0.1:7890 \
  --remote-proxy-port 17892 \
  --run-id uat-qwen35-20260617-1
```

## Observed result

- Overall: `blocked`
- Run id: `uat-qwen35-20260617-1`
- Selected host: `A2-AK-225`
- Local cache root: `/Users/Zhuanz/autoResearchData`
- Partial Qwen3.5 cache path: `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B`
- Partial cache size after abort: `32M`

## Step evidence

| Step | Status | Evidence |
|---|---:|---|
| readiness/config | pass | local config parsed correctly |
| readiness/services | fail | local observability services not all healthy |
| readiness/hw | warn | `npu-smi` saw 8 devices on A2 |
| readiness/net | warn | remote networking usable with proxy/tunnel path, but not clean enough for a zero-warning gate |
| readiness/reach | pass | remote reachability checks succeeded |
| readiness/stack | pass | target conda/env stack check succeeded |
| prepare/model-cache | partial | `Qwen3.5-2B` sidecars and `model.safetensors.index.json` downloaded; large weight shard still downloading when aborted |
| remote matrix | not reached in this attempt | run was stopped before model download completed |

## Blocking evidence

The strongest blocker is still the machine-side A2 runtime state, not the report code:

- Earlier real A2 diagnostic runs had already reached remote `torch_npu` worker setup and logged `aclInit` / `torch_npu.set_device()` failure with error code `507899`.
- The same `507899 / Resource_Busy` behavior reproduced even in a single-card run, so it is not explained by only the sync/async matrix size or Ray rank mapping.
- Today’s UAT attempt intentionally stopped once Qwen3.5 cache bootstrap had been proven to start correctly, because finishing the full 4.57GB download would not have changed the already-known A2 runtime conclusion during this turn.

## Acceptance status

- [ ] All sync/async rows through 16k completed
- [ ] `matrix-results.jsonl` contains 8 passed rows
- [ ] `report.html` contains full formal-case sections backed by real run data
- [ ] immutable config snapshot, provenance, W&B, Prometheus, manifest all exist for the successful run
- [ ] AutoResearch + dependency repo shipped commit SHAs and GitHub links recorded for the successful run

## Next manual assists

1. On `A2-AK-225`, inspect watchdog/guard/background jobs that may reset or occupy NPUs.
2. On `A2-AK-225`, run a minimum `torch_npu` repro and capture the exact output around `aclInit`.
3. Optionally provide `HF_TOKEN` locally so `Qwen3.5-2B` cache warming can complete faster on resume.

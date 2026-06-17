---
status: human_needed
phase: 14-verl-workspace-adapter-verl
updated: 2026-06-17T13:59:37Z
source: 14-UAT.md, 14-04-SUMMARY.md, pytest
---

## Verdict

Phase 14's code and report layers are verified, but the phase goal is not yet achieved end to end. The formal report path, completeness checks, Qwen3.5 cache-layout support, and focused/full regressions all pass; the real formal-case run is now narrowed to container namespace/device-handle contention on `A2-AK-225`, plus incomplete local Qwen3.5 cache warming.

## Evidence

- `uv run pytest -q tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py tests/workspace-core/test_config.py` -> `49 passed`
- `uv run pytest -q tests/test_verl_case_config.py tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py` -> `38 passed`
- `uv run pytest -q` -> `408 passed, 6 warnings`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --local-proxy-url http://127.0.0.1:7890 --remote-proxy-port 17892 --run-id uat-qwen35-20260617-1`
  -> readiness reached `stack=pass`; local Qwen3.5 cache bootstrap started correctly
- `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B` now contains tokenizer/config sidecars plus `model.safetensors.index.json`, confirming the sharded-layout adaptation is live
- On `A2-AK-225`, host `conda run -n verl-qwen3.5 python -c '... torch.tensor([1.0]).npu()'` succeeds
- On `A2-AK-225`, `docker exec verl-8.5.2-a2 ... torch.tensor([1.0]).npu()` succeeds inside the long-lived existing Verl container
- On `A2-AK-225`, a fresh `docker run --rm quay.io/ascend/verl:... python -c '... torch.tensor([1.0]).npu()'` fails with `aclInit 507899 / Resource_Busy`
- `dmesg` on `A2-AK-225` reports repeated `uda_occupy_dev_by_ns ... Conflict open udevid` errors during failed fresh-container attempts
- Host `/proc/*/fd` inspection shows long-lived `asc_dumper` processes inside container `/verl-8.5.2-a2` holding `/dev/davinci_manager` and `/dev/hisi_hdc`

## Manual Checks

- PASS: Formal report loader/rendering and strict completeness checks are implemented and regression-tested
- PASS: `Qwen/Qwen3.5-2B` is the default formal-case model across config, docs, and tests
- PASS: Hugging Face `index.json + shard` local cache layout is accepted without manual rename
- FAIL: No successful real 8-row sync/async matrix run exists yet on `A2-AK-225`
- FAIL: No successful real formal artifact bundle (`matrix-results.jsonl`, `manifest.json`, `report.html`, provenance, W&B, Prometheus evidence) exists yet for Phase 14

## Blocking Conditions

1. Fresh containers on `A2-AK-225` still fail with `torch_npu aclInit 507899 / Resource_Busy`, while the host env and a long-lived old Verl container can allocate NPU successfully.
2. The most likely immediate cause is stale namespace/device ownership inside `/verl-8.5.2-a2`, evidenced by persistent `asc_dumper` processes and `uda_occupy_dev_by_ns` kernel errors.
3. The local `Qwen3.5-2B` weight cache is not fully warmed yet; the latest run only proved that the cache bootstrap path works.

## Next Required Action

Re-run the real formal case after at least one of the following changes:

- local Qwen3.5 cache finishes downloading, or a faster authenticated HF path is available
- stale container namespace/device holders on A2 are cleared, or AutoResearch is explicitly allowed to reuse/reset the existing `/verl-8.5.2-a2` container
- a different qualifying host is selected and passes the same formal-case requirements

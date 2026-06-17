---
status: partial
phase: 14-verl-workspace-adapter-verl
updated: 2026-06-17T15:02:00Z
source: 14-UAT.md, 14-04-SUMMARY.md, pytest
---

## Verdict

Phase 14's code and report layers are verified, but the phase goal is not yet achieved end to end. The formal report path, completeness checks, Qwen3.5 cache-layout support, fresh-container machine selection, and focused/full regressions all pass; the real formal-case run is now narrowed to finishing the local `Qwen3.5-2B` shard cache on the new exact-image host path.

## Evidence

- `uv run pytest -q tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py tests/workspace-core/test_config.py` -> `49 passed`
- `uv run pytest -q tests/test_verl_case_config.py tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py` -> `38 passed`
- `uv run pytest -q` -> `408 passed, 6 warnings`
- `uv run pytest tests/test_verl_case_runner.py -k 'prepare_model_cache or resume_model_download'` -> `6 passed`
- `uv run pytest tests/test_orchestrator_verl_case.py -k 'docker_stack_override or formal_readiness_ignores_archon_and_host_python or ignores_remote_huggingface'` -> `3 passed`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --local-proxy-url http://127.0.0.1:7890 --remote-proxy-port 17892 --run-id uat-qwen35-20260617-1`
  -> readiness reached `stack=pass`; local Qwen3.5 cache bootstrap started correctly
- `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B` now contains tokenizer/config sidecars plus `model.safetensors.index.json`, confirming the sharded-layout adaptation is live
- On `A2-AK-225`, host `conda run -n verl-qwen3.5 python -c '... torch.tensor([1.0]).npu()'` succeeds
- On `A2-AK-225`, `docker exec verl-8.5.2-a2 ... torch.tensor([1.0]).npu()` succeeds inside the long-lived existing Verl container
- On `A2-AK-225`, a fresh `docker run --rm quay.io/ascend/verl:... python -c '... torch.tensor([1.0]).npu()'` fails with `aclInit 507899 / Resource_Busy`
- `dmesg` on `A2-AK-225` reports repeated `uda_occupy_dev_by_ns ... Conflict open udevid` errors during failed fresh-container attempts
- Host `/proc/*/fd` inspection shows long-lived `asc_dumper` processes inside container `/verl-8.5.2-a2` holding `/dev/davinci_manager` and `/dev/hisi_hdc`
- On `A3-AX-180`, a fresh container on the exact requested image `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5` passes the NPU smoke test (`torch.npu.is_available() -> True`, `x.cpu().tolist() -> [1.0]`)
- The latest A3 formal-case retries pass readiness into `prepare`, and the repaired resume path grows the largest local model shard to `114294784` bytes, exceeding the previous `107668954`-byte disconnect point that killed the old prepare flow

## Manual Checks

- PASS: Formal report loader/rendering and strict completeness checks are implemented and regression-tested
- PASS: `Qwen/Qwen3.5-2B` is the default formal-case model across config, docs, and tests
- PASS: Hugging Face `index.json + shard` local cache layout is accepted without manual rename
- FAIL: No successful real 8-row sync/async matrix run exists yet on the selected exact-image host path (`A3-AX-180`)
- FAIL: No successful real formal artifact bundle (`matrix-results.jsonl`, `manifest.json`, `report.html`, provenance, W&B, Prometheus evidence) exists yet for Phase 14

## Blocking Conditions

1. The local `Qwen3.5-2B` `4.55GB` weight shard is still downloading on the Mac cache path; the latest run proved resumable progress past the previous disconnect point, but the shard is not complete yet.
2. No successful real 8-row matrix has been started on `A3-AX-180` because the staged local model cache is not ready.
3. `A2-AK-225` remains a known non-default fallback with fresh-container namespace/device contention, but it is no longer the active formal-case route.

## Next Required Action

Re-run the real formal case after at least one of the following changes:

- local Qwen3.5 cache finishes downloading, or a faster authenticated HF path is available
- the real formal case is resumed on `A3-AX-180` with the current run id and exact 910b image
- the resulting 8-row matrix, manifest, report, W&B, Prometheus, and provenance artifacts are verified end to end

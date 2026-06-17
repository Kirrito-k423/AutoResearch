---
phase: 14-verl-workspace-adapter-verl
plan: 04
status: blocked
subsystem: formal-report-and-uat
tags: [verl-case, report, qwen3.5, geometry3k, uat]

requires:
  - phase: 14-01
    provides: [formal-case config, immutable snapshot, evaluation helpers]
  - phase: 14-02
    provides: [docker runner, data/model staging, provenance hooks]
  - phase: 14-03
    provides: [autoresearch run verl-case orchestration, local artifact layout]
provides:
  - Formal-case report sections for matrix, length impact, async comparison, accuracy, consistency, and provenance
  - Strict formal-case completeness checks for matrix rows and required artifacts
  - User-facing `docs/verl-case.md` for command, cache root, Docker image, model, dataset, and provenance mapping
  - Qwen3.5-2B cache handling for Hugging Face `index.json + shard` layout
affects: [autoresearch, workspace-core, workspace-adapter, docs, tests]

tech-stack:
  added: []
  patterns:
    - "Formal report stays local-first and reads only manifest-linked artifacts"
    - "Formal completeness fails closed when any sync/async matrix row is missing"
    - "Model cache accepts Hugging Face sharded safetensors layout without manual rename"

key-files:
  created:
    - .planning/phases/14-verl-workspace-adapter-verl/14-04-SUMMARY.md
    - .planning/phases/14-verl-workspace-adapter-verl/14-UAT.md
  modified:
    - autoresearch/cli.py
    - config/config.example.yaml
    - config/config.yaml
    - docs/verl-case.md
    - tests/test_orchestrator_verl_case.py
    - tests/test_report_verl_case.py
    - tests/test_verl_case_runner.py
    - tests/workspace-core/test_config.py
    - workspace-adapter/verl/case_config.py
    - workspace-adapter/verl/model_sync.py
    - workspace-core/config/schema.py

key-decisions:
  - "Formal-case default model is aligned to `Qwen/Qwen3.5-2B` per phase discussion, not the earlier VL variant."
  - "Qwen3.5 local cache warming is resumable and does not require renaming `model.safetensors-00001-of-00001.safetensors`."
  - "Plan 14-04 stays blocked until a real 8-row sync/async matrix finishes on hardware and lands a complete report bundle."

requirements-completed: []

duration: 55min
completed: 2026-06-17
---

# Phase 14 Plan 04: Formal Case Report, Verification, And UAT Closure Summary

**报告层、完整性校验和文档已经落地并通过全量测试。真实 formal case 现已切到 `A3-AX-180` 这台通过 exact 910b 镜像 fresh-container smoke test 的机器，当前主阻塞不再是代码或机器选择，而是本地 `Qwen3.5-2B` `4.55GB` 权重 shard 仍在续传完成中；本轮新增了 detached supervisor，cache 完成后会自动接着起 formal run。**

## Performance

- **Duration:** 55 min
- **Started:** 2026-06-17T13:20:00Z
- **Completed:** 2026-06-17T14:15:00Z
- **Tasks:** 4 implementation/verification tasks complete; real UAT blocked
- **Files modified:** 11 in AutoResearch, 3 in local `verl` checkout still pending ship

## Accomplishments

- Formal report pipeline is present and green: `load_verl_case_view(...)`, matrix rendering, completeness checks, and docs-based acceptance all pass.
- `Qwen/Qwen3.5-2B` is now the default formal-case model across config schema, example config, local config, CLI description, docs, and tests.
- `workspace-adapter/verl/model_sync.py` now accepts Hugging Face sharded safetensors layout through `model.safetensors.index.json` plus `model.safetensors-00001-of-00001.safetensors`.
- Focused Phase 14 suite and full repository suite both passed after the Qwen3.5 alignment.
- Real command retries now prove three things in sequence:
  1. `A2-AK-225` can be ruled out for fresh formal containers because of namespace/device contention;
  2. `A3-AX-180` can run the exact requested Verl 910b image in a fresh container with working NPU allocation;
  3. the repaired local resume path grows the live Qwen3.5 shard past the previous `107668954`-byte disconnect point.

## Verification

- `uv run pytest -q tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py tests/workspace-core/test_config.py` -> `49 passed`
- `uv run pytest -q tests/test_verl_case_config.py tests/test_verl_case_runner.py tests/test_orchestrator_verl_case.py tests/test_report_verl_case.py` -> `38 passed`
- `uv run pytest -q` -> `408 passed, 6 warnings`
- `uv run pytest tests/test_verl_case_runner.py -k 'prepare_model_cache or resume_model_download'` -> `6 passed`
- `uv run pytest tests/test_orchestrator_verl_case.py -k 'docker_stack_override or formal_readiness_ignores_archon_and_host_python or ignores_remote_huggingface'` -> `3 passed`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml --local-proxy-url http://127.0.0.1:7890 --remote-proxy-port 17892 --run-id uat-qwen35-20260617-1` -> readiness reached `stack=pass`; local Qwen3.5 cache bootstrap started; run intentionally aborted after proving resumable cache bootstrap because download bandwidth, not code, became the limiting step.
- `docker run --rm ... quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5 python3 -c 'import torch, torch_npu; ... x.cpu().tolist()'` on `A3-AX-180` -> `True`, `npu:0`, `[1.0]`
- Latest `A3-AX-180` formal retries with run id `formal-20260617-222232-a3ax180` pass readiness into `prepare`, and the largest resumable local shard grows to `114294784` bytes.

## Real UAT

See `14-UAT.md`.

High-signal observations from the real attempts:

- `A2-AK-225` readiness today:
  - `config`: pass
  - `services`: fail
  - `hw`: warn
  - `net`: warn
  - `reach`: pass
  - `stack`: pass
- The formal-case orchestrator continued past the non-fatal readiness issues and entered local asset preparation as designed.
- The new Qwen3.5 cache root `/Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B` was populated with config/tokenizer sidecars plus `model.safetensors.index.json`; after the resume fixes, the active shard checkpoint reached `114294784` bytes and continued to grow past the old failure mark.
- The latest detached supervisor run continues the same shard automatically and advanced the live checkpoint to `225607680` bytes; logs now live under `~/.autoresearch/runs/formal-20260617-222232-a3ax180/supervisor.log`, and the same supervisor will launch the real `autoresearch run verl-case` command when `model.safetensors-00001-of-00001.safetensors` becomes complete.
- Prior A2 diagnostic runs had already reached remote `torch_npu` device setup and still failed with `aclInit` / `torch_npu.set_device()` error code `507899`, `Resource_Busy`, including a single-card run.
- Host-vs-container follow-up on `A2-AK-225` narrowed the blocker further:
  - host `conda run -n verl-qwen3.5 python -c '... torch.tensor([1.0]).npu()'` succeeds;
  - `docker exec verl-8.5.2-a2 ... torch.tensor([1.0]).npu()` succeeds inside the long-lived existing Verl container;
  - a fresh `docker run --rm quay.io/ascend/verl:... python -c '... torch.tensor([1.0]).npu()'` fails with `aclInit 507899 / Resource_Busy`;
  - `dmesg` reports repeated `uda_occupy_dev_by_ns ... Conflict open udevid` errors;
  - host `/proc/*/fd` inspection shows long-lived `asc_dumper` processes inside `/verl-8.5.2-a2` holding `/dev/davinci_manager` and `/dev/hisi_hdc`.
- This points to stale container namespace/device-handle contention on A2, not a host-level inability to run `torch_npu`.
- Because the formal path stages the model from the Mac cache, `A3-AX-180` remote Hugging Face reachability is now treated as a formal-case warning rather than a hard blocker when local HF access is healthy.

## Provenance Snapshot

- AutoResearch repo:
  - branch: `codex/verl-case-formal-20260617-222232-a3ax180-phase-02-workspace-core`
  - remote: `https://github.com/Kirrito-k423/AutoResearch.git`
  - shipped commit: `46f8910`
  - commit URL: `https://github.com/Kirrito-k423/AutoResearch/commit/46f8910`
  - branch URL: `https://github.com/Kirrito-k423/AutoResearch/tree/codex/verl-case-formal-20260617-222232-a3ax180-phase-02-workspace-core`
- Local `verl` dependency repo:
  - branch: `codex/verl-case-formal-20260617-222232-a3ax180-main`
  - fork remote: `https://github.com/Kirrito-k423/verl.git`
  - upstream remote: `https://github.com/verl-project/verl.git`
  - shipped commit: `a604fc0e`
  - commit URL: `https://github.com/Kirrito-k423/verl/commit/a604fc0e`
  - branch URL: `https://github.com/Kirrito-k423/verl/tree/codex/verl-case-formal-20260617-222232-a3ax180-main`

## Issues Encountered

- `Qwen/Qwen3.5-2B` was not cached locally yet, so the first real command had to start a fresh local cache warm-up under the configured proxy.
- The public Hugging Face download remains unauthenticated and slow on this Mac/proxy path, but the failure mode has improved from “repeat disconnect around 107MB” to “resumable curl-based progress that crosses 110MB”.
- The A2 hardware/runtime blocker remains documented as a fallback hazard, but it is no longer the active formal host after the `A3-AX-180` exact-image qualification.

## User Setup Required

- If we want the local Qwen3.5 cache to finish materially faster, provide a usable `HF_TOKEN` in the environment before the next resume.
- No additional user decision is required to keep pushing on the `A3-AX-180` path; the remaining work is mostly time/bandwidth plus the final real matrix execution, and that handoff is now scripted locally.

## Next Phase Readiness

- Code and report layers are ready.
- Phase 14 cannot be marked complete until:
  1. local Qwen3.5 cache finishes,
  2. `A3-AX-180` completes all 8 sync/async rows through 16k on the exact 910b image,
  3. the formal report bundle contains full matrix, accuracy, consistency, W&B, Prometheus, manifest, config snapshot, and provenance evidence,
  4. shipped commits/branch URLs are captured for every repo touched by the run.

## Self-Check: FAILED

- **PASS:** Report loader/render/completeness tests are green.
- **PASS:** Full repository regression suite is green (`408 passed`).
- **PASS:** Real formal-case command now aligns to `Qwen/Qwen3.5-2B`, selects an exact-image-capable host (`A3-AX-180`), and resumes the local model shard past the old disconnect threshold.
- **FAIL:** No completed 8-row real matrix exists yet.
- **FAIL:** No clean shipped commit+GitHub-link provenance bundle has been captured from a successful formal run.
- **FAIL:** The local `4.55GB` Qwen3.5 shard is still incomplete, so the real matrix has not started on `A3-AX-180` yet.

---
*Phase: 14-verl-workspace-adapter-verl*
*Blocked: 2026-06-17*

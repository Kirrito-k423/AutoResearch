# Phase 14: 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环 - Context

**Gathered:** 2026-06-16T15:11:56Z
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 14 delivers the first formal, non-demo Verl case for AutoResearch:
select a usable Ascend machine through the existing 1-6 readiness skills, run a
GRPO/RL geometry reasoning case in the Ascend Verl container, collect all local
observability artifacts, and bind every experiment result to immutable
configuration plus multi-repository code provenance.

This phase upgrades the existing minimal smoke loop into a formal `verl-case`
workflow. It must not remove or weaken `autoresearch run smoke`; smoke remains
the fast minimal path from prior phases.

</domain>

<decisions>
## Implementation Decisions

### Formal Entry And Container Boundary

- **D-83:** Add a new user-facing CLI entrypoint named `autoresearch run verl-case`.
- **D-84:** Keep `autoresearch run smoke` as the minimal smoke path; `verl-case` is a separate formal case path, not a silent behavior change to smoke.
- **D-85:** The target remote image is `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`.
- **D-86:** Docker usage must follow the VeOmni Ascend A2 Docker guide patterns for Ascend device access, driver mounts, shared memory, proxy variables, checkpoint mounts, and dataset mounts.
- **D-87:** The case must run on a machine selected by the current 1-6 skills, not a hard-coded host. A2-AK-225 is the known likely candidate from prior UAT, but selection must be data-driven.

### Model, Dataset, And Cache Policy

- **D-88:** The first formal case is GRPO/RL mathematical geometry reasoning, not SFT.
- **D-89:** Use `Qwen/Qwen3.5-2B` as the model source.
- **D-90:** Use `hiyouga/geometry3k` as the dataset source.
- **D-91:** geometry3k input must preserve original multimodal `image + problem` fields; do not silently downgrade the case to text-only.
- **D-92:** Default local cache root is `/Users/Zhuanz/autoResearchData`, and this path must be configurable.
- **D-93:** Artifacts at or below 5GB, including container metadata, model, and dataset material, may be retained locally under the configured cache root.
- **D-94:** Remote no-network scenarios must be supported via the existing Mac proxy / SSH forwarding path, or by preparing local cached assets and uploading/mounting them.

### Experiment Matrix And Completion Standard

- **D-95:** The sequence-length experiment starts at `1k input / 2k output`.
- **D-96:** `ignore_eos` must be disabled for this formal case.
- **D-97:** Inference/output length doubles until `16k`; the complete matrix must include all planned lengths through `16k`.
- **D-98:** Both synchronous and asynchronous inference modes must run the complete matrix.
- **D-99:** Phase 14 is not complete unless every matrix combination finishes and produces local observability artifacts. A failed 16k or async combination is a failure to close this phase, not a best-effort warning.

### Accuracy And Consistency Standard

- **D-100:** Accuracy must be judged against geometry3k ground truth answers.
- **D-101:** The async-vs-sync experiment must also compare extracted final answers from paired samples to detect behavior drift.
- **D-102:** The report must show both ground-truth accuracy and sync/async consistency, alongside performance metrics such as tokens/s, latency, success rate, and resource observations.

### Code Provenance And Immutable Run Config

- **D-103:** The workflow may use the user's GitHub account `Kirrito-k423` to fork official upstream repositories from `main` into experiment-specific branches.
- **D-104:** Automatic commit and push are allowed for AutoResearch and modified dependency repositories such as Verl, vLLM, Transformers, and MindSpeed.
- **D-105:** Every experiment run must persist a full immutable config snapshot. Use second-level timestamps to correlate config snapshot, run id, code commits, GitHub URLs, and local artifacts.
- **D-106:** Multi-repo provenance must record repository name, upstream URL, fork URL or branch URL, branch, commit SHA, dirty status before commit, and pushed GitHub link when available.
- **D-107:** Experiment data, logs, W&B artifacts, Prometheus data, reports, immutable config, and code provenance must be recoverable from the local run directory under `~/.autoresearch/`.

### the agent's Discretion

- The exact internal module names, dataclass names, and file split are left to the planner, but they must preserve the existing layer boundaries: generic SSH/config/layout stays in `workspace-core/`, Verl-specific logic stays in `workspace-adapter/verl`, and artifact/manifest/report logic stays in `datalake/` or `autoresearch/report`.
- The researcher/planner should verify the current Verl GRPO and async-inference flags inside the target image or upstream code before naming exact training arguments.
- The researcher/planner may define sensible numeric thresholds for accuracy drift, tokens/s reporting, and timeout defaults if no official threshold exists, but the full matrix completion requirement is not discretionary.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### User-Provided External Sources

- `https://github.com/ByteDance-Seed/VeOmni/blob/main/docs/hardware_support/AscendDockerUsage/build_a2_docker.md` — Ascend A2 Docker guide covering CANN image, device mounts, driver mounts, `--shm-size`, proxy environment, checkpoint mounts, dataset mounts, and training command shape.
- `https://huggingface.co/Qwen/Qwen3.5-2B/tree/main` — model source for Qwen3.5-2B; multimodal model page with Hugging Face files and usage references.
- `https://huggingface.co/datasets/hiyouga/geometry3k` — geometry3k dataset source; use original image-plus-problem samples and answer field.

### Project State And Roadmap

- `.planning/ROADMAP.md` — Phase 14 roadmap entry and dependency on Phase 13.
- `.planning/STATE.md` — current machine facts, prior UAT evidence, and local-first constraints.
- `.planning/PROJECT.md` — core value, local-first project semantics, hardware environment, and existing constraints.
- `.planning/milestones/v1.0/REQUIREMENTS.md` — archived v1.0 requirement history; use for prior requirement vocabulary only because living `.planning/REQUIREMENTS.md` has been archived.

### Prior Phase Context

- `.planning/phases/11-orchestration/11-CONTEXT.md` — top-level CLI orchestration decisions; `run smoke` must remain minimal and Python-entrypoint based.
- `.planning/phases/12-e2e-smoke/12-CONTEXT.md` — E2E report completeness and A2-AK-225/verI real UAT defaults.
- `.planning/phases/13-m1-archive/13-CONTEXT.md` — milestone archive boundaries and known gap handling.

### Existing Implementation

- `autoresearch/cli.py` — Click command tree where `autoresearch run verl-case` must be added.
- `autoresearch/orchestrator/checks.py` — existing 1-6 readiness orchestration to reuse for machine selection.
- `autoresearch/orchestrator/smoke.py` — existing minimal collect -> report path that must remain separate from the formal case.
- `autoresearch/e2e/smoke.py` — existing E2E completeness and duration gate pattern.
- `workspace-adapter/verl/minimal_runner.py` — current Verl minimal runner; formal case logic should live near this layer but not overwrite its smoke semantics.
- `autoresearch/collect/cli.py` — current collect orchestration and final JSON pattern.
- `autoresearch/collect/manifest.py` — current manifest builder that must be extended or paralleled for formal-case metadata.
- `datalake/manifest/schema.py` — current `RunManifest` source of truth for local persisted run metadata.
- `datalake/wandb/sync.py` — remote offline W&B sync pattern.
- `datalake/prometheus/push_gateway.py` — remote Pushgateway text exposition pattern.
- `autoresearch/report/loader.py` — report bundle source of truth.
- `autoresearch/report/models.py` — report data model extension point.
- `autoresearch/report/render.py` — single-file HTML report renderer extension point.
- `workspace-core/config/schema.py` — config schema extension point for cache root, fork settings, and formal case defaults.
- `config/config.example.yaml` — documented example defaults; must not include secrets.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `run_check_all` already runs config, services, hardware, network, reachability, and stack checks and returns normalized step payloads.
- `workspace-adapter/verl/minimal_runner.py` already shows the pattern for SFTP-uploaded remote scripts, `run_in_env`, W&B offline writes, remote log paths, and `MinimalResult`.
- `run_collect` already provides the local-first sequence: runner -> W&B sync -> log fetch -> Prometheus push -> manifest write -> final JSON.
- `RunManifest` and `load_report_bundle` already make `manifest.json` the report truth source.
- `StepResult`, `step_result`, `skipped_step`, and `summarize_steps` already normalize orchestrator output.

### Established Patterns

- CLI commands print a single final JSON object on stdout; progress goes to stderr as `__AR_PROGRESS__=<json>`.
- Top-level orchestration should call Python entrypoints directly instead of shelling out to `autoresearch ...` subcommands.
- Local-first is non-negotiable: remote runs may execute inside containers, but durable state must be pulled back or represented locally.
- Existing tests patch Python entrypoints for unit coverage and reserve real A2-AK-225 UAT for manual/real validation.

### Integration Points

- Add a new `run verl-case` command under the existing `autoresearch run` group.
- Add a formal-case runner under `workspace-adapter/verl/`, separate from `minimal_runner.py`.
- Extend or create manifest/report models so formal-case fields coexist with current minimal `one_step`.
- Extend config with configurable cache root and GitHub/provenance defaults without committing secrets.
- Add tests around command routing, immutable config snapshot generation, provenance serialization, matrix construction, and report loading/rendering.

</code_context>

<specifics>
## Specific Ideas

- Default local cache root: `/Users/Zhuanz/autoResearchData`.
- Use second-level timestamps in immutable config filenames or run ids so a run can be tied back to exact code and config snapshots.
- The report should explicitly answer two experiment questions:
  1. How do different input/output sequence lengths affect performance?
  2. How do async inference settings affect performance and accuracy?
- The matrix should be visible in manifest/report as rows keyed by input length, output length, async mode, status, performance metrics, accuracy, and sync/async consistency.
- Official dependency forks should use `Kirrito-k423` and experiment-specific branches derived from run/case identifiers.

</specifics>

<deferred>
## Deferred Ideas

- Supporting text-only geometry3k can be added as a fallback or diagnostic mode in a later phase, but this phase's formal case is multimodal `image + problem`.
- Multi-node scheduling remains out of scope for Phase 14 unless the researcher proves it is required for the single formal case.
- A general experiment scheduler or web UI for experiment matrices belongs in a future phase.

</deferred>

---

*Phase: 14-跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环*
*Context gathered: 2026-06-16T15:11:56Z*

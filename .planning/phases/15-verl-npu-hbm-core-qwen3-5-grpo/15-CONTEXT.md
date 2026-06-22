# Phase 15: verl-npu-hbm-core-qwen3-5-grpo - Context

**Gathered:** 2026-06-22T11:53:31Z
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 15 upgrades the Phase 14 formal Verl case from "can complete a validation matrix" to a real, observable GRPO training experiment loop. It must add runtime NPU HBM/Core telemetry, run a true Qwen3.5-2B + geometry3k GRPO training path, capture Verl stage timings, and reorganize the data-repository artifacts so W&B and Prometheus-style visualizations can be rebuilt from the copied data bundle.

This phase does not build a general distributed scheduler, a new web UI, or a broad multi-model benchmark suite. It focuses on the single-machine formal Verl case and the evidence contract needed to understand performance, resource saturation, and stage-level timing.

</domain>

<decisions>
## Implementation Decisions

### Runtime NPU HBM/Core Telemetry

- **D-108:** Use `npu-smi info watch` as the first-class runtime sampling source. A2-AK-225 reports `npu-smi info watch -h` supports `-s` metrics including `a` for AI Core Usage, `m` for Memory Usage, and `n` for NPU Utilization.
- **D-109:** The initial sampling command should use the native watch path, for example `npu-smi info watch -d 1 -s amn`. The user originally wanted 0.5s, but the observed command help restricts `-d` to `1~100` seconds, so Phase 15 locks the native 1s watch route unless research finds a reliable sub-second API.
- **D-110:** Sampling must run continuously during each training case, starting before the Verl process and stopping after it exits. End-of-run single-point evidence is not sufficient.
- **D-111:** Persist both raw sampler output and normalized machine-readable rows. The normalized data must be suitable for plotting HBM used/total, AI Core utilization, and NPU utilization by time.
- **D-112:** Prometheus labels must preserve correlation keys: `run_id`, `case_id`, `server`, `device_id`, and metric source. If matrix row identifiers remain relevant, include `row_id` as well.
- **D-113:** At minimum, expose Prometheus-compatible metric names for HBM used, HBM total, AI Core utilization, and NPU utilization. Existing `autoresearch_npu_count` is not enough for this phase.

### Real GRPO Training Closure

- **D-114:** Phase 15 must exercise a true GRPO training loop, not only `trainer_val_only=true`. The formal training case should run with `trainer_val_only=false`.
- **D-115:** Start tuning from a single NPU with batch size 1, then gradually increase batch-related knobs to find the largest stable setting that fits HBM.
- **D-116:** After the single-card search identifies stable candidates, expand to the single-node 8-card route and maximize total throughput.
- **D-117:** Every case in the tuning matrix must run 3 training steps. A case that cannot complete 3 steps is a failed data point, not a valid throughput result.
- **D-118:** The tuning loop should record both successful and failed cases, including OOM/resource failures, so the report explains the boundary of usable HBM rather than only showing the final winner.
- **D-119:** The objective is throughput and resource saturation, not model quality benchmarking. Accuracy/reward should still be recorded when available, but the success question is whether the training loop runs, which settings fit, and which settings maximize single-card and single-node throughput.

### Verl Stage Timing Source

- **D-120:** Prefer Verl's native W&B logging path for stage timing and throughput metrics when those fields are available. Keep `trainer.logger=[console,wandb]` for the formal training path.
- **D-121:** Also parse Verl console/log output because Phase 14 showed W&B summaries alone can be too thin for detailed diagnosis.
- **D-122:** Stage timing should cover the main GRPO phases as available: rollout/inference, log probability, reference log probability, reward, advantage computation, update/backward/optimizer, validation, checkpointing, and data loading.
- **D-123:** Store stage timings per case and per training step in a durable file such as `stage-timings.jsonl`, and summarize them into W&B/report views.
- **D-124:** Only patch Verl or dependency repositories for timing instrumentation if native W&B plus log parsing cannot expose the required stages. Any such patch must be captured in provenance and pushed through the user's current branch workflow.

### Artifact Organization And Rebuildability

- **D-125:** The data-repository bundle should be organized by customer reading priority using numeric prefixes:
  - `0-report/`
  - `1-wandb/`
  - `2-prometheus/`
  - `3-raw-logs/`
  - `4-config/`
  - `5-provenance/`
  - `6-rows/`
  - `restore/`
- **D-126:** `0-report/` is the top-level customer entry point and should link to the rest of the bundle.
- **D-127:** `1-wandb/` must contain enough raw W&B offline data and rebuild scripts to recreate the historical W&B Web view under the local W&B service.
- **D-128:** `2-prometheus/` must contain raw telemetry data and rebuild instructions/scripts sufficient to recreate Prometheus-style resource curves from the copied data bundle. If live Prometheus TSDB replay is not practical, the local report must still rebuild the same Prometheus curves from the saved normalized telemetry.
- **D-129:** `3-raw-logs/` must contain raw Verl logs, sampler logs, launcher stdout/stderr, and any parser input needed to audit the extracted stage timings.
- **D-130:** Immutable config, provenance, rows, restore scripts, W&B, Prometheus, and raw logs must remain together in the `autoresearch-log` data repository, separated from the AutoResearch code repository.
- **D-131:** W&B project naming remains `verl`; W&B run display names must stay human-readable using the model/scale/algorithm/sequence/time/config convention established in Phase 14.

### the agent's Discretion

- The planner may decide the exact Python modules and data classes for sampler orchestration, normalized telemetry rows, stage timing extraction, and report rendering, as long as existing layer boundaries are respected.
- The planner may choose the exact batch-size search grid and growth rule, provided it starts with single-card BS=1, records failures, runs each case for 3 steps, and escalates stable candidates to 8-card single-node throughput.
- The planner may decide whether Prometheus rebuild is implemented as live replay, OpenMetrics export, local report rendering from telemetry JSONL, or a combination, provided the copied data bundle can recreate the visual curves without the original live service state.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Current Phase And Prior Decisions

- `.planning/ROADMAP.md` — Phase 15 scope, goal, and dependency on Phase 14.
- `.planning/PROJECT.md` — local-first project value, data/reproducibility constraints, and formal Verl current state.
- `.planning/STATE.md` — current milestone status, known hardware/network caveats, and Phase 14 artifact references.
- `.planning/phases/14-verl-workspace-adapter-verl/14-CONTEXT.md` — locked formal Verl case decisions that Phase 15 extends.
- `.planning/phases/14-verl-workspace-adapter-verl/14-05-SUMMARY.md` — final Phase 14 runtime evidence, residual caveats, and matrix result summary.
- `.planning/phases/14-verl-workspace-adapter-verl/14-VERIFICATION.md` — verified Phase 14 evidence and known Prometheus resource-metric gap.

### Existing Formal Verl Implementation

- `autoresearch/orchestrator/verl_case.py` — `autoresearch run verl-case` orchestration, artifact collection, W&B sync, Prometheus push, manifest/report generation.
- `workspace-adapter/verl/case_runner.py` — remote row runner, generated Verl command, validation-mode defaults, W&B run naming, and row result extraction.
- `workspace-adapter/verl/case_config.py` — formal case config model, matrix builder, readable run id, W&B run name, and `trainer_val_only` default.
- `workspace-adapter/verl/SKILL.md` — Verl adapter boundary, naming conventions, formal case flow, Git policy, and top troubleshooting notes.
- `config/config.example.yaml` — public non-secret config defaults for formal Verl case.

### NPU And Prometheus Existing Code

- `autoresearch/hw/probe.py` — existing SSH hardware probe and typed `npu-smi info -t memory/usages` command helpers.
- `autoresearch/hw/parser.py` — existing parser for `npu-smi info` output and typed memory/usages output.
- `datalake/prometheus/push_gateway.py` — current Pushgateway path that only pushes `autoresearch_npu_count`.
- `autoresearch/report/prometheus.py` — current report Prometheus loader and existing warnings for missing HBM/Core metrics.

### W&B, Report, And Data Bundle Existing Code

- `datalake/wandb/sync.py` — remote offline W&B fetch/sync and rebuild script generation.
- `autoresearch/report/wandb.py` — current W&B summary/report loading and fallback from matrix data.
- `autoresearch/report/verl_case.py` — formal Verl matrix report normalization and validation/training-mode diagnostics.
- `autoresearch/report/models.py` — report model extension points for Prometheus, W&B, and formal Verl case data.
- `autoresearch/report/render.py` — HTML report rendering surface where numbered artifact links and resource/stage charts should appear.
- `datalake/manifest/schema.py` — manifest source of truth for persisted run metadata.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `autoresearch.hw.parser.parse_npu_smi_info` and `parse_typed_metric_output` already understand HBM/memory and utilization fields from Ascend `npu-smi` outputs.
- `autoresearch.hw.probe.typed_query_command("memory"|"usages", device_id)` already gives an allowlisted command pattern for per-device memory/utilization supplement queries.
- `datalake.prometheus.push_gateway.push_metrics` already opens the reverse tunnel and pushes Prometheus text exposition through `curl`; Phase 15 can generalize this from one count metric to time-series telemetry.
- `datalake.wandb.sync.sync_all_runs` and rebuild helpers already pull W&B offline runs into the local data bundle and generate restore scripts.
- `workspace-adapter/verl/case_runner.py` already sets `WANDB_MODE=offline`, `WANDB_DIR`, `trainer.project_name`, and `trainer.experiment_name` inside the container.

### Established Patterns

- CLI commands must end with a single JSON object on stdout; progress belongs on stderr as `__AR_PROGRESS__=<json>`.
- Durable experiment truth belongs in the local data repository, not only in remote workdirs or live service state.
- Formal-case code lives in `workspace-adapter/verl` and `autoresearch/orchestrator/verl_case.py`; generic SSH/config/report/data logic belongs in workspace-core, datalake, or autoresearch/report as appropriate.
- Git provenance should record current-branch commits and dependency repo commits; do not create a new branch per run by default.

### Integration Points

- Add a runtime sampler around the remote Verl process in `workspace-adapter/verl/case_runner.py` or a nearby Verl adapter module.
- Extend `VerlCaseResultRow` or add adjacent models for training cases, NPU telemetry summaries, and stage timings.
- Extend `run_verl_case_orchestration` to collect sampler files, normalized telemetry, W&B runs, stage timing files, and numbered artifact directories.
- Extend report loading/rendering so HBM/Core curves and stage timing breakdowns appear in `0-report/`.
- Extend tests around npu-smi watch parsing, telemetry normalization, Prometheus evidence, artifact layout, and training-mode config.

</code_context>

<specifics>
## Specific Ideas

- Remote observation on A2-AK-225: `npu-smi info watch -h` reports `-d %d` collection delay with range `[1~100]`, so native watch cannot directly do 0.5s sampling.
- The selected Phase 15 sampling route is native `watch` at 1s, not a custom 0.5s polling loop, unless research later finds a safe lower-level API.
- Every tuning case must run 3 training steps.
- The training search should answer two performance questions separately: maximum single-card throughput and maximum 8-card single-node total throughput.
- Artifact order should match customer reading order rather than implementation order: report first, then W&B, Prometheus, raw logs, config, provenance, rows, restore.

</specifics>

<deferred>
## Deferred Ideas

- Sub-second 0.5s telemetry can be revisited if native `npu-smi watch` is insufficient and a reliable custom sampling loop proves safe.
- A full generic experiment scheduler, multi-node distributed search, or broad model/dataset benchmarking system belongs in a later phase.

</deferred>

---

*Phase: 15-verl-npu-hbm-core-qwen3-5-grpo*
*Context gathered: 2026-06-22T11:53:31Z*

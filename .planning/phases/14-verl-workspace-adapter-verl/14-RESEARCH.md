# Phase 14: Verl Formal Case Loop - Research

## RESEARCH COMPLETE

**Question answered:** What do we need to know to plan a formal, non-demo Verl case for AutoResearch?

## Source Findings

### Ascend Docker

- The VeOmni Ascend A2 guide uses a CANN 9.0.0 Ubuntu 22.04 Python 3.11 base, maps Ascend device files such as `/dev/davinci*`, `/dev/davinci_manager`, `/dev/devmm_svm`, and `/dev/hisi_hdc`, mounts host driver directories read-only, recommends larger shared memory such as `--shm-size=64G`, and shows proxy, checkpoint, and dataset mounts.
- The same guide distinguishes x86 and ARM64 environment activation. x86 images require activating `/app/.venv`; ARM64 does not.
- Phase 14 should not bake a new image locally first. The user explicitly selected `docker pull quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`; implementation should pull/run that image and keep local metadata under the configured cache root when under 5GB.

### Qwen3.5 And geometry3k

- `Qwen/Qwen3.5-2B` is an Image-Text-to-Text model on Hugging Face, apache-2.0 licensed, with a single safetensors shard around 4.55GB. It fits the user's "5GB 以内可本地保存" boundary if cache policy records exact size and refuses unbounded extras.
- Hugging Face usage examples show multimodal messages with image plus text for Transformers, vLLM, and SGLang. This supports the user decision to preserve geometry3k's `image + problem` shape instead of silently switching to text-only.
- `hiyouga/geometry3k` exposes geometry problem samples with image, prompt/problem text, and answer-style fields. Implementation must normalize records into a Verl-ready JSONL while preserving the original image path or cached file reference.

### Verl GRPO And Async

- Verl documentation exposes `actor_rollout_ref.rollout.ignore_eos`, so the formal config can explicitly set it to `false`.
- Verl has async-training recipes and fully async policy documentation; async support depends on exact upstream scripts and rollout backend. Implementation must inspect the pulled container/upstream code at runtime before choosing the final command path. This should be a runner preflight, not a hard-coded guess in CLI flags.
- The safest AutoResearch abstraction is a generated immutable case config plus a remote runner script that can adapt to detected Verl script names inside the container. If an exact expected script is missing, the run should fail with a preflight error and preserve logs/config.

## Implementation Strategy

1. Add typed Phase 14 models for cache paths, Docker image, model/dataset IDs, matrix rows, immutable config snapshots, result rows, and multi-repo provenance.
2. Add a Verl formal runner under `workspace-adapter/verl/` that:
   - Builds the length matrix: `(input_tokens=1024, output_tokens=2048)`, then output lengths `4096`, `8192`, `16384`, for both `sync` and `async`.
   - Forces `ignore_eos=false`.
   - Prepares local cache metadata under `/Users/Zhuanz/autoResearchData` by default, configurable through config and CLI.
   - Generates and uploads a remote run bundle under `/home/t00906153` or the configured `ServerSpec.workdir`.
   - Pulls and runs the selected Docker image with Ascend device/driver/shared-memory/proxy/model/dataset mounts.
   - Writes one machine-readable row per matrix combination.
3. Add top-level orchestration `autoresearch run verl-case` that:
   - Runs or reuses the existing 1-6 readiness checks for data-driven server selection.
   - Runs the formal case runner.
   - Pulls logs, W&B offline output, Prometheus metrics, immutable config, provenance, and matrix results into `~/.autoresearch/runs/<run_id>/`.
   - Emits a single final JSON object on stdout and progress on stderr.
4. Extend report/manifest layers so the two experimental questions are visible in the local report:
   - Sequence length impact on latency/tokens/s/success.
   - Async inference impact on performance, ground-truth accuracy, and sync/async consistency.

## Validation Architecture

Automated validation should cover all local deterministic behavior:

- Matrix construction includes 8 rows: 4 output lengths by 2 modes.
- `ignore_eos` serializes as `false`.
- Config defaults include `/Users/Zhuanz/autoResearchData`, model `Qwen/Qwen3.5-2B`, dataset `hiyouga/geometry3k`, and image `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`.
- Docker command builder contains Ascend device files, driver mounts, `--shm-size`, proxy env support, model mount, and dataset mount.
- Immutable config snapshot is written before remote execution and copied into the run directory.
- Provenance records include repo, upstream, fork/branch URL, branch, sha, dirty status, and pushed URL fields.
- CLI `autoresearch run verl-case` has a happy-path unit test with all remote calls mocked and emits one JSON object.
- Report loading/rendering supports formal-case matrix fields, accuracy, consistency, and links to raw artifacts.

Manual/real UAT must run on a real selected Ascend host:

- `uv run autoresearch run verl-case --server A2-AK-225 --config config/config.yaml ...`
- Docker pull succeeds or uses a prepared local cache path.
- Every strict matrix row through 16k completes for sync and async.
- Local run directory contains immutable config, provenance, matrix results, remote logs, W&B artifact, Prometheus data, manifest, and report.

## Risks And Mitigations

- **Exact Verl command drift:** Detect scripts/config keys inside the container and fail closed with captured diagnostics instead of pretending success.
- **Remote no-network:** Reuse local proxy/SSH forwarding and allow prepared local cache upload/mount paths.
- **16k OOM/timeout:** The user selected strict completion. Treat failure as phase-not-complete; report exact failing row and resource evidence.
- **Qwen3.5 multimodal support in Verl image:** Preserve image+problem data and make unsupported multimodal preprocessing a preflight failure, not a text-only fallback.
- **Multi-repo GitHub writes:** Encapsulate fork/commit/push as provenance steps with dry-run/mockable unit tests; real dependency pushes are UAT/manual.

## References

- https://github.com/ByteDance-Seed/VeOmni/blob/main/docs/hardware_support/AscendDockerUsage/build_a2_docker.md
- https://huggingface.co/Qwen/Qwen3.5-2B/tree/main
- https://huggingface.co/datasets/hiyouga/geometry3k
- https://verl.readthedocs.io/en/latest/examples/config.html
- https://verl.readthedocs.io/en/latest/advance/one_step_off.html
- https://verl.readthedocs.io/en/latest/advance/fully_async.html

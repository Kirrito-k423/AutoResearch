# Verl Formal Case

`autoresearch run verl-case` runs the formal Ascend Verl case for Qwen/Qwen3.5-2B on hiyouga/geometry3k and persists a local-first evidence bundle.

## Command

```bash
uv run autoresearch run verl-case \
  --server A2-AK-225 \
  --config config/config.yaml \
  --local-proxy-url http://127.0.0.1:7890 \
  --remote-proxy-port 17892
```

Useful options:

- `--server`: overrides config-driven machine selection; omit it to use the first configured server.
- `--cache-root`: overrides `verl_case.cache_root`; the default is `/Users/Zhuanz/autoResearchData`.
- `--skip-readiness`: skips the skills 1-6 readiness checks for controlled debugging.
- `--allow-git-push`: allows experiment repositories to commit and push provenance branches.
- `--run-id`: pins the local artifact directory name.

## Fixed Case

- Docker image: `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`
- Model: `Qwen/Qwen3.5-2B`
- Dataset: `hiyouga/geometry3k`
- Input length: `1024`
- Output lengths: `2048`, `4096`, `8192`, `16384`
- Modes: `sync`, `async`
- `ignore_eos`: `false`

The formal run is incomplete unless every sync/async row through 16k is present and passed.

## Local Cache And No-Network Path

The local cache root defaults to `/Users/Zhuanz/autoResearchData`. Keep <=5GB model/data/container artifacts there when practical. On remote hosts without external network, use local cache plus the existing proxy/tunnel readiness path:

1. Ensure local proxy is available at `127.0.0.1:7890`.
2. Let readiness use `--remote-proxy-port 17892`.
3. Keep model and dataset mounts under the configured remote workdir, normally `/home/t00906153`.

## Artifact Layout

Each run writes under `~/.autoresearch/runs/<run_id>/`:

- `config-<timestamp>.json`: immutable full run config.
- `provenance.json`: Git SHAs, dirty status, fork/branch links.
- `matrix-results.jsonl`: one row per length and inference mode.
- `verl-case.log`: local execution summary and remote paths.
- `wandb/`: local W&B artifact directory.
- `prom/formal-case-prometheus.json`: Prometheus/Pushgateway evidence metadata.
- `manifest.json`: canonical pointer to every artifact.
- `report.html`: reviewable performance, accuracy, consistency, and provenance report.

## Code And Data Correspondence

Use the run id to open `manifest.json`, then inspect:

- `config_snapshot` for the immutable config used by the run.
- `provenance[]` for AutoResearch and dependency repository commit SHAs.
- `branch_url` or `pushed_url` for GitHub links when `--allow-git-push` was used.
- `formal_case.matrix_results` for the exact rows behind the report.

Configured dependency paths live under `verl_case.dependency_repo_paths` and can include `verl`, `vllm`, `transformers`, and `mindspeed`. Missing paths are warnings so a run can still record AutoResearch provenance.

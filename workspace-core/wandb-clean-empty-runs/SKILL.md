---
name: wandb-clean-empty-runs
description: Clean AutoResearch or local W&B run directories that have no successful step evidence. Use when asked to clean wandb data, remove empty or failed W&B runs, delete W&B logs without step/validation/success metrics, or preserve only runs that contain at least one useful step signal such as output.log step metrics, wandb-summary metrics, passed_rows, val-core/val-aux metrics, or one-step probe summary values.
---

# W&B Empty Run Cleanup

## Workflow

Use `scripts/clean_wandb_empty_runs.py` for repeatable filesystem cleanup. Run commands from the AutoResearch repository root unless using an absolute path. Always run a dry-run first and inspect the candidate list before deleting.

Default roots:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_empty_runs.py
```

AutoResearch-focused roots:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_empty_runs.py \
  --root ~/.autoresearch/runs \
  --root ~/autoResearchData/autoresearch-log/wandb/offline-runs
```

Delete only after the dry-run matches the user's intent:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_empty_runs.py \
  --root ~/.autoresearch/runs \
  --root ~/autoResearchData/autoresearch-log/wandb/offline-runs \
  --delete
```

Prune empty directories left behind by deleted W&B units:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_empty_runs.py \
  --root ~/.autoresearch/runs \
  --delete \
  --prune-empty-dirs
```

Clean runs that have already been imported into the local W&B server UI:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_local_server.py \
  --entity autoresearch-local \
  --project verl
```

Delete the server-side candidates after reviewing the dry-run:

```bash
python3 workspace-core/wandb-clean-empty-runs/scripts/clean_wandb_local_server.py \
  --entity autoresearch-local \
  --project verl \
  --delete \
  --remove-files
```

## Success Signals

Keep a W&B unit when any scanned text file contains one of these signals:

- `wandb-summary.json` has at least one non-system metric key, such as `sum`, `npu_count`, `matrix_rows`, `passed_rows`, `sample_count`, `accuracy`, `val-core/*`, or `val-aux/*`.
- `output.log` or another text log contains a concrete step line like `step:0 - ...`.
- Logs contain validation completion or metric text such as `Initial validation metrics`, `validation generation end`, `val-core/`, or `val-aux/`.
- Aggregated AutoResearch summary files contain positive `passed_rows`, `matrix_rows`, or `sample_count`.

Treat `_step` alone as insufficient. W&B can create `_step: 0` even when no useful metric or successful step evidence exists.

For local W&B server cleanup, treat a run as empty when `runs.history_count = 0` and `runs.summary_metrics` contains no non-system keys after removing `_runtime`, `_timestamp`, `_step`, and `_wandb`.

## Cleanup Boundaries

The script deletes only candidate W&B units: directories named `wandb` or standalone `offline-run-*` directories. It does not delete entire experiment directories unless the W&B unit itself is the experiment directory.

When candidates are nested, the script deletes only the highest candidate parent so the same files are not counted twice. If a parent W&B directory has success evidence, a nested no-signal W&B directory can still be removed.

Use `--prune-empty-dirs` only after deletion; it removes empty directories under the provided roots, including empty run shells and empty support directories such as `prom/`.

If deleting standalone runs under `~/autoResearchData/autoresearch-log/wandb/offline-runs`, check whether `registry.jsonl` still references removed run IDs before rebuilding the local W&B UI.

For the Dockerized local W&B service, `clean_wandb_local_server.py` soft-deletes DB rows in `runs`, `runs_flat`, and `files` by setting `deleted_at`, and optionally removes the MinIO object directory under `/vol/minio/local-files/<entity>/<project>/<run>`. Restart `ar-wandb` if the browser still shows stale cached results after DB cleanup.

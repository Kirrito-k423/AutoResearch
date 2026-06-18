---
status: passed
phase: 14-verl-workspace-adapter-verl
updated: 2026-06-18T11:16:20Z
source: 14-UAT.md, formal run artifacts, pytest
combined_run_id: formal-20260618-a2ak225-combined-r1
---

# Phase 14 Verification

## Verdict

Phase 14 is verified end to end. The formal Verl case now runs on real Ascend hardware using the requested official image stack, Qwen3.5-2B, and geometry3k; the final combined artifact contains the full `1024 -> 2048/4096/8192/16384` sync/async matrix with all 8 rows passed.

## Evidence

- `uv run pytest tests/test_verl_case_runner.py tests/test_minimal_runner.py -q` -> `58 passed`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/verl-case-async-16384.local.yaml --timeout 20000 --run-id formal-20260618-a2ak225-async16384-r1 --allow-git-push --skip-readiness` -> `ok=true`
- `uv run autoresearch run verl-case --server A2-AK-225 --config config/verl-case-sync-8192.local.yaml --timeout 12000 --run-id formal-20260618-a2ak225-sync8192-r1 --allow-git-push --skip-readiness` -> `ok=true`
- `uv run autoresearch report render --run-id formal-20260618-a2ak225-combined-r1` -> `ok=true`, report path `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/report.html`
- Final matrix: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/matrix-results.jsonl`
- Final manifest: `/Users/Zhuanz/.autoresearch/runs/formal-20260618-a2ak225-combined-r1/manifest.json`

## Manual Checks

- PASS: `autoresearch run verl-case` exists and runs a formal, non-demo Verl case.
- PASS: Official image stack is recorded: `quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5`.
- PASS: Model and dataset are the requested pair: `Qwen/Qwen3.5-2B` and `hiyouga/geometry3k`.
- PASS: The final matrix has 8 rows and every row has `status=passed`.
- PASS: `ignore_eos=false` is recorded in the config snapshot and every matrix row.
- PASS: Sequence-length impact and sync-vs-async impact are visible in `report.html`.
- PASS: Config snapshot, provenance, matrix results, row logs, validation JSONL files, W&B summary, Prometheus evidence, manifest, and report are present locally.
- PASS: Multi-repo provenance records AutoResearch, Verl, and vLLM commit SHAs and GitHub branch links.
- WARN: Prometheus live query returned no current metric for the combined run, but `prom/formal-case-prometheus.json` and source-run Prometheus files are saved locally.

## Runtime Provenance

| Repo | Commit | Branch URL |
|---|---|---|
| AutoResearch | `f1047ca1b3c046e3905a54c40f0390017d891c11` | `https://github.com/Kirrito-k423/AutoResearch/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-phase-02-workspace-core` |
| verl | `76d341aa15e72d126005e105a679e6e22b394bbb` | `https://github.com/Kirrito-k423/verl/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-main` |
| vllm | `b8b302cde434df8c9289a2b465406b47ebab1c2d` | `https://github.com/Kirrito-k423/vllm/tree/codex/verl-case-formal-20260618-a2ak225-sync8192-r1-20260618-a2ak225-async16384-r1-20260618-a2ak225-async-r4-20260618-005703-a2ak225-20260617-222232-a3ax180-detached-b8b302cde` |

Transformers and MindSpeed were not modified as local dependency repositories for this formal case, so no additional fork branch was produced for them.

## Blocking Conditions

None.

## Next Required Action

Run `$gsd-verify-work 14` / `$gsd-ship` if a formal workflow gate or PR publication is desired.

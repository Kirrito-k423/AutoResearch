# Phase 14: Verl Formal Case Loop - Patterns

## Pattern Map

| New / changed area | Existing analog | Reuse rule |
|---|---|---|
| `autoresearch run verl-case` | `autoresearch run smoke` in `autoresearch/cli.py` and `autoresearch/orchestrator/smoke.py` | Keep Click wrapper thin, call Python orchestration directly, print exactly one final JSON object. |
| 1-6 readiness server selection | `autoresearch/orchestrator/checks.py::run_check_all` | Reuse readiness steps and normalized `StepResult`; do not hard-code A2-AK-225 except as a user-provided override. |
| Formal remote Verl execution | `workspace-adapter/verl/minimal_runner.py` | Keep Verl-specific SSH/upload/run logic in `workspace-adapter/verl`; preserve smoke runner semantics. |
| Remote command env wrapping | `workspace-adapter/common/conda_utils.py` | Use `run_in_env` / workdir wrapping for non-container helper commands. Docker commands should still quote paths explicitly. |
| Local run artifact layout | `autoresearch/collect/cli.py`, `datalake/manifest/writer.py`, `workspace-core/layout/paths.py` | Durable state goes under `~/.autoresearch/runs/<run_id>/`; remote state is copied back or represented locally. |
| Manifest truth source | `datalake/manifest/schema.py`, `autoresearch/collect/manifest.py` | Extend the manifest with formal-case data rather than creating unrelated run metadata. |
| Report truth source | `autoresearch/report/loader.py`, `autoresearch/report/render.py` | Report reads local manifest/artifacts only; partial data becomes warnings, not hidden remote queries. |
| W&B and Prometheus | `datalake/wandb/sync.py`, `datalake/prometheus/push_gateway.py` | Keep local-first observability and expose links/metrics from local services. |
| Config defaults | `workspace-core/config/schema.py`, `config/config.example.yaml` | Add typed defaults without secrets; real `config/config.yaml` remains ignored. |
| Tests | `tests/test_collect_cli.py`, `tests/test_orchestrator_smoke.py`, `tests/test_report_loader.py` | Mock remote/Docker/HF/GitHub operations; reserve real A2-AK-225 UAT for verification. |

## Concrete Existing Contracts To Preserve

- `emit_progress(stage, **fields)` writes `__AR_PROGRESS__=<json>` to stderr.
- All CLI commands must print one final JSON object to stdout.
- `run_smoke` remains the minimal collect -> report path and must not become the formal case.
- `RunManifest` remains the report reconstruction entrypoint.
- Configuration secrets must not be added to `config/config.example.yaml`.
- Existing tests use `CliRunner` and monkeypatch Python functions, not real SSH.

## Suggested New Modules

- `workspace-adapter/verl/case_config.py` — typed case config, matrix rows, immutable snapshot writer.
- `workspace-adapter/verl/docker.py` — Docker pull/run command builders for Ascend device/driver/proxy/mounts.
- `workspace-adapter/verl/data_prep.py` — cache metadata and geometry3k JSONL preparation boundary.
- `workspace-adapter/verl/provenance.py` — Git repository provenance capture and optional fork/commit/push hooks.
- `workspace-adapter/verl/case_runner.py` — remote bundle upload, container execution, result parsing.
- `autoresearch/orchestrator/verl_case.py` — top-level readiness -> run -> collect/report orchestration.
- `autoresearch/report/verl_case.py` — formal-case matrix/evaluation view helpers if keeping renderer small.

## Plan Split Rationale

- Plan 14-01 creates deterministic local contracts and config defaults.
- Plan 14-02 builds the remote Verl case runner and Docker/data/provenance helpers.
- Plan 14-03 wires orchestration, CLI, and local artifact persistence.
- Plan 14-04 extends report/evaluation and performs strict verification/UAT scaffolding.

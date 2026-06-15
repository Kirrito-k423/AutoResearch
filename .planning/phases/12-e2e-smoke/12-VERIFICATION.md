---
phase: 12-e2e-smoke
status: verified
verified_at: "2026-06-15"
---

# Phase 12 Verification

## Automated Tests

```bash
uv run pytest tests/test_e2e_smoke.py tests/test_report_loader.py tests/test_cli.py -q
```

Result: `14 passed`

```bash
uv run pytest -q
```

Result: `361 passed, 6 warnings`

## CLI Checks

```bash
uv run autoresearch e2e smoke --help
```

Result: help output includes `--server`, `--max-duration`, and `--archon-url`.

## Real E2E UAT

```bash
uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891
```

Result:

- `ok=true`
- `run_id=01KV62JVH0N3ZRVRMH4PYWF1VB`
- `report=/Users/Zhuanz/.autoresearch/runs/01KV62JVH0N3ZRVRMH4PYWF1VB/report.html`
- `elapsed_seconds=146.673`
- `failed_step=null`

## Requirement Mapping

- E2E-01: full M1 local CLI loop passed through readiness, collect, and report.
- E2E-02: report completeness verified html + log + wandb + Prometheus.
- E2E-03: final run completed in 146.673 seconds, under 30 minutes.
- E2E-04: Archon health endpoint was reachable and the main workflow asset existed.


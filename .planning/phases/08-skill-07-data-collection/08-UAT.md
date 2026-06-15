---
status: complete
phase: 08-skill-07-data-collection
source: 08-01-SUMMARY.md, 08-02-SUMMARY.md, 08-03-SUMMARY.md, 08-04-SUMMARY.md
started: 2026-06-15T10:28:47Z
updated: 2026-06-15T12:44:35Z
---

## Current Test

[phase complete - real collect UAT passed on A2-AK-225]

## Tests

### 1. Minimal Runner With Remote Log Path
expected: `collect_minimal(..., run_id=...)` passes run_id to the selected runner, runner writes `<workdir>/runs/<run_id>.log`, and returns `remote_log_path`.
result: pass
evidence: `uv run pytest tests/test_minimal_runner.py tests/test_collect_minimal.py -q`

### 2. Local Log Collection
expected: `collect_log()` pulls the remote run log into `~/.autoresearch/runs/<run-id>/log.txt` and reports readable errors for missing/permission failures.
result: pass
evidence: `uv run pytest tests/test_datalake_logs_collector.py -q`

### 3. Manifest And Collect CLI
expected: `autoresearch collect run` orchestrates minimal, wandb sync, log collect, prom push, manifest write, and prints exactly one JSON object.
result: pass
evidence:
- `uv run pytest tests/test_collect_cli.py tests/test_collect_manifest.py tests/test_datalake_manifest.py -q`
- `uv run autoresearch collect run --server A2-AK-225 --lib verl --config config/config.yaml --timeout 60 --pushgateway-url http://127.0.0.1:17891`
- stdout JSON: `ok=true`, `run_id=01KV5MV7N5A3RBZ6388E5HCYAP`, `manifest=/Users/Zhuanz/.autoresearch/runs/01KV5MV7N5A3RBZ6388E5HCYAP/manifest.json`, `prom_pushed=true`, `errors=[]`

### 4. Local wandb Sync Visible In UI
expected: A real run can sync into local wandb and be visible through the local wandb service.
result: pass
evidence:
- `docker logs ar-wandb --tail 160` ends with `*** All services started`
- `curl -sS -D - http://localhost:8080/ready` -> `HTTP/1.1 200 OK`
- local 8080 UI completed first-run account creation (`autoresearch-local`) and API key generation
- `.venv/bin/wandb login --relogin --host=http://localhost:8080 ...` succeeded
- `.venv/bin/wandb sync ~/.autoresearch/runs/difdkkcx/wandb` -> `Syncing: http://localhost:8080/autoresearch-local/uncategorized/runs/difdkkcx ... done.`
- `docker exec ar-wandb ... select name, project_id, user_id, display_name, state, created_at from runs order by created_at desc limit 10;`
  shows both `difdkkcx` and the real collect run `dzeibhga`, state=`finished`

### 5. Prometheus Pushgateway Visible Metric
expected: A real run pushes `autoresearch_npu_count` through pushgateway and local Prometheus can query it.
result: pass
evidence:
- temporary reverse tunnel opened: remote `17891 -> localhost:9091`
- remote probe: `_build_pushgateway_curl('A2-AK-225')` returned `exit_code=0`
- real collect run manifest records `prom_pushed: true`
- `curl 'http://localhost:9090/api/v1/query?query=autoresearch_npu_count{run_id="01KV5MV7N5A3RBZ6388E5HCYAP"}'`
  returned value `8`

## Summary

total: 5
passed: 5
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

- none

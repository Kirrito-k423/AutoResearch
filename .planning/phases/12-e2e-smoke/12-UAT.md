---
phase: 12-e2e-smoke
status: passed
completed_at: "2026-06-15"
server: A2-AK-225
lib: verl
---

# Phase 12 UAT: E2E Smoke

## Command

```bash
uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891
```

## Result

- Overall: `ok=true`
- Run id: `01KV62JVH0N3ZRVRMH4PYWF1VB`
- Report: `/Users/Zhuanz/.autoresearch/runs/01KV62JVH0N3ZRVRMH4PYWF1VB/report.html`
- Elapsed: `146.673` seconds
- Summary: 5 passed, 0 warned, 0 failed, 0 skipped

## Step Results

| Step | Status | Evidence |
|---|---:|---|
| readiness | pass | `check all` passed with 6 pass, 2 warn, 0 fail |
| smoke | pass | collect + report passed, `prometheus_ready=true` |
| report | pass | html/log/wandb/prometheus checks all passed |
| archon | pass | `http://localhost:8088/healthz` status 200 and workflow file exists |
| duration | pass | 146.673 seconds < 1800 seconds |

## Notes

- An earlier E2E attempt failed at readiness because the remote GitHub probe returned `curl exit code 35` through the reverse proxy.
- Immediate follow-up probes on remote proxy ports `17893` and default `17892` passed, so the failure was treated as transient remote network/TLS instability.
- Final UAT used the default E2E remote proxy port `17892`.
- Expected warnings remain: BMC Redfish identify is non-blocking, and remote HuggingFace/GitHub require proxy fallback.


---
phase: 05-skill-04-network-check
plan: 03
status: blocked
subsystem: network-check
tags: [tunnel-heartbeat, retry, proxy, ssh-r, real-server-uat]

requires:
  - phase: 05-02
    provides: [local tunnel state, ssh-r lifecycle, remote proxy retry rows]
provides:
  - Remote proxy curl heartbeat on top of local ssh process checks
  - Bounded tunnel rebuild retry with 1s/2s/4s backoff
  - `autoresearch net tunnel ensure` CLI for downstream Phase 6 reuse
  - Full automated network/tunnel regression coverage and real-server UAT evidence
affects: [phase-05-network-check, phase-06-service-reachability]

tech-stack:
  added: []
  patterns:
    - Heartbeat checks both local tunnel pid and remote proxy curl reachability
    - Retry loops are capped and sleeper-injectable for deterministic tests
    - Real UAT evidence is summarized with server aliases and sanitized categories only

key-files:
  created: []
  modified:
    - autoresearch/net/tunnel.py
    - autoresearch/net/probe.py
    - autoresearch/cli.py
    - tests/test_net_tunnel.py
    - tests/test_net_probe.py
    - tests/test_net_cli.py

key-decisions:
  - "`net tunnel ensure` is exposed now because Phase 6 needs a reusable tunnel readiness boundary."
  - "`net tunnel status/stop` CLI commands were not added in this plan; existing state/delete helpers are enough for tests, and manual lifecycle UX should be designed with the later operations flow."
  - "Phase 5 remains blocked until every configured server passes real `net probe` plus tunnel proxy retry UAT."

patterns-established:
  - "Do not treat a live ssh pid as enough; remote proxy curl must also pass heartbeat."
  - "All real-server UAT records must omit host, IP, user, identity file, bootstrap secret, and proxy credentials."

requirements-completed: []

duration: 28min
completed: 2026-06-09
---

# Phase 05 Plan 03: 隧道心跳、重试与真机闸门 Summary

**隧道心跳和有界重试已实现并由测试覆盖，但三台配置服务器未通过真实网络 UAT，因此 Phase 5 继续阻塞。**

## Performance

- **Duration:** 28 min
- **Started:** 2026-06-09T12:58:00Z
- **Completed:** 2026-06-09T13:26:00Z
- **Tasks:** 3 implementation/UAT tasks; code committed, real-server acceptance not satisfied
- **Files modified:** 6

## Accomplishments

- Added `heartbeat_tunnel()` to check both local ssh pid liveness and a remote curl through the loopback proxy port.
- Extended `ensure_tunnel()` with capped rebuild retry, backoff `[1, 2, 4]`, progress stages, and `last_heartbeat_ok` state updates.
- Added `run_tunnel_ensure()` and `autoresearch net tunnel ensure --server ... --remote-proxy-port ...`.
- Wired `net probe --remote-proxy-port` through the remote proxy retry path.
- Completed targeted and full automated regression suites.
- Ran local-only, per-server, tunnel ensure, and default all-server real UAT attempts.

## Task Commits

1. **Task 05-03-01/02/03: tunnel heartbeat, ensure CLI, and regression coverage** - `9793bb7`

## Files Created/Modified

- `autoresearch/net/tunnel.py` - Adds remote proxy heartbeat, capped retry, progress events, and `run_tunnel_ensure`.
- `autoresearch/net/probe.py` - Keeps `--remote-proxy-port` connected to the proxy retry path.
- `autoresearch/cli.py` - Adds `autoresearch net tunnel ensure`.
- `tests/test_net_tunnel.py` - Covers heartbeat, rebuild retry, backoff, redaction, and ensure result JSON.
- `tests/test_net_probe.py` - Covers remote proxy port forwarding and proxy retry behavior.
- `tests/test_net_cli.py` - Covers CLI help/options, single JSON stdout, exit codes, and credential redaction.

## Decisions Made

- Heartbeat target defaults to the configured baidu URL, then falls back to the first configured HTTP(S) target if needed.
- `ensure_tunnel()` keeps retry count finite and test-injectable; no background infinite loop is introduced in Phase 5.
- Real UAT uses server aliases only. Host/IP/user/key material and full raw JSON are intentionally excluded from this summary.

## Deviations from Plan

None - plan implementation scope was followed. The only non-closure is the planned real-server gate, which did not satisfy acceptance.

## Real-Server UAT

| Scope | Exit code | Rows | Severity | Failed targets | Sanitized category |
|---|---:|---:|---|---|---|
| local-only | 0 | 3 | ok | none | none |
| tunnel ensure A2-AK-225 | 0 | n/a | ok | none | none |
| A2-AK-225 | 0 | 6 | warn | none | none |
| A3-AK-182 | 0 | 6 | warn | none | none |
| A3-AX-153 | 1 | 6 | fail | baidu, huggingface, github | ssh_host_key_mismatch |
| A3-AX-176 | 1 | 6 | fail | baidu, huggingface, github | ssh_auth |
| A2-AK-176 | 1 | 6 | fail | baidu, huggingface | proxy_unavailable_auth |
| default all-server matrix | 1 | 18 | fail | A3-AX-153: baidu/huggingface/github; A3-AX-176: baidu/huggingface/github; A2-AK-176: baidu/huggingface | aggregate_real_uat_not_satisfied |

Default all-server aggregate: `ok=false`, severity `fail`, total 18, passed 5, warned 5, failed 8, proxy_used 5, proxy_failed 2. Result ordering stayed stable by config server order.

## Issues Encountered

- A3-AX-153 requires host key reconciliation before SSH-based network checks can be trusted.
- A3-AX-176 requires SSH authentication repair.
- A2-AK-176 can run a partial remote direct check, but its proxy retry path cannot authenticate/start the tunnel successfully.
- Because the final gate requires all configured servers, Plan 05-03 and Phase 5 remain blocked even though code and automated tests are complete.

## User Setup Required

Repair the three real-server blockers above, then rerun:

1. `uv run autoresearch net tunnel ensure --server A2-AK-225 --remote-proxy-port 17890`
2. `uv run autoresearch net probe --server A3-AX-153`
3. `uv run autoresearch net probe --server A3-AX-176`
4. `uv run autoresearch net probe --server A2-AK-176`
5. `uv run autoresearch net probe`

Expected closure condition: all per-server commands return exit 0 or WARN-only, and the default matrix returns `ok=true` or WARN-only with no failed server rows.

## Next Phase Readiness

- Phase 6 can reuse `autoresearch net tunnel ensure` for tunnel readiness on servers whose SSH/proxy path is healthy.
- Phase 5 cannot be closed until A3-AX-153, A3-AX-176, and A2-AK-176 pass the real network/tunnel UAT gate.

## Verification

- `uv run pytest -q tests/test_net_curl.py tests/test_net_probe.py tests/test_net_tunnel.py tests/test_net_cli.py` - PASS: 37 passed
- `uv run pytest` - PASS: 190 passed, 6 warnings
- `git diff --check` - PASS
- `uv run autoresearch net probe --local-only` - PASS: exit 0, severity ok, 3 rows
- `uv run autoresearch net tunnel ensure --server A2-AK-225 --remote-proxy-port 17890` - PASS: exit 0, heartbeat ok
- Per-server real UAT matrix - OBSERVED: 2 servers acceptable with WARN rows, 3 servers need external repair
- Default all-server matrix - OBSERVED: exit 1, 18 rows, aggregate not ready for closure

## Self-Check

- **PASS:** `autoresearch/net/tunnel.py` contains `heartbeat_tunnel`, `ensure_tunnel`, and `run_tunnel_ensure`.
- **PASS:** `autoresearch/cli.py` exposes `net tunnel ensure` and `--remote-proxy-port`.
- **PASS:** Automated tests cover heartbeat, retry, JSON stdout, redaction, and proxy retry paths.
- **PASS:** Real UAT evidence is summarized without host/IP/user/secret material.
- **NOT READY:** The all-server real UAT gate still needs external SSH/proxy repair.

---
*Phase: 05-skill-04-network-check*
*Status recorded: 2026-06-09*

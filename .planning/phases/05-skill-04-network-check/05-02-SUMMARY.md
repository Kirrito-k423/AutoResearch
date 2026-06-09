---
phase: 05-skill-04-network-check
plan: 02
status: complete_with_real_uat_issue
subsystem: network-check
tags: [ssh-r, reverse-tunnel, proxy-retry, redaction, tunnel-state]

requires:
  - phase: 05-01
    provides: [network rows, curl parser, remote direct probe, net probe CLI]
provides:
  - Local tunnel state JSON under the AutoResearch tunnels directory
  - Sanitized proxy URL handling for JSON/state/error paths
  - `ensure_tunnel` reuse/rebuild lifecycle on top of `open_reverse_tunnel`
  - Remote proxy retry attempts preserved in network rows
affects: [phase-05-network-check, phase-06-service-reachability]

tech-stack:
  added: []
  patterns:
    - Tunnel state stores local process metadata only and redacts proxy userinfo
    - Remote proxy retry uses `ALL_PROXY` and `HTTPS_PROXY` command prefixes
    - Summary counters expose `proxy_used` and `proxy_failed`

key-files:
  created:
    - autoresearch/net/tunnel.py
    - tests/test_net_tunnel.py
  modified:
    - autoresearch/net/models.py
    - autoresearch/net/probe.py
    - autoresearch/cli.py
    - workspace-core/layout/paths.py
    - workspace-core/layout/__init__.py
    - tests/test_net_probe.py
    - tests/test_net_cli.py
    - tests/workspace-core/test_layout.py

key-decisions:
  - "Tunnel state is local-only and stores redacted proxy URLs, not SSH identity or bootstrap secrets."
  - "Remote direct timeout now triggers ensure_tunnel once per server scope and preserves both direct/proxy attempts."
  - "Real A2 ssh -R currently exits immediately, so NET-TUNNEL-01 remains for the final Phase 5 UAT gate."

patterns-established:
  - "Proxy errors are sanitized with both exact URL replacement and generic http(s) userinfo redaction."
  - "A proxy retry that succeeds becomes a WARN row; a proxy path that cannot start becomes `proxy_unavailable`."

requirements-completed:
  - NET-REMOTE-01
  - NET-REMOTE-02
  - NET-REMOTE-03

duration: 20min
completed: 2026-06-09
---

# Phase 05 Plan 02: Remote Proxy Retry Summary

**Reusable local tunnel state and remote proxy retry are wired into the network matrix, with automatic redaction and explicit `proxy_unavailable` rows for real tunnel startup issues.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-09T12:57:00Z
- **Completed:** 2026-06-09T13:17:00Z
- **Tasks:** 3 implementation tasks delivered in 2 cohesive commits
- **Files modified:** 10

## Accomplishments

- Added `workspace_core.layout.TUNNELS_DIR` and included it in `ensure_root()`.
- Added `autoresearch.net.tunnel` with `TunnelState`, state path sanitization, redacted JSON writes, state load/delete, process liveness, and `ensure_tunnel`.
- Implemented `ensure_tunnel` reuse/rebuild behavior on top of `workspace_core.ssh.open_reverse_tunnel`, including local proxy URL validation and sanitized startup errors.
- Added remote proxy retry to the network matrix: direct attempt first, `ensure_tunnel` on timeout, then remote `ALL_PROXY`/`HTTPS_PROXY` curl retry in the same row.
- Added `--remote-proxy-port` to `net probe` and summary counters for `proxy_used` / `proxy_failed`.

## Task Commits

1. **Task 05-02-01/02: tunnel state + ensure lifecycle** - `67c5ab5`
2. **Task 05-02-03: remote proxy retry wiring** - `b94ebff`

## Files Created/Modified

- `autoresearch/net/tunnel.py` - Tunnel state, redaction, config lookup, local pid heartbeat, and ensure/rebuild.
- `autoresearch/net/models.py` - Adds `TunnelState`, `proxy_used`, and `proxy_failed` summary fields.
- `autoresearch/net/probe.py` - Adds `probe_remote_with_proxy_fallback`, proxy error redaction, env-prefixed remote curl, and proxy counters.
- `autoresearch/cli.py` - Adds `--remote-proxy-port` to `net probe`.
- `workspace-core/layout/paths.py` - Adds `TUNNELS_DIR`.
- `workspace-core/layout/__init__.py` - Exports `TUNNELS_DIR`.
- `tests/test_net_tunnel.py` - State, redaction, ensure, reuse, rebuild, config, and bounded-error tests.
- `tests/test_net_probe.py` - Remote proxy retry, direct-success no-ensure, and proxy-unavailable row tests.
- `tests/test_net_cli.py` - CLI help coverage for `--remote-proxy-port`.
- `tests/workspace-core/test_layout.py` - `ensure_root()` creates tunnels directory.

## Decisions Made

- `net probe` now uses proxy retry for remote probes by default; `probe_remote_direct` remains available as a pure direct helper.
- A proxy retry success stays WARN because direct connectivity still needed proxy assistance.
- `NET-TUNNEL-01` is not marked complete here because the real A2 tunnel startup did not stay alive; 05-03 owns heartbeat/retry and the final all-server gate.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Generic proxy credential redaction for ensure errors**
- **Found during:** Task 05-02-03 security review
- **Issue:** A non-`TunnelError` exception from ensure could include a credentialed proxy URL not equal to the current CLI proxy URL.
- **Fix:** Added generic http(s) userinfo redaction for proxy errors before they enter row attempts.
- **Files modified:** `autoresearch/net/probe.py`, `tests/test_net_probe.py`
- **Verification:** Proxy-unavailable test asserts `u:p` never appears in row error.
- **Committed in:** `b94ebff`

**Total deviations:** 1 auto-fixed Rule 2 issue.
**Impact on plan:** Security boundary tightened; no feature scope expansion.

## Issues Encountered

- `workspace_core` is force-included into the installed package; after adding `TUNNELS_DIR`, local tests needed `uv pip install -e .` so the `.venv` import copy reflected the workspace-core change.
- Real A2 proxy retry reached `ensure_tunnel`, but the `ssh -R` process exited immediately with rc 0. The log tail contained only the remote authorization banner, so the row correctly reported `proxy_unavailable`.

## Real-World UAT

- `uv run autoresearch net probe --server A2-AK-225 --remote-proxy-port 17890` - **exit 1**:
  - local baidu/github direct OK
  - local huggingface direct timeout then local proxy OK
  - remote baidu/github direct OK
  - remote huggingface direct timeout then proxy path could not stay open
  - output preserved direct and proxy attempts in the same remote row

## Verification

- `uv run pytest -q tests/test_net_tunnel.py tests/test_net_probe.py` - **PASS: 17 passed**
- `uv run pytest -q tests/test_net_curl.py tests/test_net_probe.py tests/test_net_cli.py tests/test_net_tunnel.py` - **PASS: 28 passed**
- `uv run pytest` - **PASS: 181 passed, 6 warnings**
- `uv run autoresearch net probe --help` - **PASS: `--remote-proxy-port` shown**
- `uv run autoresearch net probe --server A2-AK-225 --remote-proxy-port 17890` - **OBSERVED: exit 1 with explicit proxy_unavailable row**

## User Setup Required

None for code use. For the final real-server gate, verify remote SSH permits reverse forwarding and that the local proxy at `127.0.0.1:7890` is reachable before re-running all configured servers.

## Next Phase Readiness

05-03 can build on `ensure_tunnel` to add remote proxy curl heartbeat, bounded retry/backoff, and `net tunnel ensure`. The current A2 `ssh -R` immediate-exit evidence is the main real UAT case for the next plan.

## Self-Check: PASSED

- **PASS:** `autoresearch/net/tunnel.py` contains `ensure_tunnel`, `load_tunnel_state`, and redaction helpers.
- **PASS:** `workspace-core/layout/paths.py` exposes `TUNNELS_DIR`.
- **PASS:** Remote proxy retry rows preserve direct and proxy attempts.
- **PASS:** Proxy URL credentials are absent from state JSON and proxy error rows.
- **PASS:** 05-02 automated tests and full regression suite pass.

---
*Phase: 05-skill-04-network-check*
*Completed: 2026-06-09*

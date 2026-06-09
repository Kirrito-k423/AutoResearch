---
phase: 05-skill-04-network-check
plan: 01
status: complete
subsystem: network-check
tags: [curl, network-matrix, ssh, cli, proxy-fallback]

requires:
  - phase: 03-skill-01-customer-config
    provides: [config loader, network targets, server list]
  - phase: 04-skill-03-server-hardware-probe
    provides: [SSH resolution pattern, bounded remote worker pattern]
provides:
  - Pure curl command builder and delimiter-safe write-out parser
  - Local direct-first network probe with hf/github local proxy fallback
  - Remote direct curl probe through workspace_core SSH
  - JSON-only `autoresearch net probe` CLI entrypoint
affects: [phase-05-network-check, phase-06-service-reachability, experiment-report]

tech-stack:
  added: []
  patterns:
    - Curl parser stays pure and imports no SSH, Click, or config loader
    - Remote commands are built from validated HTTP(S) targets and shell-quoted argv
    - Remote probe fan-out is bounded to three workers and reordered by config

key-files:
  created:
    - autoresearch/net/__init__.py
    - autoresearch/net/models.py
    - autoresearch/net/curl.py
    - autoresearch/net/probe.py
    - tests/test_net_curl.py
    - tests/test_net_probe.py
    - tests/test_net_cli.py
  modified:
    - autoresearch/cli.py

key-decisions:
  - "Network results use flat rows plus grouped summary; WARN rows still allow exit 0."
  - "HuggingFace/GitHub local direct failures retry through the configured local proxy and keep both attempts."
  - "Remote direct failures remain hard failures in 05-01; remote ssh -R proxy fallback is intentionally left to 05-02."

patterns-established:
  - "Network CLI boundaries print one final CheckResult JSON object and send progress only to stderr."
  - "Configured network targets must pass HTTP(S), host, control-character, whitespace, and semicolon validation before execution."
  - "One failed remote worker becomes failed rows for that server without cancelling other servers."

requirements-completed:
  - NET-LOCAL-01
  - NET-LOCAL-02
  - NET-LOCAL-03
  - NET-REMOTE-01
  - NET-REMOTE-02
  - NET-REMOTE-03

duration: 14min
completed: 2026-06-09
---

# Phase 05 Plan 01: Direct Network Matrix Summary

**Curl-backed local and remote direct network matrix with JSON-only CLI output, local proxy fallback for blocked HF/GitHub, and ordered remote SSH fan-out.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-06-09T12:41:00Z
- **Completed:** 2026-06-09T12:55:36Z
- **Tasks:** 3 implementation tasks committed
- **Files modified:** 8

## Accomplishments

- Added `autoresearch.net` models for `CurlAttempt`, `NetworkRow`, grouped summaries, and JSON payload data.
- Implemented `curl --max-time 10 -L -o /dev/null -s -w ...` argv construction and delimiter-safe parser for `http_code`, `time_total`, and `speed_download`.
- Implemented local direct-first probing; HuggingFace/GitHub direct failures can retry via `http://127.0.0.1:7890` and stay WARN when proxy succeeds.
- Implemented remote direct probing through `workspace_core.ssh.SSHClient`, with safe shell quoting and finally-close semantics.
- Added `autoresearch net probe` with `--server`, `--local-only`, `--config`, `--local-proxy-url`, and `--lang`.

## Task Commits

1. **Task 05-01-01: 建立网络 row/result 模型和 curl parser** - `95a7906`
2. **Task 05-01-02: 实现本机和远程 direct 网络探测矩阵** - `dc0bee3`
3. **Task 05-01-03: 挂载 `autoresearch net probe` JSON CLI** - `6ca5bb4`

## Files Created/Modified

- `autoresearch/net/models.py` - Serializable attempt, row, summary, and payload contracts.
- `autoresearch/net/curl.py` - URL validation, curl argv builder, and write-out parser.
- `autoresearch/net/probe.py` - Local probes, remote direct probes, all-server fan-out, summary construction, and CLI boundary.
- `autoresearch/net/__init__.py` - Package exports.
- `autoresearch/cli.py` - Adds `net probe`.
- `tests/test_net_curl.py` - URL rejection, argv, parser, timeout, and malformed output coverage.
- `tests/test_net_probe.py` - Local proxy fallback, safe remote quoting, bounded concurrency, worker isolation, and summary coverage.
- `tests/test_net_cli.py` - Help flags, JSON-only stdout, progress stderr, exit code, and sensitive-key regression coverage.

## Decisions Made

- Kept local proxy success as `status="warn"` rather than `ok`, because direct path failed and the row needed fallback.
- Left remote direct failure as a hard failure in 05-01; 05-02 owns `ssh -R` fallback and proxy retry semantics.
- Reused Phase 4's exact server lookup pattern instead of importing private hardware helpers.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed.
**Impact on plan:** No scope creep.

## Issues Encountered

- While writing CLI tests, the fake config object initially lacked `network.targets`; the test fixture was fixed before the CLI task commit.
- Real A2-AK-225 remote direct probe reached SSH and curl, but `https://huggingface.co` timed out from the remote host. This is expected input for 05-02 remote proxy fallback, not a 05-01 implementation defect.

## Real-World UAT

- `uv run autoresearch net probe --local-only` - **PASS/WARN, exit 0**:
  - baidu direct OK
  - huggingface direct failed, local proxy OK
  - github direct OK
- `uv run autoresearch net probe --server A2-AK-225` - **EXPECTED exit 1 for remote direct timeout**:
  - local rows same as above
  - remote baidu direct OK
  - remote github direct OK
  - remote huggingface direct timeout (`curl exit code 28`, `http_code=0`)

## Verification

- `uv run pytest -q tests/test_net_curl.py tests/test_net_probe.py tests/test_net_cli.py` - **PASS: 16 passed**
- `uv run pytest` - **PASS: 168 passed, 6 warnings**
- `uv run autoresearch net probe --help` - **PASS: expected flags shown**
- `uv run autoresearch net probe --local-only` - **PASS/WARN: exit 0, one JSON result with proxy retry**
- `uv run autoresearch net probe --server A2-AK-225` - **PASS as 05-01 evidence / exit 1 as network state: remote direct huggingface timeout**

## User Setup Required

None - no new external service configuration required for 05-01.

## Next Phase Readiness

05-02 can attach the remote proxy path to the existing direct-timeout path. The A2-AK-225 HuggingFace timeout is a concrete UAT case for verifying `ssh -R` proxy retry and per-row direct/proxy attempt preservation.

## Self-Check: PASSED

- **PASS:** All key files from the plan exist.
- **PASS:** `autoresearch/net/curl.py` contains `build_curl_command` and `parse_curl_result`.
- **PASS:** `autoresearch/net/probe.py` contains `probe_local`, `probe_remote_direct`, `probe_all_remotes`, and `run_probe`.
- **PASS:** `autoresearch/cli.py` contains `def net_probe`.
- **PASS:** 05-01 automated tests and full regression suite pass.
- **PASS:** Real local-only UAT exits 0 with WARN-only proxy retry.

---
*Phase: 05-skill-04-network-check*
*Completed: 2026-06-09*

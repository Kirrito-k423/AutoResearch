---
status: partial
phase: 04-skill-03-server-hardware-probe
source:
  - 04-01-SUMMARY.md
  - 04-02-SUMMARY.md
  - 04-03-SUMMARY.md
started: 2026-06-09T08:11:58Z
updated: 2026-06-09T08:12:48Z
---

## Current Test

[testing paused - 3 external items outstanding]

## Tests

### 1. CLI discovery and argument handling
expected: `autoresearch hw probe --help` exposes `--server`, `--all`, and `--config`; conflicting `--server` and `--all` returns exit 2 with one structured JSON result.
result: pass
evidence: Automated on 2026-06-09; help exit 0, conflict exit 2, stdout parsed as one CheckResult JSON.

### 2. Core metric parsing across supported Ascend formats
expected: Supported `npu-smi` 24.1, 25.3, and 25.5 outputs produce integer memory total, memory used, temperature, and utilization for every parsed device.
result: pass
evidence: Full pytest suite passed 152 tests; fixtures cover standard, compound-column, and dual-chip formats.

### 3. Process occupancy and privacy boundary
expected: Occupancy records contain numeric NPU/chip/PID/memory fields; user and executable basename are enriched when available, without exposing full command lines.
result: pass
evidence: Automated parser/probe/CLI tests passed; real A2-AK-225 returned 2 process records and A3-AK-182 returned 6.

### 4. Driver, fallback, timeout, and failure isolation
expected: Driver versions are reported when available; unknown `npu-smi` falls back to `lspci` without false success; command timeout closes its SSH channel; one server failure does not cancel others.
result: pass
evidence: Full pytest suite passed; aggregate probe emitted 28 progress events and returned all 5 server results in config order.

### 5. Real probe: A2-AK-225
expected: The server connects and returns all installed devices with complete core metrics and driver versions.
result: pass
evidence: Real aggregate probe passed with 8 devices, 8 complete core records, 2 process records, and complete driver metadata.

### 6. Real probe: A3-AK-182
expected: The server connects and returns all physical chips with complete core metrics, process occupancy, and driver versions.
result: pass
evidence: Real aggregate probe passed with 16 devices, 16 complete core records, 6 process records, and complete driver metadata.

### 7. Real probe: A3-AX-153
expected: The server host identity is verified through a trusted channel, then the stored SSH host key is updated and the hardware probe completes.
result: blocked
blocked_by: third-party
reason: The current ED25519 host key differs from known_hosts. Automatic replacement is intentionally prohibited until the new fingerprint is independently verified.

### 8. Real probe: A3-AX-176
expected: The configured SSH credential authenticates successfully and the hardware probe completes.
result: blocked
blocked_by: third-party
reason: The resolved configured bootstrap password is rejected by the remote SSH service and must be updated outside chat.

### 9. Real probe: A2-AK-176
expected: `npu-smi` is available to the configured user, or an approved read-only sudo path provides it, so all 8 detected devices return core metrics and driver versions.
result: blocked
blocked_by: third-party
reason: SSH succeeds and lspci detects 8 Ascend accelerators, but `npu-smi` and Ascend driver metadata are unavailable to the unprivileged user; sudo requires explicit approval.

## Summary

total: 9
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 3

## Gaps

[none - outstanding items are external security, credential, and privilege gates]

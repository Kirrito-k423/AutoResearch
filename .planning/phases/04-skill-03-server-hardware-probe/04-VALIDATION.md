---
phase: 04
slug: skill-03-server-hardware-probe
status: approved
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-09
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x + Click `CliRunner` |
| **Config file** | `pyproject.toml` (`[tool.pytest.ini_options]`) |
| **Quick run command** | `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py tests/test_hw_cli.py` |
| **Full suite command** | `uv run pytest` |
| **Estimated runtime** | quick ~5s; full ~15s without real SSH |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest -q` against the hardware test file(s) touched by that task.
- **After every plan wave:** Run `uv run pytest`.
- **Before `$gsd-verify-work`:** Full suite and all configured real-server UAT must be green.
- **Max automated feedback latency:** 20 seconds, excluding real SSH timeouts.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | HW-NPU-01, HW-NPU-02 | T-04-01-02 | Parser consumes text only; no command execution | unit | `uv run pytest -q tests/test_hw_parser.py -k 'baseline or missing'` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | HW-CONN-01, HW-CONN-02 | T-04-01-01 | Fixed read-only commands; configured host lookup | unit/integration | `uv run pytest -q tests/test_hw_probe.py -k 'single or timeout'` | ❌ W0 | ⬜ pending |
| 04-01-03 | 01 | 1 | HW-CONN-01, HW-NPU-01, HW-NPU-02 | T-04-01-03 | stdout contains one JSON object; no secret fields | CLI/UAT | `uv run pytest -q tests/test_hw_cli.py -k server` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 2 | HW-NPU-01, HW-NPU-02 | T-04-02-01 | Unsupported query types fail closed and preserve diagnostics | unit | `uv run pytest -q tests/test_hw_parser.py -k 'variant or typed or unknown'` | ❌ W0 | ⬜ pending |
| 04-02-02 | 02 | 2 | HW-DRV-01 | T-04-02-02 | Driver reads are fixed paths and non-destructive | unit | `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py -k driver` | ❌ W0 | ⬜ pending |
| 04-02-03 | 02 | 2 | HW-NPU-03 | T-04-02-03 | Logs stay local; JSON summary is bounded; lspci cannot produce false success | unit/integration | `uv run pytest -q tests/test_hw_probe.py -k 'fallback or raw_log or lspci'` | ❌ W0 | ⬜ pending |
| 04-03-01 | 03 | 3 | HW-OCC-01, HW-OCC-02 | T-04-03-01 | Only numeric PIDs enter fixed `ps`; only `comm` is collected | unit/integration | `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py -k 'process or ps'` | ❌ W0 | ⬜ pending |
| 04-03-02 | 03 | 3 | HW-CONN-01, HW-NPU-01, HW-NPU-02 | T-04-03-02 | Workers isolate SSH clients and preserve every server result | CLI/integration | `uv run pytest -q tests/test_hw_probe.py tests/test_hw_cli.py -k all` | ❌ W0 | ⬜ pending |
| 04-03-03 | 03 | 3 | All HW requirements | T-04-03-03 | No fixture can satisfy the real-server completion gate | regression/UAT | `uv run pytest && uv run autoresearch hw probe --all` | test files W0; server availability external | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/fixtures/hw/npu_smi_25_3_rc1_no_processes.txt` — sanitized A2 baseline for HW-NPU-01/02.
- [ ] `tests/fixtures/hw/npu_smi_with_processes.txt` — process parsing for HW-OCC-01/02.
- [ ] `tests/fixtures/hw/npu_smi_missing_metric.txt` — null + field error behavior.
- [ ] `tests/fixtures/hw/npu_smi_unknown_format.txt` — unknown parser path.
- [ ] `tests/fixtures/hw/lspci_ascend.txt` — fallback classification for HW-NPU-03.
- [ ] `tests/test_hw_parser.py` — pure parser assertions.
- [ ] `tests/test_hw_probe.py` — fake SSH orchestration, failure logging, process enrichment and aggregation.
- [ ] `tests/test_hw_cli.py` — Click happy path, progress/stdout and exit code assertions.

No framework installation is needed; pytest and Click test support already exist.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each configured server returns real core metrics | HW-CONN-01, HW-NPU-01, HW-NPU-02 | CI/fixtures cannot prove current LAN/VPN, SSH credentials, driver output or installed hardware | For every name in `config/config.yaml`, run `uv run autoresearch hw probe --server NAME`; confirm non-empty devices and non-null integer memory/temp/util fields |
| Aggregate real-server completion gate | All HW requirements | Current five-server availability is external and was temporarily unavailable on 2026-06-09 | Run `uv run autoresearch hw probe --all`; require top-level `ok=true`, no failed servers, and every configured server present |
| Device count matches physical inventory | HW-NPU-01 | Fixture can validate parser but not current installed card count | Compare JSON device count with `npu-smi info` on each server; A2-AK-225 baseline is 8×910B2 |

These checks are batched at end-of-phase. A network timeout leaves Phase 4 unverified; it is not waived.

---

## Security Validation

- Remote command set is fixed and read-only.
- Server names are configuration keys, never shell fragments.
- PIDs are parsed as integers before building `ps -p`.
- Process enrichment uses `comm`, not full arguments or environment.
- Raw output logs are local under `~/.autoresearch/logs/`; success JSON omits raw output.
- Failure summaries are bounded and tests assert no credential fields are emitted.

---

## Validation Sign-Off

- [x] All tasks have automated verification or explicit Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 covers all currently missing fixtures and hardware tests.
- [x] No watch-mode flags.
- [x] Automated feedback latency target is under 20 seconds.
- [x] Real-server checks are explicitly manual/UAT and cannot be replaced by fixtures.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-09

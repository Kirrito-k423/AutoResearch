---
phase: 04
slug: skill-03-server-hardware-probe
mapped: 2026-06-09
---

# Phase 4 — Existing Pattern Map

## Data Flow

```text
Click hw probe
  -> config.from_path()
  -> server name -> HostSpec
  -> SSHClient.connect()/exec()
  -> pure parser functions
  -> CheckResult
  -> json.dumps(stdout once)
       + emit_progress(stderr)
       + raw failure log under LOGS_DIR
```

## File Classification

| New/modified file | Role | Closest existing analog | Pattern to preserve |
|---|---|---|
| `autoresearch/hw/models.py` | Hardware domain types | `autoresearch/services/_common.py::HealthResult`, `workspace-core/result/check.py::CheckResult` | TypedDict-style serializable records; lower-case severity strings |
| `autoresearch/hw/parser.py` | Pure vendor-output transforms | No direct vendor analog; follow pure business helpers in existing tests | No SSH/Click/filesystem imports; fixture-driven exact assertions |
| `autoresearch/hw/probe.py` | Config/SSH/parser orchestration | `autoresearch/ping.py`, `workspace-core/ssh/client.py` | config lookup → HostSpec → independent SSHClient → fixed commands → CheckResult |
| `autoresearch/cli.py` | `hw probe` Click wiring | existing ping/config commands in the same file | lazy import `run_*`; raise `click.exceptions.Exit` |
| `tests/test_hw_parser.py` | Parser unit tests | `tests/workspace-core/test_config.py` | direct business assertions and parametrized invalid inputs |
| `tests/test_hw_probe.py` | Orchestration tests | `tests/test_ping.py`, `tests/workspace-core/test_ssh_client.py` | fake/mocked command boundaries; assert cleanup and exact commands |
| `tests/test_hw_cli.py` | Click contract tests | `tests/test_ping.py` | parse `result.stdout` as JSON; inspect `result.stderr` for progress |
| `tests/fixtures/hw/*.txt` | Sanitized vendor samples | No existing fixture directory | stable text fixtures with no host/IP/user/secret data |

## New Files and Roles

### `autoresearch/hw/models.py`

- Owns hardware-domain TypedDict/dataclass contracts only.
- Must not import SSH, Click, filesystem or logging.
- Closest analog: `autoresearch/services/_common.py::HealthResult` and `workspace-core/result/check.py::CheckResult`.

### `autoresearch/hw/parser.py`

- Pure functions from text to models:
  - `parse_npu_smi_info`
  - `parse_driver_version_info`
  - `parse_lspci_devices`
  - `parse_ps_output`
- No filesystem access, no SSH, no progress events.
- Fixture tests call these functions directly.

### `autoresearch/hw/probe.py`

- Owns command constants, SSH lifecycle, parser orchestration, fallback, process enrichment, raw logging, single/all aggregation and exit mapping.
- Uses `workspace_core` public APIs only.
- Keeps remote commands fixed; only validated integer PIDs may be interpolated.

### `autoresearch/hw/__init__.py`

- Re-exports stable entry points such as `run_probe`, `probe_server` and parser/model symbols needed by tests.
- Follows existing package `__init__.py` export style.

### `tests/fixtures/hw/*.txt`

- Sanitized command outputs only.
- No real IP, username, home path, key path or secret.
- A fixture filename captures version/condition, not server identity.

### `tests/test_hw_parser.py`

- Pure parser tests and exact field assertions.
- Parametrize fixture variants where useful.

### `tests/test_hw_probe.py`

- Fake SSH client/command dispatcher.
- Tests fallback, partial data preservation, raw log behavior, `ps` race and all-server aggregation.

### `tests/test_hw_cli.py`

- `CliRunner` tests for options, stdout JSON, stderr progress and exit codes.

## Interfaces to Preserve

- `SSHClient.connect(connect_timeout=5.0, retries=3) -> None`
- `SSHClient.exec(command, timeout=30.0) -> tuple[int, str, str]`
- `CheckSeverity.OK/WARN/FAIL` serialize to `"ok"`, `"warn"`, `"fail"`
- `CheckResult` includes `message`; do not emit a four-field near-copy.
- Hardware `WARN` means core probe succeeded: construct `ok=true/severity=warn`; do not reuse current `fail(..., WARN)` or `merge()` behavior.
- `emit_progress(stage, level=..., **fields)` writes stderr.
- `from_path()` respects explicit path/env/default precedence.

## Source-Grounding Warnings

- Do not import private Paramiko symbols into `autoresearch/hw`.
- Do not use `workspace_core.result.merge()` for `--all`; it discards per-server data.
- Do not re-use `services.HealthResult`; hardware results have different semantics.
- Do not call `autoresearch.ping._resolve_server_host` across feature modules; extract or locally reproduce the small config-to-HostSpec helper using the same public APIs.
- Do not depend on exact spaces or column offsets in `npu-smi`.
- Do not collect `ps args` or `/proc/<pid>/cmdline`; only `comm`.
- Do not write remote state or fixture files to `/home/t00906153`; Phase 4 commands are read-only and local-first.

## Pattern Mapping Complete

The closest implementation path is a new `autoresearch.hw` package that composes the existing config/SSH/result/progress/log APIs and keeps all vendor-output parsing pure.

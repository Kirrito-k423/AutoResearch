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

## Closest Analogs

| New responsibility | Closest existing analog | Pattern to preserve |
|---|---|---|
| `hw probe` Click wiring | `autoresearch/cli.py` ping/config commands | command function imports `run_*` lazily and raises `click.exceptions.Exit` |
| Config server resolution | `autoresearch/ping.py::_resolve_server_host` | `from_path` → exact server name lookup → `resolve_host` → identity file override |
| SSH command execution | `workspace-core/ssh/client.py::SSHClient` | context manager, fixed 5s connect default, tuple result from `exec` |
| Final structured status | `workspace-core/result/check.py` | `CheckResult` with `ok/severity/data/message/error`, lower-case severity values |
| Progress | `workspace-core/progress/emitter.py` | `__AR_PROGRESS__=<json>` to stderr, never stdout |
| Failure logs | `workspace-core/log/logger.py` + `workspace-core/layout/paths.py` | local `LOGS_DIR`, UTF-8 file, parent mkdir |
| Bounded fan-out | `autoresearch/services/_common.py::check_all` | `ThreadPoolExecutor`, deterministic returned order |
| CLI assertions | `tests/test_ping.py` | parse `result.stdout` as JSON; inspect `result.stderr` for progress |

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

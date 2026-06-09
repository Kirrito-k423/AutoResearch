# Phase 5: network-check - Pattern Map

**Generated:** 2026-06-09
**Mode:** inline pattern mapper fallback (subagent spawning not used)

## New Files and Closest Analogs

| New file | Role | Closest analog | Pattern to reuse |
|---|---|---|---|
| `autoresearch/net/__init__.py` | Skill package exports | `autoresearch/hw/__init__.py` | Keep package thin; export run functions from submodules. |
| `autoresearch/net/models.py` | Typed result structures | `autoresearch/hw/models.py`, `workspace-core/result/check.py` | Use TypedDict/dataclass-style schema with `CheckResult` severity semantics. |
| `autoresearch/net/curl.py` | Pure curl command/output parsing | `autoresearch/hw/parser.py` | Keep parsing pure; no SSH, Click, or filesystem in parser module. |
| `autoresearch/net/probe.py` | Local/remote orchestration | `autoresearch/hw/probe.py`, `autoresearch/services/_common.py` | Use config loader, progress emitter, bounded worker pattern, per-target result preservation. |
| `autoresearch/net/tunnel.py` | Tunnel ensure/state/heartbeat | `workspace-core/ssh/tunnel.py`, `autoresearch/ping.py` | Build on `open_reverse_tunnel`; keep tunnel process local; expose reusable higher-level lifecycle. |
| `autoresearch/cli.py` | CLI registration | Existing `hw probe` group | Add `net` group with `probe` and `tunnel` subgroup; stdout JSON boundary in run functions. |
| `workspace-core/layout/paths.py` | Optional central tunnel directory | Existing LOGS/RUNS/SSH_KEYS dirs | Add `TUNNELS_DIR = ROOT_DIR / "tunnels"` if centralizing state path. |
| `tests/test_net_*.py` | CLI/probe/tunnel tests | `tests/test_hw_cli.py`, `tests/test_hw_probe.py`, `tests/workspace-core/test_tunnel.py` | Use CliRunner, fake SSH clients, mocked subprocess/Popen, no real network in unit tests. |

## Reusable Code Excerpts and Constraints

### CLI Boundary

- `autoresearch/cli.py` uses `@main.group()` for skill groups and `raise click.exceptions.Exit(run_*(...))`.
- `hw_probe` demonstrates `--server`, `--all`, `--config`, `--lang` options and a run-function boundary.

### Result and Exit Semantics

- `workspace-core/result/check.py` defines `CheckResult` with `ok`, `severity`, `data`, `message`, `error`.
- `autoresearch/hw/probe.py::run_probe` prints one JSON object exactly once and maps config errors to exit 2.
- Do not use `workspace_core.result.merge()` for the final network matrix if it loses per-target/per-server details.

### Config and Targets

- `workspace-core/config/schema.py::NetworkProbes.targets` already contains default `https://baidu.com`, `https://huggingface.co`, `https://github.com`.
- `workspace-core/config.loader.from_path()` is the source of truth for config path precedence.

### SSH and Remote Commands

- Remote commands must go through `workspace_core.ssh.client.SSHClient`.
- Hardware code shows the right pattern: exact config server lookup, `HostSpec` construction, `connect(connect_timeout=5.0)`, fixed commands, finally close.
- Network target URLs are user-controlled config values; plans must validate scheme and quote safely before remote curl.

### Tunnel Base Layer

- `workspace-core/ssh/tunnel.py::open_reverse_tunnel` already builds system `ssh -R`, includes `ServerAliveInterval=30`, `ServerAliveCountMax=3`, `ExitOnForwardFailure=yes`, and returns `ReverseTunnel`.
- `autoresearch/ping.py` currently treats "tunnel process started" as success; Phase 5 must add remote proxy curl heartbeat because context D-21 rejects process-only checks.

### Testing Patterns

- `tests/test_hw_cli.py` verifies JSON stdout and progress stderr. Mirror this exactly for `net probe`.
- `tests/test_hw_probe.py` verifies bounded concurrency and ordered aggregate results. Mirror this for remote server matrix.
- `tests/workspace-core/test_tunnel.py` mocks `subprocess.Popen` for tunnel command checks. Mirror this for ensure/reuse/rebuild without real SSH.

## Landmines

- `config/config.yaml` is real local state and may contain sensitive references. Plans may require reading it for UAT, but artifacts must not copy host/user/secret values.
- `curl` output can mix stderr/network errors with write-out. Parser must have a delimiter-safe contract.
- Local proxy URL may contain credentials if overridden. Always redact credentials in JSON, logs, and errors.
- Current Phase 4 real-server UAT is blocked on SSH banner. Phase 5 planning can finish, but execution completion must remain blocked until all configured servers pass true UAT.


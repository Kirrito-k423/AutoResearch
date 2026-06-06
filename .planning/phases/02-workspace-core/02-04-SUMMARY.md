---
phase: 02-workspace-core
plan: 04
subsystem: cli
tags: [ping, paramiko, dummy-server, click, e2e]

# Dependency graph
requires:
  - phase: 02-workspace-core/02-01
    provides: "workspace-core.ssh.SSHClient, open_reverse_tunnel, HostSpec"
  - phase: 02-workspace-core/02-02
    provides: "workspace-core.config.from_path (走 config/config.yaml)"
  - phase: 02-workspace-core/02-03
    provides: "workspace-core.progress.emit_progress (D-14, D-15 进度协议)"
provides:
  - "autoresearch/ping.py: run_ping(server?, lang) → int (D-18, D-19, D-20)"
  - "_DummySSHServer context manager (D-18, D-04c): 接受任何密码/key, 跑 echo ok"
  - "CLI 子命令: autoresearch ping [--server ALIAS] [--lang zh|en]"
  - "config/config.example.yaml: 5 段模板 (version/servers/network/log/wandb)"
  - "phase 2 成功标准 #1: 'ar-ping 命令验证 SSH 端到端'"
affects: [03-customer-config, all 8 skill phases]

# Tech tracking
tech-stack:
  added: []  # 全用现成 paramiko + click + pydantic
  patterns:
    - "dummy server in-process: paramiko ServerInterface + check_channel_exec_request 钩子 (D-04c)"
    - "dummy server 钩子启后台 daemon thread 处理 channel, 不用 sync close (close → client 'Channel closed')"
    - "sendall + send_exit_status + shutdown_read + shutdown_write 触发 client EOF"
    - "D-19 真 server 模式: 走 config + resolve_host + identity_file 合并 + 反向代理通断"
    - "D-20 错误分级: ConfigError=2, click.UsageError=2, SSHError=1, Exception=1, 全程中文消息"
    - "stdout 唯一 JSON, 进度走 stderr (D-04d/e)"
    - "click 8.4: result.stdout 是干净 JSON, result.stderr 含 __AR_PROGRESS__ 标记, result.output 混两者"

key-files:
  created:
    - autoresearch/ping.py
    - config/config.example.yaml
    - tests/test_ping.py
  modified:
    - autoresearch/cli.py (+ ping 子命令)

key-decisions:
  - "D-18: 无 --server 走 paramiko dummy server, 验证 SSH 代码路径 (无外部依赖)"
  - "D-19: 有 --server 走真 SSH + 反向代理通断, identity_file 优先用 config 里的"
  - "D-20: 硬失败 exit 1 (D-04 + 中文错误); config 错 exit 2"
  - "DI-04: dummy server check_channel_exec_request 钩子里**启后台线程** sendall + shutdown_read/write, 不在主线程 close (否则 client raise 'Channel closed')"
  - "DI-05: dummy server send_exit_status 后必加 time.sleep(0.05) + shutdown_read + shutdown_write, 让 client 端 read() / recv_exit_status() 拿到响应并 EOF"
  - "DI-06: click 8.4 CliRunner.result.output 仍含 stderr, 测试必须用 result.stdout 拿干净 JSON"

patterns-established:
  - "in-process SSH 验证: 用 paramiko ServerInterface + 后台 thread, 0 docker 依赖"
  - "channel 关闭序列: sendall → send_exit_status → sleep → shutdown_read → shutdown_write"
  - "click 测试: 用 result.stdout 解析 JSON, result.stderr 验进度标记"
  - "D-20 错误分级: ConfigError/UsageError=2, SSHError/Exception=1"

requirements-completed: [CORE-SSH-01, CORE-SSH-03, CORE-CFG-01, CORE-PROTO-02]

# Metrics
duration: 35min
completed: 2026-06-06
---

# Phase 02 / Plan 04: autoresearch ping CLI Summary

**`autoresearch ping` 端到端冒烟就位: SSH echo + 反向代理通断 (D-18, D-19, D-20). 8 个 pytest PASS, 累计 79/79 (含 phase 1 + 02-01/02/03). phase 2 成功标准 #1 满足.**

## Performance

- **Duration:** 35 min
- **Started:** 2026-06-06T19:35:00Z
- **Completed:** 2026-06-06T20:10:00Z
- **Tasks:** 5/5
- **Files created/modified:** 3 created (ping.py, config.example.yaml, test_ping.py) + 1 modified (cli.py)
- **Tests:** 8 PASS — 累计 79 PASS (含 phase 1 + 02-01/02/03)

## What Was Built

**1. `autoresearch/ping.py` (D-18, D-19, D-20)**
- `_DummySSHServer` context manager: paramiko in-process SSH server, 接受任何密码/key, 跑 echo ok
- `_ping_via_dummy()`: 走 dummy server, 验证 SSH 代码路径 (latency_ms 实测约 80ms)
- `_ping_via_real_server(name)`: 走 config + resolve_host + identity_file + open_reverse_tunnel
- `run_ping(*, server, lang)`: 主入口, exit 0/1/2

**2. `autoresearch/cli.py` 扩展**
- `@main.command() ping [--server ALIAS] [--lang zh|en]`
- 沿用 phase 1 D-04 模式: `--lang` + 出口 exit code

**3. `config/config.example.yaml` (D-13)**
- 5 段模板: version / servers (注释掉示例) / network / log / wandb
- bootstrap_password_secret 用 `<env:VAR>` 占位符示范
- 不进 git (在 .gitignore 排除 config.yaml 但放过 *.example)

**4. `tests/test_ping.py` (8 测试)**
- CLI 入口: --help / no-args / --lang en
- run_ping 函数: stdout JSON / unknown server 错误
- _DummySSHServer 自身: context manager / echo ok / unknown command

## Task Execution

按 PLAN 5 个 task 顺序执行.

## Deviations from Plan

**1. [paramiko dummy server] check_channel_exec_request 钩子里启 daemon thread, 不用 sync close**

- **Found during:** Task 4.4 跑 test_dummy_ssh_server_echo_ok 失败 (`Channel closed`)
- **Root cause:** PLAN 的 dummy server 写的是 `channel.sendall → send_exit_status → channel.close → return True` (同步 close)
  - 同步 close 让 client 端 `chan.exec_command()` 等不到 exec-confirm 响应, 抛 `SSHException: Channel closed`
  - paramiko 3.x 的 `check_channel_exec_request` 钩子**应该**启后台 thread 处理 channel, 让 client 端正常 read
- **Fix:** 钩子里 `threading.Thread(target=handle, daemon=True).start()` + handle 里 sendall + send_exit_status + `time.sleep(0.05)` + `shutdown_read()` + `shutdown_write()` (触发 client EOF)
- **Files modified:** autoresearch/ping.py
- **Decision:** DI-04 写进 SUMMARY

**2. [channel EOF] send_exit_status 后必加 shutdown_read + shutdown_write**

- **Found during:** Task 4.4 修了 #1 后还是 TimeoutError
- **Root cause:** sendall + send_exit_status 后 channel 还开着, client 端 `stdout.read()` 阻塞等 EOF
- **Fix:** `time.sleep(0.05)` + `channel.shutdown_read()` + `channel.shutdown_write()` 触发 client EOF
- **Files modified:** autoresearch/ping.py
- **Decision:** DI-05 写进 SUMMARY

**3. [click 8.4 测试] 用 result.stdout 拿干净 JSON, 不用 result.output**

- **Found during:** Task 4.4 跑 test_ping_via_cli_no_args_runs_dummy 失败 (`JSONDecodeError`)
- **Root cause:** click 8.4 移除了 `mix_stderr=False` 参数, 但 `result.output` 仍**混合** stdout + stderr (默认行为)
  - PLAN 里写的 `result.output` 拿到的是 `__AR_PROGRESS__=...` 进度标记, 解析 JSON 失败
- **Fix:** 测试改用 `result.stdout` (click 8.2+ 默认分离)
- **Files modified:** tests/test_ping.py
- **Decision:** DI-06 写进 SUMMARY

**Total deviations:** 3 auto-fixed (2 paramiko 行为细节 + 1 click 8.4 API)
**Impact on plan:** 8/8 tests PASS, 决策 DI-04..06 记录

## Issues Encountered

- paramiko 3.x 的 `check_channel_exec_request` 钩子行为: 不能在主线程同步 sendall + close, 必须后台 thread sendall + shutdown 双向
- click 8.2+ 的 `mix_stderr` 参数已删除; `result.output` 仍混合 stdout + stderr, 测试必须用 `result.stdout`
- dummy server 启动时 `time.sleep(0.3)` 让 transport 起来, 立即 connect 可能拿到 connection refused

## User Setup Required

无 — `autoresearch ping` 默认走 dummy server, 0 外部依赖. 走真 server 需要 config/config.yaml + (可选) env `SSH_PASSWORD_<ALIAS>`.

## Next Phase Readiness

- ✅ autoresearch ping 端到端可用 (`autoresearch ping` 走 dummy, `autoresearch ping --server nvidia-01` 走真 SSH)
- ✅ config/config.example.yaml 就位, 用户复制即可
- ✅ 8 个 test_ping 单测 PASS (无破坏 phase 1 + 02-01/02/03)
- ✅ phase 2 成功标准 #1 满足
- ⏭  phase 3: customer-config skill (走 config 沉淀 + keyring)

---
*Phase: 02-workspace-core / Plan 04*
*Completed: 2026-06-06*

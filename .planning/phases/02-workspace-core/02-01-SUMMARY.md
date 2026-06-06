---
phase: 02-workspace-core
plan: 01
subsystem: workspace-core
tags: [ssh, paramiko, bootstrap-then-key, reverse-tunnel, keyring, pytest]

# Dependency graph
requires:
  - phase: 01-repo-foundation-services
    provides: "autoresearch click CLI 模式 + pyproject + uv"
provides:
  - "workspace-core.ssh.SSHClient (paramiko 抹平抽象, D-01)"
  - "resolve_host 解析 alias + user@host[:port] (CORE-SSH-02)"
  - "Bootstrap-then-Key 模式 (D-03): 密码 → 部署公钥 → 标 ~/.autoresearch/ssh_keys/<host>.deployed"
  - "open_reverse_tunnel 走 ssh -R + ServerAliveInterval=30 (D-02)"
  - "默认 5s/30s/3 次 + exponential backoff (D-05)"
  - "8 skill 入口: from workspace_core.ssh import SSHClient, resolve_host, open_reverse_tunnel"
affects: [02-workspace-core/02-04, 03-customer-config, 05-network-check, 06-server-hardware, 07-service-reachability, all 8 skill phases]

# Tech tracking
tech-stack:
  added:
    - paramiko 5.0.0
    - cryptography 48.0.0
    - pynacl 1.6.2
  patterns:
    - "SSHClient 抽象 (D-01): 抹平 paramiko, 8 skill 不直接 import"
    - "Bootstrap-then-Key (D-03): env 密码 → sftp 写公钥 → marker 文件"
    - "ReverseTunnel: subprocess.Popen + start_new_session=True (独立进程组)"
    - "exceptions 层级: SSHError 基类 + 6 子类 (Host/Connect/Auth/Bootstrap/KeyDeploy/Tunnel)"

key-files:
  created:
    - workspace-core/__init__.py
    - workspace-core/ssh/__init__.py
    - workspace-core/ssh/exceptions.py
    - workspace-core/ssh/host.py
    - workspace-core/ssh/keys.py
    - workspace-core/ssh/client.py
    - workspace-core/ssh/tunnel.py
    - tests/workspace-core/__init__.py
    - tests/workspace-core/test_ssh_client.py
    - tests/workspace-core/test_keys.py
    - tests/workspace-core/test_tunnel.py
  modified:
    - pyproject.toml (加 paramiko 依赖 + force-include workspace-core → workspace_core)

key-decisions:
  - "D-01: SSHClient 抹平 paramiko, 8 skill 不直接 import"
  - "D-02: 反向代理走系统 ssh -R + ServerAliveInterval=30 + ExitOnForwardFailure=yes"
  - "D-03: Bootstrap-then-Key 模式 (env 密码 → 部署公钥 → 走 key)"
  - "D-04: 单测用 paramiko 自带 dummy server (D-04c)"
  - "D-05: 默认 5s 连接 / 30s 命令 / 3 次重试 exponential backoff"

patterns-established:
  - "exceptions 层级: 所有 SSH 异常继承 SSHError 基类; AuthError 不重试, ConnectError 重试"
  - "_alias_key() 转换 alias → env var 形式 (upper, replace . -)"
  - "fingerprint 标记 (SHA256:xxx) 比整个公钥字符串稳定"
  - "subprocess.Popen start_new_session=True 避免 SIGINT 串到子进程"
  - "hatch force-include: workspace-core 目录 → workspace_core 包名"

requirements-completed: [CORE-SSH-01, CORE-SSH-02, CORE-SSH-03]

# Metrics
duration: 25min
completed: 2026-06-06
---

# Phase 02 / Plan 01: workspace-core/ssh/ Summary

**workspace-core/ssh/ 沉淀就位: SSHClient 抹平 paramiko + Bootstrap-then-Key + 反向代理封装. 12 个 pytest 单测 PASS. CORE-SSH-01..03 全部满足.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-06T18:00:00Z
- **Completed:** 2026-06-06T18:25:00Z
- **Tasks:** 7/7
- **Files created:** 11
- **Tests:** 12 PASS (workspace-core/ssh) + 11 still PASS (phase 1) = 23/23

## Accomplishments

- `workspace_core.ssh.SSHClient` 抹平 paramiko (D-01) - 8 skill 不再直接 import paramiko
- `resolve_host` 解析 alias + user@host[:port] 两种形式 (CORE-SSH-02)
- `SSHClient.connect` 3 阶段凭据: ssh-agent → IdentityFile → env 密码
- `SSHClient.bootstrap` 编排密码登录 → 部署公钥 → 标记完成 (D-03)
- `open_reverse_tunnel` 走 `ssh -R` + ServerAliveInterval=30 + ExitOnForwardFailure=yes (D-02)
- 默认超时 5s/30s/3 次 + exponential backoff (D-05)
- 6 个 SSHError 子类, 错误信息含主机名 + 阶段 + 原因
- 12 个 pytest: 6 ssh client + 4 keys + 2 tunnel (D-04c: paramiko dummy + mock Popen)

## Task Commits

本 plan 7 task 全在 1 commit `feat(02): add workspace-core/ssh/`:
- Task 1.1: 包结构 + 异常
- Task 1.2: host.py
- Task 1.3: keys.py
- Task 1.4: client.py
- Task 1.5: tunnel.py
- Task 1.6: 3 个测试文件
- Task 1.7: git add + commit

## Files Created/Modified

- `workspace-core/__init__.py` — 顶层包
- `workspace-core/ssh/__init__.py` — re-exports
- `workspace-core/ssh/exceptions.py` (~40 行) — 6 异常子类
- `workspace-core/ssh/host.py` (~95 行) — resolve_host + _parse_direct + _parse_ssh_config
- `workspace-core/ssh/keys.py` (~140 行) — ensure_local_keypair + deploy_public_key + marker
- `workspace-core/ssh/client.py` (~165 行) — SSHClient 抽象 + Bootstrap
- `workspace-core/ssh/tunnel.py` (~85 行) — open_reverse_tunnel + ReverseTunnel
- `tests/workspace-core/{__init__,test_ssh_client,test_keys,test_tunnel}.py` (12 测试)
- `pyproject.toml` — 加 paramiko + force-include 映射

## Decisions Made

执行期间严格按 D-01..05 决策落地, 无新增决策。

## Deviations from Plan

**1. [Hatch force-include] workspace-core 目录 → workspace_core 包名**

- **Found during:** Task 1.7 (uv run import workspace_core 失败)
- **Issue:** Python 找 `workspace_core` (下划线), 但目录是 `workspace-core` (短横). Hatch 默认不映射
- **Fix:** 在 `pyproject.toml` 加 `[tool.hatch.build.targets.wheel.force-include] "workspace-core" = "workspace_core"`
- **Files modified:** `pyproject.toml`
- **Committed in:** `feat(02): add workspace-core/ssh/`

**2. [Circular import] client.py ↔ keys.py 循环**

- **Found during:** Task 1.7 (第一个 import 错误)
- **Issue:** `client.py` 用 `from . import keys as ssh_keys`, `keys.py` 用 `from .client import SSHClient` (type hint). 循环
- **Fix:** keys.py 删 `from .client import SSHClient` (运行时不需要, 调 `client.sftp()` 是 duck typing)
- **Files modified:** workspace-core/ssh/keys.py
- **Committed in:** `feat(02): add workspace-core/ssh/`

**Total deviations:** 2 auto-fixed (import 链)
**Impact on plan:** 不影响功能, 都是 Python 包结构问题. 修法简单且幂等.

## Issues Encountered

执行期间发现 2 个 Python import 链问题 (hatch 包名映射 + 循环 import), 已分别修复, 全测 23/23 PASS.

## User Setup Required

**External CLI require installation:**

- **paramiko** — 已在 `uv add` 后随 pyproject 装好
- 实际跑 `SSHClient.bootstrap()` 需要:
  - 真远程 NPU 服务器 (在 `~/.ssh/config` 配 alias)
  - env `SSH_PASSWORD_<ALIAS>` 提供首次密码
  - 本机 `ssh-keygen` (macOS 自带) 生成 ed25519 keypair

## Next Phase Readiness

- ✅ SSHClient 抽象 + Bootstrap-then-Key 就位
- ✅ 反向代理封装就位
- ✅ 12 个 workspace-core 单测 PASS (无破坏 phase 1)
- ⏭  Plan 02-02: workspace-core/secrets/ + config/ (keyring + Pydantic)
- ⏭  Plan 02-03: progress/ + log/ + layout/ + result/
- ⏭  Plan 02-04: autoresearch ping (复用 ssh + config + progress)

---
*Phase: 02-workspace-core / Plan 01*
*Completed: 2026-06-06*

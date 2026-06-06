# Phase 2: workspace-core 沉淀 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-06
**Phase:** 02-workspace-core
**Areas discussed:** SSH 客户端与反向代理 (A), 敏感字段 keyring (B), Pydantic config (C), ar-ping demo (D)

---

## A. SSH 客户端与反向代理实现路径

| Option | Description | Selected |
|--------|-------------|----------|
| A1.a | 直调 paramiko (轻) | |
| **A1.b** | 抽象 SSHClient 接口 (workspace-core/ssh/client.py), 抹平 paramiko | ✓ |
| A2.a | 调系统 `ssh -R` + ServerAliveInterval | ✓ |
| A2.b | paramiko 自实现 reverse tunnel | |
| A2.c | autossh (外部依赖) | |
| **A3 (新)** | **Bootstrap-then-Key**: env 一次性密码 → 部署 ssh key → 后续走 key | ✓ |
| A3.a | ssh-agent → ssh key → password | |
| A3.b | ssh key → agent → password | |
| A3.c | 并行尝试所有 | |
| A4.a | mock paramiko | |
| A4.b | testcontainers sshd | |
| **A4.c** | paramiko 自带 dummy server | ✓ |
| A5.a | 5s/3 次 重试 | |
| A5.b | 10s/5 次 重试 | |
| **A5.c** | 默认 5s/3 次, 实战调 | ✓ |

**User's choice (free text):** 
> "A1.b A2.a A3 我觉得是可以配置明文密码在 env 里，llm 密码登陆后把 ssh key 传输上去，然后后面走 key 访问；A4.c A5.c"

**Rationale captured as D-03 (Bootstrap-then-Key 模式):**
1. **Bootstrap 阶段**: env `SSH_PASSWORD_<host>` 提供一次性明文密码
2. **Deploy-key 阶段**: 密码登录后，paramiko 写本机公钥到服务器 `~/.ssh/authorized_keys`
3. **Normal 阶段**: 后续连接走 ssh-agent / IdentityFile

**Notes:** 
- 缓存 `~/.autoresearch/ssh_keys/<host>.deployed` 避免重复部署
- 已部署 key 但服务器拒绝时，硬失败 + 提示手动 `ssh-copy-id`
- A3 不是"凭据解析优先级"，是**首次连接 bootstrap 机制**——这是用户主动提出的新方案，比 A3.a/b/c 都更工程化

---

## B. 敏感字段 keyring 跨平台

| Option | Description | Selected |
|--------|-------------|----------|
| **B1.a** | python-keyring (跨平台抽象) | ✓ |
| B1.b | 平台特定 (macOS Keychain / Win Cred / Linux SS) | |
| B2.a | 单 `<keyring:xxx>` 占位符 | |
| **B2.b** | 双 `<keyring:xxx>` + `<env:VAR>` 占位符 | ✓ |
| B3.a | CI 跳过加密测试 | |
| **B3.b** | CI 用 `PlaintextKeyring` fake backend | ✓ |
| B4.a | 硬失败 (keyring 不可用就报错) | |
| **B4.b** | 软失败 (warning + 走 env fallback) | ✓ |

**User's choice (free text):**
> "b1a b2b b3b b4b"

**Notes:**
- B4.b 与 A3 联动：env 密码既是 keyring fallback，也是 SSH bootstrap 入口
- 软失败路径 print 强 warning 提醒用户
- 不硬失败避免"首次启动没配 keyring"导致全栈瘫痪

---

## C. Pydantic config

| Option | Description | Selected |
|--------|-------------|----------|
| **C1.a** | Pydantic v2 | ✓ |
| C1.b | Pydantic v1 | |
| **C2.a** | `workspace-core/config/schema.py` 单文件 | ✓ |
| C2.b | 拆 `servers/secrets/network.py` | |
| C3.a | pydantic 原生 ValidationError (英文) | |
| **C3.b** | 自包装 + 中文错误 | ✓ |
| C4.a | 固定 `./config/config.yaml` | |
| **C4.b** | 默认 + `--config` flag | ✓ |

**User's choice (free text):**
> "c 和 d 我觉得你说的默认的就好"

**Notes:** 用户接受所有 C 推荐项。

---

## D. ar-ping 端到端冒烟的 demo 服务器策略

| Option | Description | Selected |
|--------|-------------|----------|
| **D1.b** | paramiko 自带 dummy server | ✓ |
| D1.a | testcontainers sshd | |
| D1.c | 文档化要真 server, 无则退出 | |
| D2.a | `echo ok` 单命令 | |
| D2.b | `echo + uname` | |
| **D2.c** | `echo + 反向代理通断` (一个 ar-ping 覆盖 2 能力) | ✓ |
| **D3.a** | 硬失败 (exit 1) | ✓ |
| D3.b | 软失败 (status JSON, exit 0) | |

**User's choice (free text):**
> "d 我觉得你说的默认的就好"

**Notes:** 用户接受所有 D 推荐项。D1.b 不引入 testcontainers 避免 Phase 2 引入 docker 测试基建。

---

## the agent's Discretion

- D-05 默认超时具体值实战再调 (用户接受 A5.c)
- D-15 progress emit 频率由 skill 自己控制
- D-21 result schema 字段集按需增

## Deferred Ideas

- **multi-key 部署**: Phase 3+ 出现"哪个 key 用哪个 skill"再考虑
- **key 轮换 (rotation)**: M2 再说
- **Windows 平台适配**: PROJECT.md 没强调 Windows, keyring 已支持但未在本阶段测试覆盖
- **`autoresearch` 顶层 CLI 是否包含 `ar-ping`**: phase 12 顶层 CLI 编排时统一
- **D-21 result schema 的 `tags` / `duration_ms` 字段**: 实战发现缺再加

## Cross-Area Synergies Noticed

1. **A3 ↔ B4.b 联动**: env 密码既是 SSH bootstrap 入口，也是 keyring 失败 fallback —— 共用 env lookup 路径
2. **D-21 ↔ D-04e**: result schema 配合 stdout 唯一 JSON 协议
3. **D-15 ↔ D-04d**: progress 协议是 phase 1 锁定的"占位"现在 phase 2 落实现
4. **D-16 ↔ D-04e**: log 输出格式不影响 stdout JSON 唯一性 (log 走 stderr/file)

---
*Generated: 2026-06-06 by $gsd-discuss-phase 2*

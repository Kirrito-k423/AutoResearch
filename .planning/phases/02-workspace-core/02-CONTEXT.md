# Phase 2: workspace-core 沉淀 - Context

**Gathered:** 2026-06-06
**Status:** Ready for planning

<domain>
## Phase Boundary

三沉淀层（`workspace-core/` / `verl-workspace-adapter/` / `datalake/`）中的 `workspace-core/` 全部跑通：7 子模块（ssh / secrets / config / progress / log / layout / result）提供统一接口，下游 8 skill 可直接 import 使用。`ar-ping` CLI 端到端验证 SSH + 反向代理能力。
本阶段不交付 verl-workspace-adapter / datalake（Phase 11 范围），不交付 8 skill 业务逻辑（Phase 3-10 范围）。
</domain>

<decisions>
## Implementation Decisions

### SSH 客户端与反向代理 (CORE-SSH-01..03) — D-01..D-05

- **D-01 (抽象层):** 抽象一层 `SSHClient` 接口 (`workspace-core/ssh/client.py`)，抹平 paramiko 调用细节。后续 8 skill 全部走这个接口，不直接 import paramiko。
- **D-02 (反向代理):** 反向代理走**系统 `ssh -R` + ServerAliveInterval**，进程生命周期由 `start.sh` 管理（不在 Python 内长驻）。参数模板：
  ```
  ssh -N -R <remote_port>:localhost:<local_port> \
      -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
      -o ExitOnForwardFailure=yes \
      -i <identity_file> user@host
  ```
- **D-03 (Bootstrap-then-Key 模式):** **SSH 登录走三阶段**：
  1. **Bootstrap 阶段**: 首次连服务器，env `SSH_PASSWORD_<host>` 提供一次性明文密码（如 `SSH_PASSWORD_NVIDIA_01=xxx`）。CLI 提示用户："将用密码登录一次并部署 SSH key，是否继续?"
  2. **Deploy-key 阶段**: 密码登录成功后，paramiko 把本机公钥 (`~/.ssh/id_ed25519.pub` 或临时生成) 写到服务器 `~/.ssh/authorized_keys`，权限 `600`
  3. **Normal 阶段**: 后续连接走 ssh-agent 或 IdentityFile，明文密码不再使用
  - 缓存: `~/.autoresearch/ssh_keys/<host>.deployed` 标记已部署，避免重复
  - 失败: 已部署 key 但服务器仍拒绝时，**硬失败 + 提示用户手动 `ssh-copy-id`**（不自动重试密码）
- **D-04 (单测):** 单元测试用 **paramiko 自带 dummy SSH server** (`paramiko.RSAKey.generate()` + `Transport.open_server()`)；不引入 testcontainers（避免 Phase 2 引入 docker 测试基建）
- **D-05 (默认超时):** 连接 5s 超时 / 命令执行 30s / 重试 3 次 exponential backoff (1s, 2s, 4s)。实战中根据具体 skill 调，不在 workspace-core 层硬塞配置

### 敏感字段 keyring (CORE-SEC-01..02) — D-06..D-09

- **D-06 (库):** 用 `python-keyring` 跨平台抽象。macOS → Keychain / Windows → Credential Manager / Linux → SecretService。PROJECT.md 已锁。
- **D-07 (占位符双格式):**
  - `<keyring:xxx>` — dev/本机用，从系统 keyring 取
  - `<env:VAR>` — CI / 共享环境用，从 env 取
  - 解析函数 `resolve_secret(value: str) -> str`：检测前缀分发，env 不存在时尝试 keyring，最后 fallback 到明文
- **D-08 (CI 行为):** CI 环境用 `keyring.alt.file.PlaintextKeyring` fake backend 跑测试（仍测真路径），不跳过
- **D-09 (失败行为 — 软失败):** keyring 不可用时**软失败**：print warning 到 stderr，**自动 fallback 到 env lookup**。理由：避免"首次启动没配 keyring"导致全栈瘫痪；但 fallback 路径 print 强 warning 让用户知道。
  - **Bootstrap 联动**: SSH bootstrap 用的 `SSH_PASSWORD_<host>` env 变量与本机制**共用** env fallback 路径

### Pydantic config (CORE-CFG-01..02) — D-10..D-13

- **D-10 (版本):** Pydantic **v2**（事实标准，性能好，类型系统强）
- **D-11 (schema 放法):** `workspace-core/config/schema.py` **单文件**。M1 阶段 schema 还小（ServerList / NetworkProbes / SecretRef 等 <10 个 model），拆早是过度工程。Phase 3+ 复杂后**视情况**拆。
- **D-12 (错误信息):** 自包装 `pydantic.ValidationError` → 中文错误，格式 `字段路径 + 原因 + 期望值` 例：
  ```
  配置错误: servers[0].host
    原因: 字段必填但未提供
    期望: 非空字符串
  ```
- **D-13 (配置路径):** 默认 `./config/config.yaml` + `--config <path>` CLI flag 覆盖。env `AUTORESEARCH_CONFIG` 也作为兜底

### 进度协议 (CORE-PROTO-01..02) — D-14..D-15

- **D-14 (协议格式):** `__AR_PROGRESS__=<json>` 写 stderr，最终 stdout 唯一 JSON 对象（D-04e 锁定）。JSON schema：
  ```json
  {
    "stage": "ssh.connect|secrets.resolve|config.load|...",
    "ts": "2026-06-06T08:00:00Z",
    "level": "info|warn|error",
    "data": {...}            // 各 stage 自定义
  }
  ```
- **D-15 (辅助函数):** `workspace-core/progress/emitter.py` 提供 `emit_progress(stage, **fields)` 封装。**不强制**每个 skill 每次都 emit；只在阶段切换 / 关键节点 emit，避免日志淹没

### 统一日志 (CORE-LOG-01) — D-16

- **D-16:** 库 = stdlib `logging` + 自定义 `JsonFormatter`（避免引入 structlog/loguru 第三方）。字段：`timestamp / level / host / msg / ctx`。
  - CLI 输出: 人类可读格式（带 ANSI 颜色）
  - 文件输出: JSON 格式，落到 `~/.autoresearch/logs/<skill>-<date>.log`
  - 单实例: `get_logger(name)` from `workspace-core.log`，skill 自己 import

### 目录约定 (CORE-LAYOUT-01) — D-17

- **D-17:** 固定 `~/.autoresearch/runs/<run-id>/{logs,wandb,prom,manifest.json}`。惰性创建（按需 `mkdir(parents=True, exist_ok=True)`）。
  - run-id 冲突: 硬失败 + 提示 "用 --run-id <新>"
  - 跨 run 共享: `~/.autoresearch/cache/` (wandb data / 模型)
  - 跨平台: `~/.autoresearch/` 路径用 `pathlib.Path.home()`，Mac/Linux/WSL 都走 `~`

### ar-ping 端到端冒烟 (plan 02-04) — D-18..D-20

- **D-18 (demo 来源):** `ar-ping` 默认用 **paramiko 自带 dummy SSH server** 验证 SSH 客户端代码路径（单元测试式）。**真远程服务器**通过 `--server <name>` flag 走 `config/config.yaml` 解析。
  - 文档化: 无 `--server` 时 exit 0 + 提示"本地 dummy 测过；想测真服务器请配 config"
- **D-19 (跑什么):** `ar-ping --server <name>` 跑两件事：
  1. SSH 登录 + `echo ok` 验证连接
  2. 起反向代理 + 远程 `curl http://localhost:<remote_port>` 验证代理通
  - 输出: `{"ssh": true, "reverse_tunnel": true, "latency_ms": 42}` (JSON, D-04e)
- **D-20 (失败行为):** **硬失败** `exit 1` + 错误细节到 stderr。`ar-ping` 是"我能不能通"，通不了就是失败，不软化

### Result Schema (CORE-PROTO 衍生) — D-21

- **D-21:** 沉淀层再加一个 `workspace-core/result/` (虽然不在 REQUIREMENTS.md 11 条 REQ 内，但 8 skill 都需要统一返回结构)
  ```python
  class CheckResult(TypedDict):
      ok: bool
      data: dict | None
      message: str
      error: str | None
  ```
  - 标 "non-REQ addition"，归到 Phase 2 范围因为 8 skill 全用

### the agent's Discretion
- D-05 默认超时具体值实战再调
- D-15 progress emit 频率由 skill 自己控制
- D-21 result schema 字段集按需增（Phase 3-10 实战发现缺什么加什么）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目级
- `.planning/PROJECT.md` — 哲学、Core Value、Active/Out of Scope、Constraints、Key Decisions (技术栈: Python 3.11+ / paramiko / Pydantic / keyring / Click)
- `.planning/REQUIREMENTS.md` — 88 条 REQ 跨 14 组；本阶段取 CORE-SSH-01..03 + CORE-SEC-01..02 + CORE-CFG-01..02 + CORE-PROTO-01..02 + CORE-LOG-01 + CORE-LAYOUT-01
- `.planning/ROADMAP.md` — Phase 2 目标 / 依赖 / 成功标准 / 4 个 plan
- `.planning/STATE.md` — 当前进度 (Phase 1 完成, Phase 2 待开始)
- `ARCHITECTURE.md` — 完整愿景 (3 沉淀 + 8 skill 布局)
- `AGENTS.md` — 仓约定 (8 步循环 / 三沉淀层 / 进度协议 / 测试规范)

### 前情已锁定 (Phase 1)
- `.planning/phases/01-repo-foundation-services/01-CONTEXT.md` — Phase 1 决策, 关键:
  - D-03c: 端口固定 8080/9090/3000/8088
  - D-04: click 树状子命令 + `autoresearch` 单二进制
  - D-04d: `__AR_PROGRESS__=<json>` on stderr
  - D-04e: 最终 stdout 唯一 JSON 对象
  - D-05: Archon 不在 compose

### 现有实现可复用
- `autoresearch/cli.py` (phase 1) — click group 模式, 后续 `ar-ping` 复用
- `autoresearch/services/_common.py` (phase 1) — ThreadPoolExecutor 并发模式, 后续可复用
- `services/` 目录 (phase 1) — docker compose 模式参考
- 11 个 pytest 单测 (phase 1) — pytest 框架配置 + CliRunner 模式

### 外部参考
- `paramiko` 官方文档: https://docs.paramiko.org/
  - `RSAKey.generate()` + `Transport.open_server()`: dummy SSH server 写法
  - `SSHClient.open_sftp()`: sftp 传文件 (deploy key 用)
- `python-keyring` 官方文档: https://keyring.readthedocs.io/
  - `keyring.alt.file.PlaintextKeyring`: fake backend for CI
- `pydantic` v2 文档: https://docs.pydantic.dev/latest/
  - `ValidationError` 自定义: `errors(include_url=False, include_input=True)`

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`autoresearch/cli.py` 模式**: `@click.group() + @main.group() + @services.command()` 树状子命令结构，`ar-ping` 可作为 `autoresearch ping` 或独立 CLI `ar-ping` (top-level script entry)
- **`autoresearch/services/_common.py`**: ThreadPoolExecutor 并发 + TypedDict 结果模式，phase 2 的 result.py 借鉴
- **`autoresearch/services/status.py`**: `run_*(**kwargs) -> int` 返回 exit code 模式, 后续 CLI 函数都这样写
- **11 pytest 测试 (phase 1)**: `CliRunner` 模式 + `unittest.mock.patch` mock 模式, 后续单测直接复用

### Established Patterns
- **default zh / `--lang en` 切英文** (phase 1 D-04): 所有 CLI 子命令统一
- **错误信息中文优先** (phase 1 D-04 落地): 沉淀层错误也走中文
- **`subprocess.run` + `check=False` + `capture_output=True` 调外部命令** (phase 1 start.py): 反向代理 `ssh -R` 复用此模式
- **代码改动不破坏 phase 1 verification** (phase 1 教训): 沉淀层加新代码不重写 phase 1 已通过的 11 测试

### Integration Points
- **从 phase 1 `autoresearch.services._common` 复用**: `ThreadPoolExecutor` 模式可移植到 `workspace-core/result/parallel.py` (如果以后需要)
- **phase 1 services/_common.py 的 port 常量** (8088/8080/9090/3000) — Phase 2 不直接相关, 但 phase 6 以后 server probes 可能用
- **`ar-ping` 与 phase 1 services CLI 平行**: 都是 `autoresearch` 子命令

</code_context>

<specifics>
## Specific Ideas

### SSH Bootstrap UI
```
$ autoresearch ping --server nvidia-01
⚠  首次连接 nvidia-01, 将用 SSH_PASSWORD_NVIDIA_01 env 密码登录
   并部署本机 SSH key. 继续? [y/N]: y
🔐 用密码登录 nvidia-01...
🔑 部署本机公钥到 nvidia-01:~/.ssh/authorized_keys...
✅ SSH key 部署完成. 后续走 key 访问.
{"ssh": true, "reverse_tunnel": true, "latency_ms": 1234}
```

### Config 错误信息格式
```python
try:
    cfg = Config.from_yaml("config/config.yaml")
except ConfigError as e:
    # e.message 已经是中文格式化的:
    # "配置错误: servers[0].host\n  原因: 字段必填但未提供\n  期望: 非空字符串"
    print(e.message, file=sys.stderr)
    sys.exit(2)
```

### Layout 路径
```
~/.autoresearch/
├── runs/
│   └── 2026-06-06-smoke-001/
│       ├── logs/run.log
│       ├── wandb/         # wandb sync 落点
│       ├── prom/          # prom push 落点
│       └── manifest.json  # run 元信息
├── cache/                 # 跨 run 共享 (模型 / wandb data)
├── ssh_keys/              # 已部署 key 缓存
│   ├── nvidia-01.deployed # 标记文件, 内容 = 公钥 fingerprint
│   └── nvidia-02.deployed
└── logs/                  # 全局 skill 日志
    └── <skill>-<date>.log
```

</specifics>

<deferred>
## Deferred Ideas

- **multi-key 部署**: 当前 deploy 一个 key, 不支持多 key (e.g. 不同用途). Phase 3+ 出现"哪个 key 用哪个 skill"再考虑
- **key 轮换 (rotation)**: 已部署 key 不定期换. M2 再说
- **Windows 平台适配**: PROJECT.md 没强调 Windows, keyring 已支持但未在本阶段测试覆盖
- **`autoresearch` 顶层 CLI 是否包含 `ar-ping`**: 当前 D-18 倾向 `autoresearch ping`, 留到 phase 12 顶层 CLI 编排时统一
- **D-21 result schema 的 `tags` / `duration_ms` 字段**: 实战发现缺再加

</deferred>

---
*Last updated: 2026-06-06 after $gsd-discuss-phase 2 (4 areas discussed, 21 decisions captured)*

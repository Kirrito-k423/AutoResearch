# Phase 5: Skill 04 — network-check - Context

**Gathered:** 2026-06-09
**Status:** Ready for planning

<domain>
## Phase Boundary

实现 `autoresearch net`，交付本机与远程服务器的网络测速矩阵、direct/proxy 两阶段探测、以及可复用的 SSH 反向代理隧道能力。`net probe` 默认同时测本机和配置中的全部远程服务器，目标来自 `config.network.targets`，默认覆盖 baidu、huggingface、github。远程直连失败时自动通过 Mac 本机代理 `127.0.0.1:7890` 建 `ssh -R` fallback，并记录 direct/proxy attempts。

本阶段不验证远程到本地 wandb/Prometheus 服务可达性，不检查训练栈，不采集实验数据，也不生成实验报告；这些分别属于 Phase 6、Phase 7、Phase 8 和 Phase 9。Phase 5 可以先规划和实现，但完成门槛必须包含配置中全部服务器的真实网络/隧道 UAT；当前 Phase 4 的 SSH banner 阻塞若仍存在，也会阻塞 Phase 5 最终关闭。

</domain>

<decisions>
## Implementation Decisions

### CLI、输出与结果语义

- **D-01:** `autoresearch net probe` 默认执行本机测速 + 配置中全部远程服务器测速；`--server NAME` 可收窄到单台服务器。若 planner 需要保留一个只测本机的入口，可增加 `--local-only`，但默认行为必须是完整矩阵。
- **D-02:** `net probe` stdout 永远只输出唯一 JSON 对象；过程进度继续走 stderr `__AR_PROGRESS__=<json>`。不在 stdout 同时打印人类表格。
- **D-03:** JSON 以扁平 `rows` 为主，并额外提供 grouped summary，便于 CLI、报告和后续 Phase 6/9 复用。
- **D-04:** 每个 target 一行，行内保留 `attempts` 数组，例如 direct attempt 和 proxy attempt；不得只保留最终结果而隐藏失败路径。
- **D-05:** 推荐 row 字段至少包含 `location`、`server`、`target_label`、`target_url`、`effective_mode`、`status`、`http_code`、`latency_ms`、`speed_download_bps`、`attempts`、`error`。
- **D-06:** 失败语义采用混合规则：本机 baidu 失败或远程全部 target 失败为 `FAIL`；huggingface/github direct 失败先记 `WARN`，proxy fallback 仍失败再提升为 `FAIL`。
- **D-07:** CLI exit code 语义延续 Phase 4：全部成功或仅 warn 为 `0`；网络矩阵出现 `FAIL` 为 `1`；配置、参数或 target URL 非法为 `2`。

### Targets 与测速命令

- **D-08:** 网络 targets 只读 `config.network.targets`；默认值仍由 schema/example 提供 baidu、huggingface、github。target label 从 hostname 推导即可。
- **D-09:** target URL 只接受 `http://` 和 `https://`。其他 scheme 视为配置错误，避免远程 `curl` 被用来访问本地文件或非 HTTP 资源。
- **D-10:** 本机和远程测速统一使用 `curl --max-time 10 -L -o /dev/null -s -w ...`，记录 `http_code`、`time_total`/`latency_ms` 和 `speed_download`。
- **D-11:** 每个 target 的 direct 模式尝试一次；失败后 proxy 模式尝试一次；不做额外 per-target retry，避免网络检查拖得过长。
- **D-12:** 远程命令必须安全 quoting，不允许把未经验证的 target 直接拼进 shell。若实现选择 subprocess argv 或 heredoc，也必须保持 URL allowlist。

### Proxy Fallback

- **D-13:** 本机测速也采用 direct-first。huggingface/github direct 失败且本机 `127.0.0.1:7890` 可用时，自动用本机 proxy 重试并记录两次 attempts。
- **D-14:** 远程测速 direct 失败后自动 fallback：建立 `ssh -R <remote_proxy_port>:127.0.0.1:7890`，远程重试时使用 `ALL_PROXY=http://127.0.0.1:<remote_proxy_port>`。
- **D-15:** 远程代理端口默认 `17890`，避免撞远程已有代理；提供 `--remote-proxy-port` 覆盖。
- **D-16:** 本机代理地址默认 `http://127.0.0.1:7890`，提供 `--local-proxy-url` 覆盖。日志、JSON 和错误摘要必须脱敏 URL 中可能出现的凭据。
- **D-17:** 如果需要 proxy fallback 但本机代理不可用，结果应明确标出 `proxy_unavailable`，并把对应 target 或 server 计入混合失败规则。

### Tunnel Lifecycle

- **D-18:** Phase 5 必须提供可复用隧道能力，推荐 CLI 为 `autoresearch net tunnel ensure --server X`。Phase 6 可以在服务可达性测试前调用 ensure，而不是重新实现隧道逻辑。
- **D-19:** `net tunnel ensure` 使用本地状态文件 `~/.autoresearch/tunnels/<server>.json`，记录 `pid`、`remote_port`、`local_proxy_url`、`started_at`、`log_path` 和最近一次 heartbeat 结果。
- **D-20:** ensure 遇到已有隧道时，若状态文件存在且心跳通过则复用；若心跳失败则停止旧进程并重建。
- **D-21:** 隧道健康检查同时检查本地 `ssh` 子进程存活和远程 proxy curl 结果，避免“进程活着但链路假死”。
- **D-22:** 心跳间隔为 30s；断线最多重试 3 次，指数退避 1s/2s/4s，仍失败则 `FAIL`。
- **D-23:** 反向代理仍基于 Phase 2 的 `open_reverse_tunnel` / 系统 `ssh -R`，但 Phase 5 需要在其上增加健康检查、状态文件、复用/重建和 retry supervisor。
- **D-24:** 隧道进程和状态都留在本机 Mac；远程服务器不得留下持久状态文件。
- **D-25:** 隧道错误 JSON 只暴露 `tunnel_log_path` 和脱敏后的最后 500 字符摘要；不得把完整 ssh/curl 原始输出塞进 JSON。

### Completion Gate 与测试

- **D-26:** Phase 5 完成门槛从严：配置中的全部服务器都必须完成真实 `net probe` 和 tunnel fallback UAT，才能标记 Phase 5 完成。
- **D-27:** 在当前 SSH banner 外部阻塞未恢复前，可以完成代码、单测和 mock SSH 验证，但最终 Phase 5 必须保持 blocked，不得用 mock 代替真实服务器验收。
- **D-28:** 单测必须覆盖 curl 输出解析、URL scheme 拒绝、direct/proxy attempts、proxy 不可用、tunnel state reuse/rebuild、heartbeat 失败重试、CLI 唯一 JSON stdout 和敏感字段脱敏。
- **D-29:** 远程多服务器探测应复用 Phase 4 的有界并发和失败隔离模式；单台失败不阻断其他服务器继续探测，但聚合结果必须保留失败服务器和原因。

### the agent's Discretion

- 精确模块拆分，例如 `autoresearch/net/probe.py`、`autoresearch/net/tunnel.py`、`autoresearch/net/models.py`。
- `rows` 和 grouped summary 的具体 TypedDict/Pydantic model 命名。
- `curl -w` format 字符串的具体字段名，只要能稳定解析 `http_code`、耗时和下载速度。
- heartbeat 选用的默认 target。建议 baidu 优先；若 config 中没有 baidu，则使用第一个 configured target。
- 是否提供 `net tunnel status/stop` 作为 ensure 的配套命令；若实现 background supervisor，stop/status 很可能是自然需要的。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目范围与需求

- `AGENTS.md` — 仓约定、8 skill 映射、进度协议、测试规范和本地优先原则。
- `ARCHITECTURE.md` — Skill 04 network-check 与 service-reachability、train-stack-health 的边界。
- `.planning/PROJECT.md` — 远程服务器偶发断网、Mac 本机代理 `127.0.0.1:7890`、本地保留 run/log/wandb 状态等约束。
- `.planning/REQUIREMENTS.md` — `NET-LOCAL-01..03`、`NET-REMOTE-01..03`、`NET-TUNNEL-01..02`。
- `.planning/ROADMAP.md` — Phase 5 目标、成功标准和 05-01..03 plan 草案。
- `.planning/STATE.md` — 当前 Phase 4 真实服务器 SSH banner 阻塞会影响 Phase 5 UAT。

### 前置决策

- `.planning/phases/02-workspace-core/02-CONTEXT.md` — `SSHClient`、`open_reverse_tunnel`、进度协议、日志、layout 和 `CheckResult` 决策。
- `.planning/phases/03-skill-01-customer-config/03-CONTEXT.md` — config CLI、config path、脱敏和 schema 复用决策。
- `.planning/phases/04-skill-03-server-hardware-probe/04-CONTEXT.md` — `--server/--all`、有界并发、失败隔离、真实服务器 UAT 和敏感字段不泄露的已锁定模式。

### Existing Code

- `autoresearch/cli.py` — 单一 Click 命令树与 `hw probe` CLI 模式。
- `autoresearch/ping.py` — 真实 SSH + 反向代理 smoke 的现有入口。
- `autoresearch/hw/probe.py` — 多服务器有界并发、聚合结果、唯一 JSON stdout 和 progress stage 模式。
- `workspace-core/ssh/client.py` — SSH 连接、命令执行、超时和错误分类。
- `workspace-core/ssh/tunnel.py` — `ssh -R` 反向代理基础实现。
- `workspace-core/config/schema.py` — `network.targets` 默认值和 server schema。
- `workspace-core/progress/emitter.py` — `__AR_PROGRESS__=<json>` 协议。
- `workspace-core/result/check.py` — `CheckResult`、`CheckSeverity` 和 merge 语义。
- `config/config.example.yaml` — 默认 network targets 与用户配置模板。

### Tests to Mirror

- `tests/test_hw_cli.py` — CLI JSON stdout、progress stderr、exit code 和敏感字段脱敏断言。
- `tests/test_hw_probe.py` — `probe_all` 有界并发、顺序保留、worker exception 隔离和 warn-only success。
- `tests/workspace-core/test_tunnel.py` — mock `ssh -R` command、立即失败处理和 tunnel object 断言。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `workspace-core/ssh/client.py`：远程测速必须通过该 SSH 抽象执行命令，不直接 import paramiko。
- `workspace-core/ssh/tunnel.py`：已有 `open_reverse_tunnel` 构造 `ssh -R` 命令，Phase 5 在其上加 ensure/state/heartbeat/retry。
- `workspace-core/config/schema.py`：已有 `NetworkProbes.targets` 默认值，可直接作为 `net probe` 目标来源。
- `workspace-core/progress/emitter.py`：所有阶段进度走 stderr，不污染 stdout。
- `workspace-core/result/check.py`：复用 `CheckResult`/`CheckSeverity`，避免每个 skill 自定义返回结构。
- `autoresearch/hw/probe.py`：`probe_all` 的 ThreadPoolExecutor、有界并发、失败隔离和顺序保留可直接借鉴。
- `autoresearch/ping.py`：已有真实 SSH + tunnel smoke，但当前只把 tunnel 起得来当成功；Phase 5 必须补上真实 proxy curl heartbeat。

### Established Patterns

- Click group 挂在 `autoresearch` 单二进制下；Phase 5 新增 `net` group。
- CLI 子命令的机器边界应输出唯一 JSON；关键过程用 `__AR_PROGRESS__=` 事件。
- 默认中文错误，`--lang en` 切英文。
- 单测用 `CliRunner`，远程/系统命令通过 mock，不在单测中依赖真实外网或真实服务器。
- 真实服务器 UAT 是最终完成门槛；mock/fixture 不能替代外部状态验收。

### Integration Points

- `autoresearch/cli.py`：新增 `net` group、`probe` command 和 `tunnel` subgroup。
- `autoresearch/net/`：建议新增 probe、tunnel、models/curl parser 模块。
- `config/config.example.yaml`：保留默认 targets；若新增 proxy 默认值，应尽量先用 CLI flag，不急于扩 schema。
- `~/.autoresearch/tunnels/`：新增本地 tunnel state 目录。
- `tests/`：新增 net CLI、probe parser、proxy fallback、tunnel supervisor/state 测试。

</code_context>

<specifics>
## Specific Ideas

- `curl -w` 可以输出一段 JSON-like 或 delimiter-safe 格式，解析为 `http_code`、`time_total`、`speed_download`；stderr 与 stdout 需要分离，避免错误页污染解析。
- 远程 proxy retry 的环境变量建议只在单次命令前缀注入，例如 `ALL_PROXY=http://127.0.0.1:17890 HTTPS_PROXY=... curl ...`，不要修改远程 shell profile。
- tunnel 状态文件只记录运行所需元信息，不记录 SSH identity file 内容、bootstrap secret 或带凭据的 proxy URL。
- grouped summary 至少应能回答：本机通过/告警/失败数、每台远程服务器通过/告警/失败数、哪些服务器需要 proxy 才通、哪些服务器 proxy 后仍不通。

</specifics>

<deferred>
## Deferred Ideas

- 远程到本地 wandb/Prometheus 的 `/health` 或 pushgateway 探活属于 Phase 6 service-reachability。
- 训练栈环境、conda、verl/veomni 1-step dry run 属于 Phase 7 train-stack-health。
- 网络结果的 HTML 可视化和长期历史趋势属于后续 report/datalake 阶段。
- 更复杂的 proxy 配置 schema（按 target 配 expected code、timeout、proxy policy）暂不纳入 Phase 5；M1 用 CLI flag + 默认值即可。

</deferred>

---

*Phase: 5-skill-04-network-check*
*Context gathered: 2026-06-09*

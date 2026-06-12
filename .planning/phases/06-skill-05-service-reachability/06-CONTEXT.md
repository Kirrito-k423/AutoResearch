# Phase 6: Skill 05 — service-reachability - Context

**Gathered:** 2026-06-12
**Status:** Ready for planning
**Discussion mode:** user-approved defaults (skipped interactive Q&A)

<domain>
## Phase Boundary

验证远程服务器能通过 SSH 反向代理隧道访问本地 wandb (8080) 和 Prometheus (9090) + pushgateway (9091, Phase 6 引入).
本 phase 不实现"训练数据采集"(Phase 8) — 只做"连通性验证"; metric 内容/格式是 Phase 8 范畴.

</domain>

<decisions>
## Implementation Decisions

### A. wandb 端点 (D-35)
- **D-35.A1:** 远程 curl 目标固定 `http://127.0.0.1:17890/healthz` (走 ssh -R 17890 隧道回本机 8080)
- **D-35.A2:** 走 HTTP (非 HTTPS); wandb 容器内置 self-signed 没必要
- **D-35.A3:** 端口 17890 沿用 Phase 5 `net tunnel ensure` 默认, 不做 per-server 协商
- **D-35.A4:** wandb /healthz 返回 200 + JSON `{"state": "available"}` 即 PASS

### B. Prometheus pushgateway 协议 (D-36)
- **D-36.B1:** **新增** `prom/pushgateway` 容器, 端口 9091 固定, 在 `services/prometheus/compose.yml` 追加
- **D-36.B2:** Prometheus 主容器 scrape pushgateway (`job_name: pushgateway`, `targets: ['pushgateway:9091']`); Phase 6 期间 prometheus.yml 追加此 job
- **D-36.B3:** 远程 push 协议: 标准 textfile 格式 `PUT /metrics/job/<job>/instance/<host>` 走 HTTP, body 多行 metric
- **D-36.B4:** 每次 push TTL 不设 (`push.add` 不带 ?flags=); Phase 8 collect 时显式 `push.delete`
- **D-36.B5:** metric 命名 `autoresearch_reach_test` (下划线, 不带单位, Prometheus 惯例)

### C. 失败诊断行为 (D-37)
- **D-37.C1:** reach test 失败时**自动**调 `run_tunnel_ensure()` 重试一次 (bound 8s)
- **D-37.C2:** 自动重试仍失败 → 错误信息含 "请先跑 `autoresearch net tunnel ensure --server <alias>`"
- **D-37.C3:** 不做无限重试; 一次自动 + 一次显式提示 = 终止

### D. 测试 metric / 端点命名 (D-38)
- **D-38.D1:** pushgateway push URL 固定 `http://127.0.0.1:17891/metrics/job/autoresearch_reach/instance/<server>`
  - 远程 17891 = ssh -R 17891 端口, 转到本机 9091 (pushgateway)
  - 每个 server 一条 instance 标签
- **D-38.D2:** 测试 metric 内容:
  - `autoresearch_reach_test{server="<alias>"} 1` (gauge, 1=PASS / 0=FAIL)
  - 另 push `autoresearch_reach_timestamp_seconds{server="<alias>"} <unix_ts>` (记录探测时间)
- **D-38.D3:** 探测后**不主动 delete** — Phase 8 collect 用 `push.delete` 统一清理
- **D-38.D4:** push 失败不算 reach 失败 (Prometheus 主路径通了就 OK; push 是 best-effort 心跳)

### 计划范围 (Wave 建议)
- **06-01 (Wave 1):** pushgateway 容器 + prometheus.yml 追加 scrape job + `ar-services` CLI 子命令重启
- **06-02 (Wave 2):** `autoresearch reach test --server X` 端到端 — wandb /healthz + pushgateway push
- **06-03 (Wave 3, 选做):** `autoresearch reach test --all` 并发 + 失败重试 + 诊断链 (D-37)

### the agent's Discretion
- wandb /healthz 解析的 JSON 字段 (固定 `state == "available"` 即可)
- pushgateway 容器内存/重启策略 (沿用 wandb/prom 模式)
- 测试中 dummy SSH client 的 fixture 设计

</decisions>

<canonical_refs>
## Canonical References

Downstream agents MUST read these before planning or implementing:

### Tunnel / 网络层
- `autoresearch/net/tunnel.py` — Phase 5 已暴露 `run_tunnel_ensure`; Phase 6 reach 必须先调它建隧道
- `autoresearch/net/probe.py` — `_remote_proxy_curl_command()` 模板可复用为 reach 的远程 curl shell
- `autoresearch/cli.py:210-265` — `net tunnel ensure` CLI 入口参考
- `tests/test_net_tunnel.py` — fixture / mock 模式 (paramiko dummy client + injectable sleeper)

### 服务端点
- `services/wandb/compose.yml` — 端口 8080, D-03c 固定
- `services/prometheus/compose.yml` — 端口 9090, 现有 self-scrape
- `services/prometheus/prometheus.yml` — 需追加 pushgateway scrape job

### 决策
- `.planning/phases/05-skill-04-network-check/05-03-SUMMARY.md` — 明确"`net tunnel ensure` 已为 Phase 6 暴露"
- `.planning/ROADMAP.md` Phase 6 — 2 plans 规划 (本文档建议拆 3 plans, 选做第 3)

### 项目约定
- `AGENTS.md` §"进度协议模板" — 所有 CLI 子命令走 `__AR_PROGRESS__=` stderr
- `AGENTS.md` §"测试规范" — click.testing.CliRunner 测 CLI, pytest, 业务逻辑必须有断言

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `autoresearch.net.tunnel.run_tunnel_ensure` — 一键建/验 SSH 反向代理, Phase 6 reach test 入口应先调
- `autoresearch.net.probe._remote_proxy_curl_command` — 拼远程 curl 命令模板, 可作 reach wandb/prom 的基础
- `workspace_core.ssh.SSHClient.exec` — 远程命令执行; reach test 直接复用
- `workspace_core.progress.emit_progress` — 进度协议

### Established Patterns
- 远程走 ssh -R 隧道 (端口 17890 固定 for HTTP, 17891 引入 for pushgateway)
- 远程命令 timeout 默认 12s, 失败 stderr sanitized (避免泄露 cred)
- CheckResult 模式: ok/severity/data/message/error 五字段

### Integration Points
- Phase 6 reach → 调 Phase 5 `net tunnel ensure` (强依赖)
- Phase 6 reach → 调 Phase 4 hw 数据 (可达性前提是 host 已知)
- Phase 6 reach → 为 Phase 8 data-collection 提供"先验通" 边界

</code_context>

<specifics>
## Specific Ideas

- 探测失败时**自动**调 `run_tunnel_ensure` (D-37.C1) 是关键 — 用户不必手动两步
- pushgateway 不是 out-of-the-box 启的, 必须在 Phase 6 范围内引入
- 测试 metric 用 gauge 不用 counter (语义"当前可达"而非"累计次数")

## Deferred Ideas

- 远程 → 本机 Grafana (3000) 探活 — 属于 Phase 9 report 范畴, 不入 Phase 6
- 多 tunnel 端口协商 / per-server 端口 — Phase 5 已固定 17890, 不动
- TLS / mTLS wandb 通信 — 内网自签证书, HTTP 足够, 不入 Phase 6

</specifics>

---

*Phase: 06-skill-05-service-reachability*
*Context gathered: 2026-06-12*

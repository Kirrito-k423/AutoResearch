# Requirements: AutoResearch v1.0 (M1 — 最小循环)

> REQ-ID 命名规则：`<组前缀>-<3位编号>`
> 每个 REQ 都是可观测、可被 UAT 验收的具体行为。
> 阶段分配见 ROADMAP.md；本文件只列"是什么"，不列"什么时候做"。

---

## REPO — 仓库本体

- [x] **REPO-01** — 仓根有 `README.md`，含项目哲学、quickstart、8 步循环概览
- [x] **REPO-02** — 仓根有 `AGENTS.md`，给 AI 协作者的"如何在这个仓工作"指南
- [x] **REPO-03** — 仓根有 `CLAUDE.md`，与 AGENTS.md 互补（Claude Code 专用）
- [x] **REPO-04** — 仓根有 `LICENSE` (MIT)
- [x] **REPO-05** — 仓根有 `.gitignore`（Python、macOS、IDE、secrets）

## SVC — 本地服务栈

- [x] **SVC-01** — `docker-compose.yml` 起 Archon server（web UI + API）
- [x] **SVC-02** — `docker-compose.yml` 起本地 wandb（`wandb local` 模式）
- [x] **SVC-03** — `docker-compose.yml` 起 Prometheus（带自监控 scrape config）
- [x] **SVC-04** — `docker-compose.yml` 起 Grafana（预置 datasources: prometheus + 本地 wandb）

## CORE — workspace-core 沉淀

- [x] **CORE-SSH-01** — 提供 `paramiko` 封装的 SSHClient，支持 connect/exec/sftp/reverse_tunnel
- [x] **CORE-SSH-02** — 支持按 `~/.ssh/config` 别名解析目标
- [x] **CORE-SSH-03** — SSH 操作统一有超时、重试、错误信息带主机名
- [x] **CORE-SEC-01** — 敏感字段（密码、token）使用系统 keyring 加密
- [x] **CORE-SEC-02** — 配置文件中敏感字段用占位符 `<keyring:xxx>` 引用
- [x] **CORE-CFG-01** — Pydantic schema 校验 config/config.yaml
- [x] **CORE-CFG-02** — 配置加载失败时给可读错误（哪个字段、为什么错）
- [x] **CORE-PROTO-01** — 进度协议：stderr 输出 `__AR_PROGRESS__=<json>` 标记
- [x] **CORE-PROTO-02** — 最终 stdout 必须是**唯一一个** JSON 对象
- [x] **CORE-LOG-01** — 统一日志格式：时间戳、level、host、msg、ctx
- [x] **CORE-LAYOUT-01** — 固定目录约定：`~/.autoresearch/runs/<run-id>/{logs,wandb,prom,manifest.json}`

## CFG — Skill 01: customer-config

- [x] **CFG-INIT-01** — `ar-config init` 生成 `config/config.yaml` 模板
- [x] **CFG-INIT-02** — 模板含中文注释，每个字段都有说明
- [x] **CFG-INIT-03** — 已存在 config 时拒绝覆盖（除非 `--force`）
- [x] **CFG-VAL-01** — `ar-config validate` 校验现有配置
- [x] **CFG-VAL-02** — 校验失败指出哪个字段、什么问题、怎么修
- [x] **CFG-SHOW-01** — `ar-config show` 打印配置（敏感字段脱敏）

## SVC-CHK — Skill 02: local-services-health

- [x] **SVC-CHK-STAT-01** — `ar-services status` 4 服务并发生存活性检查
- [x] **SVC-CHK-STAT-02** — 输出每个服务：name / url / healthy / latency_ms
- [x] **SVC-CHK-STAT-03** — `--json` 输出可机读
- [x] **SVC-CHK-START-01** — `ar-services start` 调 docker compose up
- [x] **SVC-CHK-STOP-01** — `ar-services stop` 调 docker compose down
- [x] **SVC-CHK-DEPS-01** — 缺 docker / docker compose 时给可读错误

## HW — Skill 03: server-hardware-probe

- [ ] **HW-CONN-01** — `ar-hw probe --server X` 通过 SSH 连上目标
- [ ] **HW-CONN-02** — 5s connect timeout，超时给可读错误
- [x] **HW-NPU-01** — 解析 `npu-smi info` 输出，列出所有 NPU 卡
- [x] **HW-NPU-02** — 每张卡含 id / name / memory_total / memory_used / temperature / utilization
- [x] **HW-NPU-03** — 解析失败 fallback 到 `lspci` 列出 NPU 设备
- [ ] **HW-OCC-01** — 解析 `npu-smi info` 中的 Processes 列，列出占用方
- [ ] **HW-OCC-02** — 占用方信息含 pid / user / process_name / memory_used
- [x] **HW-DRV-01** — 报告驱动版本（CANN / npu driver）

## NET — Skill 04: network-check

- [x] **NET-LOCAL-01** — `ar-net probe` 在本机测 baidu / huggingface / github 可达性
- [x] **NET-LOCAL-02** — 每个目标记录 status / http_code / latency_ms
- [x] **NET-LOCAL-03** — 可达性 + 测速（curl `--max-time 10 -w "%{speed_download}"`）
- [x] **NET-REMOTE-01** — `ar-net probe --server X` 在远程服务器上跑同样测速
- [x] **NET-REMOTE-02** — 远程测速时复用 workspace-core 的 SSH
- [x] **NET-REMOTE-03** — 输出"本地 vs 远程"对比矩阵
- [ ] **NET-TUNNEL-01** — 远程无外网时自动建 `ssh -R` 反向代理
- [ ] **NET-TUNNEL-02** — 隧道健康检查（每 30s 发心跳，重连可重试）

> 2026-06-09: 05-03 代码和自动测试已覆盖 NET-TUNNEL-01..02 的实现路径，但全部配置服务器真实网络/隧道 UAT 尚未通过，因此这两个 REQ 保持未完成。

## REACH — Skill 05: service-reachability

- [x] **REACH-WB-01** — `ar-reach test --server X` 测远程到本地 wandb 连通
- [x] **REACH-WB-02** — 用 04 隧道转发后 curl 本地 wandb /health
- [x] **REACH-PROM-01** — 测远程到本地 Prometheus 连通
- [x] **REACH-PROM-02** — 通过 pushgateway push 一个测试 metric 验证

## STACK — Skill 06: train-stack-health

- [x] **STACK-VERL-01** — `ar-stack check --server X` 检测 verl conda env
- [x] **STACK-VERL-02** — `conda env list | grep verl` + 解析版本
- [x] **STACK-VERL-03** — 跑 1-step 干跑（`python -c "import verl; verl.trainer.main(...)"` 最小 1 步）
- [x] **STACK-VEOMNI-01** — 同上对 veomni
- [x] **STACK-VEOMNI-02** — 同上 conda 检测
- [x] **STACK-VEOMNI-03** — 同上 1-step 干跑

## COLL — Skill 07: data-collection

- [x] **COLL-RUN-01** — `ar-collect run --server X --tag smoke-001` 跑一次最小实验
- [x] **COLL-RUN-02** — 实验在远程跑，日志同时落远程和本地
- [x] **COLL-WB-01** — 远程 wandb 离线模式 → `wandb sync` → 本地 wandb
- [x] **COLL-WB-02** — 同步后本地 wandb UI 可见
- [x] **COLL-LOG-01** — 远程 log tail + 实时拉回本地
- [x] **COLL-LOG-02** — 本地 log 与远程 log 内容一致
- [x] **COLL-PROM-01** — 远程通过 pushgateway 推资源指标到本地 Prometheus
- [x] **COLL-PROM-02** — 本地 Prometheus 可见 NPU/GPU 利用率
- [x] **COLL-MANIFEST-01** — 每次 run 写 `manifest.json` 含 run_id / start_time / end_time / server / wandb_url / log_path / prom_query

> 2026-06-15: Phase 8 已完成真实 UAT。A2-AK-225 的 `autoresearch collect run` 成功打通远程 1-step、本地 wandb sync、log 拉回、pushgateway → Prometheus、manifest 写入；见 `.planning/phases/08-skill-07-data-collection/08-UAT.md` 与 `08-VERIFICATION.md`。

## RPT — Skill 08: experiment-report

- [x] **RPT-MANIFEST-01** — 读 manifest.json 重建 run 全貌
- [x] **RPT-PAGE-01** — `ar-report render --run-id X` 出单页 HTML
- [x] **RPT-PAGE-02** — 报告含 log 摘要 / wandb 关键曲线 / 资源曲线
- [x] **RPT-PAGE-03** — `--open` 在浏览器打开
- [x] **RPT-LINK-01** — 报告里嵌入 wandb 链接和 Prometheus 链接

> 2026-06-15: Phase 9 已完成真实 UAT。基于 `01KV5MV7N5A3RBZ6388E5HCYAP` 的 `autoresearch report render` 成功生成 `report.html`，并通过 `--open` 在浏览器打开；见 `.planning/phases/09-skill-08-experiment-report/09-UAT.md` 与 `09-VERIFICATION.md`。

## ARCH — Archon 适配层

- [ ] **ARCH-WF-01** — 8 skill 各自有 `.archon/workflows/ar-skill-XX.yaml`
- [ ] **ARCH-WF-02** — YAML 节点可调用对应 skill 的 Python 入口
- [ ] **ARCH-WF-03** — YAML 含 `loop:` 节点支持 STACK 和 COLL 的迭代
- [ ] **ARCH-WF-MAIN-01** — 主 workflow `ar-min-loop.yaml` 串联 8 skill
- [ ] **ARCH-WF-MAIN-02** — 主 workflow 跑完产出 RPT 报告
- [ ] **ARCH-RUN-01** — `archon workflow run ar-min-loop` 可一键跑完整循环
- [ ] **ARCH-RUN-02** — 进度在 Archon Web UI 可见

## ORCH — 顶层 CLI 编排

- [ ] **ORCH-CHECK-01** — `autoresearch check all` 串跑 8 skill 的 check 部分
- [ ] **ORCH-CHECK-02** — 输出统一报告（哪个服务 / 哪个服务器 不健康）
- [ ] **ORCH-RUN-01** — `autoresearch run smoke --server X` 跑 COLL + RPT
- [ ] **ORCH-RUN-02** — 失败时给出诊断（哪一步挂了，为什么）
- [ ] **ORCH-LOG-01** — 所有 CLI 输出遵守 `__AR_PROGRESS__=` 协议

## E2E — 端到端验证

- [ ] **E2E-01** — 一次性 M1 全循环跑通（从空 config → 跑出 smoke 报告）
- [ ] **E2E-02** — E2E 跑出的报告能完整看到 log + wandb + prom 三视图
- [ ] **E2E-03** — E2E 跑出 `< 30 min`（在 demo 服务器上）
- [ ] **E2E-04** — E2E 全过程在 Archon Web UI 可观察

---

## REQ 总数

| 前缀 | 数量 | 阶段 |
|---|---|---|
| REPO | 5 | 01 |
| SVC | 4 | 01 |
| CORE | 11 | 02 |
| CFG | 6 | 03 |
| SVC-CHK | 6 | 01 |
| HW | 8 | 04 |
| NET | 8 | 05 |
| REACH | 4 | 06 |
| STACK | 6 | 07 |
| COLL | 9 | 08 |
| RPT | 5 | 09 |
| ARCH | 7 | 10 |
| ORCH | 5 | 11 |
| E2E | 4 | 12 |
| **合计** | **88** | 13 阶段（含 M1 归档） |

> 阶段映射详见 ROADMAP.md。

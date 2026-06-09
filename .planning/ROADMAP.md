# Roadmap: AutoResearch v1.0 (M1 — 最小循环)

## Milestones

- 🚧 **v1.0 MinViable Loop** — Phases 1-13 (in progress)
- 📋 **v1.1 Stable** — error resilience, multi-server, CI (planned)
- 📋 **v2.0 Distribute** — multi-node, scheduler, multi-cloud (planned)

## Milestone Goal (v1.0)

8 个 skill 全部独立可跑，能串成 `autoresearch check all` 和 `autoresearch run smoke` 一键完成"健康检查 + 跑最小实验 + 出报告"；同一套 skill 也能通过 `archon workflow run ar-min-loop` 触发。13 阶段、88 条 REQ 全部完成、E2E smoke < 30 min。

## Phases

### Phase 1: 仓骨架与本地服务栈

**Goal**: 仓 clone 下来 `docker compose up` 就起 4 个服务，并能 `autoresearch services status` 看到全绿。
**Depends on**: Nothing (first phase)
**Requirements**: REPO-01..05, SVC-01..04
**Success Criteria** (what must be TRUE):

  1. 仓根有 README / AGENTS / CLAUDE / LICENSE / .gitignore
  2. `docker compose up -d` 起 Archon / wandb / Prometheus / Grafana
  3. 4 个服务 `/healthz` 端点全 200
  4. `autoresearch services status` 输出 4 行全 healthy

**Plans**: 4 plans
Plans:

- [x] 01-01: 仓根文档（README + AGENTS + CLAUDE + LICENSE + .gitignore）
- [x] 01-02: docker-compose.yml 4 服务 + .env.example + 启动脚本
- [x] 01-03: `autoresearch services` CLI 子命令（status / start / stop）
- [x] 01-04: UAT gap closure（start / stop 的 `--lang en` 错误文案）

### Phase 2: workspace-core 沉淀

**Goal**: 三大沉淀层 (workspace-core / verl-workspace-adapter / datalake) 的 workspace-core 部分跑通；`ar-ping` 命令验证 SSH 端到端。
**Depends on**: Phase 1
**Requirements**: CORE-SSH-01..03, CORE-SEC-01..02, CORE-CFG-01..02, CORE-PROTO-01..02, CORE-LOG-01, CORE-LAYOUT-01
**Success Criteria**:

  1. SSH client 可连 demo 服务器并跑 `echo ok`
  2. 配置文件用 Pydantic 校验，错误信息含字段名
  3. 敏感字段在文件里是 `<keyring:xxx>` 占位符
  4. 任何 skill 跑出来的进度都走 `__AR_PROGRESS__=` 协议
  5. 固定目录 layout 被 skill 写入时自动创建

**Plans**: 4 plans

Plans:

- [x] 02-01: workspace-core/ssh/ (paramiko 客户端 + reverse tunnel)
- [x] 02-02: workspace-core/secrets/ + workspace-core/config/ (keyring + Pydantic)
- [x] 02-03: workspace-core/progress/ + log/ + layout/ (协议 + 格式 + 目录)
- [x] 02-04: `ar-ping` CLI 端到端冒烟（A2-AK-225 真机 SSH + 反向隧道已验收）

### Phase 3: Skill 01 — customer-config

**Goal**: 用户能用一个命令生成、校验、查看配置；敏感字段不裸奔。
**Depends on**: Phase 2
**Requirements**: CFG-INIT-01..03, CFG-VAL-01..02, CFG-SHOW-01
**Success Criteria**:

  1. `ar-config init` 在空目录生成带中文注释的 yaml
  2. 重复 init 不覆盖
  3. `ar-config validate` 失败指出具体字段
  4. `ar-config show` 密码字段显示为 `***`

**Plans**: 2 plans

Plans:

- [x] 03-01: `ar-config init` + `ar-config validate`
- [x] 03-02: `ar-config show` + keyring 集成

### Phase 4: Skill 03 — server-hardware-probe

**Goal**: 给定服务器名，输出 NPU 列表 + 显存 + 占用方 + 驱动版本。
**Depends on**: Phase 2
**Requirements**: HW-CONN-01..02, HW-NPU-01..03, HW-OCC-01..02, HW-DRV-01
**Success Criteria**:

  1. `ar-hw probe --server X` 连上服务器
  2. JSON 含每张 NPU 的 id/name/memory/temp/util
  3. JSON 含占用方 (pid/user/proc/mem)
  4. 驱动版本字段填好
  5. `npu-smi` 解析失败时 fallback 到 lspci

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 04-01: 单服务器纵向切片（SSH → npu-smi → 核心指标 → JSON CLI）

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02: 多版本解析、驱动信息、lspci fallback 与失败诊断

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 04-03: 占用进程、`--all` 有界并发与全部真实服务器验收

### Phase 5: Skill 04 — network-check

**Goal**: 本地和远程两边的网络矩阵都查，自动建反向代理，隧道可重试。
**Depends on**: Phase 2
**Requirements**: NET-LOCAL-01..03, NET-REMOTE-01..03, NET-TUNNEL-01..02
**Success Criteria**:

  1. 本机测 baidu/hf/github 三个目标
  2. 远程服务器跑同样测速
  3. 输出"本地 vs 远程"对比表
  4. 远程无网时自动建 `ssh -R` 隧道
  5. 隧道心跳保活，断了重连

**Plans**: 3 plans
Plans:
**Wave 1**

- [ ] 05-01: 本机 + 远程测速 (curl)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 05-02: SSH 反向代理通道 (paramiko)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 05-03: 隧道心跳 + 重试

### Phase 6: Skill 05 — service-reachability

**Goal**: 验证远程服务器能通过隧道访问本地 wandb / Prometheus。
**Depends on**: Phase 5
**Requirements**: REACH-WB-01..02, REACH-PROM-01..02
**Success Criteria**:

  1. 远程 curl 本地 wandb /health 200
  2. 远程通过 pushgateway push 一个测试 metric
  3. 隧道挂了给可读错误并提示先跑 05

**Plans**: 2 plans

Plans:

- [ ] 06-01: 远程 → 本地 wandb 探活
- [ ] 06-02: 远程 → 本地 Prometheus pushgateway 探活

### Phase 7: Skill 06 — train-stack-health

**Goal**: 远程服务器 verl + veomni 各自的 conda env 健康，能跑 1-step 干跑。
**Depends on**: Phase 2
**Requirements**: STACK-VERL-01..03, STACK-VEOMNI-01..03
**Success Criteria**:

  1. `ar-stack check --server X` 同时检查 verl 和 veomni
  2. conda env 名称和 Python 版本报告出来
  3. 各跑一次 1-step 干跑（30s timeout）
  4. 失败给可读错误（conda env 缺失 / 路径错 / import 失败）

**Plans**: 3 plans

Plans:

- [ ] 07-01: 复用 workspace-core SSH + conda env 探测
- [ ] 07-02: verl 1-step 干跑
- [ ] 07-03: veomni 1-step 干跑

### Phase 8: Skill 07 — data-collection

**Goal**: 在远程跑一次最小实验，3 路数据（wandb/log/prom）都落到本地固定目录。
**Depends on**: Phase 6 + Phase 7
**Requirements**: COLL-RUN-01..02, COLL-WB-01..02, COLL-LOG-01..02, COLL-PROM-01..02, COLL-MANIFEST-01
**Success Criteria**:

  1. 远程跑训练（verl 或 veomni 1 步）
  2. 远程 wandb 离线模式 → 本地 wandb sync
  3. log 实时拉回本地
  4. 远程 prom pushgateway → 本地 Prometheus
  5. 写 manifest.json

**Plans**: 4 plans

Plans:

- [ ] 08-01: minimal-runner 抽象 + verl/veomni 实例
- [ ] 08-02: datalake/wandb/sync.py 离线→本地
- [ ] 08-03: datalake/logs/collector.py 实时拉
- [ ] 08-04: datalake/prometheus/push_gateway.py + manifest 写入

### Phase 9: Skill 08 — experiment-report

**Goal**: 给定 run-id，出一份单页 HTML，能看到 log / wandb / prom 三视图。
**Depends on**: Phase 8
**Requirements**: RPT-MANIFEST-01, RPT-PAGE-01..03, RPT-LINK-01
**Success Criteria**:

  1. `ar-report render --run-id X` 生成 `~/.autoresearch/runs/<id>/report.html`
  2. 报告嵌入 log 摘要、wandb 关键曲线、prom 资源曲线
  3. 报告里有 wandb 和 Prometheus 的跳转链接
  4. `--open` 在浏览器打开

**Plans**: 2 plans

Plans:

- [ ] 09-01: 读 manifest + 收集三路数据
- [ ] 09-02: HTML 模板 + 嵌入图表 + 浏览器打开

### Phase 10: Archon 适配层

**Goal**: 8 skill 各自有 Archon workflow YAML；主 workflow `ar-min-loop.yaml` 串联 8 skill。
**Depends on**: Phase 9
**Requirements**: ARCH-WF-01..03, ARCH-WF-MAIN-01..02, ARCH-RUN-01..02
**Success Criteria**:

  1. 8 个 `.archon/workflows/ar-skill-XX.yaml` 文件存在
  2. 每个 YAML 节点可调对应 skill 入口
  3. 主 workflow `ar-min-loop.yaml` 跑通
  4. `archon workflow run ar-min-loop` 触发整循环
  5. 进度在 Archon Web UI 可见

**Plans**: 3 plans

Plans:

- [ ] 10-01: 8 skill 各自打包成 Archon workflow YAML
- [ ] 10-02: 主 workflow ar-min-loop.yaml 串联
- [ ] 10-03: 在 Archon Web UI 验证可触发 + 可观察

### Phase 11: 顶层 CLI 编排

**Goal**: `autoresearch check all` 和 `autoresearch run smoke` 一键完成多 skill 串联。
**Depends on**: Phase 10
**Requirements**: ORCH-CHECK-01..02, ORCH-RUN-01..02, ORCH-LOG-01
**Success Criteria**:

  1. `autoresearch check all` 串跑 8 skill 的 check 部分
  2. `autoresearch run smoke --server X` 跑 COLL + RPT
  3. 失败时指出哪一步、为什么
  4. 所有 CLI 输出走 `__AR_PROGRESS__=` 协议

**Plans**: 2 plans

Plans:

- [ ] 11-01: `autoresearch check all` 编排器
- [ ] 11-02: `autoresearch run smoke` 编排器 + 失败诊断

### Phase 12: E2E 端到端 smoke

**Goal**: 一次性从空 config 跑完整循环，报告能完整看到 log + wandb + prom 三视图。
**Depends on**: Phase 11
**Requirements**: E2E-01..04
**Success Criteria**:

  1. 全新 clone + 全新 config + 跑 `autoresearch run smoke` 一次出报告
  2. 报告里 log 摘要 / wandb 曲线 / prom 资源 都可见
  3. 全过程 < 30 min
  4. Archon Web UI 全程可观察

**Plans**: 2 plans

Plans:

- [ ] 12-01: E2E 测试脚本（脚本化整个 M1 流程）
- [ ] 12-02: 报告完整性检查（断言 3 视图都齐）

### Phase 13: M1 归档

**Goal**: 跑完 `gsd-complete-milestone` 归档当前里程碑，更新 STATE.md。
**Depends on**: Phase 12
**Requirements**: 无新增 REQ
**Success Criteria**:

  1. ROADMAP 中 v1.0 标记为 ✅ shipped
  2. STATE.md 记录"v1.0 MinViable Loop 已归档"
  3. `.planning/milestones/v1.0/` 包含归档快照
  4. 准备进入 v1.1 规划

**Plans**: 1 plan

Plans:

- [ ] 13-01: 跑 `gsd-complete-milestone`，准备 v1.1

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → ... → 13

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. 仓骨架与本地服务栈 | 4/4 | Complete   | 2026-06-09 |
| 2. workspace-core 沉淀 | 4/4 | Complete   | 2026-06-09 |
| 3. Skill 01: customer-config | 2/2 | Complete   | 2026-06-09 |
| 4. Skill 03: server-hardware-probe | 2/3 | In Progress|  |
| 5. Skill 04: network-check | 0/3 | Not started | - |
| 6. Skill 05: service-reachability | 0/2 | Not started | - |
| 7. Skill 06: train-stack-health | 0/3 | Not started | - |
| 8. Skill 07: data-collection | 0/4 | Not started | - |
| 9. Skill 08: experiment-report | 0/2 | Not started | - |
| 10. Archon 适配层 | 0/3 | Not started | - |
| 11. 顶层 CLI 编排 | 0/2 | Not started | - |
| 12. E2E 端到端 smoke | 0/2 | Not started | - |
| 13. M1 归档 | 0/1 | Not started | - |

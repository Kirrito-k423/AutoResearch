# Phase 1: 仓骨架与本地服务栈 - Context

**Gathered:** 2026-06-06
**Status:** Ready for planning

<domain>
## Phase Boundary

仓 clone 下来能 `archon serve && docker compose -f services/X/compose.yml up -d` 起 4 服务（Archon + wandb + Prometheus + Grafana），并能 `autoresearch services status` 看到全绿。本阶段只交付"仓能跑起来 + 4 服务健康可探测"，不交付任何 skill 业务逻辑（skill 在 Phase 3-10 单独做）。
</domain>

<decisions>
## Implementation Decisions

### README 调性 — D-01
- **D-01:** README.md ≤ 80 行，纯宣言式（哲学 + 1 行 quickstart + LICENSE 链接 + 文档引用）
- **D-01a:** 不放 badges / FAQ / Contributing / Changelog（M1 不需要）
- **D-01b:** 8 步循环的详细描述留在 `.planning/ROADMAP.md`，README 只放一行精神

### 文档分工 — D-02
- **D-02:** 写一份 `AGENTS.md`（所有 AI 协作者都看），内容含：仓约定 / 8 步循环 / 三沉淀层 / 进度协议 / 测试规范
- **D-02a:** `CLAUDE.md` 是 `AGENTS.md` 的**相对路径** symlink（`AGENTS.md` → 同名文件，git 可追踪，跨机器不坏）
- **D-02b:** 单源真相，AGENTS.md 更新即两处生效

### 本地服务编排 — D-03
- **D-03:** 每服务一个 `docker-compose.yml`，放在 `services/<name>/compose.yml` 子目录里
- **D-03a:** `services/` 目录结构：
  ```
  services/
  ├── README.md              # 4 服务总览
  ├── archon/                # 5A 决定：只有 README.md 指向 archon.diy
  ├── wandb/{compose.yml, README.md}
  ├── prometheus/{compose.yml, prometheus.yml, README.md}
  └── grafana/{compose.yml, datasources.yml, README.md}
  ```
- **D-03b:** `autoresearch services start` 串行调 `docker compose -f services/X/compose.yml up -d`（不并行，避免端口竞争时的告警噪声）
- **D-03c:** 端口固定：wandb 8080 / Prometheus 9090 / Grafana 3000 / Archon 8088
- **D-03d:** Prometheus 自监控 scrape config：`prometheus.yml` 里 scrape 它自己
- **D-03e:** Grafana 预置两个 datasource：Prometheus (http://prometheus:9090) + 本地 wandb (http://host.docker.internal:8080)

### CLI 入口 — D-04
- **D-04:** 单 Python 包 `autoresearch/`，单二进制 `autoresearch`，所有子命令挂一棵 click 树
- **D-04a:** 入口：`python -m autoresearch`（`autoresearch/__main__.py`），同时通过 `pyproject.toml` 的 `[project.scripts]` 暴露 `autoresearch` 命令
- **D-04b:** CLI 形态：`autoresearch [group] [command] [args]`
  - M1 实现：`autoresearch services {status,start,stop}` (Phase 1 范围)
  - 后续 8 个 skill 各自挂对应 group：`autoresearch config|hw|net|reach|stack|collect|report`
- **D-04c:** 框架选 Python `click`（PROJECT.md 已锁定）
- **D-04d:** 进度协议 `__AR_PROGRESS__=<json>` on stderr（PROJECT.md Key Decisions 锁定）
- **D-04e:** 最终 stdout 必须是唯一一个 JSON 对象（默认行为；M1 阶段 01-03 子命令可放宽为人读 + `--json` flag）

### Archon 集成 — D-05
- **D-05:** Archon **不**在我们的 docker-compose 里；由用户通过 `archon serve` 单独起
- **D-05a:** `services/archon/` 目录只有 `README.md`（指向 archon.diy 安装说明 + `archon serve` 启动方式）
- **D-05b:** `autoresearch services status` 仍查 4 服务（包括 Archon via `http://localhost:8088/healthz`）
- **D-05c:** `autoresearch services start` 启动 wandb/prometheus/grafana 3 个 compose 服务，**不**起 Archon
  - 输出明确"Archon: not managed by autoresearch, run `archon serve` to start"
- **D-05d:** Archon 安装是用户进入 Phase 1 之前的**前置条件**（在 README quickstart 写明）

### SVC-01 修订 — D-06
- **D-06:** REQUIREMENTS.md 的 **SVC-01** 修订为：
  > SVC-01 — Archon 启动由 `archon serve` 控制（不在我们的 docker-compose 里），需单独安装 `archon` CLI 到 PATH
- **D-06a:** 下游 SVC-CHK-* REQ（Phase 4）无变更，按 5A 行为工作

### the agent's Discretion
- CLI 错误信息的中英混杂（默认中文，--lang en 切英文）— 自由决定
- 单测 vs 集测的覆盖比例（M1 阶段 01 可只做单测）— 自由决定
- `start.sh` 脚本的存在与否（M1 可以直接文档化命令，不必有脚本）— 自由决定

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目级
- `.planning/PROJECT.md` — 哲学、Core Value、Active/Out of Scope、Constraints、Key Decisions
- `.planning/REQUIREMENTS.md` — 88 条 REQ 跨 14 组；本阶段取 REPO-01..05 + SVC-01..04
- `.planning/ROADMAP.md` — Phase 1 目标 / 依赖 / 成功标准 / 3 个 plan

### 领域参考
- `diagram/autoresearch_arch.svg` — 4 列架构图（左：主工作区 / 中：PI Agent / 右：数据湖 + 侧栏）
- `~/.codex/get-shit-done/templates/` — GSD 阶段模板（如需复刻）
- Archon 文档：https://archon.diy/（`archon serve` 用法、`/healthz` 端点）
- wandb 本地模式：https://docs.wandb.ai/guides/hosting（`wandb local` 启动方式）
- Prometheus 自监控：https://prometheus.io/docs/prometheus/latest/configuration/configuration/#configuration-file
- Grafana provisioning datasources：https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources

### 进度协议（PROJECT.md Key Decisions 锁定）
- `__AR_PROGRESS__=<json>` 写 stderr，最终 stdout 唯一 JSON 对象
- 模板可参考 vllm-ascend-workspace 的 `__VAWS_REMOTE_TOOLBOX_PROGRESS__` 模式

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `diagram/gen.py` — 已有 Python 脚本生成 SVG 架构图；M1 不重用，但未来报告生成可参考其结构

### Established Patterns
- **greenfield 仓** — 无既有代码可集成；新写的所有 Python 包都按以下布局：
  ```
  autoresearch/
  ├── __init__.py
  ├── __main__.py
  ├── cli.py              # @click.group()
  ├── services/           # M1 范围
  │   ├── __init__.py
  │   ├── status.py
  │   ├── start.py
  │   └── stop.py
  └── ...
  ```

### Integration Points
- 与外部（Archon / wandb / Prometheus / Grafana）通过 HTTP healthz 探活
- 与用户通过 click CLI 交互

</code_context>

<specifics>
## Specific Ideas

- README quickstart 一行 = 5 步：`git clone && cd autoresearch && ./scripts/start.sh && archon serve && autoresearch services status`
- 实际上 `./scripts/start.sh` 可省（直接文档化三条 `docker compose up`），但脚本化更友好
- `autoresearch services start` 走 `subprocess.run(["docker", "compose", "-f", path, "up", "-d"])` 而非 `docker-compose` 旧命令（用 v2 plugin）
- 4 服务并发 status 查询用 `concurrent.futures.ThreadPoolExecutor`
- status 输出格式（人读）：
  ```
  NAME             URL                              HEALTHY   LATENCY_MS
  archon           http://localhost:8088            ✓         42
  wandb            http://localhost:8080            ✓         38
  prometheus       http://localhost:9090            ✓         51
  grafana          http://localhost:3000            ✓         67
  ```
- `--json` 输出（机读）：
  ```json
  {"services": [{"name": "archon", "url": "...", "healthy": true, "latency_ms": 42}, ...], "summary": {"total": 4, "healthy": 4, "unhealthy": 0}}
  ```

</specifics>

<deferred>
## Deferred Ideas

- **多用户/多租户** — M2+；Phase 1 单用户单本机
- **Web UI 自研** — 复用 Archon Web UI + wandb + Grafana，不造轮子
- **CI/CD** — Phase 1 不配置 GitHub Actions；M1.1 再说
- **服务 TLS** — 本地 localhost，不上 TLS
- **多 docker-compose profile（dev/prod）** — M1 只有 dev 配置

</deferred>

---
*Last updated: 2026-06-06 after $gsd-discuss-phase 1*

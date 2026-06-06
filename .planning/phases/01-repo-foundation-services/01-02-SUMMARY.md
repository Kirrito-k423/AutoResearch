---
phase: 01-repo-foundation-services
plan: 02
subsystem: infra
tags: [docker, docker-compose, wandb, prometheus, grafana, archon, env]

# Dependency graph
requires:
  - phase: 01-repo-foundation-services / plan 01
    provides: "仓根骨架 + 仓约定 (AGENTS.md) + D-03/D-05 决策"
provides:
  - "4 服务隔离 docker-compose (wandb / prometheus / grafana)"
  - "Archon 走外部 install (services/archon/ 只有 README)"
  - "Prometheus self-scrape 配置 (D-03d)"
  - "Grafana provisioning datasources (Prometheus + host.docker.internal wandb)"
  - "端口变量化模板 (.env.example)"
affects: [02-workspace-core, 04-skill-local-services-health, all 8 skill phases]

# Tech tracking
tech-stack:
  added:
    - docker-compose v2 (verified config -q)
    - wandb/local:0.17.5
    - prom/prometheus:v2.51.0
    - grafana/grafana:10.4.0
  patterns:
    - "每服务一个独立 compose.yml 在 services/<name>/ 子目录"
    - "端口用 ${PORT_X:-default} 变量化"
    - "Archon 不在 compose — D-05 锁定"
    - "Grafana 用 host.docker.internal 连 Mac 主机 (RESEARCH Pitfall 1)"

key-files:
  created:
    - services/README.md
    - services/archon/README.md
    - services/wandb/compose.yml
    - services/wandb/README.md
    - services/prometheus/compose.yml
    - services/prometheus/prometheus.yml
    - services/prometheus/README.md
    - services/grafana/compose.yml
    - services/grafana/datasources.yml
    - services/grafana/README.md
    - .env.example
  modified:
    - .gitignore (fix: !services/wandb/ 反向放行)

key-decisions:
  - "D-03: 每服务一个独立 compose.yml"
  - "D-03a: services/{archon,wandb,prometheus,grafana} 4 子目录"
  - "D-03c: 端口固定 wandb 8080 / Prom 9090 / Grafana 3000 / Archon 8088"
  - "D-03d: Prometheus self-scrape (容器内 localhost:9090)"
  - "D-03e: Grafana 预置 Prometheus + wandb 两个 datasource"
  - "D-05: Archon 不在 compose (services/archon/ 只有 README)"
  - "D-06: SVC-01 修订为「Archon 由 archon serve 控制」"

patterns-established:
  - "服务间容器名引用: 'http://prometheus:9090' (同 compose 网络容器名)"
  - "Mac 主机引用: 'http://host.docker.internal:PORT'"
  - "D-05 反模式: 不为外部 CLI 工具 (archon) 写 compose.yml"

requirements-completed: [SVC-01, SVC-02, SVC-03, SVC-04]

# Metrics
duration: 10min
completed: 2026-06-06
---

# Phase 01 / Plan 02: 本地服务栈 Summary

**4 服务 (wandb/prometheus/grafana/archon-stub) compose + 端口变量化模板就位；Archon 走外部 install；3 个 compose 全部 `docker compose config -q` 验证通过；SVC-01..04 全部满足。**

## Performance

- **Duration:** 10 min
- **Started:** 2026-06-06T08:06:00Z
- **Completed:** 2026-06-06T08:16:00Z
- **Tasks:** 7/7
- **Files modified:** 12 (11 created + 1 .gitignore fix)

## Accomplishments

- 4 服务目录就位：`services/{archon,wandb,prometheus,grafana}`
- 3 个独立 `docker-compose.yml` (`wandb` / `prometheus` / `grafana`) + `archon/` 无 compose (D-05 锁定)
- Prometheus self-scrape `localhost:9090` (D-03d)
- Grafana 双 datasource provisioning：Prometheus (`http://prometheus:9090`) + wandb (`http://host.docker.internal:${PORT_WANDB:-8080}`)
- `.env.example` 4 端口变量：`PORT_WANDB=8080` / `PORT_PROMETHEUS=9090` / `PORT_GRAFANA=3000` / `PORT_ARCHON=8088`
- 3 个 compose 全部 `docker compose config -q` 验证通过

## Task Commits

1. **Task 2.1: services/README.md** — 包含在 commit `270d25e` 内
2. **Task 2.2: services/archon/README.md** — 包含在 commit `270d25e` 内
3. **Task 2.3: services/wandb/{compose.yml, README.md}** — 包含在 commit `270d25e` 内
4. **Task 2.4: services/prometheus/{compose.yml, prometheus.yml, README.md}** — 包含在 commit `270d25e` 内
5. **Task 2.5: services/grafana/{compose.yml, datasources.yml, README.md}** — 包含在 commit `270d25e` 内
6. **Task 2.6: .env.example** — 包含在 commit `270d25e` 内
7. **Task 2.7: git add + commit** — `270d25e` (feat(01): add local services stack)

**Plan metadata:** `79b5aab` (fix(01-01): .gitignore 排除 wandb/ 时放过 services/wandb/)

## Files Created/Modified

- `services/README.md` (38 行) — 4 服务总览 + 端口矩阵 + 启动顺序 + 已知约束
- `services/archon/README.md` (56 行) — D-05 锁定说明 + 外部安装步骤 + 故障排查
- `services/wandb/compose.yml` (19 行) — `wandb/local:0.17.5` 端口 8080 + `wandb-data` volume
- `services/wandb/README.md` (34 行) — 启动 + 验证 (含 wandb `/healthz` 端点不确定性提示)
- `services/prometheus/prometheus.yml` (17 行) — `scrape_configs: [prometheus self-scrape localhost:9090]`
- `services/prometheus/compose.yml` (23 行) — `prom/prometheus:v2.51.0` 端口 9090 + 挂载 prometheus.yml
- `services/prometheus/README.md` (41 行) — 启动 + self-scrape 验证 (UI Status > Targets)
- `services/grafana/datasources.yml` (22 行) — 预置 Prometheus (default) + wandb (host.docker.internal)
- `services/grafana/compose.yml` (22 行) — `grafana/grafana:10.4.0` 端口 3000 + provisioning
- `services/grafana/README.md` (47 行) — 启动 + datasources 验证 + host.docker.internal Mac 限定
- `.env.example` (15 行) — 4 端口变量模板 (D-03c 默认值)
- `.gitignore` — 加 `!services/wandb/` 反向放行

## Decisions Made

执行期间 D-03 / D-03a / D-03c / D-03d / D-03e / D-05 / D-06 全部按 plan 落地，无新增决策。

## Deviations from Plan

### Auto-fixed Issues

**1. [Cross-Plan .gitignore Bug] wandb/ 规则误匹配 services/wandb/**

- **Found during:** Task 2.7 (git add services/ 时，wandb 子目录被 .gitignore 拦截)
- **Issue:** `.gitignore` 第 67 行 `wandb/` 是 plan 01-01 写的项目特有规则，但 `.gitignore` 规则对**整仓匹配**，把 `services/wandb/` 目录也排除了
- **Fix:** 在 `wandb/` 之后加一行 `!services/wandb/` 反向放行
- **Files modified:** `.gitignore` (1 行新增)
- **Verification:** `git add services/wandb/compose.yml` 不再警告忽略
- **Committed in:** `79b5aab` (独立 fix commit，不混入 feat commit)

**Total deviations:** 1 auto-fixed (跨 plan 边界)
**Impact on plan:** 必要修复，否则 plan 01-02 核心产物无法 commit。无 scope creep。

## Issues Encountered

执行期间发现 plan 01-01 的 .gitignore 误把 `services/wandb/` 排除；已用 `!services/wandb/` 反向放行修复，并以独立 fix commit 提交，不污染 01-02 的 feat commit。

## User Setup Required

**External CLI require manual installation:**

- **Archon CLI** — 必须前置安装 (走 `archon serve` 启动，不在 compose)
  ```bash
  brew install archon
  # 或见 https://archon.diy/
  ```
  详细见 [services/archon/README.md](../../services/archon/README.md)
- **Docker Desktop for Mac** — 3 个 compose 服务依赖 (wandb/prometheus/grafana)
- **复制 .env.example 为 .env** — 仅在需要覆盖默认端口时

## Next Phase Readiness

- ✅ 4 服务目录骨架就位
- ✅ Archon 决策与 4 服务隔离清晰
- ✅ Prometheus/Grafana 互联通过容器名 + 端口变量化
- ⏭  Plan 03: `autoresearch services` CLI (status/start/stop) — 准备执行
  - `_common.py` 需定义 4 服务 URL + `/healthz` 端点常量
  - `start.py` 串行调 3 个 compose up
  - `status.py` 并发查 4 服务 `/healthz` 输出 4 行表 / JSON

---
*Phase: 01-repo-foundation-services / Plan 02*
*Completed: 2026-06-06*

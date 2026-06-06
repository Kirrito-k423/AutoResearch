---
phase: 01-repo-foundation-services
plan: 03
subsystem: cli
tags: [cli, click, services, healthz, docker-compose, pytest, uv]

# Dependency graph
requires:
  - phase: 01-repo-foundation-services / plan 01
    provides: "AGENTS.md 仓约定 + D-04 决策 (click + 树状子命令)"
  - phase: 01-repo-foundation-services / plan 02
    provides: "services/{wandb,prometheus,grafana}/compose.yml 路径 + .env.example 端口变量"
provides:
  - "autoresearch Python CLI (单二进制入口)"
  - "services 子命令组: status / start / stop"
  - "4 服务并发 healthz 探测 (ThreadPoolExecutor)"
  - "端口固定 (8088/8080/9090/3000) — D-03c 落地"
  - "缺 docker / 缺 compose 文件可读中文错误"
  - "11 个 pytest 单测 (CLI smoke + status 行为 + start/stop 错误路径)"
affects: [02-workspace-core, 04-skill-local-services-health, all 8 skill phases]

# Tech tracking
tech-stack:
  added:
    - click 8.4.1 (CLI 框架)
    - requests 2.34.2 (HTTP 探测)
    - pytest 9.0.3 (测试)
    - pytest-cov 7.1.0
    - hatchling (build backend)
  patterns:
    - "@click.group() + @main.group() + @services.command() 树状子命令"
    - "run_status / run_start / run_stop 返回 int (exit code: 0/1/2)"
    - "concurrent.futures.ThreadPoolExecutor 并发探测"
    - "TypedDict (HealthResult) 描述结果 schema"
    - "--json 输出是唯一 stdout JSON 对象; 摘要走 stderr"
    - "缺 docker 用 shutil.which 探活, 给出可读中文错误"

key-files:
  created:
    - pyproject.toml
    - uv.lock
    - autoresearch/__init__.py
    - autoresearch/__main__.py
    - autoresearch/cli.py
    - autoresearch/services/__init__.py
    - autoresearch/services/_common.py
    - autoresearch/services/status.py
    - autoresearch/services/start.py
    - autoresearch/services/stop.py
    - tests/__init__.py
    - tests/test_cli.py
    - tests/test_status.py
    - tests/test_start_stop.py
  modified: []

key-decisions:
  - "D-04: click 树状子命令 (autoresearch → services → {status,start,stop})"
  - "D-04a: __main__.py 入口 + pyproject.toml [project.scripts] 双入口"
  - "D-04b: services group 形态: autoresearch services {status,start,stop}"
  - "D-04d: 进度协议 __AR_PROGRESS__=<json> on stderr (Phase 2 落实现)"
  - "D-04e: 最终 stdout 唯一 JSON 对象 (默认行为, --json 强制)"
  - "D-03b: start/stop 串行 (避免端口竞争告警噪声)"
  - "D-05/D-05c: start/stop 不含 archon, 输出明确提示"
  - "D-06: SVC-01 行为 — Archon 在 start 时不被启动, 状态仍查 /healthz"

patterns-established:
  - "M1 阶段 CLI 子命令返回 int (0/1/2), click.exceptions.Exit(code) 抛退出"
  - "default zh, --lang en 切英文 — 全 3 子命令统一"
  - "concurrent.futures 是 stdlib 探活首选 — 无第三方依赖"
  - "subprocess.run + check=False + capture_output=True 调 docker compose"

requirements-completed: [SVC-CHK-STAT-01, SVC-CHK-STAT-02, SVC-CHK-STAT-03, SVC-CHK-START-01, SVC-CHK-STOP-01, SVC-CHK-DEPS-01]

# Metrics
duration: 15min
completed: 2026-06-06
---

# Phase 01 / Plan 03: autoresearch CLI Summary

**autoresearch Python CLI (click 树状子命令) 就位；services {status,start,stop} 全部实现；4 服务并发 healthz 探测；11 个 pytest 单测全绿；SVC-CHK-* 全部满足。**

## Performance

- **Duration:** 15 min
- **Started:** 2026-06-06T08:17:00Z
- **Completed:** 2026-06-06T08:32:00Z
- **Tasks:** 9/9
- **Files modified:** 14 (all new)

## Accomplishments

- `autoresearch` 单二进制 CLI 入口就位（`uv run autoresearch`）
- 树状子命令：`autoresearch [services] [{status,start,stop}]`
- `autoresearch services status` — 人读 4 行表 / `--json` 唯一 JSON 对象
- `autoresearch services start` — 串行调 3 个 `docker compose up -d`；缺 docker 返 2 + 中文错误
- `autoresearch services stop` — 串行调 3 个 `docker compose down`
- 4 服务健康探测 URL 端口固定（archon 8088 / wandb 8080 / prometheus 9090 / grafana 3000）
- 11 个 pytest 单测 PASS（CLI smoke + status 行为 + start/stop 错误路径）

## Task Commits

1. **Task 3.1: pyproject.toml + uv.lock** — 包含在 commit `9ee922a` 内
2. **Task 3.2: __init__ / __main__ / cli** — 包含在 commit `9ee922a` 内
3. **Task 3.3: _common.py (ThreadPoolExecutor)** — 包含在 commit `9ee922a` 内
4. **Task 3.4: status.py (人读 + --json)** — 包含在 commit `9ee922a` 内
5. **Task 3.5: start.py (serial up)** — 包含在 commit `9ee922a` 内
6. **Task 3.6: stop.py (serial down)** — 包含在 commit `9ee922a` 内
7. **Task 3.7: services/__init__.py** — 包含在 commit `9ee922a` 内
8. **Task 3.8: tests/ (11 单测)** — 包含在 commit `9ee922a` 内
9. **Task 3.9: git add + commit** — `9ee922a` (feat(01): add autoresearch CLI)

## Files Created/Modified

- `pyproject.toml` (35 行) — uv-managed, click/requests/pytest 依赖, autoresearch script entry
- `uv.lock` — lockfile (16 packages)
- `autoresearch/__init__.py` — `__version__ = "0.1.0"`
- `autoresearch/__main__.py` — `python -m autoresearch` 入口
- `autoresearch/cli.py` (75 行) — `@click.group` + `services` group + 3 commands
- `autoresearch/services/__init__.py` — 包标记
- `autoresearch/services/_common.py` (~70 行) — `SERVICES` 常量 + `check_one` + `check_all` (ThreadPoolExecutor)
- `autoresearch/services/status.py` (69 行) — `_print_human` / `_print_json` / `run_status`
- `autoresearch/services/start.py` (92 行) — `_check_docker` + `_run_compose_up` + `run_start`
- `autoresearch/services/stop.py` (89 行) — 与 start.py 对称的 down 版本
- `tests/__init__.py` — 空包标记
- `tests/test_cli.py` — 3 个 CLI smoke 测试 (--version/--help/services --help)
- `tests/test_status.py` — 4 个测试 (SERVICES 常量/check_all/status --json/status human)
- `tests/test_start_stop.py` — 4 个测试 (docker 缺失返 2/--help 不崩)

## Decisions Made

执行期间 D-04 / D-04a / D-04b / D-04d / D-04e / D-03b / D-05 / D-05c / D-06 全部按 plan 落地，无新增决策。

## Deviations from Plan

**None — plan executed exactly as written.**

所有 9 个 task 的内容与 plan 一致：源码 + 测试均按模板编写，verification 步骤一次通过（v1-v8 全部 ✓）。

## Issues Encountered

None — plan 01-03 的 8 项 verification 一次通过：

```
[v1] autoresearch --version: 0.1.0                    ✓
[v2] services --help: start/status/stop 3 子命令      ✓
[v3] status human output: 5 行 (1 header + 4 服务)    ✓
[v4] status --json: services=4, summary={total:4,...}  ✓
[v5] start 缺 docker: exit=2 + 中文错误                ✓
[v6] pytest: 11 passed in 0.05s                       ✓
[v7] _common.py 4 端口 (8088/8080/9090/3000) 出现      ✓
[v8] start/stop 不含 archon (D-05 锁定)                ✓
```

## User Setup Required

**External CLIs require manual installation:**

- **uv** — 包管理工具（必装）
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Docker Desktop for Mac** — `services start/stop` 依赖 docker CLI
  - 下载：https://www.docker.com/products/docker-desktop/
- **Archon CLI** — Archon 探测需要（`archon serve` 启动后才能 healthz 通）
  ```bash
  brew install archon
  ```

## Next Phase Readiness

- ✅ CLI 入口 + 3 子命令全部就位
- ✅ 并发 healthz 探测 + JSON 输出 + 错误路径全绿
- ✅ 11 个单测覆盖核心路径
- ⏭  Phase 2: workspace-core 沉淀 (ssh / secrets / config / progress / log / layout)
  - 2 沉淀层是后续 8 skill 的地基
  - `ar-ping` 端到端冒烟
- ⏭  Phase 4: Skill 02 — local-services-health (在 CLI 基础上做更深健康检查)

---
*Phase: 01-repo-foundation-services / Plan 03*
*Completed: 2026-06-06*

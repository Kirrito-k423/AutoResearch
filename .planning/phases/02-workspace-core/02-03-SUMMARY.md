---
phase: 02-workspace-core
plan: 03
subsystem: workspace-core
tags: [progress, log, layout, result, stdlib, pytest]

# Dependency graph
requires:
  - phase: 02-workspace-core/02-01
    provides: "workspace-core/ssh/ 命名风格 (lowercase pkg + leading underscore helper)"
  - phase: 02-workspace-core/02-02
    provides: "workspace-core/secrets/, config/ 命名风格 + ConfigError 异常模式"
provides:
  - "workspace-core.progress.emit_progress (D-14, D-15): __AR_PROGRESS__=<json> 写 stderr"
  - "workspace-core.progress.PROGRESS_PREFIX 常量"
  - "workspace-core.log.get_logger / configure_root (D-16): stdlib + Human/Json formatter"
  - "workspace-core.layout.{ROOT,RUNS,LOGS,CACHE,SSH_KEYS}_DIR 5 根目录"
  - "workspace-core.layout.RunPaths dataclass + ensure_run_dir / run_dir / ensure_root / clean_run (D-17)"
  - "workspace-core.result.{CheckResult, CheckSeverity, ok, fail, merge} (D-21)"
  - "8 skill 入口: from workspace_core.progress import emit_progress / from workspace_core.log import get_logger, configure_root / from workspace_core.layout import ensure_run_dir, run_dir / from workspace_core.result import ok, fail, merge"
affects: [02-workspace-core/02-04, all 8 skill phases (03..10)]

# Tech tracking
tech-stack:
  added: []  # 全 stdlib + typing, 无新依赖
  patterns:
    - "PROGRESS_PREFIX = '__AR_PROGRESS__=' (与 AGENTS.md 锁定一致)"
    - "进度走 stderr, 最终 stdout 唯一 JSON (D-04d/e)"
    - "logger 缓存: get_logger 同名返同一对象, 不堆 handler"
    - "configure_root idempotent: 清旧 handler 再加新 (复测不污染)"
    - "RunPaths frozen dataclass: 一次解析所有路径, 避免散落 Path 拼接"
    - "_validate_run_id 防路径注入 (DEFAULT_RUN_ID_RE: ^[A-Za-z0-9][A-Za-z0-9_\\-\\.]{0,127}$)"
    - "D-17 冲突硬失败: run-id 已存在非空目录 → FileExistsError"
    - "CheckResult TypedDict (不是 dataclass): 与 phase 1 HealthResult 一致, 易序列化"
    - "merge 严重度取最高档 (FAIL > WARN > OK): 用 _SEVERITY_PRIORITY 显式映射, 不用字母序 (ASCII bug)"

key-files:
  created:
    - workspace-core/progress/__init__.py
    - workspace-core/progress/emitter.py
    - workspace-core/log/__init__.py
    - workspace-core/log/formatter.py
    - workspace-core/log/logger.py
    - workspace-core/layout/__init__.py
    - workspace-core/layout/paths.py
    - workspace-core/result/__init__.py
    - workspace-core/result/check.py
    - tests/workspace-core/test_progress.py
    - tests/workspace-core/test_log.py
    - tests/workspace-core/test_layout.py
    - tests/workspace-core/test_result.py

key-decisions:
  - "D-14: __AR_PROGRESS__=<json> 前缀固定 (AGENTS.md 锁定)"
  - "D-15: 进度走 stderr, 不污染 stdout (D-04e 唯一 JSON)"
  - "D-16: stdlib logging + HumanFormatter (颜色) + JsonFormatter (落文件)"
  - "D-17: ~/.autoresearch/{runs,logs,cache,ssh_keys}/ 4 根目录"
  - "D-21: CheckResult TypedDict (ok/severity/data/message/error) + ok/fail/merge 工厂"
  - "DI-03: merge 用 _SEVERITY_PRIORITY 显式映射 (ASCII 字母序里 'o' > 'f', 直接 max() 会拿错档)"

patterns-established:
  - "模块结构: 子包 __init__.py 导出主 API, 内部 _helper 用 leading underscore 标记"
  - "Logger 缓存: dict[str, Logger] module-level 单例, configure_root 走 root logger"
  - "路径解析: RunPaths frozen dataclass 一次返所有路径, 调用方零散 Path 拼接"
  - "Severity priority: enum + 显式 priority dict 配套, 不依赖 .value 序"

requirements-completed: [CORE-PROTO-01, CORE-PROTO-02, CORE-LOG-01, CORE-LAYOUT-01]

# Metrics
duration: 25min
completed: 2026-06-06
---

# Phase 02 / Plan 03: workspace-core/{progress, log, layout, result}/ Summary

**4 子包就位: 进度协议 (D-14/15) + 统一日志 (D-16) + 固定目录 (D-17) + CheckResult (D-21). 28 个 pytest 单测 PASS (5+7+8+8), 累计 71/71 全绿 (含 phase 1 + 02-01/02).**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-06T19:10:00Z
- **Completed:** 2026-06-06T19:35:00Z
- **Tasks:** 6/6
- **Files created:** 13 (9 source + 4 test)
- **Tests:** 28 PASS (5 progress + 7 log + 8 layout + 8 result) — 累计 71 PASS

## What Was Built

**1. workspace-core/progress/ (D-14, D-15)**
- `emit_progress(stage, *, level='info', data=None, **fields)`: 写 stderr 一行
- `PROGRESS_PREFIX = "__AR_PROGRESS__="` 常量
- `ProgressEvent` dict subclass (类型注解 / mock 用)

**2. workspace-core/log/ (D-16)**
- `HumanFormatter`: 颜色 + ctx 字段 (stderr TTY)
- `JsonFormatter`: ts/level/logger/msg + 可选 host/ctx/exc (落文件)
- `configure_root(level, log_file, enable_stderr)`: idempotent, 清旧 handler
- `get_logger(name)`: 缓存, 多次调用返同一对象

**3. workspace-core/layout/ (D-17)**
- 5 根目录常量: `ROOT_DIR/RUNS_DIR/LOGS_DIR/CACHE_DIR/SSH_KEYS_DIR`
- `DEFAULT_RUN_ID_RE` 防路径注入 (128 字符上限, 不含 `/\\` 等)
- `RunPaths` frozen dataclass: root/logs/wandb/prom/manifest
- `run_dir(rid, *, create=True)`, `ensure_run_dir(rid)` 冲突硬失败
- `ensure_root()`, `clean_run(rid)` 辅助

**4. workspace-core/result/ (D-21)**
- `CheckSeverity` enum: OK / WARN / FAIL
- `CheckResult` TypedDict: ok/severity/data/message/error
- `ok(data?, message?)` / `fail(error, data?, message?, severity?)` 工厂
- `merge(results)`: 最高严重度 + count/failed/warned 统计

## Task Execution

按 PLAN 6 个 task 顺序执行, 无 skip. 全部自动 commit.

## Deviations from Plan

**1. [ASCII 字母序 bug] merge 用 _SEVERITY_PRIORITY 显式映射, 不用 max(..., key=.value)**

- **Found during:** Task 3.5 跑 test_result.py 失败 2 个
  - `test_merge_warn_only`: 期望 [OK, WARN, OK] → WARN, 实际 FAIL
  - `test_merge_empty`: 期望 data.count=0, 实际 KeyError
- **Root cause:** PLAN 里写的 `max(results, key=lambda r: r["severity"].value)["severity"]`
  - 字母序: "fail" < "ok" (ASCII: f=102, o=111), 所以 max() 返 "ok" → merge 选 OK 档
  - 字母序与"FAIL > WARN > OK"语义不一致
  - `test_merge_empty` 失败是因为 PLAN 写的 `return ok(message="no checks run")` 没带 data.count=0
- **Fix:** 引入 `_SEVERITY_PRIORITY: dict[CheckSeverity, int] = {OK: 0, WARN: 1, FAIL: 2}`, merge 用它
  - empty case 也改为直接构造 CheckResult 显式带 data={"count": 0, "failed": 0, "warned": 0}
- **Files modified:** workspace-core/result/check.py
- **Decision:** DI-03 写进 SUMMARY, 列入 patterns-established

**Total deviations:** 1 auto-fixed (1 ASCII 排序 bug)
**Impact on plan:** 28/28 tests PASS, 决策 DI-03 记录, 后续 8 skill 用 merge() 时不会被坑

## Issues Encountered

- ASCII 字母序 vs 语义顺序不一致: 字符串排序里 "ok" > "fail" (因 'o' > 'f'), 不能用 `max(..., key=.value)`. 显式 priority dict 是更鲁棒的做法
- test_layout.py 用了 monkeypatch module-level 常量 (RUNS_DIR 等), 注意这会改 module 全局, 后续 test 之间不互相污染 (每个 fixture 都重置)

## User Setup Required

无 — 全 stdlib + typing, 0 新依赖

## Next Phase Readiness

- ✅ 4 个 workspace-core 子包就位 (progress/log/layout/result)
- ✅ 8 skill 全部能直接复用:
  - `from workspace_core.progress import emit_progress`
  - `from workspace_core.log import get_logger, configure_root`
  - `from workspace_core.layout import ensure_run_dir, run_dir`
  - `from workspace_core.result import ok, fail, merge`
- ✅ 28 个 workspace-core 单测 PASS (无破坏 phase 1 + 02-01/02)
- ⏭  Plan 02-04: autoresearch ping CLI (端到端冒烟, 复用 ssh + config + progress)

---
*Phase: 02-workspace-core / Plan 03*
*Completed: 2026-06-06*

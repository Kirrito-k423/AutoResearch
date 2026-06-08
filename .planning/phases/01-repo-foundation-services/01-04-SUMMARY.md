---
phase: 01-repo-foundation-services
plan: 04
subsystem: cli
tags: [lang, i18n, gap-closure, pytest, regression]

# Dependency graph
requires:
  - phase: 01-repo-foundation-services/01-03
    provides: "autoresearch/services/{start,stop}.py + CLI --lang 接好 (但 service 层 _check_docker 漏接)"
provides:
  - "autoresearch/services/start.py: _check_docker(lang) + except FileNotFoundError 条件分支"
  - "autoresearch/services/stop.py: 同上 (对称)"
  - "tests/test_start_stop.py: +2 测试 (--lang en 切英文错误)"
  - "01-UAT.md Test 10: issue → pass"
affects: [01-UAT.md (Test 10 二次验收)]

# Tech tracking
tech-stack:
  added: []  # 无新依赖
  patterns:
    - "i18n 一致性: _check_docker / except FileNotFoundError 都按 lang 返中/英"
    - "D-04 验证: 全 3 子命令 (status/start/stop) 现在 --lang en 都能切英文错误"
    - "CliRunner 8.2+ env= 关键字参数注入 PATH 屏蔽外部命令"

key-files:
  modified:
    - autoresearch/services/start.py (3 处: _check_docker 签名+字符串, run_start 调用点, _run_compose_up except)
    - autoresearch/services/stop.py (3 处: 同上对称)
    - tests/test_start_stop.py (+2 测试)
  created:
    - .planning/phases/01-repo-foundation-services/01-04-PLAN.md (gap closure plan)
    - .planning/phases/01-repo-foundation-services/01-04-SUMMARY.md (本文件)

key-decisions:
  - "DI-01: _check_docker 签名加 lang 参数 (而不是函数体里读 global), 跟 run_start/run_stop 调用契约一致"
  - "DI-02: 沿用 phase 1 测试模式 (CliRunner + isolated_filesystem + env= 屏蔽 PATH), 不引入新 mock 库"
  - "DI-03: '错误' not in combined 作为英文切换的关键断言 (避免 'Error' 子串假阳性)"

patterns-established:
  - "service 层所有 user-facing 字符串都走 lang 条件分支"
  - "CliRunner 8.2+ 测试用 env={'PATH': '/usr/bin:/bin'} 屏蔽外部命令, 不污染真实 PATH"
  - "二次 UAT: Test 10 result issue → pass, 累计 81/81 tests"

requirements-completed: [SVC-CHK-DEPS-01, SVC-CHK-START-01, SVC-CHK-STOP-01]

# Metrics
duration: 8min
completed: 2026-06-08
---

# Phase 01 / Plan 04: services start/stop --lang en gap closure Summary

**UAT phase 1 Test 10 issue 关闭: `autoresearch services start/stop --lang en` 现在切英文错误文案, 跟 01-03 SUMMARY 声明的"全 3 子命令统一 --lang en 切英文"对齐. 81/81 tests PASS (regression 0).**

## Performance

- **Duration:** 8 min
- **Started:** 2026-06-08T02:10:00Z
- **Completed:** 2026-06-08T02:18:00Z
- **Tasks:** 4/4
- **Files modified:** 2 (start.py, stop.py)
- **Files created:** 2 (PLAN, this SUMMARY)
- **Test files appended:** 1 (test_start_stop.py +2)
- **Tests:** 81 PASS (之前 79 + 2 new) — regression 0

## What Was Fixed

**autoresearch/services/start.py**
- `_check_docker()` → `_check_docker(lang: str)`, 字符串按 lang 切中/英
- `run_start` 调用点 → `_check_docker(lang)`
- `_run_compose_up` 的 `except FileNotFoundError` → 条件分支

**autoresearch/services/stop.py** (对称)
- 同样 3 处

**tests/test_start_stop.py**
- `test_start_missing_docker_lang_en_returns_english_error`
- `test_stop_missing_docker_lang_en_returns_english_error`
- 用 `CliRunner(env={"PATH": "/usr/bin:/bin"})` 屏蔽 docker
- 关键断言: `"错误" not in combined` (确认真的切了英文)

## Task Execution

按 01-04-PLAN.md 4 个 task 顺序执行, 无 skip.

## Deviations from Plan

无 — 严格按 plan 落地.

## Issues Encountered

无 — issue 在 plan 阶段已诊断, 修复路径清晰.

## Verification

- 81/81 tests PASS (regression 0)
- 二次 UAT: `PATH=/usr/bin:/bin .venv/bin/python -m autoresearch services start --lang en` → "Error: \`docker\` command not found. Please install Docker Desktop (macOS)." + exit 2
- 二次 UAT: 默认中文仍正确 → "错误：找不到 \`docker\` 命令。请先安装 Docker Desktop（macOS）。"
- 二次 UAT: stop --lang en 同样切英文 + exit 2

## Next Phase Readiness

- ✅ UAT phase 1 全部 pass (9 → 10/10)
- ✅ 3 service 子命令现在统一支持 --lang en 切英文错误 (D-04 完整落地)
- ⏭  phase 1 真正 close, 可进 phase 2 UAT 或 phase 3 plan

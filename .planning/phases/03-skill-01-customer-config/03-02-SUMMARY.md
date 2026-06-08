---
phase: 03-skill-01-customer-config
plan: 02
subsystem: cli
tags: [config, show, keyring, redaction, click, mock]

# Dependency graph
requires:
  - phase: 03-skill-01-customer-config/03-01
    provides: "autoresearch/config/_common.py (resolve_config_path) + cli group"
  - phase: 02-workspace-core/02-02
    provides: "workspace_core.secrets.KEYRING_AVAILABLE (Phase 2 沉淀)"
provides:
  - "autoresearch/config/show.py: run_show (CFG-SHOW-01) + _is_sensitive + _redact"
  - "autoresearch/config/keyring_cli.py: run_keyring (set/get/delete/list)"
  - "CLI: autoresearch config show + config keyring {set, get, delete, list}"
  - "15 tests PASS (7 show + 8 keyring)"
affects: [all 8 skill phases, downstream skills 可用 <keyring:NAME> 占位符]

# Tech tracking
tech-stack:
  added: []  # keyring 已在 phase 2 加, 0 新依赖
  patterns:
    - "脱敏 (D-05): (?i)(password|secret|token|credential) → '***', 例外 identity_file + keyring"
    - "递归 _redact: dict 走字段名检测, list 整体保留"
    - "Pydantic v2 model_dump() 拿 dict (不是 dict(model_dump()))"
    - "keyring CLI mock 模式: unittest.mock patch _backend_or_die"
    - "keyring 4 action + 1 list-not-supported 提示"

key-files:
  modified:
    - autoresearch/config/show.py (stub → 真实)
    - autoresearch/config/keyring_cli.py (stub → 真实)
    - autoresearch/cli.py (+ keyring group 4 子命令)
  created:
    - tests/test_config_show.py (7 测试)
    - tests/test_config_keyring.py (8 测试)

key-decisions:
  - "D-05 落地: _SENSITIVE_RE = (?i)(password|secret|token|credential), _SAFE_FIELDS = {identity_file, keyring}"
  - "DI-04: keyring 不可用时 (KEYRING_AVAILABLE=False) 返 exit 2 而不是 crash, 中文错误 + 安装提示"
  - "DI-05: keyring 没有原生 list API, 显式提示用 'get <name>' 探测 (D-09 Phase 2 已说明)"
  - "DI-06: _to_yaml_like 走 indent+sp 简化 (不依赖 PyYAML dumper, 够用即可)"

patterns-established:
  - "递归脱敏算法: dict 走 _is_sensitive(k) 标记, list 整体 in_sensitive 透传"
  - "外部依赖 mock: patch module-level helper (_backend_or_die) 而不是直接 patch keyring module"
  - "CLI 嵌套 group 命名: keyring_grp (避免跟 import keyring module 冲突)"

requirements-completed: [CFG-SHOW-01]

# Metrics
duration: 12min
completed: 2026-06-08
---

# Phase 03 / Plan 02: customer-config show + keyring Summary

**autoresearch config show (CFG-SHOW-01) + keyring 就位. 15/15 tests PASS, 累计 106/106 (含 phase 1+2+03). phase 3 全部 6 REQ 关闭.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-06-08T13:30:00Z
- **Completed:** 2026-06-08T13:42:00Z
- **Tasks:** 5/5
- **Files modified:** 2 (show.py, keyring_cli.py) + 1 (cli.py + keyring group)
- **Files created:** 2 (test_config_show.py, test_config_keyring.py)
- **Tests:** 15 PASS (7 show + 8 keyring) — 累计 106 PASS

## What Was Built

**1. autoresearch/config/show.py** (替换 stub, CFG-SHOW-01)
- `_is_sensitive(key)`: 正则 `(?i)(password|secret|token|credential)`, 例外 `identity_file` + `keyring`
- `_redact(value, in_sensitive)`: 递归脱敏, dict 走字段检测, list 整体透传
- `_to_yaml_like(data, indent)`: 简易 YAML 打印 (不依赖 PyYAML dumper)
- `run_show(config, lang, as_json)`: 调 from_path + redact + 打印/JSON

**2. autoresearch/config/keyring_cli.py** (替换 stub)
- `SERVICE = "autoresearch"` (跟 Phase 2 secrets 沉淀对齐)
- `_backend_or_die(lang)`: KEYRING_AVAILABLE 守卫, 不可用返 None + 中文错误
- `run_keyring(action, name, value, lang)`: 4 action
  - set: 需 value
  - get: 缺返 None → exit 1
  - delete: PasswordDeleteError 返 exit 1
  - list: 提示无原生 API

**3. autoresearch/cli.py**: @config.group() keyring_grp + 4 子命令

**4. tests/**
- test_config_show.py: 7 测试 (3 unit _is_sensitive/_redact + 4 CLI 端到端)
- test_config_keyring.py: 8 测试 (5 unit mocked + 3 CLI 端到端)

## Task Execution

按 03-02-PLAN.md 5 个 task 顺序执行, 无 skip.

## Deviations from Plan

**1. [test_config_keyring test_keyring_delete_not_found_returns_1] 兼容 keyring 25.x 缺 PasswordDeleteError**

- **Found during:** Task 2.4 写测试时, 某些 keyring 版本 (老) 没有 `keyring.errors.PasswordDeleteError`
- **Fix:** `getattr(__import__("keyring").errors, "PasswordDeleteError", Exception)` 兜底
- **Impact:** 测试兼容多版本 keyring

**Total deviations:** 1 auto-fixed (1 兼容性)
**Impact on plan:** 15/15 tests PASS, DI-04..06 决策记录

## Issues Encountered

- keyring 不同版本的 errors 命名空间差异: 老版本可能用 `keyring.errors.PasswordDeleteError`, 25.x 已稳定
- Pydantic v2 model_dump() 默认 mode='python' 返 dict, 嵌套数据保留
- CliRunner 跑嵌套 group 命令 (config keyring set) 走双层 dispatch

## User Setup Required

- 跑 `autoresearch config keyring set MY_SECRET --value "my-password"` 存密码
- 配置里用 `<keyring:MY_SECRET>` 占位符
- 或继续用 `<env:VAR>` + env 变量

## Next Phase Readiness

- ✅ CFG-SHOW-01 满足
- ✅ Phase 3 全部 6 REQ 关闭
- ✅ Customer-config skill 完整: init / validate / show / keyring {set, get, delete, list}
- ✅ 15 tests PASS, 累计 106 tests
- ⏭  Phase 4: local-services-health skill (已部分在 phase 1 services 子命令实现, phase 4 加并发 / JSON schema / healthz 深度)

---
*Phase: 03-skill-01-customer-config / Plan 02*
*Completed: 2026-06-08*

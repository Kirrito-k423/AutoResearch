---
phase: 02-workspace-core
plan: 02
subsystem: workspace-core
tags: [secrets, config, pydantic, keyring, pytest]

# Dependency graph
requires:
  - phase: 02-workspace-core/02-01
    provides: "workspace-core/ssh/ (虽然本 plan 不直接 import, 后续 02-04 ping 会用)"
provides:
  - "workspace-core.secrets.resolve_secret (D-06..07): <keyring:NAME> / <env:VAR> 占位符"
  - "workspace-core.secrets.resolve_dict 递归解析 (D-08)"
  - "D-09 软失败: keyring 不可用时 warning + fallback env (不抛错)"
  - "workspace-core.config.Config: Pydantic v2 schema (D-10..12) 含 ServerSpec/NetworkProbes/LogConfig/WandbConfig"
  - "workspace-core.config.from_yaml / from_path (D-12, D-13): YAML → 解密 → 校验 → 中文错误"
  - "8 skill 入口: from workspace_core.config import from_path; from workspace_core.secrets import resolve_secret"
affects: [02-workspace-core/02-04, 03-customer-config, 05-network-check, 06-server-hardware, 07-service-reachability, all 8 skill phases]

# Tech tracking
tech-stack:
  added:
    - pydantic 2.13.4
    - pyyaml 6.0.3
    - keyring 25.7.0 (dev/test 用, 让 import keyring 不失败)
    - annotated-types 0.7.0 (pydantic 传递依赖)
  patterns:
    - "双占位符 (D-06, D-07): PLACEHOLDER_RE = ^<(keyring|env):([A-Za-z0-9_\\-]+)>$"
    - "D-09 软失败: 一次性 warning, keyring 失败 → env fallback; 都不存在才 SecretError"
    - "Pydantic v2 单文件 schema: ServerSpec / NetworkProbes / LogConfig / WandbConfig 都放 schema.py"
    - "_format_validation_error 翻译 pydantic.ValidationError → 中文 (字段路径 + 类型 + 期望)"
    - "from_path 优先级: path 参数 > env AUTORESEARCH_CONFIG > ./config/config.yaml"

key-files:
  created:
    - workspace-core/secrets/__init__.py
    - workspace-core/secrets/resolver.py
    - workspace-core/config/__init__.py
    - workspace-core/config/schema.py
    - workspace-core/config/loader.py
    - tests/workspace-core/test_secrets.py
    - tests/workspace-core/test_config.py
  modified:
    - pyproject.toml (加 pydantic + pyyaml + keyring 依赖)
    - uv.lock (pydantic + pyyaml + keyring + 传递依赖)

key-decisions:
  - "D-06: <keyring:NAME> 走 keyring.get_password('autoresearch', NAME)"
  - "D-07: <env:VAR> 走 os.environ[VAR]"
  - "D-08: resolve_dict 递归 dict / list[dict] / list[str]"
  - "D-09: keyring 不可用时软失败 (warning + fallback env)"
  - "D-10: Pydantic v2 BaseModel (v2 语法, Field + field_validator)"
  - "D-11: 中文错误 (字段路径 + 原因 + 期望)"
  - "D-12: from_yaml 走单文件 schema"
  - "D-13: from_path 默认 ./config/config.yaml + env AUTORESEARCH_CONFIG 覆盖 + 参数覆盖"
  - "DI-01: 不用 _keyring_backend.py 单独文件, 把 keyring import 守卫放在 resolver.py 顶部即可"
  - "DI-02: 测试 monkeypatch keyring.get_password 直接, 不引入 PlaintextKeyring fake backend"

patterns-established:
  - "ConfigError 包含中文 message + 字段路径, 调用方直接 str(e) 给用户看"
  - "placeholder pattern: <keyring:NAME> / <env:VAR> 在 yaml 里就是字符串, loader 解析后变明文"
  - "DI-01 single-file schema: 4 个 Pydantic BaseModel 放 schema.py, 避免小类拆目录"

requirements-completed: [CORE-SEC-01, CORE-SEC-02, CORE-CFG-01, CORE-CFG-02]

# Metrics
duration: 35min
completed: 2026-06-06
---

# Phase 02 / Plan 02: workspace-core/secrets/ + config/ Summary

**双沉淀就位: secrets 占位符解析 (D-06..09 软失败) + config Pydantic v2 schema + 中文错误 (D-10..13). 20 个 pytest 单测 PASS (8 secrets + 12 config), 加 02-01 的 12 + phase 1 的 11 = 43/43.**

## Performance

- **Duration:** 35 min
- **Started:** 2026-06-06T18:30:00Z
- **Completed:** 2026-06-06T19:05:00Z
- **Tasks:** 5/5
- **Files created:** 7 (5 source + 2 test)
- **Tests:** 20 PASS (8 secrets + 12 config) — 累计 43 PASS (含 phase 1 + 02-01)

## What Was Built

**1. workspace-core/secrets/ (D-06..09)**
- `PLACEHOLDER_RE = ^<(keyring|env):([A-Za-z0-9_\\-]+)>$` 严格匹配
- `resolve_secret(value: str) -> str`: 占位符解 / 非占位符原样
- `resolve_dict(d)`: 递归 dict / list[dict] / list[str]
- `KEYRING_AVAILABLE` 软依赖: `try/except ImportError` 保护, 不强制装
- `_warn_keyring_failure_once()`: 一次性 stderr warning, 避免重复 noise

**2. workspace-core/config/ (D-10..13)**
- `ServerSpec`: name / host / port / user / identity_file / bootstrap_password_secret
- `NetworkProbes`: enabled + 默认 baidu/hf/github targets
- `LogConfig`: level + json_format + dir
- `WandbConfig`: enabled + entity + project
- `Config`: 顶层聚合 + `_server_names_unique` 校验
- `from_yaml(yaml_text) -> Config`: YAML → resolve_dict → model_validate
- `from_path(path)`: path 参数 > env > 默认
- `ConfigError`: 中文 message 包含字段路径 + 原因

## Task Execution

按 PLAN 5 个 task 顺序执行, 无 skip. 全部自动 commit.

## Deviations from Plan

**1. [keyring 依赖] 显式 `uv add keyring` 装包**

- **Found during:** Task 2.4 写完 test_secrets.py 后跑 pytest
- **Issue:** 3 个 keyring 测试 `import keyring` 直接失败 (`ModuleNotFoundError`). resolver.py 用 `try/except ImportError` 守卫所以代码本身 OK, 但测试要 monkeypatch keyring.get_password 必须要 import 成功
- **Fix:** `uv add keyring` → 自动更新 pyproject + uv.lock
- **Files modified:** pyproject.toml, uv.lock
- **Committed in:** `feat(02): add workspace-core/secrets + config`

**2. [_keyring_backend.py 合并] 单独 backend 文件取消, import 守卫放在 resolver.py**

- **Found during:** Task 2.1 写 resolver.py
- **Issue:** PLAN 列出 `workspace-core/secrets/_keyring_backend.py`, 但实际上 keyring 的 try/except ImportError 守卫 + `keyring = None` 哨兵只需要 5 行代码, 拆一个文件 over-engineering
- **Fix:** 把 5 行守卫写在 resolver.py 顶部, 删掉 _keyring_backend.py. KEYRING_AVAILABLE 仍是 module-level 单例
- **Decision:** DI-01 写进 SUMMARY

**3. [PlaintextKeyring 跳过] 测试用 monkeypatch, 不用 fake backend**

- **Found during:** Task 2.4 写 test_secrets.py
- **Issue:** PLAN 提到 `keyring.alt.file.PlaintextKeyring` fake backend (D-08), 但 `keyring.alt` 不在 `keyring` 主包里, 需要单独装. 实际上 monkeypatch `keyring.get_password` 一样能测软失败 / 真取值 / 都不存在三种路径
- **Fix:** 3 个 keyring 测试用 `monkeypatch.setattr(keyring, "get_password", lambda *a, **kw: None)` 直接 stub
- **Decision:** DI-02 写进 SUMMARY

**Total deviations:** 3 auto-fixed (1 依赖添加, 2 简化设计)
**Impact on plan:** 全部 5 个 task 完成, 20/20 tests PASS, 决策记录在 DI-01..02

## Issues Encountered

执行期间发现 1 个 missing dependency (`keyring`), 已通过 `uv add` 解决. 测试侧 2 处简化 (合并 _keyring_backend.py / 用 monkeypatch 替代 PlaintextKeyring) 不影响功能.

## User Setup Required

**External CLI require installation:**

- **keyring** — 已通过 `uv add` 装好
- 跑 `autoresearch config init` 后续会读 `config/config.yaml`, 占位符:
  - `<keyring:NAME>` 需 `python -m keyring set autoresearch NAME` 提前存
  - `<env:VAR>` 需 env 里设 VAR

## Next Phase Readiness

- ✅ secrets 占位符解析就位 (双格式 + 软失败)
- ✅ config Pydantic v2 校验就位 (中文错误 + 多来源)
- ✅ 20 个 workspace-core 单测 PASS (无破坏 phase 1 + 02-01)
- ⏭  Plan 02-03: workspace-core/progress/ + log/ + layout/ + result/ (4 子包, stdlib only)
- ⏭  Plan 02-04: autoresearch ping (复用 ssh + config + progress)

---
*Phase: 02-workspace-core / Plan 02*
*Completed: 2026-06-06*

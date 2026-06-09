---
phase: 04-skill-03-server-hardware-probe
plan: 01
status: blocked
subsystem: hardware-probe
tags: [ascend, npu-smi, ssh, click, pytest]

requires:
  - phase: 02-workspace-core
    provides: [SSHClient, config loader, CheckResult, progress emitter]
  - phase: 03-customer-config
    provides: [validated server inventory and SSH credentials]
provides:
  - Table-driven Ascend npu-smi core metric parser
  - Single-server SSH hardware probe returning CheckResult
  - autoresearch hw probe --server JSON CLI
affects: [04-02-hardware-compatibility, 04-03-hardware-processes-and-all]

tech-stack:
  added: []
  patterns: [pure vendor-output parser, fixed remote command, partial-data failure result]

key-files:
  created:
    - autoresearch/hw/models.py
    - autoresearch/hw/parser.py
    - autoresearch/hw/probe.py
    - tests/test_hw_parser.py
    - tests/test_hw_probe.py
    - tests/test_hw_cli.py
  modified:
    - autoresearch/cli.py
    - autoresearch/hw/__init__.py

key-decisions:
  - "服务器名只做 config 精确键查找，远程只执行固定常量 npu-smi info。"
  - "核心指标缺失保留部分设备数据并返回 FAIL，不用 0 冒充。"
  - "A2-AK-225 真机不可达时保留实现提交，但不标记计划或需求完成。"

patterns-established:
  - "硬件解析器不依赖 SSH、Click 或文件系统。"
  - "硬件 WARN 表示核心探测成功，显式构造 ok=true 的 CheckResult。"

requirements-completed: []

duration: 9min
completed: 2026-06-09
---

# Phase 04 Plan 01: 单服务器纵向硬件探测 Summary

**表头驱动的 Ascend 910 `npu-smi` 解析器、固定命令 SSH 编排和单一 JSON `hw probe` CLI 已交付，但 A2-AK-225 真实 SSH 门槛仍阻塞。**

## Performance

- **Duration:** 9 min
- **Started:** 2026-06-09T04:18:28Z
- **Completed:** 2026-06-09T04:26:58Z
- **Tasks:** 3 executed
- **Files modified:** 10

## Accomplishments

- 解析脱敏的 8×Ascend 910B2 双行设备表，统一输出 MiB、摄氏度和整数百分比。
- 核心字段缺失或非法时保留其他设备字段，并生成结构化 `field_errors`。
- 通过 `workspace_core.ssh` 完成 config 精确查找、5 秒连接 timeout、固定命令执行和 client 清理。
- 新增 `autoresearch hw probe --server NAME`，stdout 只含一个 CheckResult JSON，进度写 stderr，退出码分为 0/1/2。
- 硬件专项 13 个测试及仓库全量 119 个测试通过。

## Task Commits

1. **Task 04-01-01: 建立硬件结果契约和核心指标解析器** - `906d3c9`
2. **Task 04-01-02: 用 workspace_core.ssh 交付单服务器探测编排** - `9f0e2b7`
3. **Task 04-01-03: 挂载 hw probe 并跑首台真机** - `ef7a943`

## Files Created/Modified

- `autoresearch/hw/models.py` - 设备、进程、驱动、字段错误和硬件 payload 契约。
- `autoresearch/hw/parser.py` - 纯文本双行设备表解析与部分失败表达。
- `autoresearch/hw/probe.py` - 配置解析、SSH 生命周期、CheckResult 和 CLI 输出边界。
- `autoresearch/cli.py` - `hw` group 与 `hw probe` command。
- `tests/fixtures/hw/` - 脱敏 8 卡基线与缺失指标 fixture。
- `tests/test_hw_parser.py` - 核心指标、空进程、缺失和未知格式测试。
- `tests/test_hw_probe.py` - 固定命令、timeout、部分数据和关闭 client 测试。
- `tests/test_hw_cli.py` - help、唯一 JSON、progress 与 0/1/2 退出码测试。

## Decisions Made

- 未复用 `autoresearch.ping` 私有 helper；硬件域直接组合 config、HostSpec 和 SSHClient 公共 API。
- server 输出仅包含 `name/host/port`，不包含 user、identity file 或 secret 字段。
- 命令非零时仍解析 stdout，以便保留已经取得的设备数据。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 收紧双行设备记录状态机**
- **Found during:** Task 04-01-01
- **Issue:** 详情行 `0 0` 被宽松主记录正则误识别为新设备。
- **Fix:** 要求主记录中的设备名包含非数字字符，再由详情表头映射 chip/bus/HBM/AICore。
- **Files modified:** `autoresearch/hw/parser.py`
- **Verification:** `tests/test_hw_parser.py` 4 passed。
- **Committed in:** `906d3c9`

**2. [Rule 1 - Bug] 修复失败进度事件字段冲突**
- **Found during:** Task 04-01-02
- **Issue:** `emit_progress("hw.fail", stage=...)` 重复传入 `stage`，导致错误路径二次抛 `TypeError`。
- **Fix:** 附加字段改为 `failed_stage`。
- **Files modified:** `autoresearch/hw/probe.py`
- **Verification:** `tests/test_hw_probe.py` 5 passed。
- **Committed in:** `9f0e2b7`

**Total deviations:** 2 auto-fixed (2 Rule 1 bugs).
**Impact on plan:** 均为任务内正确性修复，无范围扩张。

## Issues Encountered

- 2026-06-09 12:25 和 12:26（Asia/Shanghai）两次执行 `uv run autoresearch hw probe --server A2-AK-225` 均返回 exit 1。
- SSH 目标 `192.168.9.225:22` 在 4 次尝试后无法建立会话，期间出现 `Error reading SSH protocol banner`，最终错误为 `No existing session`。
- CLI 失败行为符合协议：stdout 是单一 FAIL JSON，stderr 含 progress，设备数为 0。
- 因真实服务器未返回硬件数据，无法证明 8 张 910B2 的四项核心指标，04-01 不得标记完成。

## Known Stubs

- `autoresearch/hw/parser.py:271` - `processes=[]` 为 04-03 进程解析预留，不影响本计划核心指标目标。
- `autoresearch/hw/parser.py:272` - 驱动版本暂为 `None`，由 04-02 采集。
- `autoresearch/hw/probe.py:257` - `all_servers=True` 明确返回配置错误，`--all` 由 04-03 开放且当前未暴露在 CLI。

## Verification

- `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py tests/test_hw_cli.py` - **PASS: 13 passed**
- `uv run pytest` - **PASS: 119 passed, 6 warnings**
- `uv run autoresearch hw probe --help` - **PASS: 显示 `--server/--config/--lang`**
- `uv run autoresearch hw probe --server A2-AK-225` - **FAIL: exit 1，SSH 连接不可用**

## User Setup Required

- 连接可访问 `192.168.9.225` 的 LAN/VPN，并确认 A2-AK-225 的 SSH 服务可返回协议 banner。
- 恢复后重跑 `uv run autoresearch hw probe --server A2-AK-225`；必须 exit 0 且 8 张设备四项核心字段均非 null。

## Next Phase Readiness

- 04-02 所需解析器、探测编排和错误结构已就绪。
- 04-01 的真实 A2 验收仍是阻塞项；在通过前不推进计划完成计数或 HW requirement 状态。

## Self-Check: FAILED

- **PASS:** 10 个计划文件均存在。
- **PASS:** 任务提交 `906d3c9`、`9f0e2b7`、`ef7a943` 均存在。
- **PASS:** 硬件专项与全量自动测试通过。
- **FAILED:** A2-AK-225 真机验收未通过，未获得 8 张真实设备核心指标。

---
*Phase: 04-skill-03-server-hardware-probe*
*Recorded: 2026-06-09*

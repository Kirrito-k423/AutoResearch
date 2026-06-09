---
phase: 04-skill-03-server-hardware-probe
plan: 02
status: complete
subsystem: hardware-probe
tags: [ascend, npu-smi, lspci, driver, diagnostics]

requires:
  - phase: 04-01
    provides: [single-server SSH probe, core NPU parser, CheckResult contract]
provides:
  - Extensible multi-version npu-smi parsing with typed metric supplements
  - npu-smi header and Ascend version.info driver metadata
  - Presence-only lspci fallback that cannot report false success
  - Local raw failure logs with bounded JSON summaries
affects: [04-03-process-and-all-probe, phase-04-real-server-uat]

tech-stack:
  added: []
  patterns:
    - Canonical header aliases instead of fixed output widths
    - Allowlisted remote commands built only from parsed integer device ids
    - Failure-only local diagnostics with bounded result summaries

key-files:
  created:
    - tests/fixtures/hw/npu_smi_variant.txt
    - tests/fixtures/hw/npu_smi_unknown_format.txt
    - tests/fixtures/hw/driver_version_info.txt
    - tests/fixtures/hw/lspci_ascend.txt
  modified:
    - autoresearch/hw/models.py
    - autoresearch/hw/parser.py
    - autoresearch/hw/probe.py
    - tests/test_hw_parser.py
    - tests/test_hw_probe.py

key-decisions:
  - "默认表有效值优先；typed query 只填 None，冲突保留主表并记录 warning。"
  - "driver version.info 只用固定 cat 命令读取，缺失降级为 WARN。"
  - "lspci 只证明设备存在，动态字段保持 null，结果无条件 FAIL。"

patterns-established:
  - "所有硬件远端命令均为固定常量或由 allowlist 加已解析整数构造。"
  - "失败原文写本地 LOGS_DIR，JSON 只带最多 512 字符摘要。"

requirements-completed:
  - HW-NPU-01
  - HW-NPU-02
  - HW-NPU-03
  - HW-DRV-01

duration: 9min
completed: 2026-06-09
---

# Phase 04 Plan 02: 多版本解析、驱动信息与失败诊断 Summary

**可扩展 Ascend 表头/typed query 解析、双来源驱动版本、严格 FAIL 的 lspci fallback 和本地失败原始日志已交付。**

## Performance

- **Duration:** 9 min
- **Started:** 2026-06-09T07:05:19Z
- **Completed:** 2026-06-09T07:14:39Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments

- 将 `npu-smi` 列名集中为 canonical alias，覆盖 910B2、910B 和表头单位/空格变化。
- 仅对缺失核心字段执行 memory/temp/usages typed query，拒绝非 allowlist 类型和非整数 device id。
- 同时解析 `npu-smi 25.3.rc1` header 与固定只读 `version.info` 文件，文件缺失只产生 WARN。
- 未知或不可用的 `npu-smi` 输出降级到 `lspci -Dnn`，只保留 Huawei Ascend accelerator presence，绝不伪造动态指标成功。
- 失败时原始命令记录写入本地 `LOGS_DIR`，JSON 摘要限制为 512 字符；成功结果不含 raw output。

## Task Commits

1. **Task 04-02-01: 扩展表头解析和 typed query 核心指标补充** - `9e14e77`
2. **Task 04-02-02: 采集 npu-smi 与 Ascend driver 版本** - `2ed377d`
3. **Task 04-02-03: 增加 lspci fallback 和本地失败原始日志** - `ae9717a`

## Files Created/Modified

- `autoresearch/hw/models.py` - 增加设备描述、命令记录和 raw 摘要契约。
- `autoresearch/hw/parser.py` - 多版本 alias、typed metrics、driver 和 lspci 纯解析器。
- `autoresearch/hw/probe.py` - 固定 typed/driver/lspci 命令、合并优先级和失败日志。
- `tests/fixtures/hw/` - 多版本、未知格式、driver 与混合 lspci 脱敏样本。
- `tests/test_hw_parser.py` - parser 多版本、驱动和设备筛选断言。
- `tests/test_hw_probe.py` - allowlist、冲突、fallback、raw log 和失败降级断言。

## Decisions Made

- typed memory 查询即使返回已存在的 used 值，也不覆盖默认表；只补齐缺失 total，并记录冲突。
- raw JSON 摘要排除 `version.info` 正文，只记录该命令退出码；完整原文仅保存在本地失败日志。
- 本地日志写入失败不能掩盖原始硬件失败，改为保留 FAIL、摘要和 warning。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] 本地日志不可写时保留稳定失败结果**
- **Found during:** Task 04-02-03
- **Issue:** `write_raw_failure_log` 若因只读文件系统抛出 `OSError`，会掩盖原始探测失败并破坏稳定 JSON 契约。
- **Fix:** 先生成有界摘要，日志写入异常转为 warning，保留原始 FAIL 和 `raw_log_path=null`。
- **Files modified:** `autoresearch/hw/probe.py`, `tests/test_hw_probe.py`
- **Verification:** `test_raw_log_write_error_preserves_original_failure`
- **Committed in:** `ae9717a`

**Total deviations:** 1 auto-fixed (1 Rule 2 missing critical functionality).
**Impact on plan:** 仅增强失败路径可靠性，无范围扩张。

## Issues Encountered

- 2026-06-09 15:14（Asia/Shanghai）执行 `uv run autoresearch hw probe --server A2-AK-225` 返回 exit 1。
- `192.168.9.225:22` 四次连接均无法读取 SSH protocol banner，最终为 `No existing session`。
- stdout 仍是单一 FAIL JSON；连接阶段没有执行远端命令，因此 `driver_versions` 真机数据仍无法验收。

## Known Stubs

- `autoresearch/hw/parser.py:425` - `processes=[]` 由 04-03 实现占用进程解析。
- `autoresearch/hw/probe.py:497` - `--all` 明确在 04-03 开放；当前 CLI 仍只支持单服务器。

## Verification

- `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py` - **PASS: 25 passed**
- `uv run pytest -q tests/test_hw_cli.py` - **PASS: 4 passed**
- `uv run pytest` - **PASS: 135 passed, 6 warnings**
- fake SSH unknown/nonzero 输出 - **PASS: lspci fallback 为 FAIL，返回本地日志和有界摘要**
- A2-AK-225 真机 - **PENDING UAT: SSH banner 当前不可用**

## User Setup Required

None - no new external service configuration required.

## Next Phase Readiness

- 04-03 可直接复用 typed/driver/fallback/diagnostic 基础，补进程解析和 `--all`。
- Phase 4 真实环境 blocker 保留：恢复 A2-AK-225 LAN/VPN/SSH 后需重跑并确认 driver_versions 已填、成功 JSON raw 字段为 null。

## Self-Check: PASSED

- **PASS:** 9 个计划关键文件均存在。
- **PASS:** 任务提交 `9e14e77`、`2ed377d`、`ae9717a` 均存在。
- **PASS:** 所有自动 acceptance criteria、硬件专项和全量测试通过。
- **PENDING UAT:** A2-AK-225 真机因外部 SSH banner 不可用未完成，不影响本计划代码与 fixture 验收结论。

---
*Phase: 04-skill-03-server-hardware-probe*
*Completed: 2026-06-09*

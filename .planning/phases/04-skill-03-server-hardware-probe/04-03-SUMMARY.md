---
phase: 04-skill-03-server-hardware-probe
plan: 03
status: blocked
subsystem: hardware-probe
tags: [ascend, process-occupancy, ps, concurrency, ssh]

requires:
  - phase: 04-02
    provides: [multi-version NPU parsing, driver metadata, lspci fallback, local diagnostics]
provides:
  - Strict numeric NPU process parsing with privacy-limited ps enrichment
  - Ordered all-server probing with at most three workers and isolated failures
  - Complete automated hardware regression coverage and real-server UAT evidence
affects: [phase-04-real-server-uat, phase-05-network-check]

tech-stack:
  added: []
  patterns:
    - Fixed ps command built only from parsed integer PIDs
    - Future exceptions converted to per-server CheckResult values
    - Aggregate output reordered to configuration order

key-files:
  created:
    - tests/fixtures/hw/npu_smi_with_processes.txt
  modified:
    - autoresearch/hw/models.py
    - autoresearch/hw/parser.py
    - autoresearch/hw/probe.py
    - autoresearch/cli.py
    - tests/test_hw_parser.py
    - tests/test_hw_probe.py
    - tests/test_hw_cli.py

key-decisions:
  - "进程补全只执行固定 pid/user/comm ps 命令，process_name 最终收敛为可执行文件 basename。"
  - "全服务器聚合保留每台 CheckResult；WARN 计入成功，任一 FAIL 令顶层失败。"
  - "真实服务器 SSH banner 全部失败时保留代码提交，但计划和 Phase 4 继续 blocked。"

patterns-established:
  - "不可信进程文本必须先严格转换为非负整数，才能进入远程命令。"
  - "并发完成顺序不影响 JSON 顺序，结果始终按 config server 顺序输出。"

requirements-completed: []

duration: 9min
completed: 2026-06-09
---

# Phase 04 Plan 03: 占用进程、全量并发与真机闸门 Summary

**安全进程补全和最多 3 worker 的全服务器探测已交付，自动测试全绿，但 5 台真实服务器均因 SSH banner 失败而阻塞 Phase 4 验收。**

## Performance

- **Duration:** 9 min
- **Started:** 2026-06-09T07:19:31Z
- **Completed:** 2026-06-09T07:28:31Z
- **Tasks:** 3 implementation tasks committed; real-server acceptance blocked
- **Files modified:** 8

## Accomplishments

- 从 `npu-smi` process 区段提取严格数字 PID、NPU/chip 标识和进程显存，拒绝恶意或无效 PID。
- 仅用固定 `ps -o pid=,user=,comm= -p ...` 批量补全，竞态和权限失败保留 PID 并降为 WARN。
- `--all` 最多 3 个并发 worker，异常不取消其他探测，结果按配置顺序稳定聚合。
- hardware 专项 41 个测试和全仓 147 个测试通过。
- 对配置中的 5 台服务器逐台及聚合命令均完成真实尝试。

## Task Commits

1. **Task 04-03-01: 解析占用进程并用安全批量 ps 补全** - `a14701c`
2. **Task 04-03-02: 增加 --all 最大 3 并发和部分失败聚合** - `27ccd4a`
3. **Task 04-03-03: 完整回归与真机闸门准备** - `fa9d6a2`

## Files Created/Modified

- `autoresearch/hw/models.py` - 更新隐私受限的进程占用契约说明。
- `autoresearch/hw/parser.py` - process/ps 解析、严格整数校验和 basename 收敛。
- `autoresearch/hw/probe.py` - 安全进程补全、并发探测和保序聚合。
- `autoresearch/cli.py` - `--server` / `--all` 二选一入口。
- `tests/fixtures/hw/npu_smi_with_processes.txt` - 有效、恶意和无效进程记录样本。
- `tests/test_hw_parser.py` - process、ps 和隐私边界断言。
- `tests/test_hw_probe.py` - race、permission、并发、顺序和部分失败断言。
- `tests/test_hw_cli.py` - 参数、退出码、单 JSON 和 all-server progress 断言。

## Decisions Made

- 无进程时完全跳过 `ps`；有进程时对 PID 去重排序后只执行一次固定命令。
- worker 只调用独立 `probe_server`，future 异常在服务器边界转为 FAIL。
- 未通过真实 UAT 前不把任何 HW requirement 标记完成，也不推进 Phase 4 状态。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 进程表不再被设备 detail 表头误解析**
- **Found during:** Task 04-03-01
- **Issue:** 进入 process 区段后，设备解析状态仍可能把进程行解释为设备 detail，污染核心指标。
- **Fix:** 识别 process 表头后终止设备表解析，由独立 `parse_processes` 处理剩余记录。
- **Files modified:** `autoresearch/hw/parser.py`
- **Verification:** process race/permission 专项和 hardware 全套测试通过。
- **Committed in:** `a14701c`

**2. [Rule 1 - Bug] process_name 强制收敛为 basename**
- **Found during:** Task 04-03-03 验证矩阵审计
- **Issue:** `parse_ps_output` 会保留带路径的 `comm` 值，不满足只返回可执行文件名的 D-19。
- **Fix:** 按 `/` 取最后一段，并增加 `/usr/bin/python3 -> python3` 回归断言。
- **Files modified:** `autoresearch/hw/models.py`, `autoresearch/hw/parser.py`, `tests/test_hw_parser.py`
- **Verification:** `uv run pytest` 通过 147 tests。
- **Committed in:** `fa9d6a2`

**Total deviations:** 2 auto-fixed Rule 1 bugs.
**Impact on plan:** 两项均是计划安全/正确性要求的必要修复，无范围扩张。

## Real-Server UAT

| Server | Exit code | Devices | Severity | Core fields | Error category |
|---|---:|---:|---|---|---|
| A2-AK-225 | 1 | 0 | fail | incomplete | ssh_banner |
| A3-AX-153 | 1 | 0 | fail | incomplete | ssh_banner |
| A3-AK-182 | 1 | 0 | fail | incomplete | ssh_banner |
| A3-AX-176 | 1 | 0 | fail | incomplete | ssh_banner |
| A2-AK-176 | 1 | 0 | fail | incomplete | ssh_banner |

Aggregate `--all`: exit 1, `ok=false`, severity `fail`, total 5, passed 0, failed 5, warned 0。结果顺序与 config 一致，`failed_servers` 包含上述全部 server。

## Issues Encountered

- 5 台真实服务器均无法完成 SSH protocol banner，未执行远端硬件命令。
- 因设备数为 0，显存、温度、利用率、driver version 和真实 process 信息均未验收。
- 该外部阻塞不影响自动测试结论，但阻止 Plan 04-03、Phase 4 和全部 HW requirements 宣称完成。

## Known Stubs

None - 修改文件中的空集合和 `None` 均为结果初始化、缺失值或测试预期，不是未接线占位。

## Verification

- `uv run pytest -q tests/test_hw_parser.py tests/test_hw_probe.py tests/test_hw_cli.py` - **PASS: 41 passed**
- `uv run pytest` - **PASS: 147 passed, 6 warnings**
- 逐台真实 `hw probe --server NAME` - **FAIL: 0/5 passed, all ssh_banner**
- 真实 `hw probe --all` - **FAIL: exit 1, ok=false, failed=5**
- 聚合顺序与 config 一致 - **PASS**

## User Setup Required

恢复本机到 5 台服务器的 LAN/VPN/SSH banner 可达性后，重新执行相同的逐台和 `--all` 验收。

## Next Phase Readiness

- 进程安全、并发和聚合代码可用于后续阶段。
- Phase 4 保持 blocked；在 5 台服务器均返回非空设备和完整四项核心指标前，不得关闭本阶段。

## Self-Check: FAILED

- **PASS:** 8 个计划关键文件均存在。
- **PASS:** 任务提交 `a14701c`、`27ccd4a`、`fa9d6a2` 均存在。
- **PASS:** 自动 acceptance criteria 和全量测试通过。
- **FAIL:** 真实服务器验收 0/5 通过，aggregate `ok=false`。
- **FAIL:** Plan 04-03 的真实完成标准未满足；requirements-completed 保持为空。

---
*Phase: 04-skill-03-server-hardware-probe*
*Blocked: 2026-06-09*

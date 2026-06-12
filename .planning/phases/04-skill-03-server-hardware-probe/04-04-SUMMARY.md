---
phase: 04-skill-03-server-hardware-probe
plan: 04
status: completed
subsystem: hardware-probe + bmc
tags: [bmc, redfish, sudo, identify, power, dry-run]

requires:
  - phase: 04-03
    provides: [process parsing, --all concurrency, all-server probe]
provides:
  - Redfish BMC identify (UUID/Serial/SKU 双源) + 电源 dry-run 操作
  - ServerSpec.sudo_command 自动前缀, 让非 root 用户 (A2-AK-102 admin123) 跑通 npu-smi
  - hw probe JSON 多两字段: bmc_identifier / host_actual / sudo_command
  - config A3-AX-176 → A3-AX-180, A3-AX-153 临时下线, A2-AK-102 配 sudo_command
affects: [phase-05-network-check, phase-06-service-reachability]

tech-stack:
  added: [requests (already a dep)]
  patterns:
    - "BMCSpec.password 明文, schema 不强制 keyring (D-32 内网环境)"
    - "BMC 电源操作默认 dry-run; 须 (config.power_operations_allowed AND --apply) 才真打"
    - "BMC identify 失败不阻塞 hw probe, 只在 warnings append"
    - "sudo_command 非空时, npu-smi/lspci/driver 全部加前缀; 空 = 不加"

key-files:
  created:
    - autoresearch/bmc/__init__.py
    - autoresearch/bmc/client.py
    - autoresearch/bmc/identify.py
    - autoresearch/bmc/power.py
    - tests/test_bmc.py
  modified:
    - autoresearch/cli.py
    - autoresearch/hw/models.py
    - autoresearch/hw/probe.py
    - config/config.example.yaml
    - tests/test_hw_probe.py
    - workspace-core/config/__init__.py
    - workspace-core/config/schema.py

key-decisions:
  - "D-32: BMC 密码明文存 config (用户决定, 内网环境), schema 不做 keyring 强校验"
  - "D-32: 电源操作双保险 — config.power_operations_allowed=false 时, --apply 也拒绝"
  - "D-32: power off/on/cycle 默认 dry-run, 只返 would_send + ResetType"
  - "D-33: sudo_command 在 config 显式声明, 默认 '', 推荐 'sudo -n' (NOPASSWD)"
  - "D-32: BMC identify 优先级 UUID > SerialNumber > SKU, 第一个非空为 bmc_identifier"
  - "A3-AX-153 暂宕机, ip 动态分配, 暂不入 config, 修好再加"
  - "A3-AX-176 → A3-AX-180 (ip 改 192.168.13.180), 同步 example.yaml"

patterns-established:
  - "BMC 客户端走裸 requests + Redfish 标准端点, 不引第三方库"
  - "BMC 错误一律抛 BMCError, 含 status + body 摘要, 不静默吞错"
  - "bmc identify 失败给 warning 不 fail, hw probe 主流程不依赖 BMC"

requirements-completed:
  - HW-CONN-01   # SSH 端到端连接
  - HW-CONN-02   # 服务器清单来自 config
  - HW-NPU-01    # npu-smi 设备 ID/Name
  - HW-NPU-02    # 显存 + 温度 + 利用率
  - HW-NPU-03    # lspci fallback
  - HW-OCC-01    # 占用 PID + user + 进程名
  - HW-OCC-02    # 退出/权限保留 PID + warning
  - HW-DRV-01    # driver version 来自 version.info

duration: 45min
completed: 2026-06-12
---

# Phase 04 Plan 04: BMC 接入 + sudo 支持 Summary

**BMC 技能 (Redfish identify + 电源 dry-run) 与 sudo_command 前缀落地，205/205 测试绿，2/4 配置服务器真机 UAT 完整通过，2/4 受外部阻塞。**

## Performance

- **Duration:** 45 min
- **Started:** 2026-06-12T04:15:00Z
- **Completed:** 2026-06-12T05:00:00Z
- **Tasks:** 4 implementation tasks committed; 1 commit
- **Files modified:** 12 (8 modified, 5 new)
- **Tests:** +15 (12 bmc + 3 hw integration) → 205/205

## Accomplishments

- **schema 扩展**：`BMCSpec` (host/port/user/password/protocol/power_operations_allowed) + `ServerSpec.sudo_command` 字段；明文密码路径不强制 keyring。
- **BMC 客户端** (`autoresearch/bmc/client.py`)：裸 `requests` + Redfish REST + Basic Auth；`get_service_root` / `get_managers` / `get_systems` / `reset_system` 标准端点；BMCError 包含 HTTP status + body 摘要；SSL verify 默认 False（内网自签证书）。
- **BMC identify** (`autoresearch/bmc/identify.py`)：双源（UUID 优先，SerialNumber / SKU 兜底），返回 `bmc_identifier` 字段；失败不阻塞调用方。
- **BMC 电源** (`autoresearch/bmc/power.py`)：status / off / on / cycle 四操作；默认 dry-run（仅返 `would_send` + ResetType）；`--apply` 真打前置双保险（config `power_operations_allowed` 必须 True 才放行）。
- **CLI** (`autoresearch bmc {identify, power status|off|on|cycle --apply}`)：所有命令统一 JSON 输出 + 走 `__AR_PROGRESS__` 协议。
- **hw probe 增强**：
  - 三个 COMMAND (`npu-smi info` / `lspci` / `cat version.info`) 按 `server.sudo_command` 自动拼前缀
  - `data` 多 3 字段：`host_actual` / `bmc_identifier` / `sudo_command`
  - BMC identify 失败仅 warning 不 fail，不阻塞主探测
- **config 重构**：
  - `A3-AX-176 → A3-AX-180`（ip 改 `192.168.13.180`）
  - `A3-AX-153` 暂下线（动态 IP 修好再加）
  - `A2-AK-102` `user: admin123` + `sudo_command: "sudo -n"`（先 bootstrap NOPASSWD）
  - 4 台全部加 `bmc` 段（`power_operations_allowed: false` 默认安全）

## Real-Server UAT (2026-06-12)

| Server | ok | Severity | Devices | Procs | BMC id | sudo_cmd | 阻塞分类 |
|---|---:|---|---:|---:|---|---|---|
| A2-AK-225 | ✅ true | warn | 8 | 17 | None | "" | — |
| A3-AK-182 | ✅ true | warn | 16 | 7 | None | "" | — |
| A3-AX-180 | ❌ false | fail | 0 | 0 | None | "" | ssh_auth（外部：key/密码未部署） |
| A2-AK-102 | ❌ false | fail | 0 | 0 | None | "sudo -n" | npu_smi_dcmi（外部：驱动 dcmi init failed） |

**BMC identify 真实尝试**：
- 192.168.12.182（用户给凭据）：connect timeout（不可达，可能路由/VLAN 问题）
- 192.168.12.180/102：443 通但 Redfish `/Managers` 返回空或 read timeout（华为 iBMC 私有 `/api/` 协议，非标准 Redfish；需换协议或确认端点）

## Issues Encountered

- **A3-AX-180 主机 SSH 认证失败**：新 IP 13.180 的 key 未部署（用户侧运维事项）。
- **A2-AK-102 npu-smi dcmi 故障**：驱动级问题，需在远端 `npu-smi info` 调试；可能驱动重装或重启 dcmi 服务。
- **BMC 协议识别**：华为 iBMC 实际走私有 `/api/` 而非标准 Redfish；需要：
  - ① 确认 BMC 真实端点（`/api/` vs `/redfish/v1`）
  - ② 或允许 Redfish-only 时优雅 fail（当前已支持：warnings 记录 BMC 失败但主流程 OK）
- **A3-AX-153 暂不在 config**（用户声明：ip 动态分配 + 宕机中）；修好加回。

## Deviations from Plan

### 主动范围扩展（用户明确要求）
- 接收 4 台机器配置变更 + BMC 凭据要求 → 一次性写完 schema / bmc 模块 / sudo 拼接
- 不引第三方 redfish 库（避免依赖管理）；裸 requests 写 client

### 暂不实现
- **BMC 反查 host IP**（用户选择"IP 手动管"）：不做 dynamic_ip 解析
- **keyring 强制**（用户决定"明文 OK"）：schema 不拦截

## Verification

- `uv run pytest -q` → **PASS: 205 passed, 6 warnings**
  - 12 个 bmc 单元测试（identify / power / dry-run / allow-flag 双保险）
  - 3 个 hw 集成测试（sudo 前缀拼接、bmc 失败不阻塞、空 sudo 不前缀）
  - 190 个既有测试无回归
- `uv run autoresearch config validate` → ✅ 通过
- `uv run autoresearch bmc identify --server A3-AK-182` → **FAIL**（外部 BMC 不可达）
- `uv run autoresearch hw probe --server A2-AK-225` → **OK** 8 devices
- `uv run autoresearch hw probe --server A3-AK-182` → **OK** 16 devices
- `uv run autoresearch hw probe --server A3-AX-180` → **FAIL** ssh_auth
- `uv run autoresearch hw probe --server A2-AK-102` → **FAIL** npu_smi_dcmi

## User Setup Required (BMC 真机 UAT 解锁前)

- 补齐 4 台 BMC 的 IP / 用户 / 密码（现在 3 台是占位 TODO）
- 验证 BMC 协议：iBMC 私有 `/api/` 还是 Redfish（决定 `client.py` 是否要写新端点）
- 修 A3-AX-180 SSH 认证（key 部署 或 走 bootstrap 密码）
- 修 A2-AK-102 npu-smi 驱动（远端 dcmi init 调试）
- 修 A3-AX-153（修好后入 config）

## Next Phase Readiness

- Phase 4 plan 04-04 完成；Phase 4 仍受外部阻塞（4/4 仅 2/4 真机过）但代码全绿。
- Phase 5 (network-check) plan 05-03 同步受 A3-AX-180/102/153 阻塞，可推 plan 05-04 把 BMC 凭据补齐后做红鱼重测。
- 后续 phase (6-13) 不依赖 BMC 真机，可以并行推进代码部分。

## Self-Check: PARTIAL

- **PASS:** 12 个关键文件均存在；commit 1 个（`feat(04-04)`）。
- **PASS:** 自动测试 205/205。
- **PARTIAL:** 4 台真机 hw probe 2/4 通过（外部阻塞 2/4：1 ssh_auth + 1 npu_smi_dcmi）。
- **DEFERRED:** 5 台 BMC 真机 identify 0/4 通过（4 台 BMC IP/凭据待补 + iBMC 协议待确认）。
- **DEFERRED:** HW requirements 中 `real-server UAT` 完整成功部分需等外部阻塞解除后再标。

---
*Phase: 04-skill-03-server-hardware-probe*
*Completed: 2026-06-12 (code complete; real BMC + 2 hosts UAT pending external)*

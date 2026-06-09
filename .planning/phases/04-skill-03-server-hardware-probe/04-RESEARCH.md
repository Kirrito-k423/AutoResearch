---
phase: 04
slug: skill-03-server-hardware-probe
status: complete
researched: 2026-06-09
---

# Phase 4 — Server Hardware Probe Research

## Research Question

怎样在不绕过现有 `workspace_core` 抽象的前提下，把 Ascend 910 系列服务器的 NPU 显存、温度、利用率、占用进程和驱动版本稳定地采集为结构化 JSON，并让解析失败可诊断、可扩展、可在全部真实服务器上验收？

## Executive Summary

推荐实现为“固定命令采集 + 纯解析器 + 结果装配”三层：

1. `SSHClient` 只负责执行固定的只读命令，不在硬件 skill 中直接使用 Paramiko。
2. `npu-smi info` 是设备枚举、默认指标和进程段的主数据源；解析器按表头与分隔线识别列，不能按固定字符位置切片。
3. 当默认输出缺少核心字段时，可探测性地调用官方文档中的 typed query 形态（如 `-t usages`、`-t temp`、`-t memory`）补充；必须依据退出码和输出实际能力判断，不假设所有 910/驱动版本都支持同一参数。
4. `npu-smi` 不存在或格式未知时执行 `lspci`，但该结果只能证明设备存在，仍是 `FAIL`。
5. `npu-smi` 解析器必须是无 SSH 依赖的纯函数，并以脱敏 fixture 覆盖多版本、空进程、未知格式和字段缺失。
6. 第一份计划就交付可运行的单服务器纵向切片；第二份补兼容/诊断；第三份补进程与 `--all`，并执行全部配置服务器真机验收。

这能避免把阶段再次拆成“先写模型、再写 SSH、最后才看到服务器”的水平层。执行 04-01 后，用户就能运行 `autoresearch hw probe --server A2-AK-225` 看到真实核心指标。

## Primary Sources

- Huawei Support, `Information Querying Commands (info)`：`npu-smi info` 是设备信息查询入口，产品/版本对字段和参数的支持可能不同。  
  https://support.huawei.com/enterprise/en/doc/EDOC1100133163/2445e8ee/information-querying-commands-info
- Huawei HiAscend, `npu-smi 命令参考`：官方命令参考展示 `npu-smi info` 以及按类型查询 common/usages/temp/memory 等信息的命令形态。该文档面向 Atlas 200I A2，不能当作 910B 的精确字段契约，只用于证明命令族和版本差异确实存在。  
  https://www.hiascend.com/doc_center/source/zh/Atlas%20200I%20A2/24.1.RC2/re/npu/Atlas%20A2%20%E6%99%BA%E8%83%BD%E8%BE%B9%E7%BC%98%E7%A1%AC%E4%BB%B6%2024.1.RC2%20npu-smi%20%E5%91%BD%E4%BB%A4%E5%8F%82%E8%80%83%2001.pdf

## Existing System Fit

### Reuse without duplication

- `workspace_core.ssh.SSHClient`
  - `connect(connect_timeout=5, retries=3)` 已满足 `HW-CONN-02` 的连接超时基础。
  - `exec(command, timeout=30)` 返回 `(exit_code, stdout, stderr)`，足够执行所有只读采集命令。
  - Phase 4 不应直接 import `paramiko`。
- `workspace_core.config.from_path`
  - 读取服务器清单和凭据占位符。
  - 服务器名必须先做配置查找，再转换为 `HostSpec`；不得把用户输入拼进 shell 命令。
- `workspace_core.result.CheckResult`
  - 实际字段是 `ok/severity/data/message/error`，计划和实现必须保留 `message`，不能只实现 CONTEXT 中的简写四字段。
  - `merge()` 只保留计数，不保留每台服务器数据，因此 `--all` 需自行聚合结果，再复用相同的严重度优先级语义。
- `workspace_core.progress.emit_progress`
  - 每台服务器至少发出 connect、command、parse、complete/fail 事件。
  - stdout 最终只打印一个 JSON 对象。
- `workspace_core.layout.LOGS_DIR` 与 `workspace_core.log`
  - 解析失败时将原始 stdout/stderr 写到本机 `~/.autoresearch/logs/`。
  - 日志文件名中的服务器名必须先收敛为安全字符。
- `autoresearch.ping._resolve_server_host`
  - 已有“配置服务器 → HostSpec”的可复用模式。
  - 建议将此逻辑下沉为硬件包私有 helper 或公共配置 helper，避免硬件模块反向 import `ping.py`。

## Recommended Architecture

### Package layout

```text
autoresearch/hw/
  __init__.py
  models.py
  parser.py
  probe.py
tests/
  fixtures/hw/
    npu_smi_25_3_rc1_no_processes.txt
    npu_smi_with_processes.txt
    npu_smi_missing_metric.txt
    npu_smi_unknown_format.txt
    lspci_ascend.txt
  test_hw_parser.py
  test_hw_probe.py
  test_hw_cli.py
```

### Data contract

Use standard-library `TypedDict` or dataclasses; no new runtime dependency is needed.

- `NPUDevice`
  - `id: int | None`
  - `chip_id: int | None`
  - `name: str | None`
  - `health: str | None`
  - `bus_id: str | None`
  - `memory_total_mib: int | None`
  - `memory_used_mib: int | None`
  - `temperature_c: int | None`
  - `utilization_pct: int | None`
- `NPUProcess`
  - `npu_id: int | None`
  - `chip_id: int | None`
  - `pid: int`
  - `user: str | None`
  - `process_name: str | None`
  - `memory_used_mib: int | None`
- `DriverVersions`
  - `npu_smi: str | None`
  - `driver: str | None`
  - `package: str | None`
- `HardwareData`
  - `server`
  - `devices`
  - `processes`
  - `driver_versions`
  - `warnings`
  - `field_errors`
  - `fallback`
  - `raw_log_path`

JSON 字段建议保留单位后缀，避免消费者误解；若为了需求文本使用 `memory_total` 等短名，则必须在 `data.units` 明确 `MiB/°C/%`。不要混用两种命名。

### Command bundle

固定执行下列只读命令，命令文本由代码常量定义：

1. `npu-smi info`
2. 核心字段缺失时，按能力探测 typed query（候选：`common/usages/temp/memory`）
3. `cat /usr/local/Ascend/driver/version.info`
4. 解析出 PID 后，批量执行 `ps -o pid=,user=,comm= -p <comma-separated numeric PIDs>`
5. 主命令不可用或无法识别时执行 `lspci -Dnn`

PID 必须由解析器转换为整数后再拼接；不能把远程输出中的任意字符串直接带回 shell。服务器名只用于配置查找和日志标签，不进入远程命令。

### Parser strategy

`npu-smi info` 的默认输出包含多个区段，首批解析应分成：

- header/version parser
- device table parser
- process table parser
- driver `version.info` parser
- `lspci` parser

设备表解析流程：

1. 找到表头行并规范化列名（小写、压缩空格、删除单位标记）。
2. 根据 `|` 分隔单元格，忽略边框线。
3. 识别双行设备记录：第一行提供 id/name/health/power/temp，第二行提供 chip/bus/AICore/memory/HBM。
4. 对 `used / total` 形式按语义映射为 used、total，不依赖列宽。
5. 每张设备完成后检查四个核心指标；缺失值为 `None`，并写入带设备 id 和字段名的 `field_errors`。
6. 未识别的非空区段不能静默忽略；至少产生 warning，完全无法识别设备时触发 fallback。

typed query 是补充通道，不是对默认表格式失败的掩盖。补充成功后仍保留“默认输出版本未知”的 warning，方便以后扩 fixture。

### Result and exit behavior

单服务器返回完整 `CheckResult`：

- `OK`: 所有设备的四个核心指标齐全，只有完整或无 warning。
- `WARN`: 核心指标齐全，但驱动文件、进程 user/name 等非核心字段缺失。
- `FAIL`: SSH/命令失败、没有设备、或任一设备核心指标缺失。

`--all` 返回一个顶层 `CheckResult`，`data.results` 按配置顺序保留每台服务器结果，并额外给出 `passed_servers`、`failed_servers` 和计数。只要一台服务器失败，顶层 `ok=false`、退出码 1；其他 future 完成后仍要输出。

配置/参数错误退出 2；探测/解析失败退出 1；全部服务器成功退出 0。

## Diagnostics and Local-First Rules

- 成功路径不把完整 raw output 放入 JSON。
- 失败路径写本地日志，内容包括命令、退出码、stdout、stderr，但不得记录凭据、环境变量或 SSH 私钥路径内容。
- JSON 只返回：
  - `raw_output_summary`: 截断后的文本，建议最大 512 字符。
  - `raw_log_path`: 本地绝对路径。
- 日志文件名建议 `hw-<safe-server>-<UTC timestamp>.log`。
- `process_name` 使用 `ps ... comm=`，不使用 `args=` 或完整命令行，避免泄露训练参数和 token。

## Concurrency

`--all` 使用 `ThreadPoolExecutor(max_workers=min(3, server_count))`。提交顺序可以并发，但最终结果按配置中的服务器顺序排列，避免 JSON 每次抖动。

每个 worker 自己创建、连接并关闭 `SSHClient`；禁止跨线程共享 Paramiko client。异常必须在 worker 边界转为该服务器的 `CheckResult`，不能让一个 future 抛出后中止其余 future。

## Validation Architecture

### Automated layers

1. Parser unit tests
   - 25.3.rc1 双行设备记录，8 卡、65536 MiB、温度、利用率。
   - 无进程输出得到 `[]`。
   - 有进程输出得到 pid/device/memory。
   - 字段缺失得到 `None + field_errors + FAIL`。
   - 未知格式触发 fallback 信号。
   - `lspci` 只计 Huawei processing accelerator，不计 bridge/NIC/management device。
   - driver version file 缺失为 warning，不覆盖 `npu-smi` version。
2. Probe orchestration tests
   - fake `SSHClient` 按命令返回 fixture。
   - connect/command error 转为 FAIL，保留已采数据。
   - `ps` race/permission error保留 process 并产生 warning。
   - raw log 只在失败时创建。
3. CLI tests
   - `--server` 与 `--all` 互斥且二选一。
   - stdout 可被 `json.loads` 解析且只有一个对象。
   - stderr 包含 `__AR_PROGRESS__=`。
   - exit 0/1/2 分支。
   - `--all` 最大并发 3，失败不取消其他服务器。

### Real-server UAT

Phase 4 完成前必须针对 `config/config.yaml` 当前每台服务器运行：

```bash
uv run autoresearch hw probe --server <NAME>
```

每台都必须满足：

- SSH 连接成功。
- `devices` 非空且卡数与现场一致。
- 每张卡 `memory_total_mib`、`memory_used_mib`、`temperature_c`、`utilization_pct` 均为整数且非空。
- `driver_versions.npu_smi` 或 driver file 版本至少有一项可用；仅 driver file 缺失允许 WARN。
- stdout 是唯一 JSON，stderr 只有进度/诊断。

最后运行：

```bash
uv run autoresearch hw probe --all
```

验证所有服务器都在结果中，顺序稳定，顶层 `ok=true`。

### Current environment risk

2026-06-09 规划期间，直接对当前配置中的 5 台服务器做 8 秒 SSH 采样时全部超时，包括此前已成功验证的 `A2-AK-225`。这更像本地 LAN/VPN/服务器临时不可达，而非实现结论。

计划必须：

- 将真机 UAT 放在最终完成闸门，而不是用 fixture 替代。
- 网络不可达时保留实现和自动测试成果，但 Phase 4 状态不得标记 Complete。
- 恢复连接后重跑全部服务器，不只重跑 A2 基准机。

## Plan Shape Recommendation

### 04-01 — 单服务器真实纵向切片

交付 `autoresearch hw probe --server NAME`：配置解析 → SSH → `npu-smi info` → 核心设备指标 → CheckResult JSON。首个执行计划结束时就能连真实 A2，不再等待后续“胶水计划”。

### 04-02 — 兼容、驱动与失败诊断

增加多版本 fixture、typed query 补充、driver file、`lspci` fallback 和失败 raw log。把格式变化从线上故障变成可扩展测试样本。

### 04-03 — 占用进程、全量并发与真机闸门

增加 process parser + 安全 `ps` enrichment、`--all` 最大并发 3、部分失败聚合，并对全部配置服务器执行真机 UAT。此计划是 Phase 4 完成闸门。

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 不同驱动版本表头变化 | 核心字段无法解析 | 表头驱动 parser + fixture；typed query 仅作能力探测补充 |
| 双行记录错误配对 | 卡和指标串位 | 以 NPU/chip id 和表区段边界建状态机，遇到新记录先提交旧记录 |
| `ps` 竞态或权限不足 | 占用方不完整 | PID 保留，user/name 为 null，warning，不升级为核心 FAIL |
| raw output 泄露命令参数 | 本地日志包含敏感数据 | 不采 `ps args`，仅固定命令；日志本地化并限制 JSON 摘要 |
| 一台服务器卡住 `--all` | 用户看不到其他服务器 | 每连接 5s、命令 30s、worker 捕获异常、最多 3 并发 |
| 当前 5 台服务器不可达 | 无法关闭 Phase 4 | 代码/fixture 可推进，但真机闸门保持未通过，恢复后统一补验 |

## Research Complete

研究结论足以直接规划，无需新增用户决策。实现应优先交付单服务器端到端结果，再扩兼容和全量验收。

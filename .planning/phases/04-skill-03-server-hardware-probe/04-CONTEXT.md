# Phase 4: Skill 03 — server-hardware-probe - Context

**Gathered:** 2026-06-09
**Status:** Ready for planning

<domain>
## Phase Boundary

实现 `autoresearch hw probe`，通过 Phase 2 的 `workspace_core.ssh` 连接配置中的 Ascend 910 系列服务器，采集并结构化输出 NPU 设备、显存、温度、利用率、占用进程和驱动版本。本阶段必须使用真实服务器验收，并提供 `npu-smi` 解析失败时的 `lspci` 降级诊断。

本阶段不实现网络代理探测、远程服务可达性、训练栈检查或 NVIDIA GPU 支持；这些分别属于后续阶段或未来范围。

</domain>

<decisions>
## Implementation Decisions

### 真实服务器与兼容范围

- **D-01:** `A2-AK-225` 是首个基准服务器。已确认该机有 8 张 Ascend 910B2，单卡 65536 MiB HBM，`npu-smi 25.3.rc1` 可用。
- **D-02:** M1 支持边界是 Ascend 910 系列，不只绑定 910B2 或单一 `npu-smi` 版本；NVIDIA GPU 不纳入本阶段。
- **D-03:** 配置文件中的每台服务器都必须执行完整真机验收，不以“SSH 成功”或“识别出卡数”代替硬件指标验收。
- **D-04:** 每张 NPU 的 `memory_total`、`memory_used`、`temperature`、`utilization` 是核心必填指标。
- **D-05:** 单台服务器失败不阻断其他服务器继续探测，但失败服务器必须保留完整错误，并阻止 Phase 4 宣称全量完成。

### CLI、结果结构与退出语义

- **D-06:** CLI 提供 `autoresearch hw probe --server NAME` 探测单台服务器，以及 `autoresearch hw probe --all` 探测配置中的全部服务器。
- **D-07:** `--all` 使用有限并发，默认最多同时探测 3 台服务器。
- **D-08:** 单台服务器结果复用 `CheckResult` 风格的顶层结构：`ok`、`severity`、`data`、`error`。
- **D-09:** `data` 至少包含 server 元信息、devices、processes、driver_versions、warnings 和 field_errors。
- **D-10:** 核心指标缺失时字段值为 `null`，在 `field_errors` 中说明原因，并令该服务器 `ok=false`；不得用 `0` 冒充缺失值，也不得丢弃已经成功解析的部分数据。
- **D-11:** CLI 退出码：全部成功为 `0`；SSH、命令或解析失败为 `1`；配置或参数错误为 `2`。
- **D-12:** 指标单位统一为：显存 MiB、温度摄氏度、利用率整数百分比。
- **D-13:** 严重度规则：SSH 失败或核心指标缺失为 `FAIL`；仅非核心字段缺失为 `WARN`；字段完整为 `OK`。
- **D-14:** 最终 stdout 遵守仓进度协议，只输出唯一 JSON 对象；关键过程通过 stderr 的 `__AR_PROGRESS__=` 事件报告。

### 原始输出与诊断

- **D-15:** 成功解析时不把完整 `npu-smi` 原始输出塞入 JSON。
- **D-16:** 解析失败时把原始输出写入本地日志，并在 JSON 中返回有长度限制的摘要和日志路径，便于增加新版本 fixture。
- **D-17:** 失败不应抹掉已成功采集的数据；输出需支持用户判断是连接失败、命令不存在、格式未知还是单字段缺失。

### 占用进程补全

- **D-18:** 从 `npu-smi` 解析 PID、设备、进程显存；再按 PID 在远程执行 `ps`，补齐 user 和 process_name。
- **D-19:** `process_name` 只返回可执行文件名，不返回完整命令行参数，避免泄露训练参数、路径或 token。
- **D-20:** 若进程在 `npu-smi` 与 `ps` 之间退出，保留 PID，把无法补齐的字段置为 `null`，并增加 warning。
- **D-21:** 若 `ps` 因权限不足无法读取，保留该进程记录，user/process_name 为 `null`，并增加 warning；这类非核心字段缺失本身不令服务器失败。

### npu-smi 兼容与降级

- **D-22:** 解析器按表头与分隔结构识别字段，不使用固定字符位置切片。
- **D-23:** 测试维护多版本、空进程、有进程、字段缺失和未知格式的 `npu-smi` 输出 fixture。
- **D-24:** `npu-smi` 不存在或格式无法解析时执行 `lspci` 降级，返回可识别的设备数量、PCI 地址和原始设备描述。
- **D-25:** `lspci` 只能证明设备存在，无法提供核心动态指标，因此降级结果必须为 `ok=false` / `severity=FAIL`。
- **D-26:** 驱动信息同时采集 `npu-smi` 表头版本和 `/usr/local/Ascend/driver/version.info`；文件不存在时保留 `npu-smi` 版本并记 warning。

### 完成门槛

- **D-27:** Phase 4 完成前，当前配置中的全部服务器都必须完成真机探测，并成功解析每张卡的显存、温度和利用率。
- **D-28:** 真实服务器验收之外，fixture 单测必须覆盖 `lspci` 降级、未知格式、无进程、进程竞态和权限不足。
- **D-29:** 探测单台失败时仍继续收集其他服务器结果；最终聚合结果为失败，并明确列出通过和失败服务器。

### the agent's Discretion

- `data` 内部字段的具体嵌套层级和 Pydantic/TypedDict 型别选择。
- 多版本 fixture 的首批版本数量和文件命名。
- 原始输出摘要的长度上限、日志文件名和 progress stage 命名。
- `--all` 并发实现细节，但默认并发上限必须为 3。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目约束与需求

- `AGENTS.md` — CLI、测试、进度协议、本地优先和 Phase 4 映射的单源真相。
- `.planning/PROJECT.md` — Ascend 环境、真实服务器、本地优先和远端偶发断网等约束。
- `.planning/REQUIREMENTS.md` — `HW-CONN-01..02`、`HW-NPU-01..03`、`HW-OCC-01..02`、`HW-DRV-01`。
- `.planning/ROADMAP.md` — Phase 4 目标、成功标准和三项计划草案。
- `.planning/STATE.md` — 当前阶段位置和已完成的真实 SSH/反向隧道验证。

### 可复用前置实现

- `.planning/phases/02-workspace-core/02-CONTEXT.md` — SSHClient、错误分类、超时、进度协议、结果结构等已锁定决策。
- `.planning/phases/02-workspace-core/02-01-SUMMARY.md` — `workspace_core.ssh` 已实现接口和测试范围。
- `.planning/phases/02-workspace-core/02-03-SUMMARY.md` — `CheckResult`、日志、layout 和 progress emitter。
- `.planning/phases/02-workspace-core/02-04-SUMMARY.md` — `autoresearch ping --server` 的真实服务器入口模式。
- `ARCHITECTURE.md` — server-hardware skill 的边界及其与网络、服务、训练栈的分工。

### 真实环境样本

- `config/config.yaml` — 本机实际服务器清单；敏感值不得写入计划或提交。
- A2-AK-225 现场输出（2026-06-09 会话验证）— 8×Ascend 910B2、65536 MiB HBM、`npu-smi 25.3.rc1`、当前无运行进程、driver package `25.3.rc1`。规划阶段应将脱敏后的输出固化为测试 fixture。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `workspace-core/ssh/client.py`：统一 `connect/exec`、重试和 SSH 错误；Phase 4 不直接调用 paramiko。
- `workspace-core/ssh/host.py`：服务器目标解析。
- `workspace-core/config/loader.py` 与 `workspace-core/config/schema.py`：读取服务器清单和 identity file。
- `workspace-core/progress/emitter.py`：stderr 进度协议。
- `workspace-core/log/`：解析失败原始输出的本地日志。
- `workspace-core/result/`：`CheckResult` 和 `OK/WARN/FAIL` 聚合。
- `autoresearch/ping.py`：从配置解析服务器、真实 SSH CLI、唯一 JSON stdout 和退出码处理的现有范式。
- `autoresearch/services/_common.py`：有限并发探测模式，可借鉴但不应与硬件域混用。

### Established Patterns

- 单一 `autoresearch` Click 命令树；新增 `hw` group 和 `probe` 子命令。
- 默认中文错误，`--lang en` 切英文。
- CLI happy path 必须有 `CliRunner` 单测。
- 业务解析与 SSH/CLI 分层，fixture 测纯解析，真实服务器做 UAT。
- 所有状态和数据留在本地 Mac，远程只执行只读探测命令。

### Integration Points

- `autoresearch/cli.py`：挂载 `autoresearch hw probe`。
- `autoresearch/hw/`：新增主机探测、解析器、进程补全、驱动采集和结果 schema。
- `tests/`：CLI、探测编排和多版本解析 fixture。
- `~/.autoresearch/logs/`：未知输出和失败诊断落点。

</code_context>

<specifics>
## Specific Ideas

- 基准机 A2-AK-225 的 `npu-smi info` 是双行设备记录：第一行包含 NPU id/name/health/power/temp，第二行包含 chip/bus-id/AICore/memory/HBM。
- 当前样本的 HBM 字段形如 `3467 / 65536`，应映射为 `memory_used=3467`、`memory_total=65536` MiB。
- 进程区可能出现 `No running processes found in NPU N`，这应解析为空列表，而不是错误。
- `lspci` 样本中 Ascend 设备表现为 Huawei `Processing accelerators`，设备 ID 为 `d802`；不要把其他 Huawei bridge、网卡和管理芯片误计为 NPU。

</specifics>

<deferred>
## Deferred Ideas

- NVIDIA `nvidia-smi` 支持留给未来里程碑，不纳入 Phase 4。
- 进程完整命令行、训练参数和环境变量采集不做，避免敏感信息泄露。
- NPU 实时持续监控、历史曲线和告警属于后续 Prometheus/数据采集阶段。

</deferred>

---

*Phase: 4-skill-03-server-hardware-probe*
*Context gathered: 2026-06-09*

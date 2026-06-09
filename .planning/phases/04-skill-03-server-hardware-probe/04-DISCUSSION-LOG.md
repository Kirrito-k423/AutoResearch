# Phase 4: Skill 03 — server-hardware-probe - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-09
**Phase:** 4-skill-03-server-hardware-probe
**Areas discussed:** 首台验收服务器与兼容范围, JSON 输出与部分失败策略, NPU 进程用户信息补全, npu-smi 版本差异与 lspci 降级

---

## 首台验收服务器与兼容范围

| Decision | Selected | Alternatives |
|----------|----------|--------------|
| 基准服务器 | A2-AK-225 | 全部服务器同时作为基准；指定另一台 |
| 兼容边界 | Ascend 910 系列 | 仅 910B2/25.3.rc1；同时支持 NVIDIA |
| 其他服务器验收 | 每台完整解析核心指标 | 仅基础冒烟；只验收基准机 |
| 单机失败 | 继续探测其他机器，但阻止阶段完成 | 立即停止；仅基准机失败才阻断 |

**User's choice:** A2-AK-225 为基准，全部配置服务器完整真机验收。
**Notes:** 用户明确指出显存、温度、利用率是最重要的指标，必须解析。

---

## JSON 输出与部分失败策略

| Decision | Selected | Alternatives |
|----------|----------|--------------|
| 顶层结构 | `ok/severity/data/error` | 平铺字段；只返回硬件数据 |
| 核心指标缺失 | `null + field_errors + ok=false` | 填 0；丢弃全部 data |
| 退出码 | 成功 0、探测失败 1、配置错误 2 | SSH 成功即 0；错误统一 1 |
| 原始输出 | 失败时落日志并返回摘要 | 始终进 JSON；完全丢弃 |
| 多服务器入口 | `--server NAME` 与 `--all` | 只支持单台；默认全部 |
| 并发 | 默认最多 3 台 | 串行；无限制并发 |
| 单位 | MiB / 摄氏度 / 整数百分比 | GiB 浮点；原始字符串 |
| 严重度 | 核心失败=`FAIL`，非核心缺失=`WARN`，完整=`OK` | warning 均失败；二态结果 |

**User's choice:** 全部采用推荐结构和分级策略。
**Notes:** 部分成功数据必须保留，缺失不可伪装成零值。

---

## NPU 进程用户信息补全

| Decision | Selected | Alternatives |
|----------|----------|--------------|
| 用户补全 | 远程 `ps` 按 PID 补齐 | 只用 npu-smi；user 永远 null |
| 进程竞态 | 保留 PID，缺失置 null 并 warning | 丢弃进程；整机失败 |
| 进程名称 | 仅可执行文件名 | 完整命令行；两者都返回 |
| 权限不足 | 保留记录并 warning | 整机失败；跳过进程 |

**User's choice:** 全部采用推荐策略。
**Notes:** 不采集完整命令行，避免泄露参数和敏感信息。

---

## npu-smi 版本差异与 lspci 降级

| Decision | Selected | Alternatives |
|----------|----------|--------------|
| 解析策略 | 表头驱动、多版本 fixture | 只支持当前版本；固定位置切片 |
| lspci 降级 | 返回设备基础信息但 `ok=false` | 找到设备即成功；不执行降级 |
| 驱动版本 | npu-smi + driver/version.info | 仅 npu-smi；仅版本文件 |
| 阶段完成 | 全部配置服务器真机通过 + fixture 降级覆盖 | 只验收基准机；真机只测连接 |

**User's choice:** 全部采用推荐策略。
**Notes:** `lspci` 没有显存、温度和利用率，不能被包装成成功。

---

## the agent's Discretion

- JSON 内部嵌套和类型实现。
- fixture 数量与命名。
- 日志摘要长度和 progress stage 名称。

## Deferred Ideas

- NVIDIA GPU 支持。
- 完整进程命令行采集。
- 持续监控与历史指标。

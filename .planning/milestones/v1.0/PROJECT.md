# AutoResearch

## What This Is

AutoResearch 是一个本地驱动的 LLM 训练/调试工作流平台。所有运行数据、状态、思考过程都留在本机 Mac 上，远程服务器（NPU/GPU）只是被远控的执行终端。平台提供 8 个独立 skill 串成一个"健康检查 → 训练 → 采集 → 报告"的最小循环，并把这 8 个 skill 包装成可被 Archon workflow 触发的标准单元，让用户既能 CLI 跑也能 `archon workflow run` 跑。

## Core Value

**"常实践，详记录，知得失，会设计，有整理"——每个 skill 跑一次都留下可被复盘、可被二次开发的产物。**

如果一切失败，这一条不能失败：用户的每一次实验，都能在本地找到 (a) 实验当时的 log、(b) wandb 指标、(c) 资源曲线、(d) 决策与变更记录、(e) 失败原因与改进建议。

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

**8 步最小循环 (M1) — 每个 skill 一个 REQ 组：**

- [ ] **CFG** — 客户配置文件（GitHub 凭据、服务器清单、密码加密）
- [ ] **SVC** — 本地服务栈（Archon / wandb / Prometheus / Grafana）健康检查
- [ ] **HW** — 服务器硬件探针（SSH 连通、npu-smi、占用方）
- [ ] **NET** — 网络环境探针（baidu/huggingface/github 测速 + SSH 反向代理）
- [ ] **REACH** — 服务可达性（远程 → 本地 wandb/Prometheus 探活）
- [ ] **STACK** — 训练栈健康（verl / veomni conda env + 1-step 干跑）
- [ ] **COLL** — 数据采集（最小实验 + wandb sync + log tail + prom push）
- [ ] **RPT** — 实验报告（单页 HTML，含 log/wandb/prom 三视图）

**M1 跨 skill 能力：**

- [ ] **ARCH** — Archon workflow 适配（8 skill → Archon DAG）
- [ ] **ORCH** — 顶层 CLI 编排（`autoresearch check all` / `autoresearch run smoke`）
- [ ] **E2E** — 端到端 smoke + 报告（一次 M1 跑通）
- [ ] **CORE** — workspace-core / verl-workspace-adapter / datalake 三沉淀层

### Out of Scope

- **分布式训练调度（v2）** — v1 单机单卡跑通，多机调度留给后续里程碑
- **多云（v2）** — 假设用户主用一台远程 NPU 服务器，不接 AWS/Aliyun/Tencent 多云
- **多租户 / 团队协作（v2）** — v1 是单用户单本机，多人协作需要用户系统与权限层
- **Web UI 自研（v1 不做）** — 复用 Archon Web UI + wandb 自带 UI + Grafana，不再造轮子
- **全模型适配（v1 聚焦）** — v1 跑通 verl + veomni 两个框架即可，其他训练框架（torchtune、axolotl）留 v2
- **训练任务自动调度（v1 暂不做）** — Archon 没有内置 cron；v1 用 OS-level launchd/cron，v2 再做 archon-scheduler

## Context

**用户与硬件环境：**
- 单用户，单本机（macOS），开发主要在这台 Mac
- 远程服务器：Linux（Ubuntu/CentOS），配 NPU（Ascend 910 系列），偶发断网
- 远程账号：`root@192.168.13.154`，工作目录 `/home/t00906153`
- Mac 与远程通过 SSH 通信；远程无外网时通过 Mac 反向代理 (`127.0.0.1:7890`)

**技术栈：**
- 语言：Python 3.11+（与 verl/veomni 生态一致）
- 远程控制：paramiko（SSH 客户端），自研反向代理
- 本地服务：Docker Compose 起 Archon / wandb / Prometheus / Grafana
- 配置：Pydantic + YAML，敏感字段用系统 keyring
- CLI：Click 或 Typer
- 测试：pytest
- 文档：Markdown in `/docs`，架构图 in `/diagram`

**领域背景：**
- LLM 训练框架：verl（字节）、veomni（ByteDance 内部）
- NPU 监控：npu-smi、CANN 工具链
- 实验追踪：wandb（云或本地）、Prometheus（资源）
- 编排：Archon (coleam00/Archon, MIT)
- 渐进交付思想：GSD (open-gsd/gsd-core)
- 仓结构设计参考：maoxx241/vllm-ascend-workspace

**已知风险：**
- 远程无外网 → SSH 反向代理必须自动化且可重试
- NPU 监控命令因驱动版本差异可能字段不一样 → 解析层需要 fallback
- Archon 与我们的 8 skill 边界可能踩踏 → SKILL.md 顶部 "Use/Don't Use/Boundary" 必填
- verl/veomni 安装路径可能因 conda env 而异 → 通过 conda run 而非绝对路径

## Constraints

- **Tech stack**: Python 3.11+（与训练栈一致）
- **License**: MIT（与 Archon / vllm-ascend-workspace 对齐）
- **Local-first**: 所有 run 数据、log、wandb 落本地 Mac，远程不留状态
- **No network on remote**: 必须支持远程无外网场景，SSH 反向代理是必备能力
- **Self-contained skills**: 每个 skill 可独立运行，技能之间不强依赖
- **Archon-compatible**: 8 skill 必须能包装成 Archon workflow YAML，可被 `archon workflow run` 触发
- **可视化优先**: 每个 skill 输出必须可被 Grafana/wandb/HTML 报告消费

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 三沉淀层架构 (workspace-core / verl-adapter / datalake) | 通用 / 训练栈 / 数据 三类内容互不混用，便于单 skill 独立维护 | — Pending |
| 8 skill 1:1 映射到 8 步最小循环 | 每个 step = 一个可独立验证的 skill | — Pending |
| Archon 集成进 M1 (用户决策 2B) | M1 就要让 8 skill 可被 `archon workflow run` 触发 | — Pending |
| Docker Compose 起本地服务栈 | 与 Mac 环境隔离，启停干净 | — Pending |
| 远程 → 本地 wandb 用 wandb sync + offline 模式 | wandb 原生支持，无需自造轮子 | — Pending |
| SSH 反向代理用 paramiko 通道 + 进程内调度 | 避免外部 ssh 命令依赖，便于在 Python 上下文做重试 | — Pending |
| 进度协议用 stderr `__AR_PROGRESS__=<json>` 标记 | 与 vllm-ascend-workspace 模式一致，便于 AI 协作者解析 | — Pending |
| M1 范围 14 个阶段（用户决策 1C） | 含 Archon 适配 + 顶层 CLI + E2E + 归档 | — Pending |

---
*Last updated: 2026-06-06 after $gsd-new-project*

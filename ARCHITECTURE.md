# AutoResearch 架构 (愿景版)

> **目的**：让任何人 `git clone` 后立即看清"仓要做什么 / 怎么组织 / 我在哪一层"。
>
> 详细路线见 [.planning/ROADMAP.md](.planning/ROADMAP.md)。本文档描述**最终态 (M1 14 阶段完成时)**，
> 当前进度见 [.planning/STATE.md](.planning/STATE.md)。

## 顶层结构

```
autoresearch/
├── README.md / AGENTS.md / CLAUDE.md   # 仓根
├── pyproject.toml / uv.lock
├── services/                           # 4 个 docker compose (Phase 1)
├── config/                             # 配置文件 + schema
├── docs/                               # 用户文档
│
├── workspace-core/                     # 沉淀 1：通用底座
├── workspace-adapter/             # 沉淀 2：训练栈适配
├── datalake/                           # 沉淀 3：数据层
│
├── .agents/                            # AI 协作者入口
│   └── skills/                         # 8 个独立 skill
│       ├── 01-customer-config/         #  客户配置生成/校验/查看
│       ├── 02-local-services/          #  本地服务 healthz 检查
│       ├── 03-server-hardware/         #  SSH + npu-smi 硬件探测
│       ├── 04-network-check/           #  baidu/hf/github 测速 + SSH 反代
│       ├── 05-service-reachability/    #  远程 → 本地 wandb/prom 探活
│       ├── 06-train-stack-health/      #  conda env + verl/veomni 最小用例
│       ├── 07-data-collection/         #  跑最小实验 + wandb sync + log 采集
│       └── 08-experiment-report/       #  单页 HTML 报告 (log/wandb/prom 三视图)
│
└── tests/
```

## 三层职责

| 层 | 职责 | 互相依赖 |
|---|---|---|
| **3 沉淀** | 提供可复用底座 (ssh/secrets/config/proto/wandb/prom/...) | **互不依赖** |
| **8 skill** | 编排：调 1-N 个沉淀的接口完成一段任务 | **skill 之间不互相依赖** |
| **顶层 CLI** | 串多个 skill (`autoresearch check all`, `autoresearch run smoke`) | 不属于任何 skill |

```
   ┌─────────────────────────── 8 Skills（编排层）──────────────────────────┐
   │ 01 config │ 02 services │ 03 hw │ 04 net │ 05 reach │ 06 stack │     │
   │ 07 run+collect                │ 08 report                              │
   └──────────┬──────────┬──────────┬────────────────────────────────────────┘
              │          │          │
              ▼          ▼          ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │workspace-    │ │verl-workspace│ │   datalake   │
   │  core        │ │  -adapter    │ │              │
   │ ssh/secrets  │ │ verl/veomni  │ │ wandb/prom/  │
   │ config/proto │ │ env+minimal  │ │ log/manifest │
   │ layout/log   │ │ conda/npu    │ │              │
   └──────────────┘ └──────────────┘ └──────────────┘
        通用底座        训练栈专属        数据专属
```

## Skill 边界表

| Skill | 拥有 (Use) | 不做 (Don't Use) | Boundary |
|---|---|---|---|
| 01 customer-config | 配置文件生成、加密、校验、查看 | 任何健康检查 / 网络 / 训练 | 配置即数据 |
| 02 local-services | 启停 + healthz 检查 archon/wandb/prom/grafana | 远程服务器 / 网络 / 训练栈 | 本机 = 本地 |
| 03 server-hardware | SSH 连通、`npu-smi`/`nvidia-smi` 解析、占用方 | 网络 / 服务可达性 / 训练栈 | 硬件 ≠ 服务 |
| 04 network-check | baidu/hf/github 测速、SSH 反向代理搭建 | 训练栈 / 服务连通 | 网络 ≠ 服务 |
| 05 service-reachability | 远程 → 本地 wandb/prom 探活 | 训练栈 / 硬件 | 远程服务 ≠ 硬件 |
| 06 train-stack-health | conda env、verl/veomni 版本、最小用例 | 远程硬件 / 网络 | 训练栈 ≠ 远程 |
| 07 data-collection | 跑最小用例 + wandb sync + log 采集 + prom push | 报告渲染 | 采集 ≠ 呈现 |
| 08 experiment-report | 单页 HTML 报告 (log/wandb/prom 三视图) | 任何采集 | 报告只读 |

## 单脚本独立可跑 (关键属性)

每个 skill 的入口脚本都能独立运行，**不依赖其他 skill**：

```bash
# 单独跑 01 配置初始化
python3 .agents/skills/01-customer-config/scripts/config_init.py

# 单独跑 02 本地服务检查
python3 .agents/skills/02-local-services/scripts/services_check.py

# 指定 config + server 跑 03 硬件探测
python3 .agents/skills/03-server-hardware/scripts/hardware_probe.py \
  --config ./config/config.yaml --server nvidia-01

# 报告生成 (前提是有 run manifest 存在)
python3 .agents/skills/08-experiment-report/scripts/render_report.py \
  --run-id 2026-06-06-smoke-001 --open
```

跨 skill 串联由 **顶层 CLI orchestrator** 做（不属于任何 skill）：

```bash
autoresearch check all       # 跑 01-06 全套健康检查
autoresearch run smoke       # 跑 07+08, 自动调前面产物
autoresearch report <run-id> # 只跑 08
```

## 当前进度

| 元素 | 状态 | 阶段 |
|---|---|---|
| 仓根 5 文档 + ARCHITECTURE.md | ✅ | Phase 1 |
| `services/` 4 compose + .env.example | ✅ | Phase 1 |
| `autoresearch services {status,start,stop}` CLI | ✅ | Phase 1 |
| 11 个 pytest 单测 | ✅ | Phase 1 |
| `workspace-core/` 沉淀 | ⏳ | Phase 2 |
| `workspace-adapter/` | ⏳ | Phase 11 |
| `datalake/` | ⏳ | Phase 11 |
| `.agents/skills/0X-*/SKILL.md` | ⏳ 占位 (本目录已建) | Phase 3-10 |
| 顶层 `autoresearch check all` | ⏳ | Phase 12 |

---
*Last updated: 2026-06-06 — phase 1 完成时补完整愿景骨架*

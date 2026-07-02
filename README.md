# AutoResearch

> 本地驱动的 LLM 训练/调试工作流平台。所有数据留在本机 Mac；远程 NPU 服务器只是被远控的执行终端。

## 核心价值

AutoResearch 的核心不是替人跑命令，而是把每次实验、每次协作推进、每次投产判断变成下一次能继续利用的认知资产。

**核心竞争力：懂原理，知得失。** 懂原理，才能把现象归因到模型、数据、系统、硬件、显存、性能/MFU 和调度机制；知得失，才能判断一次尝试带来了什么、失去了什么、下一步该押什么。

人的主责：抓重点风险局点，会拒绝低优先级任务，有历史记录和全局规划；每天紧跟踪更新每个人力进展，多推动任务阻塞点，深挖掘客户需求，多沟通技术点。这些依赖人与人之间的共识、信任、责任和资源协调，AI 可以辅助记录、提醒、归纳和建模，但不能替代人去完成。

全链路工作法：抓重点风险局点，拒绝低优先级任务，维护历史记录和全局规划，每天知进展、紧跟踪、多推动，深挖客户需求，多沟通技术点，懂原理，准建模（显存、性能/MFU），知得失，快穿刺，理差距，评投产，落需求，快开发/多派活并紧跟踪，实践验，详记录，常修正，有推断，全设计，有效果，出报告。

```mermaid
flowchart LR
    A["历史记录与全局规划"] --> B["抓重点风险局点"]
    B --> C{"低优先级?"}
    C -->|"是"| D["拒绝或延后"]
    C -->|"否"| E["每日知进展/紧跟踪/多推动"]
    E --> F["推动阻塞点"]
    F --> G["深挖客户需求/多沟通技术点"]
    G --> H["懂原理/准建模<br/>显存/性能/MFU"]
    H --> I["快穿刺/理差距/知得失"]
    I --> J["评投产/落需求"]
    J --> K["快开发或多派活/紧跟踪"]
    K --> L["实践验/详记录/常修正"]
    L --> M["有推断/全设计/有效果/出报告"]
    M --> A
```

| 环节 | 人主责 | 可并行与 AI 加速 |
|---|---|---|
| 取舍 | 定重点风险局点，拒绝低优先级任务 | AI 汇总历史、提示风险、对比计划偏差 |
| 推进 | 每天知进展、紧跟踪、多推动阻塞点 | 多任务看板、会议纪要、阻塞清单可并行整理 |
| 研究 | 深挖客户需求，多沟通技术点，懂原理 | AI 辅助资料检索、原理归纳、显存/性能/MFU 建模 |
| 交付 | 快穿刺、评投产、落需求、派活跟踪 | 穿刺实验、测试、报告草稿和差距分析可并行推进 |
| 汇报 | 多汇报优势进展、后续风险和必要求助 | AI 生成日报/周报草稿，沉淀决策与复盘材料 |

每个 skill 跑一次，都必须留下可复盘、可二次开发的产物：事实记录、关键指标、失败与收益判断、建模假设、设计取舍、需求变更、验证结果和报告。

## 快速开始

> 本仓默认用 `uv run autoresearch ...` 运行 CLI。直接输入 `autoresearch`
> 需要先激活虚拟环境，见下方"为什么找不到 autoresearch"。

```bash
git clone https://github.com/<org>/autoresearch.git
cd autoresearch
uv sync

# 1) 装 Archon CLI（前置条件；详见 services/archon/README.md）
brew install coleam00/archon/archon
export CLAUDE_BIN_PATH="$(command -v claude)"

# 2) 启动 Archon。Archon 不归 `uv run autoresearch services start` 管，需要单独常驻。
archon serve --port 8088
```

另开一个终端继续：

```bash
cd autoresearch

# 3) 启本地服务栈：wandb / Prometheus + Pushgateway / Grafana
uv run autoresearch services start

# 4) 验证本地 Web 服务全绿。Archon 必须保持上一个终端在运行。
uv run autoresearch services status --json

# 5) 跑一次 readiness 检查。
uv run autoresearch check all --server A2-AK-225 --stack-lib verl

# 6) 跑一次最小实验并打开本地 HTML 报告。
uv run autoresearch run smoke \
  --server A2-AK-225 \
  --lib verl \
  --timeout 60 \
  --pushgateway-url http://127.0.0.1:17891 \
  --open
```

更完整的一键验收入口：

```bash
uv run autoresearch e2e smoke \
  --server A2-AK-225 \
  --lib verl \
  --timeout 60 \
  --pushgateway-url http://127.0.0.1:17891 \
  --open
```

### 为什么找不到 `autoresearch`

`autoresearch` 是 `pyproject.toml` 里声明的 Python console script。刚 clone
仓库时它还没有安装到你的 shell PATH，所以直接执行可能会看到：

```text
zsh: command not found: autoresearch
```

推荐写法是始终加 `uv run`：

```bash
uv run autoresearch check all --server A2-AK-225 --stack-lib verl
```

如果你想直接敲裸命令，先激活本仓虚拟环境：

```bash
uv sync
source .venv/bin/activate
autoresearch check all --server A2-AK-225 --stack-lib verl
```

## 架构

4 列架构图见 [diagram/autoresearch_arch.svg](diagram/autoresearch_arch.svg)。

## 8 步最小循环

详细描述见 [.planning/ROADMAP.md](.planning/ROADMAP.md)。概览：customer-config → local-services-health → server-hardware-probe → network-check → service-reachability → train-stack-health → data-collection → experiment-report。

## 文档

- [AGENTS.md](AGENTS.md) — AI 协作者指南（必读）
- [docs/VISUALIZATION.md](docs/VISUALIZATION.md) — 本地 Web 界面、端口、账号与常用入口
- [services/README.md](services/README.md) — 本地服务栈启动与端口说明
- [.planning/PROJECT.md](.planning/PROJECT.md) — 项目哲学 / 约束 / 关键决策
- [.planning/ROADMAP.md](.planning/ROADMAP.md) — 14 阶段路线图

## License

[MIT](LICENSE)

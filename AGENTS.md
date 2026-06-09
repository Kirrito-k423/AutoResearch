# AGENTS.md — AutoResearch 仓协作者指南

> **单源真相**：本文件即真相；`CLAUDE.md` 是它的相对路径 symlink。
> 任何 AI / 人类协作者进入此仓，先读本文件。

## 仓约定

- **Python 3.11+**；包管理用 [uv](https://github.com/astral-sh/uv)
- **CLI 框架**：[click](https://click.palletsprojects.com/) 8.1+；所有子命令挂在 `autoresearch` 单二进制下
- **服务编排**：每服务一个 `services/<name>/compose.yml`；`autoresearch services start` 串行 `docker compose -f services/X/compose.yml up -d`
- **测试**：`pytest`；M1 阶段 01 可只做单测；CLI 子命令至少 1 个 happy path 单测
- **进度协议**：子命令最终 stdout 必须是唯一一个 JSON 对象；过程进度走 stderr `__AR_PROGRESS__=<json>` 标记（Phase 2 落 CORE-PROTO-01..02）
- **本地优先**：所有 run 数据、log、wandb 落本地 Mac (`~/.autoresearch/`)，远程服务器不留状态
- **MIT License**

## 8 步最小循环（1:1 映射 8 skill）

| # | Skill | CLI group | Phase | REQ 组 |
|---|-------|-----------|-------|--------|
| 1 | customer-config | `autoresearch config` | 3 | CFG-* |
| 2 | local-services-health | `autoresearch services` | 1 | SVC-* / SVC-CHK-* |
| 3 | server-hardware-probe | `autoresearch hw` | 4 | HW-* |
| 4 | network-check | `autoresearch net` | 5 | NET-* |
| 5 | service-reachability | `autoresearch reach` | 6 | REACH-* |
| 6 | train-stack-health | `autoresearch stack` | 7 | STACK-* |
| 7 | data-collection | `autoresearch collect` | 8 | COLL-* |
| 8 | experiment-report | `autoresearch report` | 9 | RPT-* |

## 三沉淀层

- `workspace-core/`：通用（SSH / config / secrets / progress / log / layout）
- `verl-workspace-adapter/`：训练栈适配（verl / veomni）
- `datalake/`：数据采集与持久化（wandb / log / prom / manifest）

互不混用；每个 skill 可独立维护。

## 服务端口固定

- Archon: 8088（**不**在我们的 compose 里；走 `archon serve`）
- wandb (local): 8080
- Prometheus: 9090
- Grafana: 3000

## 进度协议模板

```python
import sys, json
def emit_progress(stage: str, **fields):
    msg = {"stage": stage, **fields}
    print(f"__AR_PROGRESS__={json.dumps(msg, ensure_ascii=False)}", file=sys.stderr)
```

## 测试规范

- 单测放 `tests/`；命名 `test_<module>.py`
- 使用 `click.testing.CliRunner` 测 CLI 子命令
- 业务逻辑必须有断言；不允许 "no assertions in test"
- M1 不强制覆盖率；但每个 CLI 子命令至少 1 个 happy path 单测

## 仓结构（M1 完整态）

```
README.md
AGENTS.md
CLAUDE.md          # symlink → AGENTS.md
LICENSE
.gitignore
pyproject.toml
autoresearch/      # Python 包
  __init__.py
  __main__.py
  cli.py
  services/        # M1 范围
    __init__.py
    _common.py
    status.py
    start.py
    stop.py
  config/          # Phase 3
  hw/              # Phase 4
  ...
services/          # Docker Compose
  archon/          # 只有 README
  wandb/
  prometheus/
  grafana/
tests/
diagram/
docs/
```

## 重要决策

- Archon 集成走 `archon serve`（不在 docker-compose 里）
- Docker Compose v2 plugin（`docker compose` 子命令），不用 v1 binary
- `host.docker.internal` 给 Grafana 连本机 wandb 用
- 默认 CLI 错误信息中文；`--lang en` 切英文

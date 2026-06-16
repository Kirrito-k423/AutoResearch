# AutoResearch 可视化界面

本项目的可视化面都跑在本机 Mac 上。远程服务器只负责执行训练/探测，数据通过
wandb sync、log 拉取和 Pushgateway/Prometheus 回到本机。

## 服务地址与账号

| 服务 | 地址 | 用途 | 登录账号 |
|---|---|---|---|
| Archon Web UI | http://localhost:8088 | 查看 repo-local workflows，例如 `ar-min-loop` | 本仓未配置 Web 登录账号；依赖本机 Archon/Claude/Codex 配置 |
| W&B Local | http://localhost:8080 | 查看本地同步后的 wandb run、summary 和曲线 | 当前本机：`autoresearch-local@wandb.com` / `AutoResearch2026!` |
| Prometheus | http://localhost:9090 | 查询 Pushgateway 抓到的实验/资源指标 | 无登录 |
| Prometheus Targets | http://localhost:9090/targets | 查看 Prometheus 自身和 Pushgateway scrape 状态 | 无登录 |
| Pushgateway | http://localhost:9091 | 接收远程推送的最小实验指标 | 无登录 |
| Grafana | http://localhost:3000 | 查看 Prometheus datasource；后续可做 dashboard | 初始 `admin` / `admin` |
| HTML 实验报告 | `~/.autoresearch/runs/<run-id>/report.html` | 单次实验复盘入口，含 log / W&B / Prometheus 三视图 | 本地文件，无登录 |

> Grafana 密码如果已经改过，会保存在 Docker volume `ar-grafana-data` 里；
> 此时以改后的密码为准，不再是 `admin/admin`。

## 启动顺序

Archon 不是 Docker Compose 服务，必须单独开一个终端常驻：

```bash
export CLAUDE_BIN_PATH="$(command -v claude)"
archon serve --port 8088
```

另开终端启动 AutoResearch 管理的本地服务：

```bash
uv run autoresearch services start
uv run autoresearch services status --json
```

`services status` 检查 5 个端点：

| 服务 | 健康检查 |
|---|---|
| Archon | http://localhost:8088/healthz |
| W&B Local | http://localhost:8080/ready |
| Prometheus | http://localhost:9090/-/healthy |
| Grafana | http://localhost:3000/api/health |
| Pushgateway | http://localhost:9091/-/healthy |

如果 Archon 没有单独运行，`services status` 会显示 4/5 healthy，这是预期的。

## 第一次跑出报告

推荐先跑 readiness，再跑 smoke：

```bash
uv run autoresearch check all --server A2-AK-225 --stack-lib verl

uv run autoresearch run smoke \
  --server A2-AK-225 \
  --lib verl \
  --timeout 60 \
  --pushgateway-url http://127.0.0.1:17891 \
  --open
```

更完整的一键验收：

```bash
uv run autoresearch e2e smoke \
  --server A2-AK-225 \
  --lib verl \
  --timeout 60 \
  --pushgateway-url http://127.0.0.1:17891 \
  --open
```

命令成功后会输出 JSON，其中 `report` 字段指向本地 HTML：

```text
~/.autoresearch/runs/<run-id>/report.html
```

报告里会包含：

- run/server/lib/conda env/NPU count 摘要；
- `manifest.json`、`log.txt`、wandb artifact 目录和 Prometheus query 链接；
- `Log View`：最小实验日志摘要；
- `W&B View`：本地 wandb summary；
- `Prometheus View`：按 `run_id` 查询到的指标。

## 常用入口

### W&B Local

打开：

```bash
open http://localhost:8080
```

当前这台 Mac 的本地 W&B 管理员账号：

```text
email: autoresearch-local@wandb.com
password: AutoResearch2026!
```

这是 `ar-wandb-data-v2` Docker volume 内的本机账号，不是 W&B 云端账号。
如果重建 volume 或换机器，账号可能需要重新初始化或重置。

AutoResearch 的 collect 流程会把远程 offline wandb run 同步回本机。报告里的
`W&B View` 会链接到 W&B Local 根页面，并保留对应 `wandb_run_id`。

### Prometheus

查看 targets：

```bash
open http://localhost:9090/targets
```

查询某次 run 的 NPU 数：

```bash
open 'http://localhost:9090/graph?g0.expr=autoresearch_npu_count'
```

报告会生成更精确的 run-specific query，例如：

```promql
autoresearch_npu_count{run_id="<run-id>"}
```

### Grafana

打开：

```bash
open http://localhost:3000
```

初始登录：

```text
username: admin
password: admin
```

Grafana 已通过 provisioning 配好 datasource：

| Datasource | 容器内地址 | 说明 |
|---|---|---|
| Prometheus | `http://prometheus:9090` | 默认 datasource |
| wandb | `http://host.docker.internal:8080` | 从 Grafana 容器访问 Mac 上的 W&B Local |

M1 目前没有内置 Grafana dashboard；报告 HTML 是当前主可视化交付件。

### Archon

打开：

```bash
open http://localhost:8088
```

常用验证：

```bash
archon validate workflows ar-min-loop
AR_STACK_LIBS=verl archon workflow run ar-min-loop --no-worktree ""
```

如果 Web UI 打不开，先确认前台终端里的 `archon serve --port 8088` 还在运行。

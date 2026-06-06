# datalake — 沉淀 3：数据层

> 实验数据的"采集 + 持久化 + 查询"层。所有 run 数据落本地 Mac (`~/.autoresearch/`)。

## 职责

| 子模块 | 职责 | 关键接口 |
|---|---|---|
| `wandb/sync.py` | 把远程 offline run sync 到本地 wandb | `sync_run(run_id, server_url)` |
| `wandb/local_server.py` | 启停本地 wandb 服务 (替代 docker) | `LocalWandbServer.start/stop` |
| `wandb/api_client.py` | 通过 HTTP API 查 wandb 指标 | `query_metrics(run_id) -> DataFrame` |
| `prometheus/push_gateway.py` | 远程 pushgateway 接收端 | `push_metrics(host, metrics)` |
| `prometheus/exporters/` | nvidia-exporter / 自定义 NPU exporter | `NPUMetricsExporter` |
| `prometheus/queries.py` | PromQL 封装 | `query_gpu_util(server, range)` |
| `logs/collector.py` | 远程 log tail/回传 | `tail_remote_log(server, path)` |
| `logs/parser.py` | 解析 train log 关键事件 | `parse_train_log(text) -> TrainLogEvents` |
| `manifest/schema.py` | "一次 run = 一个 manifest" Pydantic 模型 | `RunManifest(run_id, started_at, ...)` |
| `manifest/writer.py` | 写 manifest 到 `~/.autoresearch/runs/<id>/manifest.json` | `RunManifestWriter.write(m)` |

## 设计原则

- **本地优先**：所有数据落 `~/.autoresearch/`，远程不留状态
- **manifest 是真相源**：任何 run 都先有 manifest，后有数据
- **可单独跑**：每个子模块都能 import 后独立调用

## 状态

⏳ **Phase 11 待开发** — 当前目录为占位。

---
*详见 `.planning/ROADMAP.md` Phase 11*

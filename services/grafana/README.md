# Grafana

> 本地 Grafana；M1 阶段预置 Prometheus + wandb 两个 datasource。

## 启动

```bash
docker compose -f services/grafana/compose.yml up -d
# 或
uv run autoresearch services start
```

## 验证

```bash
# 健康检查
curl http://localhost:3000/api/health
# 期望: {"database":"ok",...}

# Web UI
open http://localhost:3000
# 本地 dashboard 允许匿名只读访问；管理登录默认 admin / admin

# 实验切片 dashboard
open http://localhost:3000/d/autoresearch-npu/autoresearch-experiment-telemetry?orgId=1

# 机器长期监控 dashboard
open http://localhost:3000/d/autoresearch-machine-telemetry/autoresearch-machine-telemetry?orgId=1

# Datasource 验证
open http://localhost:3000/datasources
# 期望: 看到 Prometheus 和 wandb 两个；Prometheus 标 "default"
```

## 怎么阅读 Prometheus 数据

- `http://localhost:3000` 是 Grafana 首页，只是可视化入口；没有进入 dashboard 时不会直接显示曲线。
- `http://localhost:9090` 才是 Prometheus 原生查询页，可以直接输入 PromQL。
- 实验切片视图：
  `http://localhost:3000/d/autoresearch-npu/autoresearch-experiment-telemetry?orgId=1`
- 机器长期监控视图：
  `http://localhost:3000/d/autoresearch-machine-telemetry/autoresearch-machine-telemetry?orgId=1`
- 四台机器可通过 `var-server` 参数直达，例如：
  `http://localhost:3000/d/autoresearch-machine-telemetry/autoresearch-machine-telemetry?orgId=1&var-server=A2-AK-225`

常用 PromQL：

```promql
autoresearch_npu_hbm_used_mib
autoresearch_npu_aicore_utilization_percent
autoresearch_machine_npu_hbm_used_mib
autoresearch_machine_npu_aicore_utilization_percent
autoresearch_machine_npu_sample_time_seconds
autoresearch_experiment_case_info
autoresearch_experiment_case_start_time_seconds
autoresearch_experiment_case_end_time_seconds
autoresearch_npu_count
```

按单次 run 过滤：

```promql
autoresearch_npu_hbm_used_mib{run_id="Qwen35-2B-GRPO-1Kto16K-260623d-130014s-train-modes-sync-async-noignoreeos"}
```

按机器长期监控过滤：

```promql
autoresearch_machine_npu_hbm_used_mib{server="A2-AK-225",chip_id=~".+"}
autoresearch_machine_npu_aicore_utilization_percent{server="A2-AK-225",chip_id=~".+"}
```

按实验 case 查看 W&B 名称和时间窗口：

```promql
present_over_time(autoresearch_experiment_case_info{run_id="Qwen35-2B-GRPO-1Kto16K-260623d-130014s-train-modes-sync-async-noignoreeos"}[5s])
autoresearch_experiment_case_start_time_seconds{run_id="Qwen35-2B-GRPO-1Kto16K-260623d-130014s-train-modes-sync-async-noignoreeos"}
autoresearch_experiment_case_end_time_seconds{run_id="Qwen35-2B-GRPO-1Kto16K-260623d-130014s-train-modes-sync-async-noignoreeos"}
```

## 为什么会看到直线

Pushgateway 只保存每个 label set 的当前 gauge 值，不是历史样本导入器。
如果 run 结束后才把 `telemetry-latest-openmetrics.prom` 推一次，Prometheus 会在后续 scrape 中反复看到同一个最新值，Grafana 就是一条直线。

正式 GRPO case 的运行期采样仍是 0.5s：row 脚本会持续写 `npu-smi-watch.raw.log`，并在训练进程运行期间把最新 `autoresearch_npu_*` 与 `autoresearch_machine_npu_*` 推到 Pushgateway。Prometheus 的 pushgateway job 以 500ms scrape，这样新 run 的 Grafana 曲线来自运行期真实 scrape。历史数据包里的完整 0.5s 原始曲线仍以 `2-prometheus/telemetry-openmetrics.prom` 和 `6-rows/cases/*/npu-telemetry.jsonl` 为准。

不跑训练但要长期看四台机器资源时，另开终端运行：

```bash
uv run autoresearch hw monitor --all --interval 0.5
```

`refresh=30s` 只是 Grafana 页面刷新；Prometheus scrape Pushgateway 是 500ms；真正的新数据来自 `autoresearch hw monitor` 或正在运行的 GRPO row 脚本。机器长期监控 dashboard 的 `Sample Age` 卡使用 `time() - autoresearch_machine_npu_sample_time_seconds`，它持续变大就说明采样进程停了，哪怕 Prometheus 仍在 scrape Pushgateway。

只验证一次采样与 push：

```bash
uv run autoresearch hw monitor --all --once
```

## Datasources

启动时通过 `datasources.yml` 自动 provisioning：
- **Prometheus** (default)：`http://host.docker.internal:9090`（Grafana 和 Prometheus 在不同 compose 网络，不能用 `prometheus:9090`）
- **wandb**：`http://host.docker.internal:8080`（Mac 主机网络）

## 登录账号

本地 dashboard 通过 `GF_AUTH_ANONYMOUS_ENABLED=true` 允许匿名只读访问。
管理账号由 `services/grafana/compose.yml` 配置：

```text
username: admin
password: admin
```

如果首次登录后改过密码，Grafana 会把新密码保存到 Docker volume
`ar-grafana-data`，之后以新密码为准。

## 关键点（RESEARCH Pitfall 1）

`host.docker.internal` 是 Docker Desktop (Mac/Windows) 提供的特殊 DNS，
让容器内能访问 Mac 主机服务。在 Linux 上需加：
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```
M1 阶段只面向 Mac（PROJECT.md 锁 Mac 单机），暂不处理 Linux。

## 端口

默认 3000（D-03c）；可通过 `.env` 里 `PORT_GRAFANA=3001` 覆盖。

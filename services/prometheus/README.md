# Prometheus

> 本地 Prometheus；M1 阶段只跑自监控，Phase 7+ 接 pushgateway 收远程 NPU 资源数据。

## 启动

```bash
docker compose -f services/prometheus/compose.yml up -d
# 或
uv run autoresearch services start
```

## 验证

```bash
# 自监控端点
curl http://localhost:9090/-/healthy
# 期望: "Prometheus is Healthy."

# 自监控 scrape 状态（Web UI）
open http://localhost:9090/targets
# 期望: "prometheus" job 显示 UP

# 查 self-scrape 指标
curl 'http://localhost:9090/api/v1/query?query=up{job="prometheus"}'
# 期望: vector 含 1 个 value=1
```

## 自监控

`prometheus.yml` 里 `prometheus` job 抓取 Prometheus 自己的 `/metrics` 端点（localhost:9090）。
- 容器内 localhost 是容器自己（关键点，**不**是 `prometheus:9090`）
- 验证：Web UI Status > Targets，`prometheus` job 应显示 UP

## NPU Telemetry

`pushgateway` job 抓取本地 Pushgateway：
- `honor_labels: true` 保留 run push 时带的 `server`、`run_id`、`case_id` 等标签。
- `scrape_interval: 500ms` 用于 formal GRPO 运行期资源曲线；采样进程每 0.5s 写 `npu-smi-watch.raw.log` 并 push 最新 gauge。
- `autoresearch_npu_*` 是实验切片指标，保留 `run_id/case_id/server/device_id`。
- `autoresearch_machine_npu_*` 是机器长期监控指标，只保留 `server/device_id/chip_id/source`，避免每个实验 case 复制一组设备曲线。
- `autoresearch_machine_npu_sample_time_seconds` 是真实采样写入时间，用于区分“硬件值没变化”和“采样进程停了但 Pushgateway 还在暴露旧值”。
- `autoresearch_machine_host_*` 是机器级 Host CPU/内存指标，只保留 `server/source`，与 NPU 机器指标同一个 Pushgateway 分组一起 PUT，避免覆盖。内存会拆分 `used/free/available/shared/buff_cache/occupied(total-free)`，其中 `used` 对齐 `free` 命令里的进程占用视角，`occupied` 对齐 `used + buff/cache` 的非空闲视角。
- `autoresearch_machine_host_sample_time_seconds` 是 Host CPU/内存真实采样写入时间。
- `autoresearch_experiment_case_info` 关联 `run_id/case_id/server/wandb_project/wandb_run_name`；新 run 还会带 `case_started_at/case_finished_at` 标签。
- `autoresearch_experiment_case_start_time_seconds`、`autoresearch_experiment_case_end_time_seconds`、`autoresearch_experiment_case_elapsed_seconds` 提供 case 时间窗口和耗时，用于 Grafana 按实验切片。
- run 结束后一次性 push 的 latest gauge 只能证明“最终值”；历史曲线必须来自运行期持续 push 后 Prometheus scrape，或从数据仓里的 `telemetry-openmetrics.prom` / `npu-telemetry.jsonl` 离线重建。

机器长期监控入口：

```bash
uv run autoresearch hw monitor --all --interval 0.5
```

## 数据持久化

`prometheus-data` named volume；`docker volume inspect ar-prometheus-data`。

## Web UI 与登录

| 服务 | 地址 | 登录 |
|---|---|---|
| Prometheus | http://localhost:9090 | 无登录 |
| Targets | http://localhost:9090/targets | 无登录 |
| Pushgateway | http://localhost:9091 | 无登录 |

## 端口

默认 9090（D-03c）；可通过 `.env` 里 `PORT_PROMETHEUS=<unused-port>` 覆盖。
注意不要和 Pushgateway 默认端口 9091 撞。

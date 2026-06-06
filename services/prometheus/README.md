# Prometheus

> 本地 Prometheus；M1 阶段只跑自监控，Phase 7+ 接 pushgateway 收远程 NPU 资源数据。

## 启动

```bash
docker compose -f services/prometheus/compose.yml up -d
# 或
autoresearch services start
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

## 数据持久化

`prometheus-data` named volume；`docker volume inspect ar-prometheus-data`。

## 端口

默认 9090（D-03c）；可通过 `.env` 里 `PORT_PROMETHEUS=9091` 覆盖。

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

# AutoResearch NPU dashboard
open http://localhost:3000/d/autoresearch-npu/autoresearch-npu-telemetry?orgId=1

# Datasource 验证
open http://localhost:3000/datasources
# 期望: 看到 Prometheus 和 wandb 两个；Prometheus 标 "default"
```

## 怎么阅读 Prometheus 数据

- `http://localhost:3000` 是 Grafana 首页，只是可视化入口；没有进入 dashboard 时不会直接显示曲线。
- `http://localhost:9090` 才是 Prometheus 原生查询页，可以直接输入 PromQL。
- AutoResearch NPU 曲线在 Grafana dashboard：
  `http://localhost:3000/d/autoresearch-npu/autoresearch-npu-telemetry?orgId=1`

常用 PromQL：

```promql
autoresearch_npu_hbm_used_mib
autoresearch_npu_aicore_utilization_percent
autoresearch_npu_count
```

按单次 run 过滤：

```promql
autoresearch_npu_hbm_used_mib{run_id="Qwen35-2B-GRPO-1Kto16K-260623d-130014s-train-modes-sync-async-noignoreeos"}
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

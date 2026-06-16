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
# 默认 admin / admin（首次登录会要求改密码；可跳过）

# Datasource 验证
open http://localhost:3000/datasources
# 期望: 看到 Prometheus 和 wandb 两个；Prometheus 标 "default"
```

## Datasources

启动时通过 `datasources.yml` 自动 provisioning：
- **Prometheus** (default)：`http://prometheus:9090`（容器名服务发现）
- **wandb**：`http://host.docker.internal:8080`（Mac 主机网络）

## 登录账号

初始账号由 `services/grafana/compose.yml` 配置：

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

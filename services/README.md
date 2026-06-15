# AutoResearch 本地服务栈

> 4 个独立 Docker Compose 服务；Archon 单独管理（不在我们的 compose 里）。

## 服务总览

| 服务 | 端口 | 镜像 | compose 文件 | 启动方式 |
|------|------|------|--------------|----------|
| **Archon** | 8088 | (本地 CLI) | — | `archon serve --port 8088`（用户自管） |
| **wandb (local)** | 8080 | `wandb/local:0.17.5` | `wandb/compose.yml` | autoresearch services start |
| **Prometheus** | 9090 | `prom/prometheus:v2.51.0` | `prometheus/compose.yml` | autoresearch services start |
| **Grafana** | 3000 | `grafana/grafana:10.4.0` | `grafana/compose.yml` | autoresearch services start |

## 启动顺序

1. **前置**：先装 `archon` CLI（见 [archon/README.md](archon/README.md)），再 `archon serve --port 8088 &`
2. 启动 3 个 docker 服务：
   ```bash
   autoresearch services start
   # 或手动：
   docker compose -f services/wandb/compose.yml up -d
   docker compose -f services/prometheus/compose.yml up -d
   docker compose -f services/grafana/compose.yml up -d
   ```
3. 验证全绿：
   ```bash
   autoresearch services status
   ```

## 端口冲突处理

如果 8080/9090/3000 任一被占，编辑 `.env`（基于 `.env.example`）改端口变量，compose 用 `${VAR}` 引用。

## 已知约束
- Archon 不在 compose 里（D-05 锁定）
- 端口 wandb 8080 / Prom 9090 / Grafana 3000 / Archon 8088 **固定**（D-03c）
- `host.docker.internal` 是 Mac/Windows Docker Desktop 默认；Linux 需要 `extra_hosts`
- 本地优先：所有数据落本机 Mac 容器 volume，远程 NPU 服务器不涉及

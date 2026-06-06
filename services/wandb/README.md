# wandb (本地)

> 本地模式 wandb；M1 阶段只起服务，actual 数据采集在 Phase 9 (data-collection)。

## 启动

```bash
docker compose -f services/wandb/compose.yml up -d
# 或
autoresearch services start
```

## 验证

```bash
curl http://localhost:8080/healthz
# 期望 200 OK 或 404（wandb local 镜像可能不暴露 /healthz，需要查 README 调整）
```

> **注意**：wandb/local 镜像的 health 端点路径**可能**不是 `/healthz`。
> 如果 `/healthz` 404，请用以下命令探活：
> ```bash
> curl -I http://localhost:8080/
> ```
> 然后在 `autoresearch/services/_common.py` 把 `WANDB_HEALTH_URL` 常量改正确。
> （这是 RESEARCH.md Open Question 1 的解答路径；先按 `/healthz` 走，遇到再修。）

## 端口

默认 8080（D-03c 锁定）；可通过 `.env` 里 `PORT_WANDB=8081` 覆盖。

## 数据持久化

`wandb-data` named volume，docker volume inspect ar-wandb-data 查看位置。

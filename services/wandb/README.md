# wandb (本地)

> 本地模式 wandb；M1 阶段只起服务，actual 数据采集在 Phase 9 (data-collection)。

## 启动

```bash
docker compose -f services/wandb/compose.yml up -d
# 或
uv run autoresearch services start
```

## 验证

```bash
curl http://localhost:8080/ready
# 期望 200 OK
```

## Web UI 与登录

- 地址：http://localhost:8080
- 当前这台 Mac 的本地管理员账号：
  - email: `autoresearch-local@wandb.com`
  - password: `AutoResearch2026!`
- 这是 `ar-wandb-data-v2` Docker volume 内的本机账号，不是 W&B 云端账号。
- 如果重建 volume 或换机器，账号可能需要重新初始化或重置。
- AutoResearch 报告会保留 `wandb_run_id` 和本地 W&B 入口链接。

## 端口

默认 8080（D-03c 锁定）；可通过 `.env` 里 `PORT_WANDB=8081` 覆盖。

## 数据持久化

`ar-wandb-data-v2` named volume，`docker volume inspect ar-wandb-data-v2` 查看位置。

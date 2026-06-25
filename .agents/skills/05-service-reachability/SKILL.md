---
name: service-reachability
description: Verify that remote training servers can reach local AutoResearch services such as W&B, Prometheus, Grafana, and Pushgateway. Use when testing service URLs from a remote host, validating SSH reverse proxy behavior, or implementing reachability CLI results.
---

# Skill 05: service-reachability

> 从远端服务器，探活本机的 wandb / Prometheus / Grafana。

## Boundary

| Use | Don't Use |
|---|---|
| 远程跑 curl 探本机 wandb /prometheus / grafana | 硬件 (这是 03) |
| 验证 SSH 反向代理生效 | 网络测速 (这是 04) |
| 输出可达性表 (4 端点 × N 服务器) | 训练栈 (这是 06) |

## 入口

```bash
python3 .agents/skills/05-service-reachability/scripts/reachability_check.py \
  --config ./config/config.yaml --server nvidia-01
```

## 状态

⏳ **Phase 7 待开发**。

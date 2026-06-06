# Skill 02: local-services

> 启停 + healthz 检查本机 archon / wandb / Prometheus / Grafana。

## Boundary

| Use | Don't Use |
|---|---|
| `services_check.py` (4 healthz 并发) | 远程服务器 |
| `services_start.py` (串行 docker compose up) | 网络测速 |
| `services_stop.py` (串行 docker compose down) | 训练栈 |
| 读取本机 `.env` 端口变量 | 报告渲染 |

## 入口

```bash
python3 .agents/skills/02-local-services/scripts/services_check.py
python3 .agents/skills/02-local-services/scripts/services_start.py
python3 .agents/skills/02-local-services/scripts/services_stop.py
```

## 当前实现

**Phase 1 已实现** `autoresearch services {status,start,stop}` CLI。
**Phase 4 计划**：把实现从 `autoresearch/services/` 子包迁移到本目录；
顶层 CLI 改为薄包装，指向本 skill 的入口脚本。

## 状态

🟡 **Phase 1 部分实现 (作为 CLI)**；Phase 4 完整迁移。

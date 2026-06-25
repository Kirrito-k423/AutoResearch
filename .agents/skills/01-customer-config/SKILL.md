---
name: customer-config
description: Generate, validate, inspect, and safely handle AutoResearch customer configuration files. Use when working on config init/show/validate commands, Pydantic config schema behavior, keyring or env secret placeholders, redacted display, or config/config.yaml templates.
---

# Skill 01: customer-config

> 生成 / 校验 / 查看客户配置。敏感字段 (密码/SSH key/API token) 不裸奔。

## Boundary

| Use | Don't Use |
|---|---|
| 配置文件生成 (`config_init.py`) | 任何健康检查 |
| 加密字段读写 (keyring) | 网络 / 训练栈 |
| 校验 (Pydantic schema) | 服务可达性 |
| 脱敏显示 (`***` 密码) | 报告渲染 |

## 入口

```bash
python3 .agents/skills/01-customer-config/scripts/config_init.py --out ./config/config.yaml
python3 .agents/skills/01-customer-config/scripts/config_validate.py --config ./config/config.yaml
python3 .agents/skills/01-customer-config/scripts/config_show.py --config ./config/config.yaml
```

## 状态

⏳ **Phase 3 待开发** — 当前为占位。

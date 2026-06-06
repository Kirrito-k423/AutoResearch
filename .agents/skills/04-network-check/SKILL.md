# Skill 04: network-check

> 测外网 (baidu/hf/github) 速度 + 搭 SSH 反向代理。

## Boundary

| Use | Don't Use |
|---|---|
| 测 `baidu.com` / `huggingface.co` / `github.com` 延迟与带宽 | 训练栈 (这是 06) |
| 启动 SSH 反向代理 (本机 7890 → 远程) | 远程服务可达 (这是 05) |
| 验证代理可用 | 硬件 (这是 03) |

## 入口

```bash
python3 .agents/skills/04-network-check/scripts/network_probe.py \
  --config ./config/config.yaml --server nvidia-01
```

## 状态

⏳ **Phase 6 待开发**。

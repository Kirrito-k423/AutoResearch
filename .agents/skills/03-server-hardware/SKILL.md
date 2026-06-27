---
name: server-hardware-probe
description: Probe remote GPU/NPU server hardware over SSH and parse npu-smi or nvidia-smi outputs. Use when collecting accelerator inventory, driver versions, memory/core utilization, process occupancy, partial hardware data, or hardware probe CLI behavior.
---

# Skill 03: server-hardware

> SSH 连到远端 NPU/GPU 服务器，跑 `npu-smi` / `nvidia-smi` 解析硬件规格和占用方。

## Boundary

| Use | Don't Use |
|---|---|
| SSH 连通 (paramiko) | 网络测速 (这是 04) |
| 解析 `npu-smi info` 输出 | 服务可达性 (这是 05) |
| 解析 `nvidia-smi` 输出 | 训练栈健康 (这是 06) |
| 列出占用方 (`nvidia-smi --query-compute-apps=pid,process_name,used_memory`) | 报告渲染 |

## 入口

```bash
python3 .agents/skills/03-server-hardware/scripts/hardware_probe.py \
  --config ./config/config.yaml --server nvidia-01
```

## 状态

⏳ **Phase 5 待开发**。

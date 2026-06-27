# --dashboard-port

- **参数名**：`--dashboard-port`
- **分类**：效率
- **中文解释**：文档说明：Ray Dashboard 使用的端口；SkyPilot 示例固定为 `8265`，并在文档中通过 `sky status --endpoint 8265` 获取 Dashboard URL。
- **常见值**：8265
- **来源环境变量**：无
- **性能影响**：机制推断：只影响监控端口选择，通常不改变训练吞吐；端口冲突会导致 Ray Dashboard 启动或暴露失败。
- **精度影响**：机制推断：Dashboard 端口不参与训练计算，通常不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:37` --dashboard-port=8265
- `examples/tutorial/skypilot/verl-grpo.yaml:34` --dashboard-port=8265
- `examples/tutorial/skypilot/verl-ppo.yaml:45` --dashboard-port=8265

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

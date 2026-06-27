# --port

- **参数名**：`--port`
- **分类**：效率
- **中文解释**：文档说明：Ray head 节点监听的集群通信端口；SkyPilot 示例使用 `6379`，worker 通过该端口发现并加入 Ray 集群。
- **常见值**：6379
- **来源环境变量**：无
- **性能影响**：机制推断：端口号本身不影响吞吐；端口冲突、防火墙或地址不可达会导致 Ray 集群无法启动或 worker 无法加入。
- **精度影响**：机制推断：通信端口不参与模型计算，通常不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:35` --port=6379 \
- `examples/tutorial/skypilot/verl-grpo.yaml:32` --port=6379 \
- `examples/tutorial/skypilot/verl-ppo.yaml:43` --port=6379 \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

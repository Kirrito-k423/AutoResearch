# --disable-usage-stats

- **参数名**：`--disable-usage-stats`
- **分类**：效率
- **中文解释**：文档说明：Ray 启动参数，用于关闭 Ray usage stats/遥测采集；Verl 多节点和 SkyPilot 示例在 head/worker 启动 Ray 时都带上该开关。
- **常见值**：未提取
- **来源环境变量**：无
- **性能影响**：机制推断：通常不影响训练吞吐；在无外网或受限网络环境中可减少遥测相关网络尝试和日志噪声。
- **精度影响**：机制推断：只控制 Ray 使用统计上报，不参与模型、数据或优化器计算，通常不影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-grpo.yaml:95` ps aux | grep ray | grep $HEAD_IP:6379 &> /dev/null || ray start --address $HEAD_IP:6379 --disable-usage-stats
- `examples/tutorial/skypilot/verl-ppo.yaml:105` ps aux | grep ray | grep $HEAD_IP:6379 &> /dev/null || ray start --address $HEAD_IP:6379 --disable-usage-stats

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

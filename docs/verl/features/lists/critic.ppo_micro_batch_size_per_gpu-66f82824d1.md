# critic.ppo_micro_batch_size_per_gpu

- **参数名**：`critic.ppo_micro_batch_size_per_gpu`
- **分类**：效率
- **中文解释**：控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。
- **常见值**：4
- **来源环境变量**：无
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-ppo.yaml:87` critic.ppo_micro_batch_size_per_gpu=4 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

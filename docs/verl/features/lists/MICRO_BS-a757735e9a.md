# MICRO_BS

- **参数名**：`MICRO_BS`
- **分类**：效率
- **中文解释**：文档说明：router replay 示例中的每 GPU micro batch 变量，同时写入 actor PPO、rollout log-prob 和 ref log-prob 的 `*_micro_batch_size_per_gpu`，控制单次前向/反向在本地 GPU 组处理的样本数。
- **常见值**：3
- **来源环境变量**：MICRO_BS
- **性能影响**：文档说明：Verl 建议尽量把 `*micro_batch_size_per_gpu` 调到显存允许的较大值以提升训练速度；过大容易 OOM，长序列场景需要降低 micro batch。
- **精度影响**：机制推断：micro batch 主要是性能/显存参数；若梯度累积和全局 batch 归一化保持一致，通常不直接改变目标，但可能通过 OOM、动态 batch 或数值归约顺序间接影响稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:23` micro_bs=${MICRO_BS:-3}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

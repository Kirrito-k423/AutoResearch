# CRITIC_TP

- **参数名**：`CRITIC_TP`
- **分类**：效率
- **中文解释**：文档说明：critic Megatron 的 tensor parallel size，示例将 `CRITIC_TP` 写入 `critic.megatron.tensor_model_parallel_size`，用于切分 critic 的张量/线性层计算。
- **常见值**：2
- **来源环境变量**：CRITIC_TP
- **性能影响**：文档说明：Megatron 并行参数需要匹配显存和通信；增大 TP 可降低单卡权重/激活压力，但层内 collective 通信会增加，TP 很大时通信成本更明显。
- **精度影响**：机制推断：正确 TP 切分通常不改变 critic 数学目标；并行拓扑、checkpoint 切分或数值归约差异可能带来轻微数值差异或直接不兼容。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:26` critic_tp=${CRITIC_TP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

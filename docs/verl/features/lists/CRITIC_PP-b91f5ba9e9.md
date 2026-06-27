# CRITIC_PP

- **参数名**：`CRITIC_PP`
- **分类**：效率
- **中文解释**：文档说明：critic Megatron 的 pipeline parallel size，示例将 `CRITIC_PP` 写入 `critic.megatron.pipeline_model_parallel_size`，用于把 critic 网络层切分到多个流水并行 stage。
- **常见值**：2
- **来源环境变量**：CRITIC_PP
- **性能影响**：文档说明：Megatron PP/TP/EP/CP 需要按显存和网络约束平衡；增大 PP 可降低单卡层数和激活压力，但会引入 pipeline bubble 与跨 stage 通信。
- **精度影响**：机制推断：正确流水切分通常应保持 critic 计算等价；若与模型层数、checkpoint 或 actor/ref 并行拓扑不匹配，可能加载失败或影响 value/reward 估计稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:27` critic_pp=${CRITIC_PP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

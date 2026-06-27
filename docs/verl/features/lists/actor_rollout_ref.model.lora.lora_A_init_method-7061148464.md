# actor_rollout_ref.model.lora.lora_A_init_method

- **参数名**：`actor_rollout_ref.model.lora.lora_A_init_method`
- **分类**：效率
- **中文解释**：文档说明：Megatron LoRA 低秩矩阵 A 的初始化方法；官方配置默认 `xavier`，本示例使用 `kaiming`。
- **常见值**：kaiming
- **来源环境变量**：无
- **性能影响**：机制推断：初始化方法只发生在训练启动/适配器创建阶段，不改变每步计算图或通信规模，性能影响通常可以忽略。
- **精度影响**：机制推断：初始化会影响 LoRA 训练早期的梯度尺度与收敛稳定性；`kaiming`/`xavier` 都是常见初始化，但需结合激活分布、学习率和 rank 观察。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh:64` actor_rollout_ref.model.lora.lora_A_init_method=kaiming

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

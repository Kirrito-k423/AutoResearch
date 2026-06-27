# actor_rollout_ref.model.lora.alpha

- **参数名**：`actor_rollout_ref.model.lora.alpha`
- **分类**：效率
- **中文解释**：文档说明：Megatron LoRA 的 alpha 缩放系数，即低秩投影更新的权重因子；Verl LoRA 文档默认示例为 32，本 batch 示例通过 `LORA_ALPHA` 设为 64。
- **常见值**：64
- **来源环境变量**：LORA_ALPHA
- **性能影响**：机制推断：alpha 只是缩放系数，不改变 LoRA rank、参数量或主要算子规模；性能更多受 rank、target modules、merge/refit 方式影响。
- **精度影响**：机制推断：alpha 改变低秩更新的有效幅度；过大可能让适配更新过激，过小可能学习不足，通常要和 rank、学习率一起调节。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh:63` actor_rollout_ref.model.lora.alpha=${lora_alpha}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

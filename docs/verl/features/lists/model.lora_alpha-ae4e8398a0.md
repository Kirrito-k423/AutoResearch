# model.lora_alpha

- **参数名**：`model.lora_alpha`
- **分类**：效率
- **中文解释**：设置 SFT/LoRA 训练中的 LoRA alpha 缩放系数；官方参数表说明 `actor_rollout_ref.model.lora_alpha` 默认 16，SFT trainer 会把它写入 LoRA adapter 配置。
- **常见值**：16
- **来源环境变量**：LORA_ALPHA
- **性能影响**：机制推断：`lora_alpha` 主要改变 LoRA 更新缩放，不改变 adapter rank 或目标模块数量，因此对显存/吞吐通常影响很小。
- **精度影响**：机制推断：alpha 会改变 LoRA 分支的有效更新幅度；过小可能欠适配，过大可能放大更新并影响训练稳定性或泛化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh:42` "model.lora_alpha=${LORA_ALPHA}"
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh:52` "model.lora_alpha=${LORA_ALPHA}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

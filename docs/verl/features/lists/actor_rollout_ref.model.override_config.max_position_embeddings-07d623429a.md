# actor_rollout_ref.model.override_config.max_position_embeddings

- **参数名**：`actor_rollout_ref.model.override_config.max_position_embeddings`
- **分类**：效率
- **中文解释**：机制推断：覆盖 HuggingFace model config 中的 `max_position_embeddings`，用于把模型声明的最大位置长度调到当前长上下文训练/rollout 需要的上限。
- **常见值**：$max_position_embeddings
- **来源环境变量**：无
- **性能影响**：机制推断：更大的位置上限通常意味着允许更长 prompt/response，attention、KV cache、激活和显存压力都会随有效序列长度上升；只改 config 而实际序列不变时性能影响有限。
- **精度影响**：机制推断：上限太小会导致长样本截断或运行报错；上限超过模型预训练/位置编码可靠范围时，可能出现长上下文泛化下降，需要配合 RoPE/模型配置验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:89` +actor_rollout_ref.model.override_config.max_position_embeddings=$max_position_embeddings \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

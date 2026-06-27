# actor_rollout_ref.model.lora.merge

- **参数名**：`actor_rollout_ref.model.lora.merge`
- **分类**：效率
- **中文解释**：文档说明：LoRA 权重同步/refit 时是否先把 adapter 合并进 base model 再传给 rollout engine；`True` 表示同步完整合并权重，`False` 表示尽量原生加载 adapter delta。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Megatron-Bridge LoRA 文档说明 merge 可带来更好的推理速度，但会增加 refit/权重同步时间；FSDP LoRA 文档还说明 SGLang 当前要求 `merge=True`。
- **精度影响**：文档说明：官方文档明确提醒合并 LoRA 后传 vLLM 可能有潜在精度损失；若 adapter 原生加载与合并权重数学一致，则通常不改变训练目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:54` +actor_rollout_ref.model.lora.merge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

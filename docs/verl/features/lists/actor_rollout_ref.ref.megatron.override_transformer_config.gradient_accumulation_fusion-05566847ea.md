# actor_rollout_ref.ref.megatron.override_transformer_config.gradient_accumulation_fusion

- **参数名**：`actor_rollout_ref.ref.megatron.override_transformer_config.gradient_accumulation_fusion`
- **分类**：效率
- **中文解释**：文档说明：Reference Megatron transformer config 中的梯度累积融合开关；Verl 性能建议把 actor 侧该开关作为额外加速项，本 ref 示例显式设为 `False` 以匹配 Megatron-FSDP 示例兼容性。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：开启 fused gradient accumulation 可减少梯度累积 kernel/内存写入开销获得额外速度；设为 `False` 会放弃该融合收益，但可能规避特定 ref/Megatron-FSDP 路径兼容问题。
- **精度影响**：机制推断：融合与否理论上只改变执行方式，不改变梯度含义；浮点累积顺序不同可能带来微小数值差异，通常不影响 reference forward-only 结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:78` ++actor_rollout_ref.ref.megatron.override_transformer_config.gradient_accumulation_fusion=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

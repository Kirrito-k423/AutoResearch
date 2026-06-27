# actor_rollout_ref.ref.megatron.override_transformer_config.use_flash_attn

- **参数名**：`actor_rollout_ref.ref.megatron.override_transformer_config.use_flash_attn`
- **分类**：效率
- **中文解释**：文档说明：Reference Megatron transformer config 中是否使用 Flash Attention；Ascend/NPU 特性文档将 `use_flash_attn` 标为注意力计算加速开关。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Flash Attention 通过融合/IO-aware 注意力实现降低显存访问和显存峰值，通常提升长序列 reference logprob 吞吐；需后端、dtype 和设备支持。
- **精度影响**：机制推断：主要是数值实现差异，不改变目标公式；与普通 attention 相比可能有微小浮点误差，需要在高精度敏感的 KL/logprob 场景监控一致性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:155` ++actor_rollout_ref.ref.megatron.override_transformer_config.use_flash_attn=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

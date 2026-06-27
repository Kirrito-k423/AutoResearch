# actor_rollout_ref.actor.megatron.override_transformer_config.use_flash_attn

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.use_flash_attn`
- **分类**：效率
- **中文解释**：文档说明：Megatron transformer config 中启用 FlashAttention/高效 attention backend 的开关，Ascend 和大模型 Megatron 示例常显式设为 True。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：FlashAttention 通常降低 attention 显存访问和中间激活占用，提高长序列 attention 吞吐；不支持的模型/硬件可能需要回退。
- **精度影响**：机制推断：目标函数不变，但 fused attention kernel 与普通实现存在浮点舍入顺序差异；通常只带来微小数值差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:198` +actor_rollout_ref.actor.megatron.override_transformer_config.use_flash_attn=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:131` +actor_rollout_ref.actor.megatron.override_transformer_config.use_flash_attn=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:125` +actor_rollout_ref.actor.megatron.override_transformer_config.use_flash_attn=True

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

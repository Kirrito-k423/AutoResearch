# actor_rollout_ref.model.use_fused_kernels

- **参数名**：`actor_rollout_ref.model.use_fused_kernels`
- **分类**：效率
- **中文解释**：文档说明：控制是否启用 Verl 支持模型的 fused kernels，主要优化输出 head/模型相关内核；与 Liger 这类模型内部 fused kernel 可并用。
- **常见值**：False、True
- **来源环境变量**：USE_FUSED_KERNELS
- **性能影响**：文档说明：官方最佳实践建议对支持模型开启 fused kernels 以获得额外性能；性能调优文档说明它与 Liger 同用时可形成更好的速度-显存折中。
- **精度影响**：机制推断：通常是等价内核替换，不改变训练目标；但部分功能存在兼容约束（如某些算法需关闭直到 fused kernels 支持所需 logits），不兼容时风险主要体现为运行失败或数值路径差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/grpo_trainer/run_seed_oss_36b_fsdp.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:108` actor_rollout_ref.model.use_fused_kernels=True
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:131` actor_rollout_ref.model.use_fused_kernels=False
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:80` actor_rollout_ref.model.use_fused_kernels=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:102` actor_rollout_ref.model.use_fused_kernels=True
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh:135` actor_rollout_ref.model.use_fused_kernels=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

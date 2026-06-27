# actor_rollout_ref.ref.megatron.use_mbridge

- **参数名**：`actor_rollout_ref.ref.megatron.use_mbridge`
- **分类**：效率
- **中文解释**：文档说明：为 reference model 的 Megatron 后端启用 mbridge/Megatron-Bridge 权重格式转换；当模型以 Megatron 训练或需要与 actor 的 Megatron 配置对齐时，用它保证参考模型能按相同并行格式加载权重。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：mbridge 主要影响权重转换、加载和同步链路；它可能增加启动或权重同步开销，但能避免 Megatron 权重格式不匹配造成的运行失败。
- **精度影响**：机制推断：成功转换后不应改变 reference 目标；若桥接版本或格式不一致，可能造成权重加载失败或参考 logprob/KL 口径异常。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:118` actor_rollout_ref.ref.megatron.use_mbridge=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:113` actor_rollout_ref.ref.megatron.use_mbridge=True
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh:86` actor_rollout_ref.ref.megatron.use_mbridge=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:204` actor_rollout_ref.ref.megatron.use_mbridge=True
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:75` actor_rollout_ref.ref.megatron.use_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

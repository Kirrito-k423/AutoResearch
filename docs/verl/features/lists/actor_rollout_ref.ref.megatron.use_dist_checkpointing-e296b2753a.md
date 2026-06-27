# actor_rollout_ref.ref.megatron.use_dist_checkpointing

- **参数名**：`actor_rollout_ref.ref.megatron.use_dist_checkpointing`
- **分类**：效率
- **中文解释**：文档说明：控制 reference model 的 Megatron 后端是否使用分布式 checkpoint 格式加载权重；通常与 actor 保持一致，保证 ref logprob/KL 所用权重来源可恢复。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响 ref 模型加载、恢复和 checkpoint I/O；ref 通常不训练，因此对 optimizer step 计算无直接影响，但能降低超大 ref 权重集中加载的内存压力。
- **精度影响**：机制推断：格式本身不改变 ref 数值；若 ref checkpoint 路径或分片不匹配，会改变参考策略 logprob/KL，进而影响 RL 训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:88` actor_rollout_ref.ref.megatron.use_dist_checkpointing=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:252` actor_rollout_ref.ref.megatron.use_dist_checkpointing=True
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:185` actor_rollout_ref.ref.megatron.use_dist_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:154` actor_rollout_ref.ref.megatron.use_dist_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:153` actor_rollout_ref.ref.megatron.use_dist_checkpointing=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

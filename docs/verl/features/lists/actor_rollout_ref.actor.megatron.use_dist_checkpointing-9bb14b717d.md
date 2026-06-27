# actor_rollout_ref.actor.megatron.use_dist_checkpointing

- **参数名**：`actor_rollout_ref.actor.megatron.use_dist_checkpointing`
- **分类**：效率
- **中文解释**：文档说明：控制 actor Megatron 后端是否使用分布式 checkpoint 格式保存/加载权重；通常与 `dist_checkpointing_path` 配套，用于 MCore/Megatron 大模型权重。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响 checkpoint 加载/保存的 I/O、内存峰值和启动恢复流程；分布式权重可避免超大模型集中汇聚成单份 HF 权重，但不直接改变单个训练 step 的前后向计算。
- **精度影响**：机制推断：若加载的是同一模型权重，格式选择不改变训练目标；路径、分片或转换不匹配会造成权重错误，从而直接破坏 rollout/logprob/KL 信号。
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

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:66` actor_rollout_ref.actor.megatron.use_dist_checkpointing=True
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:250` actor_rollout_ref.actor.megatron.use_dist_checkpointing=True
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:183` actor_rollout_ref.actor.megatron.use_dist_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:128` actor_rollout_ref.actor.megatron.use_dist_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:122` actor_rollout_ref.actor.megatron.use_dist_checkpointing=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

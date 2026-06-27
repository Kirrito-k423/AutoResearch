# actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer

- **参数名**：`actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer`
- **分类**：效率
- **中文解释**：文档说明：Actor Megatron/hybrid optimizer 的精度感知优化器开关；Verl best practices 将它与 CPU optimizer offload、D2H/H2D overlap 一起列为混合优化器配套开关。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：主要服务于 CPU offload/hybrid optimizer 场景，可降低 GPU 优化器状态压力；代价是 CPU/GPU 状态管理和传输链路更复杂。
- **精度影响**：机制推断：目标是保持优化器状态/更新的合理精度，通常不改变算法；不同优化器数值路径可能造成轻微可复现性差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:90` +actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer=True
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:123` +actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer=True \
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:81` +actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer=True
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:140` +actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:104` +actor_rollout_ref.actor.optim.override_optimizer_config.use_precision_aware_optimizer=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

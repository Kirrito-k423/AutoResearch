# actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction

- **参数名**：`actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction`
- **分类**：效率
- **中文解释**：把参数、梯度或优化器状态卸载到 CPU/主机侧，降低 HBM 压力但可能拖慢训练。
- **常见值**：1、1.0
- **来源环境变量**：OPTIMIZER_OFFLOAD_FRACTION
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
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

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:88` +actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction=${optimizer_offload_fraction}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:121` +actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction=1 \
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh:79` +actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction=1
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:138` +actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction=1
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh:102` +actor_rollout_ref.actor.optim.override_optimizer_config.optimizer_offload_fraction=1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

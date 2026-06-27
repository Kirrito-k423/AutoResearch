# actor_rollout_ref.actor.strategy

- **参数名**：`actor_rollout_ref.actor.strategy`
- **分类**：效率
- **中文解释**：文档说明：actor 训练后端策略选择，examples 中主要为 `fsdp2` 或 `megatron`；官方 examples 约定把 train-backend 暴露为脚本级配置，perf 文档说明可用 `actor_rollout_ref.actor.strategy="fsdp2"` 启用 FSDP2。
- **常见值**：fsdp2、megatron
- **来源环境变量**：无
- **性能影响**：文档说明：FSDP2 在官方引用的 TorchTitan benchmark 中有较低显存和轻微吞吐收益；Megatron 适合大模型多维并行，但需要更多通信/并行配置调优。
- **精度影响**：机制推断：训练后端不应改变算法目标；不同后端的数值路径、checkpoint 格式和混合精度实现可能带来微小差异或兼容风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：15
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_seed_oss_36b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`
- `examples/tuning/scaling/run_qwen2_5_32b_megatron.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:148` actor_rollout_ref.actor.strategy=fsdp2
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:76` actor_rollout_ref.actor.strategy=fsdp2
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:63` actor_rollout_ref.actor.strategy=fsdp2
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:107` actor_rollout_ref.actor.strategy=fsdp2
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:79` actor_rollout_ref.actor.strategy=fsdp2

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

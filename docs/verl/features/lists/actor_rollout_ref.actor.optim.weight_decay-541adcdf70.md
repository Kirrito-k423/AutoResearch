# actor_rollout_ref.actor.optim.weight_decay

- **参数名**：`actor_rollout_ref.actor.optim.weight_decay`
- **分类**：效率
- **中文解释**：文档说明：Actor 优化器权重衰减系数；Verl best practices 给出常见值 0.1，Ascend 参数表说明该项用于防止过拟合。
- **常见值**：0.1
- **来源环境变量**：无
- **性能影响**：机制推断：几乎不影响单步吞吐或显存；主要影响 actor 更新的正则化强度和收敛路径。
- **精度影响**：文档说明：权重衰减用于正则化、防止过拟合；过高会压制策略适配，过低可能增加过拟合或不稳定风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:88` actor_rollout_ref.actor.optim.weight_decay=0.1 \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:75` actor_rollout_ref.actor.optim.weight_decay=0.1
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:89` actor_rollout_ref.actor.optim.weight_decay=0.1
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:86` actor_rollout_ref.actor.optim.weight_decay=0.1
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:138` actor_rollout_ref.actor.optim.weight_decay=0.1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

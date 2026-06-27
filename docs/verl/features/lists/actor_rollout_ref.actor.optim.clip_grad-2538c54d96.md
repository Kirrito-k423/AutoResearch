# actor_rollout_ref.actor.optim.clip_grad

- **参数名**：`actor_rollout_ref.actor.optim.clip_grad`
- **分类**：算法
- **中文解释**：文档说明：actor 优化器的梯度裁剪阈值，常见值 `1.0`；在 optimizer step 前限制梯度范数，避免单次更新过大。
- **常见值**：1.0
- **来源环境变量**：无
- **性能影响**：机制推断：需要额外计算/同步梯度范数，通常相对训练前后向成本较小；对大规模分布式训练会有少量通信/归约开销。
- **精度影响**：机制推断：直接影响优化动态而非损失定义；阈值较低会抑制大梯度、提升稳定性但可能减慢收敛，阈值过高或关闭可能增加梯度爆炸和策略崩坏风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
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

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:89` actor_rollout_ref.actor.optim.clip_grad=1.0 \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:76` actor_rollout_ref.actor.optim.clip_grad=1.0
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:90` actor_rollout_ref.actor.optim.clip_grad=1.0
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:87` actor_rollout_ref.actor.optim.clip_grad=1.0
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:139` actor_rollout_ref.actor.optim.clip_grad=1.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

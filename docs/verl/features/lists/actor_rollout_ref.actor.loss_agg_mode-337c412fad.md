# actor_rollout_ref.actor.loss_agg_mode

- **参数名**：`actor_rollout_ref.actor.loss_agg_mode`
- **分类**：算法
- **中文解释**：文档说明：actor loss 从 token/sequence loss 矩阵聚合成标量的方式；官方最佳实践称 `token-mean` 符合 Dr.GRPO/DAPO 推荐，`seq-mean-token-mean` 可复现原 GRPO 行为。
- **常见值**："token-mean"、seq-mean-token-mean、seq-mean-token-sum-norm、token-mean
- **来源环境变量**：无
- **性能影响**：机制推断：聚合计算本身很轻，不是主要吞吐瓶颈；但不同归一化会改变梯度尺度，可能影响需要的调参和重跑次数。
- **精度影响**：文档说明：不同聚合方式改变长短序列在 loss 中的权重和梯度尺度，直接影响训练稳定性以及与论文/基线的可比性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:76` actor_rollout_ref.actor.loss_agg_mode=seq-mean-token-sum-norm
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:102` actor_rollout_ref.actor.loss_agg_mode=seq-mean-token-mean
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:67` actor_rollout_ref.actor.loss_agg_mode=seq-mean-token-mean
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:95` actor_rollout_ref.actor.loss_agg_mode=token-mean \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:82` actor_rollout_ref.actor.loss_agg_mode=token-mean

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

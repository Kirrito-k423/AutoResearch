# MTP_LOSS_SCALING_FACTOR

- **参数名**：`MTP_LOSS_SCALING_FACTOR`
- **分类**：算法
- **中文解释**：文档说明：`MTP_LOSS_SCALING_FACTOR` 是 examples 暴露的多 token 预测（MTP）训练损失缩放因子，写入 `model.mtp.mtp_loss_scaling_factor` 或 `actor_rollout_ref.model.mtp.mtp_loss_scaling_factor`。
- **常见值**：0.1、0.2
- **来源环境变量**：MTP_LOSS_SCALING_FACTOR
- **性能影响**：机制推断：该因子本身几乎不改变算量；只有启用 MTP 训练时才会引入额外预测头/损失计算，缩放因子主要改变梯度权重。
- **精度影响**：机制推断：直接改变 MTP 辅助目标相对主语言建模/RL 目标的权重；过大可能压制主目标，过小则 MTP 学习信号不足。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:32` mtp_loss_scaling_factor=${MTP_LOSS_SCALING_FACTOR:-0.1}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:27` mtp_loss_scaling_factor=${MTP_LOSS_SCALING_FACTOR:-0.1}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:24` mtp_loss_scaling_factor=${MTP_LOSS_SCALING_FACTOR:-0.2}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:88` MTP_LOSS_SCALING_FACTOR=${MTP_LOSS_SCALING_FACTOR:-0.1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

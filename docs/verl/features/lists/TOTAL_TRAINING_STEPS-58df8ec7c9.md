# TOTAL_TRAINING_STEPS

- **参数名**：`TOTAL_TRAINING_STEPS`
- **分类**：效率
- **中文解释**：文档说明：`TOTAL_TRAINING_STEPS` 是 examples 暴露的训练总步数环境变量，通常写入 `trainer.total_training_steps`；Verl 参数表说明该字段为 `null` 时按 epoch 自动计算。
- **常见值**：1、3000、400、50000
- **来源环境变量**：TOTAL_TRAINING_STEPS
- **性能影响**：机制推断：训练 wall time、样本消耗、日志/checkpoint 次数通常随总步数近似线性增加；较小步数适合 smoke test，较大步数用于完整训练。
- **精度影响**：机制推断：直接影响优化时长；步数过少容易欠训练，步数过多可能过拟合或放大不稳定训练动态，最佳值依赖数据量和学习率计划。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:38` total_training_steps=${TOTAL_TRAINING_STEPS:-400}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:50` total_training_steps=${TOTAL_TRAINING_STEPS:-3000}
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:40` total_training_steps=${TOTAL_TRAINING_STEPS:-50000}
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:21` TOTAL_TRAINING_STEPS=${TOTAL_TRAINING_STEPS:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

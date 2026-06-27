# actor_rollout_ref.actor.optim.lr_warmup_steps

- **参数名**：`actor_rollout_ref.actor.optim.lr_warmup_steps`
- **分类**：算法
- **中文解释**：文档说明：Actor 优化器学习率预热步数；Verl best practices 给出 10 作为示例，配置注释说明正数会优先于 `lr_warmup_steps_ratio`，非正值则回退到比例计算。
- **常见值**：0、10
- **来源环境变量**：WARMUP_STEPS
- **性能影响**：机制推断：几乎不改变单步吞吐；但预热过长会让有效学习率上升更慢，增加达到同等效果所需的训练步数。
- **精度影响**：机制推断：预热可缓解训练初期大更新导致的不稳定；过短可能震荡，过长可能学习偏慢或欠拟合。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:86` actor_rollout_ref.actor.optim.lr_warmup_steps=10 \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:74` actor_rollout_ref.actor.optim.lr_warmup_steps=10
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:87` actor_rollout_ref.actor.optim.lr_warmup_steps=0
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:93` actor_rollout_ref.actor.optim.lr_warmup_steps=${warmup_steps}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:85` actor_rollout_ref.actor.optim.lr_warmup_steps=10

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

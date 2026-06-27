# actor_rollout_ref.actor.entropy_checkpointing

- **参数名**：`actor_rollout_ref.actor.entropy_checkpointing`
- **分类**：算法
- **中文解释**：Actor 训练中对 entropy 计算启用专门的重计算/checkpointing；它弥补普通 gradient checkpointing 不覆盖 entropy 计算的情况。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Verl 性能调优文档说明 entropy logits 张量显存很大，开启该项可降低训练时 entropy 计算的峰值显存，但会引入重算开销。
- **精度影响**：机制推断：checkpointing/recompute 应保持同一 entropy 公式，不改变 RL 目标；正常情况下不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:152` actor_rollout_ref.actor.entropy_checkpointing=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:102` actor_rollout_ref.actor.entropy_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:84` actor_rollout_ref.actor.entropy_checkpointing=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

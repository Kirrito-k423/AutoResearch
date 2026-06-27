# actor_rollout_ref.ref.entropy_checkpointing

- **参数名**：`actor_rollout_ref.ref.entropy_checkpointing`
- **分类**：算法
- **中文解释**：控制 reference/ref 路径在熵或 logits 相关计算中是否使用 checkpointing/recompute；官方参数表说明 `ref.entropy_checkpointing` 表示是否对熵计算使用梯度检查点。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：entropy checkpointing 通过重计算降低熵计算峰值显存，代价是额外前向/重算时间；适合长序列或大模型内存紧张场景。
- **精度影响**：机制推断：checkpointing 目标是以重算换显存，不改变熵或 logprob 的数学定义；仅可能带来极小数值顺序差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:147` actor_rollout_ref.ref.entropy_checkpointing=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:129` actor_rollout_ref.ref.entropy_checkpointing=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

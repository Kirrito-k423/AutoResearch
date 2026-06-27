# actor_rollout_ref.actor.fsdp_config.entropy_checkpointing

- **参数名**：`actor_rollout_ref.actor.fsdp_config.entropy_checkpointing`
- **分类**：算法
- **中文解释**：FSDP actor 配置下的 entropy 计算重计算开关，用于在训练时降低 entropy logits 相关的峰值显存。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：Ascend/Verl 文档均描述该项是在训练时对熵计算启用重计算以降低显存峰值；代价是额外计算时间。
- **精度影响**：机制推断：该开关改变的是显存换算力的执行方式，不改变 entropy loss/bonus 的数学定义；正常情况下不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:89` actor_rollout_ref.actor.fsdp_config.entropy_checkpointing=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:118` actor_rollout_ref.actor.fsdp_config.entropy_checkpointing=True
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:89` actor_rollout_ref.actor.fsdp_config.entropy_checkpointing=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

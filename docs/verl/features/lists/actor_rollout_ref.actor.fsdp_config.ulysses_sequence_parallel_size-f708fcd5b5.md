# actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size

- **参数名**：`actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Actor FSDP 配置中的 Ulysses 序列并行大小；Verl performance tuning 建议在长上下文训练中将 `ulysses_sequence_parallel_size>1` 用于 actor/ref/critic/reward。
- **常见值**：1、2、4、8
- **来源环境变量**：SP_SIZE
- **性能影响**：文档说明：序列并行可降低长序列下单卡激活/注意力显存压力，帮助训练 32k 以上上下文；代价是额外序列切分通信和调度复杂度。
- **精度影响**：机制推断：并行方式不改变损失定义；但若不开启导致必须降低 token 上限、micro batch 或截断样本，会间接影响训练信号。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:151` actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size=${sp_size}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:99` actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size=${sp_size}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:92` actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:119` actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh:128` actor_rollout_ref.actor.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

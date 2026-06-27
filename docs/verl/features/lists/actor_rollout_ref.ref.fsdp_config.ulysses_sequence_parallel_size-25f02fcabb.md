# actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size

- **参数名**：`actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Reference FSDP 配置中的 Ulysses 序列并行大小；Verl 支持不同模型设置不同的 `ulysses_sequence_parallel_size`，reference 通常需与 actor 的长序列 logprob 计算容量匹配。
- **常见值**：1、2、4、8
- **来源环境变量**：SP_SIZE
- **性能影响**：文档说明：可降低 reference logprob 长序列前向计算的单卡显存压力；同时引入序列并行通信，实际吞吐取决于序列长度和硬件拓扑。
- **精度影响**：机制推断：不改变 reference 模型目标；若设置过小导致 OOM、降 token 上限或跳过长样本，会间接影响 KL/logprob 训练信号。
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

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:159` actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size=${sp_size}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:141` actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size=${sp_size}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:103` actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:143` actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh:129` actor_rollout_ref.ref.fsdp_config.ulysses_sequence_parallel_size=${SP_SIZE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

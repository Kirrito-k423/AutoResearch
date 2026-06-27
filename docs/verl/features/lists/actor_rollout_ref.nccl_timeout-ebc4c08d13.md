# actor_rollout_ref.nccl_timeout

- **参数名**：`actor_rollout_ref.nccl_timeout`
- **分类**：效率
- **中文解释**：文档说明：actor/rollout/ref 分布式通信的 NCCL 超时时间（秒）；大模型、多节点、长序列或 checkpoint 同步较慢时会在 examples 中调大。
- **常见值**：10800、1200、14400、7200
- **来源环境变量**：无
- **性能影响**：机制推断：不提升通信带宽或吞吐；调大可避免慢 collective 被过早判定失败，调小能更快暴露死锁/网络故障但可能误杀正常的大规模操作。
- **精度影响**：机制推断：不改变模型计算或优化目标；主要影响慢通信是继续等待还是提前失败，只有在超时导致作业中断/重启时才会间接影响训练连续性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:80` actor_rollout_ref.nccl_timeout=14400
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:185` actor_rollout_ref.nccl_timeout=1200
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:145` actor_rollout_ref.nccl_timeout=10800
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:140` actor_rollout_ref.nccl_timeout=7200
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:62` actor_rollout_ref.nccl_timeout=14400

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

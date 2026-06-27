# ACTOR_CP

- **参数名**：`ACTOR_CP`
- **分类**：效率
- **中文解释**：文档说明：examples 中用于设置 actor Megatron `context_parallel_size` 的环境变量，即上下文/序列维度并行度，主要服务长上下文训练。
- **常见值**：1、2
- **来源环境变量**：ACTOR_CP
- **性能影响**：文档说明：Verl best practices 建议在 PP/TP/EP/ETP/CP 间平衡显存和网络约束，CP 可扩展序列容量但会增加通信。
- **精度影响**：机制推断：上下文并行不改变目标函数；若它让更长上下文免于截断，可能间接改善任务覆盖，否则主要是数值并行路径差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:36` actor_cp=${ACTOR_CP:-1}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:31` actor_cp=${ACTOR_CP:-2}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:28` actor_cp=${ACTOR_CP:-1}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:40` actor_cp=${ACTOR_CP:-1}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:44` actor_cp=${ACTOR_CP:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# actor_rollout_ref.rollout.val_kwargs.top_k

- **参数名**：`actor_rollout_ref.rollout.val_kwargs.top_k`
- **分类**：算法
- **中文解释**：文档说明：验证阶段 rollout 的 Top-K 采样参数；Verl 配置文档说明 `val_kwargs.top_k` 专用于 validation，`-1` 常用于 vLLM 表示不启用 Top-K，HF rollout 常用 `0`。
- **常见值**：-1
- **来源环境变量**：TOP_K
- **性能影响**：机制推断：通常不是主要吞吐瓶颈；较小 Top-K 会限制候选 token 集合，但整体耗时仍主要由生成长度、batch 和后端调度决定。
- **精度影响**：文档说明：直接改变验证采样分布和多样性；与 `temperature`、`top_p`、`do_sample`、`n` 一起决定评测方差和是否更接近贪心输出。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:117` actor_rollout_ref.rollout.val_kwargs.top_k=-1 \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:131` actor_rollout_ref.rollout.val_kwargs.top_k=${top_k}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:142` actor_rollout_ref.rollout.val_kwargs.top_k=-1
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:166` actor_rollout_ref.rollout.val_kwargs.top_k=${top_k}
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:184` actor_rollout_ref.rollout.val_kwargs.top_k=-1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

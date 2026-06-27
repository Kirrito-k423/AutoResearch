# actor_rollout_ref.rollout.val_kwargs.n

- **参数名**：`actor_rollout_ref.rollout.val_kwargs.n`
- **分类**：效率
- **中文解释**：文档说明：验证阶段每个 prompt 生成的候选数；官方 Best Practices 建议小测试集可增大 `n`（如 64）以降低方差，常用起点为 `n=1`。
- **常见值**：$n_resp_per_prompt_val、1
- **来源环境变量**：VAL_N
- **性能影响**：机制推断：验证生成成本近似随 `n` 线性增长，显存/KV cache/日志体积也随候选数上升。
- **精度影响**：文档说明：增大验证采样数可降低小评测集指标方差，但评测口径会改变，需与历史结果保持一致。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：13
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:154` actor_rollout_ref.rollout.val_kwargs.n=1
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:100` actor_rollout_ref.rollout.val_kwargs.n=1
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:119` actor_rollout_ref.rollout.val_kwargs.n=1 \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:133` actor_rollout_ref.rollout.val_kwargs.n=1
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:144` actor_rollout_ref.rollout.val_kwargs.n=1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

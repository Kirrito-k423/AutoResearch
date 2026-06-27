# actor_rollout_ref.rollout.val_kwargs.temperature

- **参数名**：`actor_rollout_ref.rollout.val_kwargs.temperature`
- **分类**：算法
- **中文解释**：文档说明：验证 rollout 的采样温度；官方 Best Practices 建议验证时设置 `temperature > 0` 以避免重复思维链，实用起点为 `temperature=1.0`。
- **常见值**：1.0
- **来源环境变量**：TEMPERATURE、VAL_TEMPERATURE
- **性能影响**：机制推断：温度缩放本身开销很小；但温度改变输出长度和采样路径，可能间接影响验证耗时。
- **精度影响**：文档说明：直接改变验证采样分布和指标方差；温度过低更确定但可能重复，过高更多样但结果波动更大。
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

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:155` actor_rollout_ref.rollout.val_kwargs.temperature=1.0
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:101` actor_rollout_ref.rollout.val_kwargs.temperature=1.0
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:115` actor_rollout_ref.rollout.val_kwargs.temperature=1.0 \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:129` actor_rollout_ref.rollout.val_kwargs.temperature=${temperature}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:140` actor_rollout_ref.rollout.val_kwargs.temperature=1.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

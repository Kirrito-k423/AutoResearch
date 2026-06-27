# actor_rollout_ref.rollout.val_kwargs.top_p

- **参数名**：`actor_rollout_ref.rollout.val_kwargs.top_p`
- **分类**：算法
- **中文解释**：文档说明：验证 rollout 的 nucleus sampling 阈值；官方 Best Practices 把 `top_p=0.7` 作为验证采样实用起点，也有脚本用 `1.0` 表示不过滤概率尾部。
- **常见值**：0.7、1.0
- **来源环境变量**：VAL_TOP_P
- **性能影响**：机制推断：top-p 过滤有少量采样开销；主要间接影响输出长度、重复率和验证生成时间。
- **精度影响**：文档说明：较低 top_p 会收窄候选集合、降低随机性；较高 top_p 增加多样性和方差，评测需固定口径。
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

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:156` actor_rollout_ref.rollout.val_kwargs.top_p=0.7
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:102` actor_rollout_ref.rollout.val_kwargs.top_p=0.7
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:116` actor_rollout_ref.rollout.val_kwargs.top_p=0.7 \
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:130` actor_rollout_ref.rollout.val_kwargs.top_p=${val_top_p}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:141` actor_rollout_ref.rollout.val_kwargs.top_p=0.7

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

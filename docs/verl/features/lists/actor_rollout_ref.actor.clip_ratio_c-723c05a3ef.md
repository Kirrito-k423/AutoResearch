# actor_rollout_ref.actor.clip_ratio_c

- **参数名**：`actor_rollout_ref.actor.clip_ratio_c`
- **分类**：算法
- **中文解释**：文档说明：Dual-clip PPO 的额外裁剪常数，官方 PPO README/算法文档说明它在 advantage 为负时为 policy ratio 乘积设置下界，默认约 3.0；examples 中常设 10.0 或更大。
- **常见值**：10.0、10000.0
- **来源环境变量**：ACTOR_CLIP_RATIO_C
- **性能影响**：机制推断：仅增加 loss 中一次条件裁剪/下界计算，吞吐影响可忽略。
- **精度影响**：文档说明：直接改变 PPO surrogate objective 的负优势样本约束；较小值更强地限制极端更新，较大值接近弱化 dual-clip 保护。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：13
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:79` actor_rollout_ref.actor.clip_ratio_c=10000.0
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:105` actor_rollout_ref.actor.clip_ratio_c=10.0
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:70` actor_rollout_ref.actor.clip_ratio_c=10.0
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:98` actor_rollout_ref.actor.clip_ratio_c=10.0 \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:85` actor_rollout_ref.actor.clip_ratio_c=10.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# CLIP_RATIO_HIGH

- **参数名**：`CLIP_RATIO_HIGH`
- **分类**：算法
- **中文解释**：文档说明：examples 环境变量，用来填写 `actor_rollout_ref.actor.clip_ratio_high`，即 PPO/GSPO/DAPO 等 policy objective 的 importance sampling 上界裁剪比例。
- **常见值**：0.2、0.28、4e-4
- **来源环境变量**：CLIP_RATIO_HIGH
- **性能影响**：机制推断：几乎不改变训练吞吐，只改变 loss 中 clamp/ratio 逻辑；极端取值可能通过训练不稳定增加重跑成本。
- **精度影响**：文档说明：官方最佳实践称 `clip_ratio_low/high` 是 importance sampling clipping bounds，并给 DAPO 建议 `0.2/0.28`；high 越大允许正向策略更新更激进，稳定性风险更高。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:24` CLIP_RATIO_HIGH=${CLIP_RATIO_HIGH:-4e-4}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:25` clip_ratio_high=${CLIP_RATIO_HIGH:-4e-4}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:30` clip_ratio_high=${CLIP_RATIO_HIGH:-0.28}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:25` clip_ratio_high=${CLIP_RATIO_HIGH:-0.28}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:22` clip_ratio_high=${CLIP_RATIO_HIGH:-0.28}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

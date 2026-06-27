# CLIP_RATIO_LOW

- **参数名**：`CLIP_RATIO_LOW`
- **分类**：算法
- **中文解释**：文档说明：examples 环境变量，用来填写 `actor_rollout_ref.actor.clip_ratio_low`，即 importance sampling 下界裁剪比例；CISPO 示例把 low 设到 10 以近似关闭下侧裁剪。
- **常见值**：0.2、10、3e-4
- **来源环境变量**：CLIP_RATIO_LOW
- **性能影响**：机制推断：不显著影响每步计算成本，只改变策略损失的裁剪边界。
- **精度影响**：文档说明：官方最佳实践称 low/high 是 importance sampling 裁剪边界；low 控制负向/下界更新约束，过松或过紧都会改变探索和稳定性。
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

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:23` CLIP_RATIO_LOW=${CLIP_RATIO_LOW:-3e-4}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:24` clip_ratio_low=${CLIP_RATIO_LOW:-3e-4}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:29` clip_ratio_low=${CLIP_RATIO_LOW:-0.2}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:24` clip_ratio_low=${CLIP_RATIO_LOW:-0.2}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:21` clip_ratio_low=${CLIP_RATIO_LOW:-0.2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

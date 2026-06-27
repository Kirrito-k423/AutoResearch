# actor_rollout_ref.actor.clip_ratio_high

- **参数名**：`actor_rollout_ref.actor.clip_ratio_high`
- **分类**：算法
- **中文解释**：文档说明：PPO/DAPO importance sampling ratio 的上裁剪界；Best Practices 对 DAPO 推荐 `clip_ratio_high=0.28`，部分 GSPO/CISPO 示例按算法改为更小或特殊值。
- **常见值**：$CLIP_DEFAULT、$clip_ratio_high、0.2、0.28、0.4、4e-4
- **来源环境变量**：ACTOR_CLIP_RATIO_HIGH、CLIP_HIGH、CLIP_RATIO、CLIP_RATIO_HIGH
- **性能影响**：机制推断：只是 loss 里的标量裁剪阈值，计算开销可忽略；主要影响训练动态而非吞吐。
- **精度影响**：文档说明：上界越小，越严格限制正优势样本的策略更新幅度，通常更稳但可能学习慢；上界过大则可能允许过激更新。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：16
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:78` actor_rollout_ref.actor.clip_ratio_high=${clip_ratio_high}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:66` actor_rollout_ref.actor.clip_ratio_high=${clip_ratio}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:104` actor_rollout_ref.actor.clip_ratio_high=${CLIP_RATIO_HIGH}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:69` actor_rollout_ref.actor.clip_ratio_high=${clip_ratio_high}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:97` actor_rollout_ref.actor.clip_ratio_high=${clip_ratio_high} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

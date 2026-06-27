# actor_rollout_ref.rollout.top_p

- **参数名**：`actor_rollout_ref.rollout.top_p`
- **分类**：算法
- **中文解释**：文档说明：Nucleus/Top-P 采样阈值，用累计概率限制候选 token 集合；官方建议与 temperature、top_k 一起作为 rollout 采样旋钮调节探索。
- **常见值**：0.7、1、1.0
- **来源环境变量**：ROLLOUT_TOP_P、TOP_P
- **性能影响**：机制推断：对大模型前向成本影响较小，主要改变采样后处理候选集；可能通过输出多样性和 EOS 分布间接影响生成时长。
- **精度影响**：文档说明：官方最佳实践建议 rollout 保持足够随机性，验证可从 `top_p=0.7` 起步；调低 top_p 会收窄探索，调高更接近全分布采样。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：11
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:122` actor_rollout_ref.rollout.top_p=1.0
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:127` actor_rollout_ref.rollout.top_p=${top_p}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:138` actor_rollout_ref.rollout.top_p=1.0
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:162` actor_rollout_ref.rollout.top_p=${top_p}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:187` actor_rollout_ref.rollout.top_p=${rollout_top_p}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

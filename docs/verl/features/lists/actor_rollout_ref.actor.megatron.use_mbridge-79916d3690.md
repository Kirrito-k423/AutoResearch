# actor_rollout_ref.actor.megatron.use_mbridge

- **参数名**：`actor_rollout_ref.actor.megatron.use_mbridge`
- **分类**：效率
- **中文解释**：文档说明：Megatron 训练后端的 mbridge 格式转换开关；官方 Best Practices 说明 Megatron 训练模型需要启用 mbridge，当前必须为 True。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：主要影响模型初始化、权重格式转换与 checkpoint/HF 互转流程；训练 step 吞吐通常由并行配置和 offload 主导。
- **精度影响**：机制推断：不应改变数值目标；若格式转换版本不匹配或权重映射错误，会造成加载失败或数值不一致风险。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：19
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:93` actor_rollout_ref.actor.megatron.use_mbridge=True
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:84` actor_rollout_ref.actor.megatron.use_mbridge=True
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:105` actor_rollout_ref.actor.megatron.use_mbridge=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:92` actor_rollout_ref.actor.megatron.use_mbridge=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:110` actor_rollout_ref.actor.megatron.use_mbridge=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

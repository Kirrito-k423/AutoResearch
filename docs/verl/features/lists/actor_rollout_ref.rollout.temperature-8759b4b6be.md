# actor_rollout_ref.rollout.temperature

- **参数名**：`actor_rollout_ref.rollout.temperature`
- **分类**：算法
- **中文解释**：文档说明：rollout 采样温度，用来调节 token 分布的随机性；官方最佳实践将它与 `top_p`、`top_k` 一起列为 rollout 采样旋钮。
- **常见值**：1.0
- **来源环境变量**：ROLLOUT_TEMPERATURE、TEMPERATURE
- **性能影响**：机制推断：采样温度主要改变 token 分布，单步前向计算基本不变；极端分布可能通过生成长度或 EOS 分布轻微影响端到端耗时。
- **精度影响**：文档说明：官方建议 rollout 保持足够随机性；temperature 越高探索越强、方差越大，越低越接近贪心采样。
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

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:121` actor_rollout_ref.rollout.temperature=1.0
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:126` actor_rollout_ref.rollout.temperature=${temperature}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:137` actor_rollout_ref.rollout.temperature=1.0
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:161` actor_rollout_ref.rollout.temperature=${temperature}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:186` actor_rollout_ref.rollout.temperature=${rollout_temperature}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

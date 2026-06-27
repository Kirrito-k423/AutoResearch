# actor_rollout_ref.actor.megatron.expert_model_parallel_size

- **参数名**：`actor_rollout_ref.actor.megatron.expert_model_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Megatron MoE expert parallel 的模型并行规模，决定专家层在多少并行组/设备间切分或分布，常与 TP、ETP、PP 一起配置。
- **常见值**：$EP、16、2、4、8
- **来源环境变量**：ACTOR_EP、EP
- **性能影响**：文档说明：EP 可降低单卡专家参数压力并改变 MoE token dispatch/通信模式；设置不当会增加跨卡通信、负载不均或路由瓶颈。
- **精度影响**：机制推断：并行规模不改变目标函数；但专家分片/路由配置错误会导致 checkpoint 不匹配、训练失败或有效 batch 受限。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：15
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:88` actor_rollout_ref.actor.megatron.expert_model_parallel_size=${actor_ep}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:79` actor_rollout_ref.actor.megatron.expert_model_parallel_size=${actor_ep}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:105` actor_rollout_ref.actor.megatron.expert_model_parallel_size=${actor_ep}
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:64` actor_rollout_ref.actor.megatron.expert_model_parallel_size=${ACTOR_EP}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:146` actor_rollout_ref.actor.megatron.expert_model_parallel_size=$EP

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

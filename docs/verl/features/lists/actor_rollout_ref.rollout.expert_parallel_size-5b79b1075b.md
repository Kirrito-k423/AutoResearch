# actor_rollout_ref.rollout.expert_parallel_size

- **参数名**：`actor_rollout_ref.rollout.expert_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧 MoE expert parallel 大小，参数表默认 1；用于控制推理引擎中的专家并行切分。
- **常见值**：$infer_ep、1、128、2、64、8
- **来源环境变量**：GEN_MOE_EP、ROLLOUT_EP
- **性能影响**：机制推断：增大 EP 可分摊 MoE expert 权重和计算，支撑更大模型或更高并发，但增加专家路由通信与调度复杂度。
- **精度影响**：机制推断：正确切分应保持等价输出；并行/路由实现不兼容可能带来同步或数值差异，通常不是主动调精度的参数。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:113` actor_rollout_ref.rollout.expert_parallel_size=$infer_ep \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:115` actor_rollout_ref.rollout.expert_parallel_size=$infer_ep \
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:77` actor_rollout_ref.rollout.expert_parallel_size=8
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:227` actor_rollout_ref.rollout.expert_parallel_size=${gen_moe_ep}
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:108` actor_rollout_ref.rollout.expert_parallel_size=$infer_ep \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

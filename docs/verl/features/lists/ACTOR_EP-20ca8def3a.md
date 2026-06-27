# ACTOR_EP

- **参数名**：`ACTOR_EP`
- **分类**：效率
- **中文解释**：文档说明：examples 环境变量，通常映射到 actor/ref Megatron `expert_model_parallel_size`，用于控制 MoE actor/reference 的专家并行度。
- **常见值**：2、4、8
- **来源环境变量**：ACTOR_EP
- **性能影响**：文档说明：官方最佳实践要求 EP/ETP/TP/PP/CP 按显存和网络约束平衡；增大 `ACTOR_EP` 可降低每卡专家负载，但增加专家通信和拓扑敏感性。
- **精度影响**：机制推断：正确 expert parallel 是等价并行，不直接改变目标；如果 actor/ref EP 不一致或与 checkpoint 权重布局不匹配，会影响加载、KL/reference logprob 或直接失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:37` actor_ep=${ACTOR_EP:-8}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:29` actor_ep=${ACTOR_EP:-8}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:38` actor_ep=${ACTOR_EP:-8}
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:26` ACTOR_EP=${ACTOR_EP:-4}
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:43` actor_ep=${ACTOR_EP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

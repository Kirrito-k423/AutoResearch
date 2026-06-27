# actor_rollout_ref.ref.mindspeed.expert_model_parallel_size

- **参数名**：`actor_rollout_ref.ref.mindspeed.expert_model_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：Reference MindSpeed/Megatron MoE 的专家并行 EP 大小，表示专家在多少并行 rank 间切分/分布；示例与 actor 的 `train_ep` 保持一致。
- **常见值**：4
- **来源环境变量**：无
- **性能影响**：文档说明：Verl best practices 要求 reference Megatron parallelism 与 actor 保持同步；EP 越大单卡专家参数和计算压力越低，但专家路由/all-to-all 通信与负载均衡成本越高。
- **精度影响**：机制推断：正确配置时不改变 reference 策略；EP 与 checkpoint/actor 不一致会造成专家权重切分或路由不匹配，影响 ref logprob 和 KL。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:160` actor_rollout_ref.ref.mindspeed.expert_model_parallel_size=${train_ep}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

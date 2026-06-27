# actor_rollout_ref.actor.mindspeed.expert_model_parallel_size

- **参数名**：`actor_rollout_ref.actor.mindspeed.expert_model_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：MindSpeed/Megatron Actor 的专家并行（EP）大小，用于 MoE 模型中把专家划分到多个 rank。该字段继承 Megatron 引擎配置语义；Verl dataclass 注释说明 `expert_model_parallel_size` 是 MoE expert model parallel size。
- **常见值**：4
- **来源环境变量**：无
- **性能影响**：文档说明：Verl 性能实践建议 EP/ETP 与 TP/PP/CP 一起按显存和网络成本平衡；增大 EP 可降低单 rank 专家权重压力，但会增加 MoE token dispatch/all-to-all 通信和负载均衡要求。
- **精度影响**：机制推断：EP 不改变专家函数或路由目标；但并行划分会改变通信/归约顺序，配置不整除专家数、top-k 或硬件拓扑不匹配时会导致性能抖动或运行失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:123` actor_rollout_ref.actor.mindspeed.expert_model_parallel_size=${train_ep}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

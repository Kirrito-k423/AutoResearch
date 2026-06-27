# actor_rollout_ref.ref.veomni.expert_parallel_size

- **参数名**：`actor_rollout_ref.ref.veomni.expert_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：VeOmni ref 配置默认从 actor 侧继承 `expert_parallel_size`，该示例显式把 reference model 的 MoE expert parallel size 固定为 1，用于控制 ref logprob 前向时专家维度如何切分。
- **常见值**：1"
- **来源环境变量**：无
- **性能影响**：机制推断：增大 ref 侧 EP 可分摊 MoE expert 权重和计算，但会增加专家路由/all-to-all 通信；ref 只做前向/logprob，配置过小可能显存吃紧，配置过大可能通信开销超过收益。
- **精度影响**：机制推断：正确专家并行切分通常不改变 reference logprob 的数学含义；若与 actor/rollout、checkpoint 或后端支持不匹配，可能导致加载失败、路由不一致或轻微数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:78` actor_rollout_ref.ref.veomni.expert_parallel_size=1"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

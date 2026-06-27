# actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_token_dispatcher_type

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_token_dispatcher_type`
- **分类**：效率
- **中文解释**：机制推断：传给 MindSpeed/Megatron Core 的 MoE token dispatcher 类型，控制 token 在专家并行 rank 之间如何分发与收集；示例使用 `alltoall` 适配 Qwen3 MoE 的 MindSpeed NPU 训练。
- **常见值**：alltoall
- **来源环境变量**：无
- **性能影响**：文档说明：Verl 性能建议把 `moe_token_dispatcher_type` 列为 MoE 推荐性能旋钮；`alltoall` 会使用跨卡 all-to-all 通信分发专家 token，能配合 EP/ETP 降低单卡专家负载，但收益受网络拓扑和 dispatcher 后端影响。
- **精度影响**：机制推断：不改变 RL 目标或损失公式；若 dispatcher 类型与 MindSpeed/Megatron 后端、EP/ETP 配置不匹配，可能导致路由/通信错误并破坏训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh:144` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.moe_token_dispatcher_type=alltoall

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

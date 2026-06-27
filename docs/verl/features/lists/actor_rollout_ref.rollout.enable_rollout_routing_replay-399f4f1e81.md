# actor_rollout_ref.rollout.enable_rollout_routing_replay

- **参数名**：`actor_rollout_ref.rollout.enable_rollout_routing_replay`
- **分类**：效率
- **中文解释**：文档说明：启用 rollout 阶段的 MoE router replay 支持；Router Replay 的 R3 模式要求 actor 侧 `router_replay.mode=R3`，同时 rollout 后端返回专家路由结果。
- **常见值**：${ENABLE_ROLLOUT_ROUTING_REPLAY}
- **来源环境变量**：ENABLE_ROLLOUT_ROUTING_REPLAY
- **性能影响**：机制推断：启用后 rollout 需要捕获、传递 routed experts 元数据，可能增加后端返回字段、内存和序列化开销；收益是支持 MoE 路由回放和更一致的 RL 训练路径。
- **精度影响**：文档说明：Router Replay 目标是记录并回放路由决策以提升 MoE 行为一致性；错误地与 R2 同时启用或后端不支持会直接报错，配置正确时不应主动改变奖励目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:135` actor_rollout_ref.rollout.enable_rollout_routing_replay=${ENABLE_ROLLOUT_ROUTING_REPLAY}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

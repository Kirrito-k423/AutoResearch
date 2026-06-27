# ENABLE_ROLLOUT_ROUTING_REPLAY

- **参数名**：`ENABLE_ROLLOUT_ROUTING_REPLAY`
- **分类**：效率
- **中文解释**：文档说明：控制 `actor_rollout_ref.rollout.enable_rollout_routing_replay` 的环境变量；Router Replay 的 R3 模式要求 actor 侧设为 `R3`，同时 rollout 侧启用路由重放，以记录并回放 MoE 推理阶段的专家路由。
- **常见值**：未提取
- **来源环境变量**：ENABLE_ROLLOUT_ROUTING_REPLAY
- **性能影响**：机制推断：启用后 rollout 需要返回/传递路由选择结果，并在训练侧重放，可能增加元数据传输、内存和实现约束；关闭则少一些路由记录开销。
- **精度影响**：文档说明：R3 可同时缓解训练-推理框架偏差和策略陈旧导致的 MoE 路由不一致，是大尺寸 MoE 训推一致性和训练稳定性的关键开关。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:16` ENABLE_ROLLOUT_ROUTING_REPLAY=${ENABLE_ROLLOUT_ROUTING_REPLAY:-}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# ROUTING_REPLAY_MODE

- **参数名**：`ROUTING_REPLAY_MODE`
- **分类**：效率
- **中文解释**：选择 MoE router replay 模式，脚本将其传给 `actor_rollout_ref.actor.megatron.router_replay.mode`；`R2` 是常规路由记录/重放，`R3` 是面向 RL rollout 的路由重放并会配合 rollout 侧 `enable_rollout_routing_replay`。
- **常见值**：R3
- **来源环境变量**：ROUTING_REPLAY_MODE
- **性能影响**：文档说明：router replay 需要记录/传递/重放 MoE 路由选择，支持多 GPU/多节点但依赖后端返回路由结果；会引入额外元数据处理，收益主要是复现性而非吞吐。
- **精度影响**：文档说明：该功能用于让 MoE 路由决策可记录和重放，提升训练运行间一致性；它不改变优化目标，但错误模式或后端不支持会导致路由不一致或运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:15` ROUTING_REPLAY_MODE=${ROUTING_REPLAY_MODE:-R3}        # R2 | R3

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

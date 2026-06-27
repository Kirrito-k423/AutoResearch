# actor_rollout_ref.actor.megatron.router_replay.mode

- **参数名**：`actor_rollout_ref.actor.megatron.router_replay.mode`
- **分类**：效率
- **中文解释**：文档说明：Megatron Actor 的 Router Replay 模式开关，用于 MoE 路由重放。示例 README 给出可选 `disabled`、`R2`、`R3`；`R2` 记录/重放 Actor 侧路由，`R3` 需要同时开启 rollout 路由结果返回并与 `actor_rollout_ref.rollout.enable_rollout_routing_replay=True` 配合。
- **常见值**：R3
- **来源环境变量**：ROUTING_REPLAY_MODE
- **性能影响**：文档说明：Router Replay 会记录或复用 MoE 路由选择，增加路由数据传递/存储和后端兼容要求；R3 还依赖 rollout backend 返回 router selection，端到端开销与后端实现相关。
- **精度影响**：机制推断：目的是让训练/回放阶段使用一致路由，降低 rollout 与 actor 更新之间的路由漂移；模式配置错误可能导致路由不一致、MoE 训练信号偏移或直接触发兼容性检查。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:111` actor_rollout_ref.actor.megatron.router_replay.mode=${ROUTING_REPLAY_MODE}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

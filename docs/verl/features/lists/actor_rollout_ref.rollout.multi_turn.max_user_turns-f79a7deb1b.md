# actor_rollout_ref.rollout.multi_turn.max_user_turns

- **参数名**：`actor_rollout_ref.rollout.multi_turn.max_user_turns`
- **分类**：效率
- **中文解释**：文档说明：多轮 rollout/工具调用中的最大用户轮数；参数表说明默认 `null`，fully_async multi-turn 示例会设置该字段限制交互轮次。
- **常见值**：1
- **来源环境变量**：无
- **性能影响**：机制推断：上限越大，单条样本可能产生更多轮对话、工具调用和 token，rollout 时间、KV cache、队列占用随之上升；较小上限可控成本但可能提前截断交互。
- **精度影响**：机制推断：对需要工具调用或多轮推理的任务，允许更多用户轮可能提高完成率；上限过低会截断轨迹并削弱奖励信号，单轮任务通常不受直接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:88` actor_rollout_ref.rollout.multi_turn.max_user_turns=1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

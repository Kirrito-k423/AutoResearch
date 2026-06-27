# actor_rollout_ref.rollout.multi_turn.tool_config_path

- **参数名**：`actor_rollout_ref.rollout.multi_turn.tool_config_path`
- **分类**：配置
- **中文解释**：多轮/工具调用 rollout 的工具配置文件路径；Skypilot multiturn 示例把它指向 GSM8K tool config，用于声明可用工具及调用设置。
- **常见值**："$PROJECT_DIR/examples/sglang_multiturn/config/tool_config/gsm8k_tool_config.yaml"
- **来源环境变量**：无
- **性能影响**：机制推断：启用工具配置后，rollout 可能产生工具调用、等待外部执行或多轮交互，端到端延迟和并发压力取决于工具实现。
- **精度影响**：机制推断：工具集合和响应截断策略会改变 agent 可获得的信息与动作空间，进而影响多轮任务成功率；路径错误会导致工具不可用。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:87` actor_rollout_ref.rollout.multi_turn.tool_config_path="$PROJECT_DIR/examples/sglang_multiturn/config/tool_config/gsm8k_tool_config.yaml" \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

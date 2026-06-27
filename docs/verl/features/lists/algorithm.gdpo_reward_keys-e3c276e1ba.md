# algorithm.gdpo_reward_keys

- **参数名**：`algorithm.gdpo_reward_keys`
- **分类**：算法
- **中文解释**：GDPO 多奖励训练要聚合的 reward component 名称列表；示例用 `["accuracy_reward", "format_reward"]`，这些 key 必须由自定义 `compute_score` 返回。
- **常见值**：'["accuracy_reward", "format_reward"]'
- **来源环境变量**：无
- **性能影响**：机制推断：列表聚合本身开销很小；若 key 对应的 reward 计算需要额外解析、模型调用或沙箱执行，则会增加 reward 阶段延迟。
- **精度影响**：文档说明：GDPO README 将该参数列为 key flag，源码要求 GDPO 必须提供各 reward component key；选择哪些奖励参与聚合会直接改变优化目标和 rubric 权衡。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh:40` +algorithm.gdpo_reward_keys='["accuracy_reward", "format_reward"]'

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

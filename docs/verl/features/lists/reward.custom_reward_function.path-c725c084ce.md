# reward.custom_reward_function.path

- **参数名**：`reward.custom_reward_function.path`
- **分类**：配置
- **中文解释**：自定义奖励函数所在 Python 文件路径；Verl 会动态导入该文件中的指定函数，未设置时使用内置 `reward_score` 里的预实现奖励函数。
- **常见值**："$REPO_ROOT/verl/utils/reward_score/rlla.py"
- **来源环境变量**：无
- **性能影响**：文档说明：自定义奖励函数会在 reward 计算阶段执行；函数文件中的实现若包含复杂解析、外部 API、模型调用或较慢 I/O，会增加 reward 计算延迟并降低 RL step 吞吐。
- **精度影响**：机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh:85` reward.custom_reward_function.path="$REPO_ROOT/verl/utils/reward_score/rlla.py"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

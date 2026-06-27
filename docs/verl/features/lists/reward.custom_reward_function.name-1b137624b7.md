# reward.custom_reward_function.name

- **参数名**：`reward.custom_reward_function.name`
- **分类**：配置
- **中文解释**：自定义奖励文件中的函数名；默认通常为 `compute_score`，当同一 Python 文件包含多个奖励函数时，可通过该参数选择本次实验要调用的评分函数。
- **常见值**：compute_score
- **来源环境变量**：无
- **性能影响**：文档说明：自定义奖励函数会在 reward 计算阶段执行；所选函数若包含复杂解析、外部 API、模型调用或较慢 I/O，会增加 reward 计算延迟并降低 RL step 吞吐。
- **精度影响**：机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh:86` reward.custom_reward_function.name=compute_score

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

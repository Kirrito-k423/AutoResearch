# VAL_TEMPERATURE

- **参数名**：`VAL_TEMPERATURE`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `actor_rollout_ref.rollout.val_kwargs.temperature`，控制验证 rollout 的采样温度；官方 Best Practices 建议验证时设置 `temperature > 0` 以避免重复思维链，实用起点为 1.0。
- **常见值**：1.0
- **来源环境变量**：VAL_TEMPERATURE
- **性能影响**：机制推断：温度缩放本身开销很小；但会改变输出长度和采样路径，可能间接影响验证耗时。
- **精度影响**：文档说明：直接改变验证采样分布和指标方差；温度过低更确定但可能重复，过高更多样但结果波动更大。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:70` val_temperature=${VAL_TEMPERATURE:-1.0}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

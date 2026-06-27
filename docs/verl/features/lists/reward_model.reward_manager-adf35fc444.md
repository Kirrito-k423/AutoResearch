# reward_model.reward_manager

- **参数名**：`reward_model.reward_manager`
- **分类**：算法
- **中文解释**：文档说明：选择 reward manager，即规则奖励的聚合与处理策略；官方配置说明中 `dapo` 用于 DAPO，`naive` 用于 GRPO，`prime` 可用于并行验证场景。
- **常见值**：dapo
- **来源环境变量**：无
- **性能影响**：文档说明：不同 reward manager 的奖励计算和验证方式不同；例如 `prime` 可并行验证，`dapo` 会额外处理 overlong penalty，可能影响 reward 端吞吐。
- **精度影响**：文档说明：该参数定义奖励聚合语义，`dapo` 会包含 DAPO 风格长度惩罚等逻辑，直接改变 RL 训练信号。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:126` reward_model.reward_manager=dapo \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:111` reward_model.reward_manager=dapo
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:107` reward_model.reward_manager=dapo

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

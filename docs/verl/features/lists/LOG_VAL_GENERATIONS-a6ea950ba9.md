# LOG_VAL_GENERATIONS

- **参数名**：`LOG_VAL_GENERATIONS`
- **分类**：效率
- **中文解释**：文档说明：验证阶段写入日志的生成样本数量，示例将 `LOG_VAL_GENERATIONS` 写入 `trainer.log_val_generations`；常用于在 console/wandb 中抽样查看模型输出。
- **常见值**：10
- **来源环境变量**：LOG_VAL_GENERATIONS
- **性能影响**：文档说明：增加该值会增加日志序列化、传输和存储量；机制推断：通常不增加验证生成总量，只影响保存/展示的样本数量。
- **精度影响**：机制推断：只改变可观测日志，不改变训练目标或验证指标计算；更多样本有助于人工发现模式崩塌、乱码或格式错误。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:73` log_val_generations=${LOG_VAL_GENERATIONS:-10}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

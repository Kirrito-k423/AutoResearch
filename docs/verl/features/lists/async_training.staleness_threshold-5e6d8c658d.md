# async_training.staleness_threshold

- **参数名**：`async_training.staleness_threshold`
- **分类**：效率
- **中文解释**：文档说明：fully_async_policy 允许使用陈旧样本的阈值；源码要求非负，并用 `(staleness_threshold + 1) * trigger_parameter_sync_step` 参与最大待处理样本数计算。
- **常见值**：0.5
- **来源环境变量**：STALENESS_THRESHOLD
- **性能影响**：文档说明：官方 staleness 消融显示阈值越大，异步流水线最终收益越明显，但响应长度变化可能带来训练不稳定，需要结合资源和任务调参。
- **精度影响**：文档说明：stale samples 会让训练更偏 off-policy；官方 7B 实验称未显著影响结果，但阈值过大可能让样本与当前策略差距增大，影响稳定性和最终指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:135` async_training.staleness_threshold=${staleness_threshold} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

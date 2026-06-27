# STALENESS_THRESHOLD

- **参数名**：`STALENESS_THRESHOLD`
- **分类**：效率
- **中文解释**：控制 fully async 训练中的 `async_training.staleness_threshold`，表示允许 Trainer 使用旧参数生成样本的最大比例；0 近似同步训练，大于 0 则允许异步 stale samples。
- **常见值**：0.5
- **来源环境变量**：STALENESS_THRESHOLD
- **性能影响**：文档说明：fully async 文档说明该值大于 0 时 rollout 可继续生产并减少同步等待，提升流水线利用率；过高会让更多旧样本进入训练。
- **精度影响**：文档说明：官方文档明确提醒 `staleness_threshold` 过高会使用更多旧样本、影响模型表现，并建议小于 1；0 更接近 on-policy，但吞吐收益较小。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:41` staleness_threshold=${STALENESS_THRESHOLD:-0.5}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

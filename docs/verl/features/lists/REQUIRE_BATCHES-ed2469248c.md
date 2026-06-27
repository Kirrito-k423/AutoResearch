# REQUIRE_BATCHES

- **参数名**：`REQUIRE_BATCHES`
- **分类**：效率
- **中文解释**：文档说明：FullyAsyncTrainer 每次从队列取多少个 `ppo_mini_batch_size` 的样本后执行训练；官方 fully async 文档称其用于控制流式分发中的样本数量。
- **常见值**：1
- **来源环境变量**：REQUIRE_BATCHES
- **性能影响**：文档说明：`require_batches` 越接近 1 越接近纯 streaming，训练气泡更小；较大值会一次等待更多样本，可能提高批处理饱满度但增加等待和队列压力。
- **精度影响**：文档说明：它会改变每次本地更新消费的样本窗口，并与 `trigger_parameter_sync_step`、`staleness_threshold` 共同决定样本新鲜度；过大可能增加 off-policy/stale sample 影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:43` require_batches=${REQUIRE_BATCHES:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

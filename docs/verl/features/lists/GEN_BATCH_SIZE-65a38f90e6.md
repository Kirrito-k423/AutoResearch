# GEN_BATCH_SIZE

- **参数名**：`GEN_BATCH_SIZE`
- **分类**：效率
- **中文解释**：文档说明：Fully Async 策略下的生成 batch 大小环境变量，示例将它写入 `data.gen_batch_size`；官方 fully async 文档说明该策略使用 streaming sample production，默认值为 1。
- **常见值**：1
- **来源环境变量**：GEN_BATCH_SIZE
- **性能影响**：文档说明：在 fully async 中 `data.train_batch_size` 不生效而 `data.gen_batch_size` 控制流式样本生产粒度；增大可能提高 rollouter 产样批量效率，但会提高瞬时显存/队列压力。
- **精度影响**：机制推断：生成批量本身不是奖励或优化目标；若改变样本生产节奏、队列陈旧度或一次训练可见样本组成，可能间接影响异步训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:25` gen_batch_size=${GEN_BATCH_SIZE:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

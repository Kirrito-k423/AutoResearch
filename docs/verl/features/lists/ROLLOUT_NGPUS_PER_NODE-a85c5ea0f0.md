# ROLLOUT_NGPUS_PER_NODE

- **参数名**：`ROLLOUT_NGPUS_PER_NODE`
- **分类**：效率
- **中文解释**：文档说明：fully async 示例环境变量，写入 `rollout.n_gpus_per_node`，控制异步 rollout 资源池每个节点分配多少 GPU，而不是每个 prompt 的响应数。
- **常见值**：4
- **来源环境变量**：ROLLOUT_NGPUS_PER_NODE
- **性能影响**：文档说明：fully async 文档将 `rollout.n_gpus_per_node` 与 `rollout.nnodes` 一起用于划分 rollout 资源；增大可提升生成服务容量和并发，但会占用更多 GPU 并改变训练/rollout 资源配比。
- **精度影响**：机制推断：资源规模本身不改变采样分布；若资源不足造成队列堆积、超时或异步策略滞后，可能间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:21` ROLLOUT_NGPUS_PER_NODE=${ROLLOUT_NGPUS_PER_NODE:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

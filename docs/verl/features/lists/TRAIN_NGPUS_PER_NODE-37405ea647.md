# TRAIN_NGPUS_PER_NODE

- **参数名**：`TRAIN_NGPUS_PER_NODE`
- **分类**：效率
- **中文解释**：控制 fully async split-placement 中 Trainer 组每个节点使用的 GPU 数，映射到 `trainer.n_gpus_per_node`；与 `TRAIN_NNODES` 一起决定训练侧资源总量。
- **常见值**：4
- **来源环境变量**：TRAIN_NGPUS_PER_NODE
- **性能影响**：文档说明：fully async 示例把训练和 rollout 资源分组，官方多节点配置用 `trainer.n_gpus_per_node` 与 `trainer.nnodes` 定义训练资源；增加每节点 GPU 可提高并行容量，但也增加节点内通信和并行策略约束。
- **精度影响**：机制推断：GPU 数本身不改变损失函数；若同时改变全局 batch、并行切分、随机归约顺序或异步新鲜度，结果可能间接变化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:19` TRAIN_NGPUS_PER_NODE=${TRAIN_NGPUS_PER_NODE:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# TRAIN_NNODES

- **参数名**：`TRAIN_NNODES`
- **分类**：效率
- **中文解释**：控制 fully async split-placement 中 Trainer 组使用的节点数，映射到 `trainer.nnodes`；与 `TRAIN_NGPUS_PER_NODE` 一起决定训练侧资源总量。
- **常见值**：1
- **来源环境变量**：TRAIN_NNODES
- **性能影响**：文档说明：fully async 脚本说明可用 `TRAIN_NNODES`/`ROLLOUT_NNODES` 扩展为真正多节点运行；训练节点数增加可扩大训练侧并行资源，但带来 Ray 调度、跨节点通信和同步开销。
- **精度影响**：机制推断：节点数本身不改变算法目标；若伴随全局 batch、并行策略、同步频率或随机归约顺序变化，会间接影响训练轨迹和可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:18` TRAIN_NNODES=${TRAIN_NNODES:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

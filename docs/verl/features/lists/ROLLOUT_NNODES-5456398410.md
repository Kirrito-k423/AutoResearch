# ROLLOUT_NNODES

- **参数名**：`ROLLOUT_NNODES`
- **分类**：效率
- **中文解释**：文档说明：fully async 示例环境变量，写入 `rollout.nnodes`，控制异步 rollout 资源池使用的节点数，而不是每个 prompt 的响应数。
- **常见值**：1
- **来源环境变量**：ROLLOUT_NNODES
- **性能影响**：文档说明：fully async 文档将 `rollout.nnodes` 与 `rollout.n_gpus_per_node` 一起用于设置 rollout 资源规模；节点数越多生成服务容量越高，但跨节点调度、网络和成本也增加。
- **精度影响**：机制推断：资源节点数本身不改变算法目标；若扩容/缩容改变异步等待时间、策略滞后或失败重试，可能间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:20` ROLLOUT_NNODES=${ROLLOUT_NNODES:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

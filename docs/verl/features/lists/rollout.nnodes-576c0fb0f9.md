# rollout.nnodes

- **参数名**：`rollout.nnodes`
- **分类**：算法
- **中文解释**：fully-async/one-step-off 场景下 rollout 资源池使用的节点数；与 `rollout.n_gpus_per_node` 共同决定生成侧独立扩展规模。
- **常见值**：1
- **来源环境变量**：ROLLOUT_NNODES
- **性能影响**：文档说明：one-step-off 文档说明可通过 `trainer.nnodes` 与 `rollout.nnodes` 独立调节训练/rollout 并行度；增加 rollout 节点可提升生成吞吐，但带来 Ray 调度、跨节点网络和资源规划开销。
- **精度影响**：机制推断：节点数不直接改变算法；若多节点调度改变全局 batch、样本到达顺序、失败重试或随机性，才可能造成间接差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:133` rollout.nnodes=${ROLLOUT_NNODES} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

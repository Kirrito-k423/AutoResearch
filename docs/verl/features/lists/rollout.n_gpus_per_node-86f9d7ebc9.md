# rollout.n_gpus_per_node

- **参数名**：`rollout.n_gpus_per_node`
- **分类**：算法
- **中文解释**：fully-async/one-step-off 场景下 rollout 资源池每个节点分配的 GPU 数；与 `rollout.nnodes` 一起决定生成侧资源规模。
- **常见值**：4
- **来源环境变量**：ROLLOUT_NGPUS_PER_NODE
- **性能影响**：文档说明：one-step-off 文档建议按训练/rollout 阶段耗时动态调整 `rollout.n_gpus_per_node`；增加 rollout GPU 可提升生成吞吐、减少训练等待，但会占用更多设备并可能改变资源放置约束。
- **精度影响**：机制推断：资源数本身不改变采样分布或训练目标；只有当资源调整伴随 batch、随机种子、超时或部分 rollout 策略变化时才可能间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:134` rollout.n_gpus_per_node=${ROLLOUT_NGPUS_PER_NODE} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

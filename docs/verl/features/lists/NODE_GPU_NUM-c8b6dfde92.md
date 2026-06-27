# NODE_GPU_NUM

- **参数名**：`NODE_GPU_NUM`
- **分类**：效率
- **中文解释**：机制推断：示例中的单节点设备数参数，写入 `trainer.n_gpus_per_node`，表示每个训练节点参与任务的 GPU/NPU 数量。
- **常见值**：8
- **来源环境变量**：NODE_GPU_NUM
- **性能影响**：机制推断：增大每节点设备数可提高单节点吞吐和并行规模，但也增加节点内通信和显存分配复杂度；与真实设备数不一致会导致调度或初始化失败。
- **精度影响**：机制推断：设备数本身不改变模型数学定义；若有效 world size、batch size 或并行切分随之变化，可能间接影响梯度统计与可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:66` NODE_GPU_NUM=${NODE_GPU_NUM:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

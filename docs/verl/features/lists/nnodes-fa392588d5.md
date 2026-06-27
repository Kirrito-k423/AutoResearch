# nnodes

- **参数名**：`nnodes`
- **分类**：效率
- **中文解释**：示例脚本中的分布式节点数，通常与每节点 GPU 数一起决定训练或 rollout 任务的总资源规模。
- **常见值**：2、8
- **来源环境变量**：nnodes
- **性能影响**：机制推断：增大节点数可提供更多 GPU 并行度和显存容量，适合大模型/长上下文；同时会增加跨节点通信、Ray 调度和故障恢复成本。
- **精度影响**：机制推断：节点数本身不改变算法目标；若同时改变全局 batch、并行划分或随机种子，才可能间接影响收敛轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:22` nnodes=${nnodes:-8}
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:13` nnodes=${nnodes:-2}
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:19` nnodes=${nnodes:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

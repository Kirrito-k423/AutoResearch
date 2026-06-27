# --nproc-per-node

- **参数名**：`--nproc-per-node`
- **分类**：效率
- **中文解释**：机制推断：`torchrun` 每个节点启动的本地训练进程数，通常与本机可用 GPU/NPU 数量一致；示例中用 `NUM_TRAINERS` 控制。
- **常见值**：${NUM_TRAINERS:-8}
- **来源环境变量**：无
- **性能影响**：机制推断：决定单节点并行进程和设备使用规模；增大可提升并行吞吐和显存总量，但也增加通信与调度开销，超过设备数会失败或严重争用。
- **精度影响**：机制推断：若全局 batch、随机种子和并行归一化保持一致，通常不直接改变精度；若进程数变化连带改变有效 batch 或数据切分，则会影响训练动态。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:79` torchrun --standalone --nnodes=1 --nproc-per-node=${NUM_TRAINERS:-8} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

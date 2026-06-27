# data.num_workers

- **参数名**：`data.num_workers`
- **分类**：效率
- **中文解释**：源码说明：SFT DataLoader 的 worker 数，`StatefulDataLoader(..., num_workers=config.data.num_workers)` 使用它并行加载/整理样本；示例设置为 0 表示主进程加载。
- **常见值**：0
- **来源环境变量**：无
- **性能影响**：机制推断：更多 worker 可提升数据读取、模板处理和 collate 并行度，但会增加 CPU、内存和进程调度开销；0 更简单稳定但可能让数据加载成为瓶颈。
- **精度影响**：机制推断：不直接改变训练目标或样本内容；只有在 worker 随机性、数据顺序、超时或加载失败导致样本口径变化时才会间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:88` data.num_workers=0 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

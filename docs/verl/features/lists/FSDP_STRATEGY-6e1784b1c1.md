# FSDP_STRATEGY

- **参数名**：`FSDP_STRATEGY`
- **分类**：效率
- **中文解释**：文档说明：SFT/FSDP engine 的策略选择变量，示例把 `FSDP_STRATEGY` 写入 `engine.strategy`；常见值 `fsdp2` 表示使用 PyTorch FSDP2 后端。
- **常见值**："fsdp2"
- **来源环境变量**：FSDP_STRATEGY
- **性能影响**：文档说明：Verl 性能文档称 FSDP2 相比 FSDP1 平均 GPU 显存约低 7%、BF16 吞吐约提升 1.5%，并改善 DTensor/逐参数分片组合性；实际仍取决于模型和硬件。
- **精度影响**：机制推断：策略选择主要影响并行和内存实现，通常不作为精度超参；不同分片/归约路径可能带来轻微数值差异，也可能通过能否训练更大模型间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:22` FSDP_STRATEGY=${FSDP_STRATEGY:-"fsdp2"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

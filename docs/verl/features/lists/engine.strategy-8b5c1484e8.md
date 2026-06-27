# engine.strategy

- **参数名**：`engine.strategy`
- **分类**：效率
- **中文解释**：文档说明：SFT engine 使用的分布式训练策略标识；FSDP engine 支持 `fsdp`/`fsdp2`，示例通过 `FSDP_STRATEGY` 选择新版 FSDP2 路径。
- **常见值**："fsdp2"
- **来源环境变量**：FSDP_STRATEGY
- **性能影响**：机制推断：策略决定 FSDP 实现、分片/通信/状态管理路径；`fsdp2` 可能改善新版 PyTorch FSDP 的调度和显存行为，但也更依赖当前 PyTorch/硬件兼容性。
- **精度影响**：机制推断：不改变算法目标；不同 FSDP 实现的归约顺序、混合精度处理和 checkpoint 恢复路径可能带来细小数值或复现差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:44` engine.strategy=${FSDP_STRATEGY} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

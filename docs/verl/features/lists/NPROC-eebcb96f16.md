# NPROC

- **参数名**：`NPROC`
- **分类**：效率
- **中文解释**：机制推断：`torchrun --nproc_per_node` 的本地进程数，通常等于单节点参与训练的 GPU 数量。
- **常见值**：8
- **来源环境变量**：NPROC
- **性能影响**：机制推断：进程数过低会闲置设备，过高会造成设备争用、显存竞争或通信压力；正确值决定单节点并行利用率。
- **精度影响**：机制推断：本身不改变优化目标；若改变 world size 后没有同步调整 batch/学习率/梯度累积，可能间接改变收敛轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:11` NPROC=${NPROC:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

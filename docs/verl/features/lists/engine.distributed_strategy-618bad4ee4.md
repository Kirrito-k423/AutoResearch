# engine.distributed_strategy

- **参数名**：`engine.distributed_strategy`
- **分类**：效率
- **中文解释**：选择 AutoModel engine 的分布式训练策略；官方配置注释给出可选方向包括 `fsdp2`、`megatron_fsdp`、`ddp`，examples 使用 `fsdp2`。
- **常见值**：fsdp2
- **来源环境变量**：无
- **性能影响**：文档说明：该策略决定参数分片、梯度同步和并行后端；`fsdp2` 通常用通信换显存，`ddp` 实现简单但副本显存更高，Megatron 相关策略更适合大模型并行。
- **精度影响**：机制推断：策略本身不改变损失函数；不同后端的规约顺序、混合精度和 checkpoint/resume 行为可能造成轻微数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:32` engine.distributed_strategy=fsdp2 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:35` engine.distributed_strategy=fsdp2 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

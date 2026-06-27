# optim.min_lr_ratio

- **参数名**：`optim.min_lr_ratio`
- **分类**：算法
- **中文解释**：学习率衰减后的最低学习率比例，通常用于 cosine scheduler；最低学习率约等于初始学习率乘以该比例。
- **常见值**：0.01、0.1
- **来源环境变量**：无
- **性能影响**：机制推断：不直接改变单步吞吐；较高的最低学习率可能保持更强更新但增加后期震荡，较低值可能更平稳但收敛更慢。
- **精度影响**：文档说明：Verl 配置和源码说明该值控制 decay 后 `min_lr = lr * min_lr_ratio`；它会影响训练后期收敛、稳定性和最终模型质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:41` optim.min_lr_ratio=0.1 \
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:45` optim.min_lr_ratio=0.1 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:59` optim.min_lr_ratio=0.01 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# optim.lr_warmup_steps_ratio

- **参数名**：`optim.lr_warmup_steps_ratio`
- **分类**：算法
- **中文解释**：文档说明：SFT optimizer 中的学习率 warmup 步数占总训练步数比例；当显式 warmup steps 未设置或小于等于 0 时，用总步数乘该比例得到 warmup 阶段长度。
- **常见值**：0.01、0.1、0.2
- **来源环境变量**：无
- **性能影响**：机制推断：通常不改变单步算子吞吐；比例越大，学习率达到目标值越晚，可能需要更多训练步才能达到同等收敛进度。
- **精度影响**：文档说明：该参数控制 warmup 长度，影响优化稳定性和收敛速度；过短可能早期震荡，过长可能收敛偏慢或欠训练。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:37` optim.lr_warmup_steps_ratio=0.01 \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:52` optim.lr_warmup_steps_ratio=0.01 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:43` optim.lr_warmup_steps_ratio=0.2
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:40` optim.lr_warmup_steps_ratio=0.2 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:54` optim.lr_warmup_steps_ratio=0.1 \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

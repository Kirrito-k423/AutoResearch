# optim.weight_decay

- **参数名**：`optim.weight_decay`
- **分类**：效率
- **中文解释**：文档说明：通用优化器权重衰减系数；Verl 配置文档将其定义为 optimizer weight decay，Ascend 参数表说明其用于抑制过拟合。
- **常见值**：0、0.1
- **来源环境变量**：无
- **性能影响**：机制推断：几乎不影响单步吞吐，只增加优化器更新中的常规正则项；主要影响收敛路径而非系统效率。
- **精度影响**：文档说明：权重衰减用于正则化和防止过拟合；过高可能欠拟合，过低可能泛化或稳定性不足。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:38` optim.weight_decay=0.1 \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:53` optim.weight_decay=0.1 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:44` optim.weight_decay=0.1
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:41` optim.weight_decay=0.1 \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:45` optim.weight_decay=0.1

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

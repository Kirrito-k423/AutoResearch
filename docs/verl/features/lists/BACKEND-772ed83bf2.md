# BACKEND

- **参数名**：`BACKEND`
- **分类**：效率
- **中文解释**：文档说明：SFT 示例中选择训练引擎的环境变量，常见值为 `fsdp` 或 `megatron`，随后被写入 `engine=${backend}` 和 `optim=${backend}`。
- **常见值**：fsdp、megatron
- **来源环境变量**：BACKEND
- **性能影响**：文档说明：Verl 安装文档建议 FSDP/FSDP2 用于原型和通用训练，Megatron 面向更强扩展性；切换 backend 会改变并行策略、通信模式和可训练模型规模。
- **精度影响**：机制推断：理论目标通常不变，但不同 backend 的混合精度、重计算、并行切分和 kernel 实现可能带来细小数值差异，影响严格复现。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:12` backend=${BACKEND:-fsdp}
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:18` backend=${BACKEND:-megatron}
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:17` backend=${BACKEND:-megatron}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

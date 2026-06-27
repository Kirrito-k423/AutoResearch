# optim.betas

- **参数名**：`optim.betas`
- **分类**：效率
- **中文解释**：文档说明：优化器 Adam/AdamW 的一阶、二阶动量系数；Verl 参数表将 `optim.betas` 解释为 Adam 优化器动量系数，examples 常用 `[0.9, 0.95]`。
- **常见值**："[0.9,0.95]"、'[0.9,0.95]'、[0.9,0.95]"
- **来源环境变量**：无
- **性能影响**：机制推断：不明显改变单步吞吐或显存规模；主要影响优化器状态更新的数值轨迹和达到目标质量所需步数。
- **精度影响**：机制推断：改变梯度一阶/二阶矩的平滑程度，进而影响收敛速度、震荡和最终稳定性；过小或过大都可能使 RL 微调更不稳。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:39` optim.betas="[0.9,0.95]" \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:54` optim.betas="[0.9,0.95]" \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:45` "optim.betas=[0.9,0.95]"
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:42` optim.betas='[0.9,0.95]' \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:46` optim.betas="[0.9,0.95]"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

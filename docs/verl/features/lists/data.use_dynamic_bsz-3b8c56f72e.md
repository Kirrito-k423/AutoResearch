# data.use_dynamic_bsz

- **参数名**：`data.use_dynamic_bsz`
- **分类**：效率
- **中文解释**：文档说明：SFT 数据/训练侧是否启用动态 batch size；启用后按 token 数组织 batch，使每次 forward 处理相近数量的 token，而不是固定样本数。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：Verl performance tuning 明确说动态 batch 可显著提升训练效率并降低显存使用；需要配合 `max_token_len_per_gpu` 调 token 上限。
- **精度影响**：机制推断：不改变样本和损失定义；但 batch packing、梯度累积边界或 token 上限设置不当时，会影响有效 batch 与训练稳定性。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:86` data.use_dynamic_bsz=True \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:27` data.use_dynamic_bsz=True
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:24` data.use_dynamic_bsz=True \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:81` data.use_dynamic_bsz=True \
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:85` data.use_dynamic_bsz=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

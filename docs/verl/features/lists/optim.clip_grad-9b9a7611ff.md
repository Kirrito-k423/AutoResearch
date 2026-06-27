# optim.clip_grad

- **参数名**：`optim.clip_grad`
- **分类**：算法
- **中文解释**：文档说明：通用优化器梯度裁剪阈值；Verl 参数表和 best practices 都将 `clip_grad` 解释为 gradient clipping value/threshold，常见值为 1.0。
- **常见值**：1.0
- **来源环境变量**：无
- **性能影响**：机制推断：会增加很小的梯度范数计算/裁剪开销，通常不是吞吐瓶颈。
- **精度影响**：机制推断：限制过大梯度可降低训练震荡和爆炸风险；阈值过低会压制有效更新，过高则保护不足。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:40` optim.clip_grad=1.0 \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:55` optim.clip_grad=1.0 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:46` optim.clip_grad=1.0
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:43` optim.clip_grad=1.0 \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:47` optim.clip_grad=1.0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

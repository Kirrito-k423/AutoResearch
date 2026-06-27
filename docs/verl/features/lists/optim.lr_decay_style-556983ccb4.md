# optim.lr_decay_style

- **参数名**：`optim.lr_decay_style`
- **分类**：算法
- **中文解释**：文档说明：Megatron/MCore optimizer 的学习率衰减策略；官方配置支持 `constant`、`linear`、`cosine`、`inverse_square_root` 等，examples 中常用 `cosine`。
- **常见值**：cosine
- **来源环境变量**：无
- **性能影响**：机制推断：不直接改变每 step 计算量；但会影响达到目标效果所需 step 数、稳定训练窗口和是否需要更长/更短调参周期。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:57` optim.lr_decay_style=cosine \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:48` optim.lr_decay_style=cosine
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:49` optim.lr_decay_style=cosine
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:59` optim.lr_decay_style=cosine \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:106` optim.lr_decay_style=cosine \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

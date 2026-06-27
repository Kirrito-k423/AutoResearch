# optim.lr_warmup_init

- **参数名**：`optim.lr_warmup_init`
- **分类**：算法
- **中文解释**：文档说明：Megatron/MCore optimizer warmup 开始时的初始学习率，随后在 warmup steps 内升到主学习率；examples 中常设为 `0`。
- **常见值**：0
- **来源环境变量**：无
- **性能影响**：机制推断：不改变单 step 计算成本；较保守的 warmup 初值可能需要更多 step 才达到有效学习率，但可降低早期不稳定导致的重跑成本。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:56` optim.lr_warmup_init=0 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:47` optim.lr_warmup_init=0
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:48` optim.lr_warmup_init=0
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:58` optim.lr_warmup_init=0 \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:105` optim.lr_warmup_init=0 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

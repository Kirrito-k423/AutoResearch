# optim.min_lr

- **参数名**：`optim.min_lr`
- **分类**：算法
- **中文解释**：文档说明：Megatron/MCore optimizer 学习率衰减后的下限；调度器会在 decay 过程中不低于该最小学习率，examples 常用 `1e-6` 或 `2e-6`。
- **常见值**："1e-6"、1e-6、2e-6
- **来源环境变量**：MIN_LR
- **性能影响**：机制推断：不改变每 step 计算量；会影响后期继续训练的有效更新幅度，进而影响达到收敛/停止标准所需时间。
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

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:58` optim.min_lr=2e-6 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:49` optim.min_lr=1e-6
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:50` optim.min_lr=2e-6
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:53` optim.min_lr=${MINLR} \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:100` optim.min_lr=${MIN_LR} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

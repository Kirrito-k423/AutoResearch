# optim.lr

- **参数名**：`optim.lr`
- **分类**：算法
- **中文解释**：文档说明：优化器学习率，控制参数更新步长；在 actor 侧官方 Best Practices 建议从 `1e-5` 或 `1e-6` 附近开始。
- **常见值**："1e-5"、1e-4、1e-5、2e-5
- **来源环境变量**：LR
- **性能影响**：机制推断：学习率本身不改变单步算子成本；但过大导致不稳定/回滚、过小需要更多 step，都会改变达标总耗时。
- **精度影响**：文档说明：直接影响收敛速度和稳定性；过大可能发散或 reward hacking，过小可能欠拟合或训练进展慢。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：13
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:36` optim.lr=2e-5 \
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:51` optim.lr=2e-5 \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:42` optim.lr=1e-5
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:39` optim.lr=1e-5 \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:23` optim.lr=1e-4 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

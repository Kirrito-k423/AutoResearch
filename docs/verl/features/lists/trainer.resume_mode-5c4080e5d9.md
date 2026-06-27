# trainer.resume_mode

- **参数名**：`trainer.resume_mode`
- **分类**：效率
- **中文解释**：文档说明：控制训练从 checkpoint 恢复的模式，支持 `disable`、`auto`、`resume_path`；`auto` 会从 `default_local_dir` 中自动寻找最新 checkpoint，`disable` 表示从头训练。
- **常见值**：auto、disable
- **来源环境变量**：RESUME_MODE
- **性能影响**：文档说明：恢复模式本身不改变每步吞吐；`auto`/`resume_path` 会增加启动时查找和加载 checkpoint 的时间，但可避免已完成步骤重跑。
- **精度影响**：机制推断：正确恢复可延续 optimizer、scheduler 和 global step 状态；错误路径或强制 `disable` 会改变训练连续性和随机过程，影响可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:151` trainer.resume_mode=auto \
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:175` trainer.resume_mode=auto
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:155` trainer.resume_mode=auto
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:152` trainer.resume_mode=auto
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:184` trainer.resume_mode=auto

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# SP_SIZE

- **参数名**：`SP_SIZE`
- **分类**：效率
- **中文解释**：文档说明：示例将 `SP_SIZE` 映射到 Ulysses sequence parallel size（actor/ref 或 SFT engine），用于把长序列训练切到多个设备；`>1` 常用于长上下文场景降低单卡序列维度的显存压力。
- **常见值**：1、2、4、8
- **来源环境变量**：SP_SIZE
- **性能影响**：文档说明：`ulysses_sequence_parallel_size>1` 支持长上下文训练，长序列（如 >32k）场景通常还需要降低 micro batch 或 token 上限以避免 OOM；机制上可降低单卡激活/注意力压力，但会增加跨卡通信。
- **精度影响**：机制推断：等价并行配置本身不改变优化目标；但并行度、max token 或 micro batch 调整不当可能导致截断、OOM 或有效 batch 变化，间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:26` SP_SIZE=${SP_SIZE:-}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:53` sp_size=${SP_SIZE:-1}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:70` sp_size=${SP_SIZE:-4}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:46` sp_size=${SP_SIZE:-8}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:17` SP_SIZE=${SP_SIZE:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

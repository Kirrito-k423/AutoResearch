# EXPERIMENT_NAME

- **参数名**：`EXPERIMENT_NAME`
- **分类**：配置
- **中文解释**：示例脚本中的实验名环境变量，通常传入 `trainer.experiment_name`，用于日志、W&B run、trace 和 checkpoint 子目录命名。
- **常见值**：GRPO-Qwen3_5-27B、GRPO-Qwen3_5-35B、dapo_mimo_7b_mtp_fully_async、deepseek_v3_671b_vllm_megatron、glm41v_9b_function_rm、grpo_mistral13B-skyworkLlama8b-hhrlhf、gsm8k-sft-qwen2_5_0_5b、gsm8k-sft-qwen3-8b-instruct、mimo_7b_mtp_${rollout_backend、mimo_7b_mtp_sglang_megatron、minicpmo2_6_function_rm、moonlight_megatron_ep
- **来源环境变量**：EXPERIMENT_NAME
- **性能影响**：文档说明：quickstart/checkpoint 文档把 checkpoint 路径组织为 `checkpoints/${trainer.project_name}/${trainer.experiment_name}`；该命名参数通常不影响计算性能。
- **精度影响**：文档说明：实验名仅用于追踪和产物归档，不直接改变训练数据、模型或优化目标。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：63
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:49` experiment_name=${EXPERIMENT_NAME:-qwen3_30b_a3b_${LOSS_MODE}_vllm_megatron}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:32` experiment_name=${EXPERIMENT_NAME:-qwen3_8b_vllm_fsdp}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:33` experiment_name=${EXPERIMENT_NAME:-qwen3_8b_vllm_fsdp}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:36` EXPERIMENT_NAME=${EXPERIMENT_NAME:-qwen3_8b_vllm_fsdp}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:41` experiment_name=${EXPERIMENT_NAME:-qwen3_30b_a3b_vllm_megatron}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

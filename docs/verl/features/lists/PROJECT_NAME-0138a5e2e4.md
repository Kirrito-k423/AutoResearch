# PROJECT_NAME

- **参数名**：`PROJECT_NAME`
- **分类**：配置
- **中文解释**：示例脚本中的项目名环境变量，通常传入 `trainer.project_name`，作为日志、W&B project、trace 和 checkpoint 根目录的一部分。
- **常见值**：GRPO-Qwen3_5、gsm8k-sft、mtp、multiturn-sft、verl_cispo_gsm8k_math、verl_distill_geo3k、verl_distill_gsm8k_math、verl_distill_mopd_gsm8k_geo3k、verl_dppo_qwen3_moe、verl_full_hh_rlhf_examples、verl_gdpo、verl_gmpo_gsm8k_math
- **来源环境变量**：PROJECT_NAME
- **性能影响**：文档说明：quickstart/checkpoint 文档把 checkpoint 路径组织为 `checkpoints/${trainer.project_name}/${trainer.experiment_name}`；项目名本身不改变训练计算。
- **精度影响**：文档说明：项目名用于追踪和归档，不直接影响模型参数更新或评测结果。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:48` project_name=${PROJECT_NAME:-verl_dppo_qwen3_moe}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:31` project_name=${PROJECT_NAME:-verl_reinforce_plus_plus_gsm8k_math}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:32` project_name=${PROJECT_NAME:-verl_gmpo_gsm8k_math}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:35` PROJECT_NAME=${PROJECT_NAME:-verl_gspo_gsm8k_math}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:40` project_name=${PROJECT_NAME:-verl_gspo_qwen3_moe}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

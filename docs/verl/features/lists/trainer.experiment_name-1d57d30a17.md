# trainer.experiment_name

- **参数名**：`trainer.experiment_name`
- **分类**：配置
- **中文解释**：训练运行的实验名，用于 wandb/swanlab/mlflow/trackio 等日志后端标识单次 run，并参与默认 checkpoint 路径 `checkpoints/${trainer.project_name}/${trainer.experiment_name}`。
- **常见值**："${EXPERIMENT_NAME}"、"${exp_name}"、"${experiment_name}"、"ppo_clip_multi_rs"、"rloo_seq_is_pure"、$exp_name、'qwen2_7b_megatron_fsdp'、'qwen3_30b_veomni'、'qwen3_5_35b_megatron'、SFT-qwen2.5-7b-mfsdp、deepseek_v3_671b_vllm_megatron、experiment_name_gsm8k
- **来源环境变量**：EXPERIMENT_NAME、experiment_name
- **性能影响**：机制推断：仅作为日志与 checkpoint 路径标识，通常不改变训练吞吐；名称冲突或不规范主要影响归档、检索和恢复定位。
- **精度影响**：机制推断：不参与模型前向、反向或奖励计算，通常不直接影响精度；主要影响实验对比和结果追踪口径。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：93
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
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
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:126` trainer.experiment_name=${experiment_name}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:93` trainer.experiment_name=${experiment_name}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:99` trainer.experiment_name=${experiment_name}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:136` trainer.experiment_name=${EXPERIMENT_NAME}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:121` trainer.experiment_name=${experiment_name}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

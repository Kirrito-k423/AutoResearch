# trainer.project_name

- **参数名**：`trainer.project_name`
- **分类**：配置
- **中文解释**：训练项目名，用于 wandb/swanlab/mlflow/trackio 等日志系统归组实验；也参与默认 checkpoint 路径 `checkpoints/${trainer.project_name}/${trainer.experiment_name}`。
- **常见值**："${PROJECT_NAME}"、"${project_name}"、"rollout_corr_multi_rs_example"、"rollout_corr_rloo_example"、$project_name、'verl_grpo_example_gsm8k_math'、'verl_grpo_qwen3_5_35b_geo3k'、'verl_qwen3_veomni'、gsm8k-sft、hellaswag-sft、mtp、verl_cispo_gsm8k_math
- **来源环境变量**：PROJECT_NAME
- **性能影响**：机制推断：仅作为日志项目与 checkpoint 路径标识，通常不改变计算性能；命名冲突主要影响归档、权限或远端 tracking 查询。
- **精度影响**：机制推断：不进入模型训练计算，通常不直接影响精度；会影响跨 run 聚合、对比和最佳 checkpoint 选择的管理口径。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:125` trainer.project_name=${project_name}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:92` trainer.project_name=${project_name}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:98` trainer.project_name=${project_name}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:135` trainer.project_name=${PROJECT_NAME}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:120` trainer.project_name=${project_name}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

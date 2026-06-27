# PPO_MICRO_BATCH_SIZE_PER_GPU

- **参数名**：`PPO_MICRO_BATCH_SIZE_PER_GPU`
- **分类**：效率
- **中文解释**：控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。
- **常见值**：1、10、16、2、32
- **来源环境变量**：PPO_MICRO_BATCH_SIZE_PER_GPU
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：11
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_seed_oss_36b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:14` PPO_MICRO_BATCH_SIZE_PER_GPU=${PPO_MICRO_BATCH_SIZE_PER_GPU:-16}
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:11` PPO_MICRO_BATCH_SIZE_PER_GPU=${PPO_MICRO_BATCH_SIZE_PER_GPU:-10}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:23` PPO_MICRO_BATCH_SIZE_PER_GPU=${PPO_MICRO_BATCH_SIZE_PER_GPU:-10}
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:13` PPO_MICRO_BATCH_SIZE_PER_GPU=${PPO_MICRO_BATCH_SIZE_PER_GPU:-32}
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh:13` PPO_MICRO_BATCH_SIZE_PER_GPU=${PPO_MICRO_BATCH_SIZE_PER_GPU:-10}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

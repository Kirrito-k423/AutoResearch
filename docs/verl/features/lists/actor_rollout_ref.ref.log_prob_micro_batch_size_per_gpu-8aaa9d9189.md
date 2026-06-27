# actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu

- **参数名**：`actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu`
- **分类**：效率
- **中文解释**：控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。
- **常见值**：1、16、2、20、3、32、4、64、8
- **来源环境变量**：LOG_PROB_MICRO_BATCH_SIZE_PER_GPU、MICRO_BS、REF_LOG_PROB_MICRO_BATCH_SIZE_PER_GPU
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：31
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:82` actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=${LOG_PROB_MICRO_BATCH_SIZE_PER_GPU}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:150` actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=1
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:99` actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=1
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:139` actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=${LOG_PROB_MICRO_BATCH_SIZE_PER_GPU}
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:112` actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=${LOG_PROB_MICRO_BATCH_SIZE_PER_GPU}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

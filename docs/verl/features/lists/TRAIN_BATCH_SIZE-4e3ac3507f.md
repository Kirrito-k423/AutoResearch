# TRAIN_BATCH_SIZE

- **参数名**：`TRAIN_BATCH_SIZE`
- **分类**：效率
- **中文解释**：控制训练全局 batch，影响样本吞吐、梯度稳定性和单步耗时。
- **常见值**：1024、128、16、192、256、32、512、64、96
- **来源环境变量**：TRAIN_BATCH_SIZE
- **性能影响**：机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：57
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
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:26` train_batch_size=${TRAIN_BATCH_SIZE:-256}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:14` train_batch_size=${TRAIN_BATCH_SIZE:-1024}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:12` train_batch_size=${TRAIN_BATCH_SIZE:-1024}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:14` TRAIN_BATCH_SIZE=${TRAIN_BATCH_SIZE:-}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:51` train_batch_size=${TRAIN_BATCH_SIZE:-512}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# data.val_files

- **参数名**：`data.val_files`
- **分类**：配置
- **中文解释**：指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。
- **常见值**："$TEST_DATA_PATH"、"$TEST_FILE"、"$test_files"、"$val_files"、"${TEST_FILE}"、"${TRAIN_FILES}"、"${VAL_FILES}"、"['$GSM8K_TEST_FILE', '$MATH_TEST_FILE']"、"['$HOME/data/gsm8k/test.parquet', '$HOME/data/math/test.parquet']"、"['$gsm8k_test_path', '$math_test_path']"、"['$val_file']"、$DATA_DIR/test.parquet
- **来源环境变量**：TEST_FILE、VAL_FILES、test_files、test_path
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：91
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:61` data.val_files="['$val_file']"
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:48` data.val_files="$val_files"
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:49` data.val_files="$val_files"
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:86` data.val_files="['$GSM8K_TEST_FILE', '$MATH_TEST_FILE']"
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:52` data.val_files="['$val_file']"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

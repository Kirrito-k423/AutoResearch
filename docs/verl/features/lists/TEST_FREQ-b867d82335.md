# TEST_FREQ

- **参数名**：`TEST_FREQ`
- **分类**：配置
- **中文解释**：示例脚本中的验证/测试频率环境变量，通常传入 `trainer.test_freq` 控制每隔多少 step 计算验证指标。
- **常见值**：-1、10、20、5
- **来源环境变量**：TEST_FREQ
- **性能影响**：文档说明：quickstart 指出 `val/test_score/openai/gsm8k` 会按 `trainer.test_freq` 计算；更频繁验证会增加评测耗时，`-1` 常用于关闭周期性验证。
- **精度影响**：机制推断：评测频率不直接改变训练更新；但会影响早停/模型选择/问题排查的粒度，从而间接影响最终选用 checkpoint。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：54
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:46` test_freq=${TEST_FREQ:-10}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:29` test_freq=${TEST_FREQ:-5}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:30` test_freq=${TEST_FREQ:-5}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:33` TEST_FREQ=${TEST_FREQ:-10}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:38` test_freq=${TEST_FREQ:-10}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

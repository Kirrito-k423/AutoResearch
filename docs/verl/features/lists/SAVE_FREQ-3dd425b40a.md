# SAVE_FREQ

- **参数名**：`SAVE_FREQ`
- **分类**：配置
- **中文解释**：示例脚本中的 checkpoint 保存频率环境变量，通常传入 `trainer.save_freq`；`-1` 常表示不按步保存。
- **常见值**：-1、10、100、20、200、2000、5、50
- **来源环境变量**：SAVE_FREQ
- **性能影响**：文档说明：quickstart/多节点示例设置 `trainer.save_freq`，checkpoint 文档说明会写入 project/experiment 目录；频繁保存会增加 I/O 和端到端耗时，`-1` 可减少保存开销。
- **精度影响**：机制推断：保存频率不改变训练目标；但影响可恢复点密度，故障后从较旧 checkpoint 恢复可能间接改变训练轨迹。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:45` save_freq=${SAVE_FREQ:-50}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:28` save_freq=${SAVE_FREQ:-20}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:29` save_freq=${SAVE_FREQ:-20}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:32` SAVE_FREQ=${SAVE_FREQ:-20}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:37` save_freq=${SAVE_FREQ:-50}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

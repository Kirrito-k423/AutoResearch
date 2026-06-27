# trainer.test_freq

- **参数名**：`trainer.test_freq`
- **分类**：配置
- **中文解释**：按 iteration 控制验证/测试频率；正数表示每隔对应训练步运行验证，`-1`/非正值通常表示不按频率触发验证，SFT 中还可用 `after_each_epoch` 表示每个 epoch 后验证。
- **常见值**：${TEST_FREQ}、-1、10、20、5、50、after_each_epoch
- **来源环境变量**：TEST_FREQ
- **性能影响**：机制推断：验证越频繁，生成/打分和指标汇总越多，会占用训练资源并拉长 wall-clock 时间；频率过低则减少监控开销。
- **精度影响**：机制推断：不直接参与参数更新，通常不改变最终梯度；更频繁验证有助于及时发现退化和选择 checkpoint，但本身不是精度提升机制。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：83
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:131` trainer.test_freq=${test_freq}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:97` trainer.test_freq=${test_freq}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:103` trainer.test_freq=${test_freq}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:140` trainer.test_freq=${test_freq}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:126` trainer.test_freq=${test_freq}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

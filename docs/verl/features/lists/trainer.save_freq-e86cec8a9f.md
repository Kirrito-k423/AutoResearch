# trainer.save_freq

- **参数名**：`trainer.save_freq`
- **分类**：配置
- **中文解释**：按 iteration 控制 actor/critic checkpoint 保存频率；正数表示每隔对应步数保存，`-1`/非正值在 PPO trainer 中表示不按频率保存。
- **常见值**：$save_freq、${SAVE_FREQ}、-1、10、100、20、200、2000、40、4000、5、50
- **来源环境变量**：SAVE_FREQ
- **性能影响**：机制推断：保存越频繁，checkpoint 序列化、分片写盘和远端同步 I/O 越多，端到端训练时间和存储占用会增加；关闭保存可减少 I/O 但降低容错。
- **精度影响**：机制推断：不改变优化目标或梯度，通常不直接影响精度；会影响故障恢复、回滚和选择历史最优 checkpoint 的能力。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:130` trainer.save_freq=${save_freq}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:96` trainer.save_freq=${save_freq}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:102` trainer.save_freq=${save_freq}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:139` trainer.save_freq=${save_freq}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:125` trainer.save_freq=${save_freq}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

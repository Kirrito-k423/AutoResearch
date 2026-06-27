# trainer.total_epochs

- **参数名**：`trainer.total_epochs`
- **分类**：算法
- **中文解释**：总训练 epoch 数；Verl trainer 按该值遍历训练 dataloader，未显式设置 `total_training_steps` 时训练步数通常由 dataloader 长度乘以 `trainer.total_epochs` 得到。
- **常见值**：1、10、1000、15、2、20、4、5、50
- **来源环境变量**：TOTAL_EPOCHS
- **性能影响**：机制推断：epoch 越多，总训练步数、rollout/反向/验证/保存次数通常越多，端到端耗时和资源消耗近似随训练步数增加。
- **精度影响**：机制推断：增加训练预算可能改善收敛和任务指标，但过多 epoch 也可能带来过拟合、奖励过优化或 RL 训练不稳定。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：89
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:132` trainer.total_epochs=${total_epochs}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:98` trainer.total_epochs=${total_epochs}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:104` trainer.total_epochs=${total_epochs}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:141` trainer.total_epochs=${TOTAL_EPOCHS}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:127` trainer.total_epochs=${total_epochs}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

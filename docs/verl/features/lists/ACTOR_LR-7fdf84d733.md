# ACTOR_LR

- **参数名**：`ACTOR_LR`
- **分类**：算法
- **中文解释**：示例脚本中的 actor 学习率环境变量，通常传入 `actor_rollout_ref.actor.optim.lr`。
- **常见值**：1.0e-05、1e-5、1e-6、3e-6、5e-8
- **来源环境变量**：ACTOR_LR
- **性能影响**：机制推断：不改变单步算子规模，但影响收敛所需 step 数；过大造成不稳定会浪费训练时间，过小会拖慢达到目标指标的速度。
- **精度影响**：文档说明：官方 best practices 建议从 `1e-5` 或 `1e-6` 附近开始；该值直接影响优化稳定性、探索后策略更新幅度和最终效果。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:32` actor_lr=${ACTOR_LR:-1e-6}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:20` actor_lr=${ACTOR_LR:-3e-6}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:18` actor_lr=${ACTOR_LR:-1e-6}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:20` ACTOR_LR=${ACTOR_LR:-1e-6}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:21` actor_lr=${ACTOR_LR:-1e-6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# ROLLOUT_N

- **参数名**：`ROLLOUT_N`
- **分类**：算法
- **中文解释**：示例脚本中的每 prompt 采样响应数环境变量，通常传入 `actor_rollout_ref.rollout.n`。
- **常见值**：1、16、2、4、5、8
- **来源环境变量**：ROLLOUT_N
- **性能影响**：文档说明：GRPO README 写明总 trajectories = `train_batch_size * rollout.n`，best practices 给出 GRPO/DAPO 常见较大取值；增大 `n` 会近似线性增加生成、打分和 log-prob 计算量。
- **精度影响**：文档说明：`rollout.n` 是每个 prompt 的生成数，GRPO 要求至少 2；更多样本增强组内比较和探索信号，但也可能增加 off-policy drift 与训练成本。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：52
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:42` rollout_n=${ROLLOUT_N:-16}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:25` rollout_n=${ROLLOUT_N:-8}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:26` rollout_n=${ROLLOUT_N:-5}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:29` ROLLOUT_N=${ROLLOUT_N:-16}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:34` rollout_n=${ROLLOUT_N:-16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

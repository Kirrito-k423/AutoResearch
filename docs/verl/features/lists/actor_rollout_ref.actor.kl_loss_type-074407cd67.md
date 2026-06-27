# actor_rollout_ref.actor.kl_loss_type

- **参数名**：`actor_rollout_ref.actor.kl_loss_type`
- **分类**：算法
- **中文解释**：选择 actor KL loss 的计算形式，例如 `kl`/`abs`/`mse`/`low_var_kl`/`full`，决定如何估计当前策略与参考策略的 KL 差异。
- **常见值**：$kl_loss_type、low_var_kl
- **来源环境变量**：无
- **性能影响**：机制推断：不同 KL 公式的额外计算通常小于模型前后向主耗时；若选择更完整的 KL 形式，可能增加少量张量计算和内存读写。
- **精度影响**：文档说明：PPO README 列出 `kl(k1)`、`abs`、`mse(k2)`、`low_var_kl(k3)`、`full` 等类型，并说明其用于计算 actor 与 reference policy 的 KL；不同估计方式会影响约束强度、方差和训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：48
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`

## 证据片段

- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:73` actor_rollout_ref.actor.kl_loss_type=low_var_kl
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:97` actor_rollout_ref.actor.kl_loss_type=low_var_kl
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh:74` actor_rollout_ref.actor.kl_loss_type=low_var_kl
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:72` actor_rollout_ref.actor.kl_loss_type=low_var_kl
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:64` actor_rollout_ref.actor.kl_loss_type=low_var_kl

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

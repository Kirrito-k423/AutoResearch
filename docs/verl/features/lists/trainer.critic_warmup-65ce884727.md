# trainer.critic_warmup

- **参数名**：`trainer.critic_warmup`
- **分类**：算法
- **中文解释**：文档说明：Critic 预热步数；Ray trainer 文档/源码语义是在全局步数达到该阈值后才执行 actor 更新，常见示例设为 0 表示不单独预热 critic。
- **常见值**：$critic_warmup、0
- **来源环境变量**：无
- **性能影响**：机制推断：大于 0 会在预热阶段增加只训练 critic 的迭代时间，但可能让后续 actor 更新使用更稳定的 value baseline。
- **精度影响**：机制推断：PPO/GAE 依赖 critic 估值，适当预热可能降低优势估计噪声；GRPO 等无 critic 流程通常设 0，影响较小。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：45
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:123` trainer.critic_warmup=0
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:90` trainer.critic_warmup=0
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:96` trainer.critic_warmup=0
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:133` trainer.critic_warmup=0
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:118` trainer.critic_warmup=0

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

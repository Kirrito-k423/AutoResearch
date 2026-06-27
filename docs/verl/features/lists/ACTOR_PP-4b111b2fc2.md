# ACTOR_PP

- **参数名**：`ACTOR_PP`
- **分类**：效率
- **中文解释**：机制推断：用户侧环境变量，通常映射到 `actor_rollout_ref.actor.megatron.pipeline_model_parallel_size` 和 ref 侧同名配置，表示 actor Megatron pipeline parallel 的切分段数。
- **常见值**：1、12、2、3、8
- **来源环境变量**：ACTOR_PP
- **性能影响**：文档说明：Megatron PP/TP/EP/ETP/CP 需要按显存、网络拓扑和通信成本平衡；PP 增大可降低单卡层数/显存，但会引入 pipeline bubble 和跨阶段通信。
- **精度影响**：机制推断：并行切分不改变目标函数；错误切分或与 ref/critic 不一致可能导致加载失败、数值差异或训练中断。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：18
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`
- `examples/tuning/scaling/run_qwen2_5_32b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:36` actor_pp=${ACTOR_PP:-1}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:28` actor_pp=${ACTOR_PP:-1}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:35` actor_pp=${ACTOR_PP:-1}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:30` actor_pp=${ACTOR_PP:-2}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:27` actor_pp=${ACTOR_PP:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

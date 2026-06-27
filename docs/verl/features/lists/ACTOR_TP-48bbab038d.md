# ACTOR_TP

- **参数名**：`ACTOR_TP`
- **分类**：效率
- **中文解释**：机制推断：用户侧环境变量，通常映射到 `actor_rollout_ref.actor.megatron.tensor_model_parallel_size` 和 ref 侧同名配置，表示 actor Megatron tensor parallel 的切分度。
- **常见值**：2、4、8
- **来源环境变量**：ACTOR_TP
- **性能影响**：文档说明：TP 增大可降低每卡参数/激活压力，但会增加张量并行通信；官方建议与 PP/EP/ETP/CP 和硬件拓扑一起平衡。
- **精度影响**：机制推断：并行切分不改变优化目标；若与 checkpoint、ref 或 rollout 并行配置不匹配，可能造成加载失败或数值一致性风险。
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:35` actor_tp=${ACTOR_TP:-2}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:27` actor_tp=${ACTOR_TP:-2}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:34` actor_tp=${ACTOR_TP:-2}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:29` actor_tp=${ACTOR_TP:-2}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:26` actor_tp=${ACTOR_TP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

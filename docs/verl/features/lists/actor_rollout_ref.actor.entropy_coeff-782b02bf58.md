# actor_rollout_ref.actor.entropy_coeff

- **参数名**：`actor_rollout_ref.actor.entropy_coeff`
- **分类**：算法
- **中文解释**：Actor loss 中的熵正则系数，用来鼓励策略保持一定随机性和探索能力。
- **常见值**：$entropy_coeff、0、0.0
- **来源环境变量**：ENTROPY_COEFF
- **性能影响**：机制推断：熵项只增加很小的 loss 统计/归约开销，通常不影响主要吞吐；真正影响端到端耗时的是它对收敛速度和探索轨迹的间接作用。
- **精度影响**：机制推断：较大熵系数会增强探索和输出多样性，但可能降低收敛确定性；过小则更快收敛到当前高 reward 模式，探索不足风险更高。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：65
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:85` actor_rollout_ref.actor.entropy_coeff=${entropy_coeff}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:68` actor_rollout_ref.actor.entropy_coeff=${entropy_coeff}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:74` actor_rollout_ref.actor.entropy_coeff=${entropy_coeff}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:111` actor_rollout_ref.actor.entropy_coeff=${ENTROPY_COEFF}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:76` actor_rollout_ref.actor.entropy_coeff=${entropy_coeff}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

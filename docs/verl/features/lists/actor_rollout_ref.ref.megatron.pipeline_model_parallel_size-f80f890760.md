# actor_rollout_ref.ref.megatron.pipeline_model_parallel_size

- **参数名**：`actor_rollout_ref.ref.megatron.pipeline_model_parallel_size`
- **分类**：效率
- **中文解释**：控制流水并行切分度，降低单卡层数和激活压力，但会引入 pipeline bubble。
- **常见值**：${actor_pp、1、12、16、2、3、6、8
- **来源环境变量**：ACTOR_PP、PP、REF_PP、actor_pp
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：21
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:114` actor_rollout_ref.ref.megatron.pipeline_model_parallel_size=${actor_pp}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:109` actor_rollout_ref.ref.megatron.pipeline_model_parallel_size=${actor_pp}
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:123` actor_rollout_ref.ref.megatron.pipeline_model_parallel_size=${actor_pp} \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:108` actor_rollout_ref.ref.megatron.pipeline_model_parallel_size=${actor_pp}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:151` actor_rollout_ref.ref.megatron.pipeline_model_parallel_size=${actor_pp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

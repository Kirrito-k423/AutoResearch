# ROLLOUT_GPU_MEM_UTIL

- **参数名**：`ROLLOUT_GPU_MEM_UTIL`
- **分类**：效率
- **中文解释**：示例脚本中的 rollout 显存利用率环境变量，通常传入 `actor_rollout_ref.rollout.gpu_memory_utilization` 控制推理后端显存预算。
- **常见值**：0.25、0.4、0.5、0.6、0.65、0.7、0.75、0.8、0.85
- **来源环境变量**：ROLLOUT_GPU_MEM_UTIL
- **性能影响**：文档说明：best practices 建议在不 OOM 的前提下尽量提高该值，常见 0.8-0.9；perf tuning 说明不同推理后端定义不同，过高可能 OOM，0.5-0.7 常是吞吐和稳定性的折中。
- **精度影响**：机制推断：显存比例不直接改变采样分布；但 OOM、回退批大小或 KV cache 容量不足会间接影响可完成的 rollout 和训练稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：60
- **需要子代理补证**：否

## 示例脚本

- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/generation/run_deepseek_llm_7b.sh`
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

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:41` rollout_gpu_mem_util=${ROLLOUT_GPU_MEM_UTIL:-0.8}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:24` rollout_gpu_mem_util=${ROLLOUT_GPU_MEM_UTIL:-0.6}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:25` rollout_gpu_mem_util=${ROLLOUT_GPU_MEM_UTIL:-0.6}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:28` ROLLOUT_GPU_MEM_UTIL=${ROLLOUT_GPU_MEM_UTIL:-}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:55` rollout_gpu_mem_util=${ROLLOUT_GPU_MEM_UTIL:-0.6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

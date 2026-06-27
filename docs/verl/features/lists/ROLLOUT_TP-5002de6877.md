# ROLLOUT_TP

- **参数名**：`ROLLOUT_TP`
- **分类**：效率
- **中文解释**：示例脚本中的 rollout tensor parallel size，通常传入 `actor_rollout_ref.rollout.tensor_model_parallel_size` 控制推理后端张量并行度。
- **常见值**：1、16、2、32、4、8
- **来源环境变量**：ROLLOUT_TP
- **性能影响**：文档说明：best practices 建议逐步增大 TP 来扩展 KV cache 容量，同时关注通信成本，尤其 TP > 8 后通信开销更明显。
- **精度影响**：机制推断：并行切分理论上不改变模型输出；不同后端/并行度的数值归约和失败重试可能带来很小的间接差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：57
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

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:40` rollout_tp=${ROLLOUT_TP:-4}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:23` rollout_tp=${ROLLOUT_TP:-2}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:24` rollout_tp=${ROLLOUT_TP:-2}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:27` ROLLOUT_TP=${ROLLOUT_TP:-}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:54` rollout_tp=${ROLLOUT_TP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

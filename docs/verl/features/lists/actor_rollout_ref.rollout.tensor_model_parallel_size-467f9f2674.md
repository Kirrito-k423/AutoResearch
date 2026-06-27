# actor_rollout_ref.rollout.tensor_model_parallel_size

- **参数名**：`actor_rollout_ref.rollout.tensor_model_parallel_size`
- **分类**：效率
- **中文解释**：控制张量并行切分度，降低单卡权重/KV 压力，但会增加层内通信。
- **常见值**："${ROLLOUT_TP}"、$GEN_TP、$infer_tp、${rollout_tp、1、16、2、32、4、8
- **来源环境变量**：GEN_TP、INFER_TP、ROLLOUT_TP、rollout_tp
- **性能影响**：机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：78
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
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
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:103` actor_rollout_ref.rollout.tensor_model_parallel_size=${rollout_tp}
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:75` actor_rollout_ref.rollout.tensor_model_parallel_size=${rollout_tp}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:81` actor_rollout_ref.rollout.tensor_model_parallel_size=${rollout_tp}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:118` actor_rollout_ref.rollout.tensor_model_parallel_size=${rollout_tp}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:95` actor_rollout_ref.rollout.tensor_model_parallel_size=${rollout_tp}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

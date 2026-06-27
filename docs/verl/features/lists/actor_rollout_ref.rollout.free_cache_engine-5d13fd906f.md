# actor_rollout_ref.rollout.free_cache_engine

- **参数名**：`actor_rollout_ref.rollout.free_cache_engine`
- **分类**：效率
- **中文解释**：文档说明：vLLM rollout cache engine 释放开关；官方 vLLM 0.8+ 升级文档建议与 `enforce_eager=False` 一起配置，以使用 CUDA graph/V1 engine 能力。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：机制推断：启用释放 cache engine 可在训练/rollout 切换时回收部分推理缓存显存，降低 OOM 风险；代价是下一轮 rollout 可能需要重建缓存/引擎状态。
- **精度影响**：机制推断：不改变采样参数或训练目标；若关闭导致显存不足，可能间接影响任务完成或迫使降低 batch/token 上限。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：18
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/grpo_trainer/run_seed_oss_36b_fsdp.sh`
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`
- `examples/tuning/lora/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:112` actor_rollout_ref.rollout.free_cache_engine=True
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:133` actor_rollout_ref.rollout.free_cache_engine=False
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:77` actor_rollout_ref.rollout.free_cache_engine=False
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:117` actor_rollout_ref.rollout.free_cache_engine=True
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:133` actor_rollout_ref.rollout.free_cache_engine=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

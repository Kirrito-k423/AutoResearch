# actor_rollout_ref.rollout.enable_chunked_prefill

- **参数名**：`actor_rollout_ref.rollout.enable_chunked_prefill`
- **分类**：效率
- **中文解释**：文档说明：vLLM rollout 的 chunked prefill 开关，将长 prompt 的 prefill 拆块调度；官方 Best Practices 标注为 vLLM 专用，通常与 `max_num_batched_tokens` 一起调。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：启用可提升 GPU 利用率，尤其是长上下文/大 batch rollout；但 batch token 上限过小或后端不匹配时可能带来额外调度开销。
- **精度影响**：机制推断：只改变 prefill 调度方式，不改变采样分布；若引发 OOM 或后端兼容问题才会间接影响训练/评测完成度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：24
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/profile/run_qwen2_5_vl_7b_torch_memory.sh`
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:111` actor_rollout_ref.rollout.enable_chunked_prefill=True \
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:110` actor_rollout_ref.rollout.enable_chunked_prefill=False
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:75` actor_rollout_ref.rollout.enable_chunked_prefill=False
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:115` actor_rollout_ref.rollout.enable_chunked_prefill=True
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:135` actor_rollout_ref.rollout.enable_chunked_prefill=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

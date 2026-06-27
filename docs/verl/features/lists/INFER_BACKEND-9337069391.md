# INFER_BACKEND

- **参数名**：`INFER_BACKEND`
- **分类**：效率
- **中文解释**：文档说明：examples 脚本中的 rollout 推理后端选择开关，映射到 `actor_rollout_ref.rollout.name`；官方 GRPO README 说明支持脚本可在 `vllm`、`sglang`、`trtllm` 间选择。
- **常见值**：vllm
- **来源环境变量**：INFER_BACKEND
- **性能影响**：文档说明：不同 rollout backend 的吞吐、显存、特性支持和额外 engine kwargs 不同，官方建议按基础设施 benchmark/tune。
- **精度影响**：机制推断：后端本身不改变训练目标，但采样实现、支持的参数、detokenization/多模态处理差异可能造成评测波动。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：14
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_megatron.sh`
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:10` INFER_BACKEND=${INFER_BACKEND:-vllm}
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:9` INFER_BACKEND=${INFER_BACKEND:-vllm}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:10` INFER_BACKEND=${INFER_BACKEND:-vllm}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:10` INFER_BACKEND=${INFER_BACKEND:-vllm}
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh:4` INFER_BACKEND=${INFER_BACKEND:-vllm}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

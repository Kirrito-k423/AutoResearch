# actor_rollout_ref.rollout.engine_kwargs.trtllm.moe_config.backend

- **参数名**：`actor_rollout_ref.rollout.engine_kwargs.trtllm.moe_config.backend`
- **分类**：效率
- **中文解释**：机制推断：传给 TensorRT-LLM 的 MoE backend 选择，示例通过 `trtllm_moe_backend` 传入 `DEEPGEMM`，用于指定 MoE 专家计算/调度后端。
- **常见值**：DEEPGEMM
- **来源环境变量**：TRTLLM_MOE_BACKEND
- **性能影响**：机制推断：不同 MoE backend 会影响 expert GEMM、路由通信和内核融合效率；选择高性能 backend 可能提升 MoE rollout 吞吐，选择不兼容 backend 会导致启动失败或回退。
- **精度影响**：机制推断：后端选择目标上应保持等价推理，但不同 kernel、低精度累加或量化路径可能带来细微数值差异；错误 backend 主要表现为兼容性或稳定性问题。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:234` +actor_rollout_ref.rollout.engine_kwargs.trtllm.moe_config.backend=${trtllm_moe_backend}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# TRTLLM_MOE_BACKEND

- **参数名**：`TRTLLM_MOE_BACKEND`
- **分类**：效率
- **中文解释**：控制 TRT-LLM rollout 的 MoE kernel/backend 选择，映射到 `actor_rollout_ref.rollout.engine_kwargs.trtllm.moe_config.backend`；示例默认 `DEEPGEMM`。
- **常见值**：DEEPGEMM
- **来源环境变量**：TRTLLM_MOE_BACKEND
- **性能影响**：机制推断：MoE backend 决定 TRT-LLM 处理专家 GEMM/dispatch 的实现，可能显著影响 MoE rollout 吞吐、显存与硬件适配；不同后端应按 GPU 架构和 batch shape benchmark。
- **精度影响**：机制推断：若 backend 是数值等价 kernel 替换，通常不改变训练目标；但低精度或不同累加路径可能带来细小数值差异，不兼容时会直接运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:62` trtllm_moe_backend=${TRTLLM_MOE_BACKEND:-DEEPGEMM}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

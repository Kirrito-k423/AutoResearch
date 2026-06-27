# USE_FUSED_KERNELS

- **参数名**：`USE_FUSED_KERNELS`
- **分类**：效率
- **中文解释**：控制 `actor_rollout_ref.model.use_fused_kernels`，为支持的模型启用 Verl fused kernels，主要优化模型/输出 head 相关内核；示例默认关闭以保守兼容。
- **常见值**：False
- **来源环境变量**：USE_FUSED_KERNELS
- **性能影响**：文档说明：官方 best practices 建议对支持模型开启 fused kernels 以获得额外性能；性能调优文档说明它与 Liger 位于不同优化层，可一起形成更好的速度-显存折中。
- **精度影响**：机制推断：通常是等价 kernel 替换，不改变训练目标；若当前算法或模型路径不兼容，风险主要是运行失败或轻微数值路径差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:17` USE_FUSED_KERNELS=${USE_FUSED_KERNELS:-False}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

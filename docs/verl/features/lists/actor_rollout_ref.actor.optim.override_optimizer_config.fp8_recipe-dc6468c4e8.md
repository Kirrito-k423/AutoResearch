# actor_rollout_ref.actor.optim.override_optimizer_config.fp8_recipe

- **参数名**：`actor_rollout_ref.actor.optim.override_optimizer_config.fp8_recipe`
- **分类**：效率
- **中文解释**：文档说明：传给 Megatron `OptimizerConfig` 的 FP8 recipe override；Verl FP8 文档中 `blockwise` 用于 FP8 end-to-end 训练的块级缩放策略，需与 transformer FP8 和 rollout FP8 配置配套。
- **常见值**："blockwise"
- **来源环境变量**：无
- **性能影响**：文档说明：FP8 end-to-end 通过 FP8 forward/backward、FP8 optimizer states 和 FP8 rollout 最大化显存节省与吞吐；`blockwise` 依赖 CUDA 12.9+ 与 Transformer Engine 块级 FP8 支持。
- **精度影响**：文档说明：Verl FP8 文档报告 FP8 end-to-end 在测试设置下与 BF16 baseline 精度接近，但低精度会改变训练/推理分布匹配和 KL，需要配合 FP8 recipe、rollout 校正和硬件支持谨慎验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:87` # +actor_rollout_ref.actor.optim.override_optimizer_config.fp8_recipe="blockwise"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

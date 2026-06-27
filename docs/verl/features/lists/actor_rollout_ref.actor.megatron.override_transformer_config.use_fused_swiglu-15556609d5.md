# actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_swiglu

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_swiglu`
- **分类**：效率
- **中文解释**：文档说明：Megatron SwiGLU 融合算子开关；Ascend 高级特性文档说明该参数用于使用融合算子加速 SwiGLU 激活函数，默认值为 `False`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：融合 SwiGLU 可减少 MLP 激活相关小算子和显存往返，NPU 性能文档将其列为训练侧优化项；收益依赖模型是否使用 SwiGLU 以及后端 kernel 支持。
- **精度影响**：机制推断：与普通 SwiGLU 目标等价，但融合 kernel 会改变舍入路径；必须与 `swiglu=True` 和模型结构匹配，否则会造成结构或数值错误。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:135` +actor_rollout_ref.actor.megatron.override_transformer_config.use_fused_swiglu=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

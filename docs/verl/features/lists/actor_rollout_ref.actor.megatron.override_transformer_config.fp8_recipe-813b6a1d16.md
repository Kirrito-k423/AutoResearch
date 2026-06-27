# actor_rollout_ref.actor.megatron.override_transformer_config.fp8_recipe

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.fp8_recipe`
- **分类**：效率
- **中文解释**：文档说明：Megatron FP8 的 recipe 配置，官方 FP8 文档示例使用 `fp8_recipe: "blockwise"`，表示采用 block-wise scaling 方案来管理 FP8 缩放。
- **常见值**："blockwise"
- **来源环境变量**：无
- **性能影响**：文档说明：`blockwise` recipe 是官方列出的 FP8 支持配置；相比非 FP8 训练，主要性能收益来自 FP8 低位宽，recipe 本身会增加缩放统计/应用逻辑，但通常是换取可用精度的必要成本。
- **精度影响**：文档说明：block-wise scaling 用更细粒度的缩放改善 FP8 数值覆盖范围，通常比粗粒度缩放更稳；recipe 与 `fp8` 模式不匹配时可能导致训练不稳定或指标下降。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:86` # +actor_rollout_ref.actor.megatron.override_transformer_config.fp8_recipe="blockwise"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

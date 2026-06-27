# actor_rollout_ref.actor.megatron.override_transformer_config.fp8

- **参数名**：`actor_rollout_ref.actor.megatron.override_transformer_config.fp8`
- **分类**：效率
- **中文解释**：文档说明：Megatron Transformer Engine FP8 训练开关，官方 FP8 文档示例在 `actor_rollout_ref.actor.megatron.override_transformer_config` 下设置 `fp8`，支持 `hybrid` 和 `e4m3` 等模式，用于让前向/反向使用 FP8 路径。
- **常见值**："e4m3"
- **来源环境变量**：无
- **性能影响**：文档说明：FP8 训练通过降低数据位宽减少显存和带宽压力，并可提升支持硬件上的矩阵计算吞吐；实际收益依赖 Transformer Engine、模型结构和硬件 FP8 能力。
- **精度影响**：文档说明：FP8 是低精度训练，会引入量化误差；官方文档给出 Qwen3-30B-A3B 和 Qwen3-8B 的验证场景，但超出验证组合时需要关注 loss 稳定性、溢出和最终指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:85` # +actor_rollout_ref.actor.megatron.override_transformer_config.fp8="e4m3" # e4m3 or hybrid

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

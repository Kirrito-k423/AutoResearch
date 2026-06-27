# optim.optimizer

- **参数名**：`optim.optimizer`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 的优化器类名；Verl 会与 `optim.optimizer_impl` 拼成动态导入目标，例如 `transformer_engine.pytorch.optimizers.fused_adam.FusedAdam`。
- **常见值**：FusedAdam
- **来源环境变量**：无
- **性能影响**：文档说明：`FusedAdam` 使用融合优化器实现，通常减少 Adam 更新阶段的 kernel 调用和内存访问；收益依赖 TransformerEngine、dtype 和分片/offload 配置。
- **精度影响**：机制推断：同等超参下目标仍是 Adam/AdamW 类更新；融合实现、低精度状态和 master weights 配置会改变数值路径，需要与基线做收敛验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:51` optim.optimizer=FusedAdam \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

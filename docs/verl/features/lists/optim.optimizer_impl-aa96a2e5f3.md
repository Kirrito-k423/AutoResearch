# optim.optimizer_impl

- **参数名**：`optim.optimizer_impl`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 的 Python 模块路径；Verl 使用动态 import 从该模块中取 `optim.optimizer` 指定的类来构造优化器。
- **常见值**：transformer_engine.pytorch.optimizers.fused_adam
- **来源环境变量**：无
- **性能影响**：文档说明：选择 `transformer_engine.pytorch.optimizers.fused_adam` 会进入 TransformerEngine 融合 Adam 实现，通常比纯 Python/标准 torch 路径更适合大模型低精度训练。
- **精度影响**：机制推断：模块路径本身不定义训练目标，但不同优化器实现可能在 dtype、epsilon、状态存储和融合顺序上有差异，会影响可复现性和微小数值轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:52` optim.optimizer_impl=transformer_engine.pytorch.optimizers.fused_adam \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

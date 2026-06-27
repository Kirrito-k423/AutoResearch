# optim.store_param_remainders

- **参数名**：`optim.store_param_remainders`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 传给底层优化器的参数余量/残差存储开关；Verl `_build_optimizer` 会把该字段加入优化器配置，常与低精度 master weights/FusedAdam 一起使用以保留低精度更新的剩余信息。
- **常见值**：true
- **来源环境变量**：无
- **性能影响**：机制推断：开启会增加额外 optimizer 状态存储，提升显存/内存占用；但可降低低精度参数更新的信息损失，适合追求低精度训练稳定性的路径。
- **精度影响**：机制推断：通常有助于低精度优化器保留更新残差、改善数值稳定性；具体收益依赖底层 FusedAdam 对该参数的实现和 dtype 组合。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:62` optim.store_param_remainders=true \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

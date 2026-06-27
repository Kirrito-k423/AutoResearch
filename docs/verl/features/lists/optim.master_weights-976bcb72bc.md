# optim.master_weights

- **参数名**：`optim.master_weights`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 传给底层优化器的 master weights 开关；在低精度参数训练时保留一份高精度主权重用于优化器更新。
- **常见值**：true
- **来源环境变量**：无
- **性能影响**：机制推断：开启 master weights 会增加一份主权重状态，占用更多显存/内存，但可配合低精度参数训练降低更新误差。
- **精度影响**：机制推断：通常有利于低精度训练稳定性和可收敛性；关闭可省内存但可能让优化器直接在低精度权重上累积误差。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:61` optim.master_weights=true \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

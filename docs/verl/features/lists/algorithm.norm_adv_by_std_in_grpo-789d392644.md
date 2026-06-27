# algorithm.norm_adv_by_std_in_grpo

- **参数名**：`algorithm.norm_adv_by_std_in_grpo`
- **分类**：效率
- **中文解释**：文档说明：控制 GRPO 优势是否按组内标准差归一化；官方 GRPO 文档说明设为 `False` 会关闭 std norm，Dr.GRPO 使用这种做法。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：计算开销很小，主要不是吞吐参数；但它会改变 advantage 尺度，从而影响梯度幅度、loss 曲线和优化稳定性。
- **精度影响**：文档说明：`True` 按原始 GRPO 用 std 缩放优势，`False` 只减去组均值；该选择会改变训练动态和长度/奖励尺度偏置，是会影响最终效果的算法参数。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:59` algorithm.norm_adv_by_std_in_grpo=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

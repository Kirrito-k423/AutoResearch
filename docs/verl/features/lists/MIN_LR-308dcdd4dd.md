# MIN_LR

- **参数名**：`MIN_LR`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，传入 Megatron/SFT optimizer 的 `min_lr`，表示学习率衰减后的最低学习率；Verl 配置文档说明 `lr_decay_style` 会在 warmup 后把学习率按策略衰减到 `min_lr`。
- **常见值**：2e-6
- **来源环境变量**：MIN_LR
- **性能影响**：机制推断：不直接改变单步计算量；但会影响达到目标指标所需 step 数和调参周期，间接影响总训练成本。
- **精度影响**：机制推断：最低学习率过高可能导致后期震荡，过低可能使后期更新停滞；合理设置有助于收敛稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:71` MIN_LR=${MIN_LR:-2e-6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

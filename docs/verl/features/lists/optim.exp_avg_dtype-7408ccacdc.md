# optim.exp_avg_dtype

- **参数名**：`optim.exp_avg_dtype`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 中 Adam 一阶动量 `exp_avg` 状态的存储 dtype；Verl 会把 `bf16`、`fp32`、`fp16` 等短名转换为对应的 `torch.dtype` 后传给底层优化器。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：将一阶动量状态设为 `bf16` 可降低 optimizer state 显存和带宽压力；代价是优化器状态精度降低，实际收益取决于 FusedAdam/分片策略。
- **精度影响**：机制推断：一阶动量低精度存储会改变 Adam 更新轨迹，可能影响收敛稳定性；通常需要与 master weights、二阶动量 dtype 和学习率设置一起验证。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:63` optim.exp_avg_dtype=bf16 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

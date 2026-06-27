# optim.warmup_style

- **参数名**：`optim.warmup_style`
- **分类**：效率
- **中文解释**：文档说明：FSDP optimizer 的旧版 warmup/lr scheduler 风格字段；源码中该字段已标记为 deprecated，设置后会映射到 `lr_scheduler_type`，支持 `constant`、`cosine`。
- **常见值**：cosine
- **来源环境变量**：无
- **性能影响**：机制推断：不直接改变每 step 计算量；学习率 warmup/调度形状会影响达到目标效果所需训练步数和调参周期。
- **精度影响**：机制推断：会影响优化动态、早期稳定性和最终收敛；`cosine` 与 `constant` 的学习率轨迹不同，可能改变训练质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:42` optim.warmup_style=cosine \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

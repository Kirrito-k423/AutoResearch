# optim.init_lr_ratio

- **参数名**：`optim.init_lr_ratio`
- **分类**：算法
- **中文解释**：AutoModel optimizer 的 warmup 初始学习率比例；官方配置注释写明 `init_lr = lr * init_lr_ratio`，examples 用 0 或 0.1 控制 warmup 起点。
- **常见值**：0、0.1
- **来源环境变量**：无
- **性能影响**：机制推断：该参数不改变单步计算量；更合适的 warmup 起点可减少发散和无效训练步，过低可能导致前期学习偏慢。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:44` optim.init_lr_ratio=0 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:58` optim.init_lr_ratio=0.1 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

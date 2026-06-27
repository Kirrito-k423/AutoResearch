# optim.lr_scheduler_type

- **参数名**：`optim.lr_scheduler_type`
- **分类**：算法
- **中文解释**：选择 optimizer 学习率调度类型；官方配置文档说明 FSDP/AutoModel 侧可选 `constant`、`cosine`，AutoModel 配置还列出 `linear`、`inverse-square-root` 等衰减风格。
- **常见值**：cosine
- **来源环境变量**：无
- **性能影响**：机制推断：调度器本身计算开销极小；合适的 schedule 可提高训练步利用率，错误 schedule 可能导致收敛慢、震荡或需要重跑。
- **精度影响**：机制推断：影响优化动态、稳定性和收敛速度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:46` optim.lr_scheduler_type=cosine \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:60` optim.lr_scheduler_type=cosine \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

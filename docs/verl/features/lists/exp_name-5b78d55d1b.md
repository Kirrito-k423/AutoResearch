# exp_name

- **参数名**：`exp_name`
- **分类**：配置
- **中文解释**：脚本局部实验名变量；示例传给 `trainer.experiment_name`，并与 `project_name` 一起参与 checkpoint 目录命名，用于标识具体 run 或配置组合。
- **常见值**：'qwen3_5_122b_megatron'
- **来源环境变量**：exp_name
- **性能影响**：机制推断：仅作为日志和目录标识，通常不改变训练吞吐；若参与 checkpoint 路径，名称冲突、路径过长或落到慢存储会影响保存/恢复 I/O。
- **精度影响**：机制推断：不参与前向、反向或奖励计算；主要影响实验追踪、结果对比和断点恢复定位。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:45` exp_name=${exp_name:-'qwen3_5_122b_megatron'}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

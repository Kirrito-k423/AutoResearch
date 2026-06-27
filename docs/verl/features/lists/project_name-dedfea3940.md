# project_name

- **参数名**：`project_name`
- **分类**：配置
- **中文解释**：脚本局部项目名变量；示例传给 `trainer.project_name`，用于 wandb/swanlab/mlflow 等日志归组，并常与实验名一起组成 checkpoint 路径。
- **常见值**：'verl_grpo_qwen3_5_122b_geo3k'
- **来源环境变量**：project_name
- **性能影响**：机制推断：仅作为日志项目和目录标识，通常不改变计算吞吐；命名冲突主要影响归档、权限、tracking 查询或恢复定位。
- **精度影响**：机制推断：不参与模型训练计算，通常不直接影响精度；会影响跨 run 聚合、对比和最佳 checkpoint 管理口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:44` project_name=${project_name:-'verl_grpo_qwen3_5_122b_geo3k'}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

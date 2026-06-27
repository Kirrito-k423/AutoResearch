# output_path

- **参数名**：`output_path`
- **分类**：配置
- **中文解释**：脚本级输出根目录；示例用 `$output_path/$project_name/$exp_name` 生成 `trainer.default_local_dir`，用于保存 checkpoint 等运行产物。
- **常见值**：$HOME/output
- **来源环境变量**：output_path
- **性能影响**：机制推断：路径变量本身不改变计算；若对应存储较慢、容量不足或为网络盘，会拖慢 checkpoint 写入/恢复并影响端到端耗时。
- **精度影响**：机制推断：不参与前向、反向或奖励计算；主要影响产物保存、断点恢复和实验结果可追溯性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:18` output_path=${output_path:-$HOME/output}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

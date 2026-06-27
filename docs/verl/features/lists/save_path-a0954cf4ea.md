# save_path

- **参数名**：`save_path`
- **分类**：配置
- **中文解释**：SFT GSM8K 示例脚本的第二个位置参数，传给 `trainer.default_local_dir` 作为 checkpoint 和训练产物保存目录。
- **常见值**："Qwen/Qwen3.5-122B/verl_checkpoint"
- **来源环境变量**：save_path
- **性能影响**：机制推断：路径本身不改变训练计算；若保存目录位于慢盘、网络盘或空间不足，会拖慢 checkpoint 写入/恢复并可能导致保存失败。
- **精度影响**：机制推断：不参与前向、反向或奖励计算；主要影响断点恢复、产物保留和实验复现能力。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:49` save_path=${save_path:-"Qwen/Qwen3.5-122B/verl_checkpoint"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

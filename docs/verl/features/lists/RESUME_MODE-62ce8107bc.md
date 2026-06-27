# RESUME_MODE

- **参数名**：`RESUME_MODE`
- **分类**：效率
- **中文解释**：机制推断：训练器 checkpoint 恢复模式，示例写入 `trainer.resume_mode`；`disable` 表示不从已有 checkpoint 自动恢复。
- **常见值**：disable
- **来源环境变量**：RESUME_MODE
- **性能影响**：机制推断：主要影响启动阶段是否扫描/加载 checkpoint；恢复会增加启动 I/O，但可避免已完成训练浪费，`disable` 则从头开始。
- **精度影响**：机制推断：不改变算法本身；若误设为从旧 checkpoint 恢复或禁用恢复，会改变训练起点、累计步数和最终结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:75` RESUME_MODE=${RESUME_MODE:-disable}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

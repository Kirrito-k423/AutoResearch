# SAVE_PATH

- **参数名**：`SAVE_PATH`
- **分类**：配置
- **中文解释**：SFT 示例的 checkpoint 保存目录，脚本把它传给 `trainer.default_local_dir` 用于保存模型、优化器和 extra 状态。
- **常见值**：/root/checkpoints/Qwen2.5-Math-7B
- **来源环境变量**：SAVE_PATH
- **性能影响**：机制推断：保存路径影响 checkpoint 写入/保留/恢复速度；慢盘或空间不足会拖慢保存步骤甚至中断训练。
- **精度影响**：机制推断：正常保存路径不改变训练；若用于恢复的目录错误，可能从错误 checkpoint 继续，间接改变最终模型。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:7` SAVE_PATH=${SAVE_PATH:-/root/checkpoints/Qwen2.5-Math-7B}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

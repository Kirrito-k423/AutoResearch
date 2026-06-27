# trainer.resume_from_path

- **参数名**：`trainer.resume_from_path`
- **分类**：配置
- **中文解释**：文档说明：指定从哪个 checkpoint 路径恢复训练；官方配置说明中它只在 `trainer.resume_mode=resume_path` 时生效。
- **常见值**：checkpoints/
- **来源环境变量**：无
- **性能影响**：机制推断：恢复时需要读取分片模型、优化器和额外状态，启动阶段会增加 I/O 和同步时间；训练中不改变每步计算开销。
- **精度影响**：文档说明：正确恢复可延续模型、优化器和 step 状态，保持训练连续性；错误路径或不完整 checkpoint 会改变训练轨迹甚至恢复失败。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:131` trainer.resume_from_path=checkpoints/
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:131` trainer.resume_from_path=checkpoints/
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh:56` trainer.resume_from_path=checkpoints/ \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

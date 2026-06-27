# trainer.log_val_generations

- **参数名**：`trainer.log_val_generations`
- **分类**：效率
- **中文解释**：文档说明：控制验证阶段写入日志的生成样本数量；默认值为 0，examples 常设为 10 或 100，用于在 wandb/console 等日志中抽样查看模型输出。
- **常见值**：10、100
- **来源环境变量**：LOG_VAL_GENERATIONS
- **性能影响**：文档说明：增加该值会增加日志序列化、传输和存储量；机制推断：通常不增加验证生成本身的样本数，只影响被保存/展示的样本数量，因此计算吞吐影响较小。
- **精度影响**：机制推断：只改变可观测日志，不改变训练目标或验证指标计算；但更多样本有助于人工发现模式崩塌、乱码或格式错误。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:152` trainer.log_val_generations=10 "$@"
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:176` trainer.log_val_generations=10
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:153` trainer.log_val_generations=100
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:185` trainer.log_val_generations=10
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:219` trainer.log_val_generations=${log_val_generations}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

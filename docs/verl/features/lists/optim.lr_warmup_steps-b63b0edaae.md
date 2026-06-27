# optim.lr_warmup_steps

- **参数名**：`optim.lr_warmup_steps`
- **分类**：算法
- **中文解释**：优化器学习率 warmup 的步数；Verl/Megatron 配置中该字段优先级高于 warmup ratio，负数表示交给 `lr_warmup_steps_ratio`。
- **常见值**：10、5
- **来源环境变量**：无
- **性能影响**：机制推断：不直接改变每步计算量；warmup 过长可能延后有效学习、增加达到目标效果所需步数，过短可能增加早期不稳定重跑风险。
- **精度影响**：文档说明：配置文档将其定义为 warmup 步数；合理 warmup 可缓解训练初期梯度/学习率冲击，影响稳定性和最终收敛。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:44` optim.lr_warmup_steps=5
- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:54` optim.lr_warmup_steps=10 \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:101` optim.lr_warmup_steps=10 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

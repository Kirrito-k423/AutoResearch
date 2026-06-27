# actor_rollout_ref.ref.megatron.override_transformer_config.sequence_parallel

- **参数名**：`actor_rollout_ref.ref.megatron.override_transformer_config.sequence_parallel`
- **分类**：效率
- **中文解释**：机制推断：Reference Megatron transformer config 的 sequence parallel 开关，在 tensor parallel 组内切分序列维度相关激活，常用于长上下文/大模型场景。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：开启后可降低单卡激活显存并支持更长序列，但需要额外 scatter/gather 通信；收益依赖 TP 大小、序列长度和网络带宽。
- **精度影响**：机制推断：正确切分/聚合时不改变 reference logprob；若 TP/sequence parallel 配置与 actor 或 checkpoint 不一致，会导致权重/激活形状错误或 KL 计算异常。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:156` +actor_rollout_ref.ref.megatron.override_transformer_config.sequence_parallel=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

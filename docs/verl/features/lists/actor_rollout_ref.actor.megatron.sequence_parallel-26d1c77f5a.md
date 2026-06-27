# actor_rollout_ref.actor.megatron.sequence_parallel

- **参数名**：`actor_rollout_ref.actor.megatron.sequence_parallel`
- **分类**：效率
- **中文解释**：文档说明：Actor Megatron 引擎级 sequence parallel 开关，官方参数表默认 `true`，Verl dataclass 注释说明它控制 Megatron 并行中的序列并行；当 TP size 为 1 时配置校验会将 sequence parallel 置为 false。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：SP 在 TP 基础上切分序列维度，可降低长序列激活显存并改善并行效率；同时会增加序列维通信，且只有在合适 TP/硬件拓扑下才有效。
- **精度影响**：机制推断：不改变损失或模型结构；分布式切分会改变聚合顺序，可能出现微小数值差异。与 `override_transformer_config.sequence_parallel` 或 TP 配置不一致时可能导致运行错误。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:106` actor_rollout_ref.actor.megatron.sequence_parallel=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

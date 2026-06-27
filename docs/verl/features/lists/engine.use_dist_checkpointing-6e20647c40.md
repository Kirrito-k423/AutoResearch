# engine.use_dist_checkpointing

- **参数名**：`engine.use_dist_checkpointing`
- **分类**：效率
- **中文解释**：文档说明：Megatron/MCore engine 是否使用分布式 checkpoint；启用后按并行拓扑保存/加载分片权重或优化器状态，而不是集中式单体 checkpoint。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：主要影响保存、加载和恢复的 I/O 与内存峰值；超大模型使用分布式 checkpoint 可降低集中加载压力，但会增加分片元数据和拓扑匹配要求。
- **精度影响**：机制推断：不改变当前训练 step 的数学；若分布式 checkpoint 与 TP/PP/EP/DP 配置不匹配，可能导致恢复失败或续训状态不一致。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:63` engine.use_dist_checkpointing=False \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# actor_rollout_ref.actor.checkpoint.save_contents

- **参数名**：`actor_rollout_ref.actor.checkpoint.save_contents`
- **分类**：效率
- **中文解释**：文档说明：指定 Actor checkpoint 保存哪些内容，继承 Verl checkpoint 配置语义；常见内容包括 `model`、`optimizer`、`extra`，其中 `extra` 包含 RNG 等辅助恢复状态。Actor Megatron-FSDP 示例还说明 optimizer 单独保存不受支持，列出 optimizer 时应同时包含 model。
- **常见值**："${save_contents}"
- **来源环境变量**：无
- **性能影响**：文档说明：保存内容越多，checkpoint 写盘时间、存储空间和可能的分布式同步开销越高；只保存模型可降低 IO，但会牺牲完整断点续训能力。
- **精度影响**：机制推断：不影响当前 step 的训练数值；但恢复训练时若缺少 optimizer、scheduler 或 RNG/extra 状态，续训轨迹、学习率状态和可复现性会改变。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:108` actor_rollout_ref.actor.checkpoint.save_contents="${save_contents}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

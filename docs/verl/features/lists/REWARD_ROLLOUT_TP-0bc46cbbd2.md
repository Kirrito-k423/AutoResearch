# REWARD_ROLLOUT_TP

- **参数名**：`REWARD_ROLLOUT_TP`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `reward.reward_model.rollout.tensor_model_parallel_size`，控制奖励模型 rollout/inference engine 的张量并行度。
- **常见值**：1
- **来源环境变量**：REWARD_ROLLOUT_TP
- **性能影响**：文档说明：rollout TP 可切分推理模型权重和 KV 压力、扩大可承载模型/序列；TP 增大也会引入层内通信，特别是较高 TP 时通信成本需关注。
- **精度影响**：机制推断：正确的张量并行切分通常保持奖励模型数学结果等价；不同并行后端可能带来轻微数值差异，配置错误则可能启动失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:22` REWARD_ROLLOUT_TP=${REWARD_ROLLOUT_TP:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

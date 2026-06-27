# REWARD_PROMPT_LENGTH

- **参数名**：`REWARD_PROMPT_LENGTH`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `reward.reward_model.rollout.prompt_length`，设置奖励模型 rollout/推理侧可接收的 prompt token 长度上限；Mistral Nemo + SkyworkRM 示例默认 8192。
- **常见值**：8192
- **来源环境变量**：REWARD_PROMPT_LENGTH
- **性能影响**：机制推断：prompt 上限越长，奖励模型推理的 KV/cache、显存和 attention 计算成本越高；上限过低可省资源但会截断输入。
- **精度影响**：机制推断：过短会截断题目或上下文，影响奖励模型判断；足够长可保留信息，但过长主要增加成本而不一定提升奖励质量。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:23` REWARD_PROMPT_LENGTH=${REWARD_PROMPT_LENGTH:-8192}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

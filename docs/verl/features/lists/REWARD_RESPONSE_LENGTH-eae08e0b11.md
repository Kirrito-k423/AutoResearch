# REWARD_RESPONSE_LENGTH

- **参数名**：`REWARD_RESPONSE_LENGTH`
- **分类**：算法
- **中文解释**：文档说明：示例环境变量，写入 `reward.reward_model.rollout.response_length`，设置奖励模型 rollout/推理侧可处理的 response token 长度上限；Mistral Nemo + SkyworkRM 示例默认 4096。
- **常见值**：4096
- **来源环境变量**：REWARD_RESPONSE_LENGTH
- **性能影响**：机制推断：response 上限越长，奖励模型推理和打分的 token 处理、显存和延迟越高；上限过低可省资源但会截断回答。
- **精度影响**：机制推断：过短会截断模型答案或推理链，可能让奖励模型误判；足够长有助于完整评价，但过长会放大长答案成本和噪声。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:24` REWARD_RESPONSE_LENGTH=${REWARD_RESPONSE_LENGTH:-4096}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

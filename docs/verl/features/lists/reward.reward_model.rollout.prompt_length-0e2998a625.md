# reward.reward_model.rollout.prompt_length

- **参数名**：`reward.reward_model.rollout.prompt_length`
- **分类**：算法
- **中文解释**：reward model rollout 可接收的最大 prompt 长度；示例设为 `8192`，用于给奖励模型保留更长上下文输入。
- **常见值**：8192
- **来源环境变量**：REWARD_PROMPT_LENGTH
- **性能影响**：机制推断：最大 prompt 越长，reward model 推理的 prefill、KV cache 和显存需求越高，过大可能降低吞吐或触发 OOM。
- **精度影响**：机制推断：过小会截断奖励模型可见上下文，使评分缺少题目或对话信息；足够大时通常不改变评分目标，只影响是否能完整覆盖输入。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:76` reward.reward_model.rollout.prompt_length=${REWARD_PROMPT_LENGTH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

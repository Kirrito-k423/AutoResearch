# reward.reward_model.rollout.response_length

- **参数名**：`reward.reward_model.rollout.response_length`
- **分类**：算法
- **中文解释**：reward model rollout 的最大 response 长度；示例设为 `4096`，用于限定奖励模型处理/生成响应部分的 token 预算。
- **常见值**：4096
- **来源环境变量**：REWARD_RESPONSE_LENGTH
- **性能影响**：机制推断：长度越大，reward model 的解码或打分序列越长，KV cache、显存和单样本延迟都会上升。
- **精度影响**：机制推断：过小会截断候选回答，可能让奖励模型看不到完整推理或最终答案；足够覆盖真实回答后通常不直接改变奖励目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:77` reward.reward_model.rollout.response_length=${REWARD_RESPONSE_LENGTH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

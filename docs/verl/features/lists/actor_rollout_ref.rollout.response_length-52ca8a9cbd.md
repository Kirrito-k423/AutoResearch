# actor_rollout_ref.rollout.response_length

- **参数名**：`actor_rollout_ref.rollout.response_length`
- **分类**：效率
- **中文解释**：文档说明：rollout 侧 response 最大生成长度，通常继承 `data.max_response_length`。RL rollout 会最多生成到这个长度，用它限制答案、推理链或工具响应后的模型输出预算。
- **常见值**："${RESPONSE_LENGTH}"、8192
- **来源环境变量**：MAX_RESPONSE_LENGTH
- **性能影响**：机制推断：response 长度越大，decode token 数、KV cache、reward/logprob 计算和训练样本张量长度通常近似上升；过大降低吞吐，过小提高截断概率。
- **精度影响**：文档说明：该长度决定模型可完成答案的最大空间；过短会截断长推理或代码/数学答案，过长则可能引入冗余输出并改变长度相关奖励。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:185` actor_rollout_ref.rollout.response_length=${max_response_length}
- `examples/generation/run_deepseek_llm_7b.sh:41` actor_rollout_ref.rollout.response_length="${RESPONSE_LENGTH}" \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

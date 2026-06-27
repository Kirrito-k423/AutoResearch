# actor_rollout_ref.rollout.prompt_length

- **参数名**：`actor_rollout_ref.rollout.prompt_length`
- **分类**：效率
- **中文解释**：文档说明：rollout 侧 prompt 最大长度，通常继承 `data.max_prompt_length`。它决定生成/打分时为输入问题、上下文或多模态 prompt 预留的 token 长度预算。
- **常见值**："${PROMPT_LENGTH}"、2048
- **来源环境变量**：MAX_PROMPT_LENGTH
- **性能影响**：机制推断：prompt 长度越大，prefill 计算、KV cache 和显存占用越高，也会挤占同一 `max_model_len` 下 response 空间；过小可提升吞吐但可能丢上下文。
- **精度影响**：文档说明：超长 prompt 处理与 `data.max_prompt_length`/truncation 直接相关；长度不足会截断或拒绝长样本，改变任务上下文和训练数据分布。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:184` actor_rollout_ref.rollout.prompt_length=${max_prompt_length}
- `examples/generation/run_deepseek_llm_7b.sh:40` actor_rollout_ref.rollout.prompt_length="${PROMPT_LENGTH}" \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

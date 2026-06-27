# PROMPT_LENGTH

- **参数名**：`PROMPT_LENGTH`
- **分类**：效率
- **中文解释**：机制推断：generation server 示例中的输入 prompt token 长度上限，写入 `actor_rollout_ref.rollout.prompt_length`。
- **常见值**：2048
- **来源环境变量**：PROMPT_LENGTH
- **性能影响**：机制推断：更长 prompt 会增加预填充计算、KV cache 和显存占用；过小可提升吞吐但会限制可处理上下文。
- **精度影响**：机制推断：上限过低会截断或拒绝长输入，损失题目上下文；合理增大可保留更多上下文，但不直接改变模型参数。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:21` PROMPT_LENGTH=${PROMPT_LENGTH:-2048}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

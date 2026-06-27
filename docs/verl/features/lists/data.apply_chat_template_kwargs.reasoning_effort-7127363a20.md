# data.apply_chat_template_kwargs.reasoning_effort

- **参数名**：`data.apply_chat_template_kwargs.reasoning_effort`
- **分类**：效率
- **中文解释**：机制推断：传给 tokenizer/processor `apply_chat_template` 的模型特定参数；GPT-OSS 示例用它设置 reasoning effort，并提示 high reasoning effort 需要更大的 `max_response_length`。
- **常见值**：medium
- **来源环境变量**：REASONING_EFFORT
- **性能影响**：机制推断：更高 reasoning effort 往往让模板诱导更长推理输出，增加生成 token、KV cache 和 rollout 时间；medium/low 可降低 token 成本但可能减少推理深度。
- **精度影响**：机制推断：对支持该模板字段的模型，reasoning effort 会影响回答风格和推理长度，可能提升复杂推理题表现；若 token 预算不足，高 effort 反而更容易截断。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:78` +data.apply_chat_template_kwargs.reasoning_effort=${REASONING_EFFORT}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

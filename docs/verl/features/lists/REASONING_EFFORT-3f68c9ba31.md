# REASONING_EFFORT

- **参数名**：`REASONING_EFFORT`
- **分类**：效率
- **中文解释**：机制推断：传给 `data.apply_chat_template_kwargs.reasoning_effort` 的 chat template 参数；在 GPT-OSS 示例中用于控制模板生成的 reasoning effort 档位，默认 `medium`。
- **常见值**：medium
- **来源环境变量**：REASONING_EFFORT
- **性能影响**：机制推断：更高 reasoning effort 可能让模板诱导更长推理或更大响应预算需求，增加生成 token、耗时和显存/KV cache 压力。
- **精度影响**：机制推断：会改变训练/rollout prompt 的模板语义和推理风格，可能影响复杂推理任务表现；不是 Verl 优化器本身的精度参数。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:17` REASONING_EFFORT=${REASONING_EFFORT:-medium}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

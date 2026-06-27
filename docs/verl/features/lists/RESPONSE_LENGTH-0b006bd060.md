# RESPONSE_LENGTH

- **参数名**：`RESPONSE_LENGTH`
- **分类**：效率
- **中文解释**：机制推断：generation server 示例中的生成响应 token 长度上限，写入 `actor_rollout_ref.rollout.response_length`。
- **常见值**：1024
- **来源环境变量**：RESPONSE_LENGTH
- **性能影响**：机制推断：响应上限越长，解码步数、KV cache、输出存储和端到端生成耗时越高；较短上限可提升吞吐但容易截断输出。
- **精度影响**：机制推断：更长响应允许复杂推理和完整答案，过短会截断解题过程；过长则可能增加冗长、跑题或评测成本。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:22` RESPONSE_LENGTH=${RESPONSE_LENGTH:-1024}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

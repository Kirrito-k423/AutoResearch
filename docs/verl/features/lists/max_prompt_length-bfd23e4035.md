# max_prompt_length

- **参数名**：`max_prompt_length`
- **分类**：效率
- **中文解释**：控制 prompt 最大长度，增大可覆盖更长输入，但会增加激活、注意力和数据处理成本。
- **常见值**：512
- **来源环境变量**：max_prompt_length
- **性能影响**：机制推断：长度越大，显存、KV cache 和单步/生成耗时通常上升。
- **精度影响**：机制推断：改变有效上下文、输出空间或样本保留策略，可能影响任务准确率。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:49` max_prompt_length=${max_prompt_length:-512}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

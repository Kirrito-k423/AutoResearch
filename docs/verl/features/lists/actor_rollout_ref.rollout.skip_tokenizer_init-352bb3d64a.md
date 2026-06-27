# actor_rollout_ref.rollout.skip_tokenizer_init

- **参数名**：`actor_rollout_ref.rollout.skip_tokenizer_init`
- **分类**：配置
- **中文解释**：rollout engine 启动时是否跳过 tokenizer 初始化；router replay 示例设为 `True`，官方 Ascend 参数表也将其描述为“是否跳过分词器初始化”。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：跳过 tokenizer 初始化可减少 rollout engine 启动/内存开销，适合由 Verl 外部流程已完成 tokenization 的场景；若后端仍需要 tokenizer 功能，可能导致运行失败。
- **精度影响**：机制推断：不改变采样算法；但在需要文本到 token 或 chat template 的路径上错误跳过 tokenizer，可能造成输入处理不一致或直接报错。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:165` actor_rollout_ref.rollout.skip_tokenizer_init=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

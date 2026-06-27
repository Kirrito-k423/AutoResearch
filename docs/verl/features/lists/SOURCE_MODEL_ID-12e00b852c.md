# SOURCE_MODEL_ID

- **参数名**：`SOURCE_MODEL_ID`
- **分类**：效率
- **中文解释**：指定 GPT-OSS 示例要从 Hugging Face/模型仓下载并转换的源模型 ID；脚本默认 `openai/gpt-oss-20b`，随后用 Transformers 加载并保存到本地 `MODEL_DIR` 供 Verl 训练使用。
- **常见值**：openai/gpt-oss-20b
- **来源环境变量**：SOURCE_MODEL_ID
- **性能影响**：机制推断：源模型决定下载体积、加载/反量化耗时、显存需求和后续 rollout/训练成本；更换为更大或不同格式模型会显著改变启动与运行资源。
- **精度影响**：机制推断：源模型权重和 tokenizer 直接决定训练初始能力与输出分布；换模型会改变基线精度、可训练性和与脚本中 `reasoning_effort` 等配置的兼容性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:4` SOURCE_MODEL_ID=${SOURCE_MODEL_ID:-openai/gpt-oss-20b}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

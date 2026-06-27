# OUTPUT_PATH

- **参数名**：`OUTPUT_PATH`
- **分类**：配置
- **中文解释**：生成示例的输出 parquet 路径，脚本将其写入 `+data.output_path`，用于保存 rollout-only generation 的结果。
- **常见值**：$HOME/data/gsm8k/deepseek_llm_7b_gen_test.parquet
- **来源环境变量**：OUTPUT_PATH
- **性能影响**：机制推断：主要影响结果写盘阶段；输出目录在慢盘、远程盘或空间不足时会增加端到端耗时或导致任务失败。
- **精度影响**：机制推断：不改变生成内容；但覆盖旧文件、写到错误路径或后处理读取错结果会影响评测口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/generation/run_deepseek_llm_7b.sh`

## 证据片段

- `examples/generation/run_deepseek_llm_7b.sh:19` OUTPUT_PATH=${OUTPUT_PATH:-$HOME/data/gsm8k/deepseek_llm_7b_gen_test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

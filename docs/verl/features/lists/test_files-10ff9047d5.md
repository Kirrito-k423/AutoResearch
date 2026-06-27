# test_files

- **参数名**：`test_files`
- **分类**：配置
- **中文解释**：指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。
- **常见值**："['$gsm8k_test_path', '$math_test_path']"、$HOME/data/geo3k/test.parquet
- **来源环境变量**：test_files
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:26` test_files=${test_files:-"['$gsm8k_test_path', '$math_test_path']"}
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:38` test_files=${test_files:-$HOME/data/geo3k/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# VAL_FILES

- **参数名**：`VAL_FILES`
- **分类**：配置
- **中文解释**：指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。
- **常见值**：$HOME/data/gsm8k_sft/test.parquet、${AIME_VAL:-${DATA_DIR
- **来源环境变量**：VAL_FILES
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:25` val_files=${VAL_FILES:-${AIME_VAL:-${DATA_DIR}/data/AIME-2024/data/aime-2024.parquet}}
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:9` VAL_FILES=${VAL_FILES:-$HOME/data/gsm8k_sft/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

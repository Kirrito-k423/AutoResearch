# TRAIN_FILES

- **参数名**：`TRAIN_FILES`
- **分类**：配置
- **中文解释**：指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。
- **常见值**：$HOME/data/gsm8k_sft/train.parquet、${DAPO_MATH_TRAIN:-${DATA_DIR、${DATASET_DIR
- **来源环境变量**：TRAIN_FILES
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:24` train_files=${TRAIN_FILES:-${DAPO_MATH_TRAIN:-${DATA_DIR}/data/DAPO-Math-17k/data/dapo-math-17k.parquet}}
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:8` TRAIN_FILES=${TRAIN_FILES:-$HOME/data/gsm8k_sft/train.parquet}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:47` TRAIN_FILES=${TRAIN_FILES:-${DATASET_DIR}/train.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

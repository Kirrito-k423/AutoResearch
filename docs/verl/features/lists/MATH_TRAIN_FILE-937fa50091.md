# MATH_TRAIN_FILE

- **参数名**：`MATH_TRAIN_FILE`
- **分类**：配置
- **中文解释**：指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。
- **常见值**：$HOME/data/math/train.parquet
- **来源环境变量**：MATH_TRAIN_FILE
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:40` MATH_TRAIN_FILE=${MATH_TRAIN_FILE:-$HOME/data/math/train.parquet}
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:39` MATH_TRAIN_FILE=${MATH_TRAIN_FILE:-$HOME/data/math/train.parquet}
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:42` math_train=${MATH_TRAIN_FILE:-$HOME/data/math/train.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

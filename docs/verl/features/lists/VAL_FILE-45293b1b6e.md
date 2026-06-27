# VAL_FILE

- **参数名**：`VAL_FILE`
- **分类**：配置
- **中文解释**：文档说明：examples 中用于指定验证集 parquet 路径的环境变量，通常传入 `data.val_files` 或脚本内 `val_file`，决定训练/评测时读取哪份验证数据。
- **常见值**：$HOME/data/aime-2024/test.parquet、$HOME/data/geo3k/test.parquet
- **来源环境变量**：VAL_FILE
- **性能影响**：机制推断：不改变训练前后向计算；验证集越大或存储越慢，验证阶段 I/O、生成和指标计算耗时越高。
- **精度影响**：机制推断：不改变训练更新本身，但会直接决定验证指标和人工观察样本的分布；错误路径或口径不一致会导致指标不可比。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:53` val_file=${VAL_FILE:-$HOME/data/aime-2024/test.parquet}
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:44` val_file=${VAL_FILE:-$HOME/data/aime-2024/test.parquet}
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:38` val_file=${VAL_FILE:-$HOME/data/aime-2024/test.parquet}
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:47` val_file=${VAL_FILE:-$HOME/data/aime-2024/test.parquet}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:59` val_file=${VAL_FILE:-$HOME/data/aime-2024/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

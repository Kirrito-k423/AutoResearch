# math_test_path

- **参数名**：`math_test_path`
- **分类**：配置
- **中文解释**：MATH 验证/测试集 parquet 路径；示例把它与 `gsm8k_test_path` 组装成 `test_files`，再传给 `data.val_files` 用于评测。
- **常见值**：$HOME/data/math/test.parquet
- **来源环境变量**：math_test_path
- **性能影响**：文档说明：`data.val_files` 是验证 parquet，可为单个文件或列表；路径本身不改变训练算子，但验证集大小和存储位置会影响评测加载与端到端耗时。
- **精度影响**：机制推断：通常不直接参与训练梯度；但它改变 MATH 评测口径，并可能影响基于验证结果进行 checkpoint 选择或实验比较的判断。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:23` math_test_path=${math_test_path:-$HOME/data/math/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

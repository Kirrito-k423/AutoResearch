# TEST_DATA_PATH

- **参数名**：`TEST_DATA_PATH`
- **分类**：配置
- **中文解释**：router replay 示例中的验证/测试 parquet 路径，脚本将其传给 `data.val_files`。
- **常见值**：$HOME/data/gsm8k/test.parquet
- **来源环境变量**：TEST_DATA_PATH
- **性能影响**：机制推断：影响验证数据读取和评测耗时；大文件、慢盘或远程路径会增加验证阶段时间。
- **精度影响**：机制推断：不改变训练更新本身，但决定验证集口径；路径错误会让指标不可比或失真。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:19` TEST_DATA_PATH=${TEST_DATA_PATH:-$HOME/data/gsm8k/test.parquet}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

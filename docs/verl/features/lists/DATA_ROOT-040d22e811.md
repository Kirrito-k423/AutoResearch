# DATA_ROOT

- **参数名**：`DATA_ROOT`
- **分类**：效率
- **中文解释**：文档说明：数据根目录变量，Ascend/示例文档常用它拼接数据集、checkpoint 或评测数据路径；batch-12 命中的 VLM SFT 脚本也把它作为可覆盖的本地根路径。
- **常见值**：$PWD
- **来源环境变量**：DATA_ROOT
- **性能影响**：机制推断：目录变量本身不改变计算；若指向慢速存储，会影响数据读取、预处理和 checkpoint I/O。
- **精度影响**：机制推断：不直接改变优化目标；当它指向不同数据集或标注版本时，会改变训练/验证样本来源。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:6` DATA_ROOT=${DATA_ROOT:-$PWD}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

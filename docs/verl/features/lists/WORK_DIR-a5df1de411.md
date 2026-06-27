# WORK_DIR

- **参数名**：`WORK_DIR`
- **分类**：配置
- **中文解释**：机制推断：示例脚本的工作根目录，Qwen3-Next 等脚本用它组织模型目录、数据集目录和运行产物路径。
- **常见值**："${HOME
- **来源环境变量**：WORK_DIR
- **性能影响**：机制推断：不直接改变训练算子性能；若该目录位于慢速存储，会影响模型/数据读取、checkpoint I/O 和启动速度。
- **精度影响**：机制推断：工作目录本身不改变精度，但它决定读取哪个模型权重和数据文件；目录内容变化会改变初始化与数据口径。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:11` WORK_DIR=${WORK_DIR:-"${HOME}/verl"}
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:8` WORK_DIR=${WORK_DIR:-"${HOME}/verl"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

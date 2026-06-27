# RAY_DATA_HOME

- **参数名**：`RAY_DATA_HOME`
- **分类**：效率
- **中文解释**：机制推断：examples 使用的本地或共享数据根目录，常用于拼接模型、数据和 checkpoint 路径，如 `${RAY_DATA_HOME}/data/...`、`${RAY_DATA_HOME}/ckpts/...`。
- **常见值**："${HOME
- **来源环境变量**：RAY_DATA_HOME
- **性能影响**：机制推断：不改变计算图；目录所在存储的吞吐和延迟会影响数据读取、模型加载以及 checkpoint 保存/恢复。
- **精度影响**：机制推断：路径本身不影响精度；若指向不同数据集、模型权重或 checkpoint，会直接改变实验输入和结果。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:53` RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl"}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:21` RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl"}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:11` RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl"}
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:21` RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl"}
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:27` RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

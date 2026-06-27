# NDEVICES_PER_NODE

- **参数名**：`NDEVICES_PER_NODE`
- **分类**：效率
- **中文解释**：文档说明：examples 的用户可调环境变量，表示每节点设备数/本地进程数，常用于派生 `trainer.n_gpus_per_node`、rollout 设备数或 `torchrun --nproc_per_node`。
- **常见值**：16、8
- **来源环境变量**：NDEVICES_PER_NODE
- **性能影响**：机制推断：设备数越多通常提高并行吞吐和显存容量，但也增加跨卡通信；需要与 TP/PP/EP/DP 等并行度匹配。
- **精度影响**：机制推断：设备数本身不改变目标；若导致全局 batch、随机种子、数据切分或并行配置变化，会间接影响收敛和可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:12` NDEVICES_PER_NODE=${NDEVICES_PER_NODE:-}
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:45` n_devices_per_node=${NDEVICES_PER_NODE:-8}
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:14` NDEVICES_PER_NODE=${NDEVICES_PER_NODE:-}
- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:44` n_devices_per_node=${NDEVICES_PER_NODE:-8}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:16` NDEVICES_PER_NODE=${NDEVICES_PER_NODE:-}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

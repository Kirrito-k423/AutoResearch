# NPUS_PER_NODE

- **参数名**：`NPUS_PER_NODE`
- **分类**：效率
- **中文解释**：文档说明：Ascend/NPU examples 中用于声明每个节点可用 NPU 数，并传给 Ray resources 与 `trainer.n_gpus_per_node`；需要与实际机器资源和 `NNODES` 配套。
- **常见值**：16、8
- **来源环境变量**：NPUS_PER_NODE
- **性能影响**：机制推断：增加每节点 NPU 数可扩大并行资源和总吞吐，但也提高集合通信、Ray 调度和跨卡同步压力；设置不匹配会导致资源申请失败或挂起。
- **精度影响**：机制推断：资源数不直接改变算法；但若改变全局 batch、并行切分或随机种子同步路径，可能带来训练稳定性和可复现性差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：7
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh`
- `examples/profile/run_qwen3_8b_npu_profile_e2e.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:26` NPUS_PER_NODE=${NPUS_PER_NODE:-}
- `examples/profile/run_qwen3_8b_npu_profile_e2e.sh:14` NPUS_PER_NODE=${NPUS_PER_NODE:-8}
- `examples/profile/run_qwen3_8b_npu_profile_discrete.sh:14` NPUS_PER_NODE=${NPUS_PER_NODE:-8}
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:23` NPUS_PER_NODE=${NPUS_PER_NODE:-16}
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:20` NPUS_PER_NODE=${NPUS_PER_NODE:-16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

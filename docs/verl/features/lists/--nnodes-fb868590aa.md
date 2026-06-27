# --nnodes

- **参数名**：`--nnodes`
- **分类**：效率
- **中文解释**：文档说明：`torchrun` 的节点数量参数，控制多节点训练启动规模；示例中可固定为 1，也可由 `${NNODES}` 注入。
- **常见值**：${NNODES}、1
- **来源环境变量**：无
- **性能影响**：机制推断：增加节点可扩大 GPU 数和并行规模，但会引入跨节点通信、同步、启动协调和故障恢复开销；资源数不匹配会导致挂起或启动失败。
- **精度影响**：机制推断：节点数本身不直接改变算法；若随之改变全局 batch、数据并行度或随机种子划分，可能间接影响优化轨迹和可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:26` torchrun --nnodes=1 --nproc_per_node=${nproc_per_node} \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:74` torchrun --nnodes=1 --nproc_per_node=8 ${ENTRYPOINT} \
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:131` --nnodes=${NNODES} \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

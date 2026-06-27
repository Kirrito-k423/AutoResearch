# --nproc_per_node

- **参数名**：`--nproc_per_node`
- **分类**：效率
- **中文解释**：文档说明：`torchrun` 每个节点启动的进程数/设备进程数；官方 checkpoint 文档在分布式合并 Megatron checkpoint 时用 `torchrun --nproc_per_node 1 --nnodes 8 ...` 示例说明其控制本节点 worker 数。
- **常见值**：$NPROC、$nproc_per_node、${NUM_GPUS}、${nproc_per_node}、8
- **来源环境变量**：无
- **性能影响**：机制推断：通常应匹配本节点可用 GPU/NPU 数或合并任务需要的 worker 数；过低浪费设备，过高会争抢显存/端口并导致启动失败。
- **精度影响**：机制推断：不改变算法；但进程数决定分布式拓扑和 checkpoint shard 读取方式，配置错误会导致训练/合并失败或状态不完整。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：12
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh`

## 证据片段

- `examples/sft/multiturn/run_qwen2_5_0_5b_fsdp.sh:26` torchrun --nnodes=1 --nproc_per_node=${nproc_per_node} \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:73` torchrun --standalone --nnodes=1 --nproc_per_node=$NPROC \
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:17` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:16` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh:14` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

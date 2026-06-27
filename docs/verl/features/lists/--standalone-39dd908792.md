# --standalone

- **参数名**：`--standalone`
- **分类**：效率
- **中文解释**：文档说明：Verl SFT examples 通过 `torchrun --standalone --nnodes=1` 启动单机分布式训练；这是启动器参数，不是 Verl Hydra 配置。
- **常见值**：--nnodes=1
- **来源环境变量**：无
- **性能影响**：机制推断：用于单机 rendezvous，通常不改变模型每步吞吐；与 `--nproc_per_node`/设备数结合决定启动的本地进程规模。
- **精度影响**：机制推断：启动方式本身不改变算法；进程数、数据并行和随机性变化会间接影响有效 batch、数据顺序与可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh`
- `examples/sft/gsm8k/run_gemma_7b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen2_5_0_5b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_8b_fsdp.sh`
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh`
- `examples/sft/gsm8k/run_seed_oss_36b_fsdp.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:79` torchrun --standalone --nnodes=1 --nproc-per-node=${NUM_TRAINERS:-8} \
- `examples/sft/gsm8k/run_qwen_megatron_fsdp.sh:73` torchrun --standalone --nnodes=1 --nproc_per_node=$NPROC \
- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:17` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
- `examples/sft/gsm8k/run_gemma_2b_fsdp.sh:16` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
- `examples/sft/gsm8k/run_deepseek_coder_6_7b_fsdp.sh:14` torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

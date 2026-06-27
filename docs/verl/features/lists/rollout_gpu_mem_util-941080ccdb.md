# rollout_gpu_mem_util

- **参数名**：`rollout_gpu_mem_util`
- **分类**：效率
- **中文解释**：控制 rollout engine 可使用的显存比例，影响 KV cache 容量、吞吐和 OOM 风险。
- **常见值**：0.6
- **来源环境变量**：rollout_gpu_mem_util
- **性能影响**：文档说明：`gpu_memory_utilization` 越高，rollout 后端可用于权重/KV cache/静态内存的比例越高，通常能提升并发和吞吐；过高会增加 OOM 风险，官方 perf 文档建议按后端调优，0.5-0.7 常较均衡，offload 后 0.8-0.9 也常见。
- **精度影响**：机制推断：显存比例本身不改变采样分布或训练目标；但过低可能限制 KV cache/并发并诱发更保守的长度或 batch 设置，过高 OOM 则会影响实验完成率。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:42` rollout_gpu_mem_util=${rollout_gpu_mem_util:-0.6}
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:73` rollout_gpu_mem_util=${rollout_gpu_mem_util:-0.6}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# rollout_tp

- **参数名**：`rollout_tp`
- **分类**：效率
- **中文解释**：示例脚本中的 rollout tensor parallel size，通常传入 `actor_rollout_ref.rollout.tensor_model_parallel_size`，控制推理模型张量切分到多少张卡。
- **常见值**：2、4
- **来源环境变量**：rollout_tp
- **性能影响**：文档说明：Verl 性能调优文档指出较小 TP 可产生更多 DP rollout 副本并提升吞吐，但会增加 KV cache 占用；较大 TP 降低单卡模型显存但增加层内通信。
- **精度影响**：机制推断：张量并行只改变推理切分方式，不应改变生成分布；浮点归约顺序差异通常很小。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:41` rollout_tp=${rollout_tp:-2}
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:72` rollout_tp=${rollout_tp:-2}
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh:105` rollout_tp=${rollout_tp:-4}
- `examples/router_replay/run_qwen3_30b_a3b_megatron.sh:53` rollout_tp=${rollout_tp:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

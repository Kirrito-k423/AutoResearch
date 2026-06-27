# actor_rollout_ref.rollout.data_parallel_size

- **参数名**：`actor_rollout_ref.rollout.data_parallel_size`
- **分类**：效率
- **中文解释**：文档说明：rollout 推理侧数据并行大小，参数表默认 1；examples 对大模型或 VeOmni 等场景设置为 8、32 或 `$infer_dp`。
- **常见值**：$infer_dp、${ROLLOUT_DP:-8}、${ROLLOUT_DP}、1、32、8
- **来源环境变量**：ROLLOUT_DP
- **性能影响**：机制推断：增加 rollout DP 可并行处理更多 prompt，提高生成吞吐，但会复制模型/缓存或与 TP/EP 竞争设备资源。
- **精度影响**：机制推断：数据并行本身不改变采样分布；改变并行切分可能影响样本顺序、随机种子和吞吐-新鲜度，间接影响可复现性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：9
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:112` actor_rollout_ref.rollout.data_parallel_size=$infer_dp \
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:114` actor_rollout_ref.rollout.data_parallel_size=$infer_dp \
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh:76` actor_rollout_ref.rollout.data_parallel_size=8
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:107` actor_rollout_ref.rollout.data_parallel_size=$infer_dp \
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:171` actor_rollout_ref.rollout.data_parallel_size=${ROLLOUT_DP:-8}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

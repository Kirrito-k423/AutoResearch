# actor_rollout_ref.rollout.max_model_len

- **参数名**：`actor_rollout_ref.rollout.max_model_len`
- **分类**：效率
- **中文解释**：文档说明：设置 rollout 推理后端可接收的最大序列长度；Verl/NPU 文档将其解释为模型最大序列长度，examples 通常设为 `max_prompt_length + max_response_length` 或再加余量。
- **常见值**：$(( max_prompt_length + max_response_length + 1 ))、$((max_prompt_length + max_response_length))、$max_model_len、10240
- **来源环境变量**：ROLLOUT_MAX_MODEL_LEN
- **性能影响**：机制推断：长度越大，KV cache、调度预留和 decode/prefill 时间通常上升；过小会限制 batch token 上限或导致长样本无法进入 rollout。
- **精度影响**：机制推断：足够覆盖 prompt+response 时不直接影响精度；设得过小会截断/拒绝长样本，改变训练或评测数据分布。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_vl_8b_fsdp.sh:78` actor_rollout_ref.rollout.max_model_len=${max_num_tokens}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:84` actor_rollout_ref.rollout.max_model_len=${max_num_tokens}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:91` actor_rollout_ref.rollout.max_model_len=${max_num_tokens}
- `examples/on_policy_distillation_trainer/run_qwen3_8b_megatron.sh:88` actor_rollout_ref.rollout.max_model_len=${max_num_tokens}
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:122` actor_rollout_ref.rollout.max_model_len=$max_model_len \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# actor_rollout_ref.rollout.enforce_eager

- **参数名**：`actor_rollout_ref.rollout.enforce_eager`
- **分类**：效率
- **中文解释**：文档说明：vLLM rollout 是否强制 eager 执行；设为 False 时可使用 CUDA graph，设为 True 时禁用 CUDA graph，通常用于显存紧张或图捕获不稳定场景。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：文档说明：`enforce_eager=False` 允许 CUDA graph 提速但会占用额外显存；`True` 可缓解显存压力但通常牺牲部分推理吞吐。
- **精度影响**：机制推断：不改变模型权重或采样参数；但图模式/显存配置导致的 OOM、回退或 batch 变小会间接影响运行稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：23
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_4b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_8b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh:111` actor_rollout_ref.rollout.enforce_eager=False
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:76` actor_rollout_ref.rollout.enforce_eager=False
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:122` actor_rollout_ref.rollout.enforce_eager=True
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:118` actor_rollout_ref.rollout.enforce_eager=False
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:136` actor_rollout_ref.rollout.enforce_eager=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

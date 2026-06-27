# actor_rollout_ref.ref.megatron.dist_checkpointing_path

- **参数名**：`actor_rollout_ref.ref.megatron.dist_checkpointing_path`
- **分类**：配置
- **中文解释**：文档说明：reference model 的 Megatron 分布式 checkpoint 加载路径；用于在 `ref.megatron.use_dist_checkpointing=True` 时读取参考模型分片权重。
- **常见值**：$DIST_CKPT_PATH、${MCORE_MODEL_PATH}、${WORK_DIR}、Qwen/Qwen3-30B-A3B-mcore
- **来源环境变量**：MCORE_MODEL_PATH
- **性能影响**：文档说明：主要影响 ref 模型启动/恢复时的 I/O 和内存峰值；对训练 step 的前后向吞吐影响较小，但大模型 ref 加载错误会导致作业无法开始。
- **精度影响**：机制推断：路径决定 ref 权重来源；错误或过期 checkpoint 会改变参考策略 logprob/KL，影响 RL 约束和最终训练轨迹。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:89` actor_rollout_ref.ref.megatron.dist_checkpointing_path=$DIST_CKPT_PATH
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:251` actor_rollout_ref.ref.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:184` actor_rollout_ref.ref.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:153` actor_rollout_ref.ref.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:154` actor_rollout_ref.ref.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

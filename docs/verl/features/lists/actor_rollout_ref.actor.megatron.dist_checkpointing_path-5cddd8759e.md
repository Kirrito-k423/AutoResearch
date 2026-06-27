# actor_rollout_ref.actor.megatron.dist_checkpointing_path

- **参数名**：`actor_rollout_ref.actor.megatron.dist_checkpointing_path`
- **分类**：配置
- **中文解释**：文档说明：actor Megatron 分布式 checkpoint 的加载路径；当 `use_dist_checkpointing=True` 时，Verl 会从该路径读取 MCore/Megatron 分片权重。
- **常见值**：$DIST_CKPT_PATH、${MCORE_MODEL_PATH}、${WORK_DIR}、Qwen/Qwen3-30B-A3B-mcore
- **来源环境变量**：MCORE_MODEL_PATH
- **性能影响**：文档说明：主要影响启动/恢复时的 I/O、并行文件系统压力和内存峰值；路径指向本地高速盘、共享盘或远端挂载会显著影响恢复耗时。
- **精度影响**：机制推断：路径本身不改变算法，但它决定实际加载哪份 actor 权重；错误路径、旧 checkpoint 或分片不匹配会直接改变训练初始点和 rollout 行为。
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

- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:67` actor_rollout_ref.actor.megatron.dist_checkpointing_path=$DIST_CKPT_PATH
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:249` actor_rollout_ref.actor.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh:182` actor_rollout_ref.actor.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:127` actor_rollout_ref.actor.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}
- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh:124` actor_rollout_ref.actor.megatron.dist_checkpointing_path=${MCORE_MODEL_PATH}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

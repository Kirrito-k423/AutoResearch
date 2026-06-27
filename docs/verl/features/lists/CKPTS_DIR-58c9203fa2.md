# CKPTS_DIR

- **参数名**：`CKPTS_DIR`
- **分类**：配置
- **中文解释**：机制推断：示例脚本中用于组装 `trainer.default_local_dir` 或 checkpoint 目录的环境变量，常由 `${RAY_DATA_HOME}/ckpts/<project>/<exp>` 派生。
- **常见值**："${HOME、"${RAY_DATA_HOME、.ckpt
- **来源环境变量**：CKPTS_DIR
- **性能影响**：机制推断：不改变每步计算；目录所在磁盘或网络文件系统会影响保存、恢复和 checkpoint 清理耗时。
- **精度影响**：机制推断：路径本身不影响精度；但错误目录可能导致未能恢复目标 checkpoint、覆盖旧 checkpoint 或从头训练，影响可复现性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：11
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_235b_a22b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:54` CKPTS_DIR=${CKPTS_DIR:-"${RAY_DATA_HOME}/ckpts/${project_name}/${experiment_name}"}
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:23` CKPTS_DIR=${CKPTS_DIR:-"${RAY_DATA_HOME}/ckpts/${PROJECT_NAME}/${EXPERIMENT_NAME}"}
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:59` CKPTS_DIR=${CKPTS_DIR:-"${HOME}/verl/ckpts/${project_name}/${experiment_name}"}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:13` CKPTS_DIR=${CKPTS_DIR:-}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:77` ckpts_dir=${CKPTS_DIR:-"${RAY_DATA_HOME}/ckpts/${PROJECT_NAME}/${EXPERIMENT_NAME}"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

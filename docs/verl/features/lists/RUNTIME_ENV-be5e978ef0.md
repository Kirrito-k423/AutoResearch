# RUNTIME_ENV

- **参数名**：`RUNTIME_ENV`
- **分类**：效率
- **中文解释**：文档说明：`RUNTIME_ENV` 指向 Ray job 的 runtime env YAML，examples 默认使用 `verl/trainer/runtime_env.yaml`，其中声明 `working_dir`、排除 `.git` 以及 NCCL/HCCL 等环境变量。
- **常见值**："${WORKING_DIR
- **来源环境变量**：RUNTIME_ENV
- **性能影响**：文档说明：runtime env 会影响 Ray 作业启动、代码分发和通信环境变量；正确设置可改善多机启动/通信可靠性，错误路径或不合适的 env var 会导致提交失败或通信异常。
- **精度影响**：机制推断：通常不直接影响精度；只有当 runtime env 改变后端、通信或确定性相关环境变量时，才可能间接改变数值行为。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:27` RUNTIME_ENV=${RUNTIME_ENV:-"${WORKING_DIR}/verl/trainer/runtime_env.yaml"}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:17` RUNTIME_ENV=${RUNTIME_ENV:-"${WORKING_DIR}/verl/trainer/runtime_env.yaml"}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:54` RUNTIME_ENV=${RUNTIME_ENV:-"${WORKING_DIR}/verl/verl/trainer/runtime_env.yaml"}
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:27` RUNTIME_ENV=${RUNTIME_ENV:-"${WORKING_DIR}/verl/trainer/runtime_env.yaml"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

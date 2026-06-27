# WORKING_DIR

- **参数名**：`WORKING_DIR`
- **分类**：配置
- **中文解释**：文档说明：Ray job / runtime-env 使用的工作目录，示例默认 `${PWD}`，并通过 `--working-dir "${WORKING_DIR}"` 把 Verl 代码和运行环境提交给 Ray。
- **常见值**："${PWD
- **来源环境变量**：WORKING_DIR
- **性能影响**：机制推断：目录本身不改变训练吞吐；如果工作目录很大、位于慢盘或远程同步较慢，会增加 Ray job 打包、上传和启动耗时。
- **精度影响**：机制推断：通常不直接影响精度；只有当它指向了错误版本的代码、配置或数据目录时，才会改变实验结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:26` WORKING_DIR=${WORKING_DIR:-"${PWD}"}
- `examples/grpo_trainer/run_qwen3_vl_30b_a3b_fsdp.sh:16` WORKING_DIR=${WORKING_DIR:-"${PWD}"}
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:53` WORKING_DIR=${WORKING_DIR:-"${PWD}"}
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:26` WORKING_DIR=${WORKING_DIR:-"${PWD}"}

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

# --config-path

- **参数名**：`--config-path`
- **分类**：配置
- **中文解释**：文档说明：Hydra 启动参数，用于指定配置目录（如 `config` 或 `./config`），与 `--config-name` 一起定位 trainer YAML。
- **常见值**："$CONFIG_PATH"、./config、config
- **来源环境变量**：无
- **性能影响**：机制推断：仅影响配置解析路径，通常不影响吞吐；路径错误会启动失败或加载非预期配置。
- **精度影响**：机制推断：本身不改变算法；加载了错误目录中的同名配置会改变超参和训练结果。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：10
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:63` --config-path=config \
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:124` --config-path=./config
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:132` --config-path=./config
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:101` --config-path=config \
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:119` --config-path=./config

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

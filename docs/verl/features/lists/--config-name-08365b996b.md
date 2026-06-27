# --config-name

- **参数名**：`--config-name`
- **分类**：配置
- **中文解释**：文档说明：Hydra 启动参数，用于选择 Verl trainer 配置文件名，如 `ppo_trainer.yaml`、`ppo_megatron_trainer.yaml`、`fully_async_ppo_megatron_trainer.yaml`。
- **常见值**：$CONFIG_NAME、'fully_async_ppo_megatron_trainer.yaml'、'gsm8k_multiturn_grpo'、'ppo_megatron_trainer.yaml'、'ppo_trainer.yaml'
- **来源环境变量**：无
- **性能影响**：机制推断：本身只是选择配置入口；实际性能由被选 YAML 中的并行、batch、rollout backend、异步和资源设置决定。
- **精度影响**：机制推断：本身不直接影响精度；选错配置会改变算法、后端或默认超参，从而显著改变训练行为。
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

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:64` --config-name='fully_async_ppo_megatron_trainer.yaml' \
- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:125` --config-name=$CONFIG_NAME
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:133` --config-name=$CONFIG_NAME
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh:102` --config-name='ppo_megatron_trainer.yaml' \
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:120` --config-name=$CONFIG_NAME

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

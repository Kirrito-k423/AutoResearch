# reward.reward_manager.name

- **参数名**：`reward.reward_manager.name`
- **分类**：配置
- **中文解释**：文档说明：选择 reward manager 实现的注册名；Verl 会用该 name 解析奖励管理器类并选择对应的默认打分函数，示例中用于切换 `dapo`、`gdpo` 等奖励聚合/计算策略。
- **常见值**：dapo、gdpo
- **来源环境变量**：无
- **性能影响**：机制推断：不同 reward manager 可能改变奖励计算、聚合、批处理或异步调度路径；它不是模型主算子开关，主要影响 reward 侧 CPU/调度耗时。
- **精度影响**：文档说明：reward manager 决定 RL 奖励信号的组织方式；从 DAPO/GDPO 等策略切换会直接改变优化目标和训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:114` reward.reward_manager.name=dapo
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:157` reward.reward_manager.name=dapo
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:159` reward.reward_manager.name=dapo
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh:87` reward.reward_manager.name=gdpo

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

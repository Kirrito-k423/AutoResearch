# actor_rollout_ref.actor.fsdp_config.use_orig_params

- **参数名**：`actor_rollout_ref.actor.fsdp_config.use_orig_params`
- **分类**：效率
- **中文解释**：文档说明：FSDP1 初始化时是否保留/使用原始参数视图；Verl FSDP 配置标注该项仅适用于 FSDP1，默认 False。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：保留原始参数视图可能增加少量参数管理开销，但能提升某些优化器、PEFT 或按原参数名访问场景的兼容性；通常不是主要吞吐瓶颈。
- **精度影响**：机制推断：参数表示方式不改变训练目标；如果某些模块依赖原始参数视图，开启可避免兼容性问题，否则通常不直接影响精度。
- **NPU/Ascend 证据**：部分
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:67` actor_rollout_ref.actor.fsdp_config.use_orig_params=True
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:83` actor_rollout_ref.actor.fsdp_config.use_orig_params=True
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh:65` actor_rollout_ref.actor.fsdp_config.use_orig_params=True

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

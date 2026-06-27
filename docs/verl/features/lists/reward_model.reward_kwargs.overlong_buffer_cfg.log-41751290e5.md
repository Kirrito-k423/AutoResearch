# reward_model.reward_kwargs.overlong_buffer_cfg.log

- **参数名**：`reward_model.reward_kwargs.overlong_buffer_cfg.log`
- **分类**：算法
- **中文解释**：源码说明：控制 DAPO overlong buffer 是否把 `overlong_reward` 和是否超长的标记写入 `reward_extra_info`，用于观测惩罚触发情况。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：开启日志会增加少量 Python 列表追加和指标上报开销；默认 `False` 时不产生这部分额外记录。
- **精度影响**：源码说明：该开关只控制额外信息记录，不改变奖励数值本身，通常不直接影响训练精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:130` +reward_model.reward_kwargs.overlong_buffer_cfg.log=False \
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:109` +reward_model.reward_kwargs.overlong_buffer_cfg.log=False
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:111` +reward_model.reward_kwargs.overlong_buffer_cfg.log=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

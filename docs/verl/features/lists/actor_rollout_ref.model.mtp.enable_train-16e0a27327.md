# actor_rollout_ref.model.mtp.enable_train

- **参数名**：`actor_rollout_ref.model.mtp.enable_train`
- **分类**：效率
- **中文解释**：控制 MTP 辅助预测头是否参与训练；通常与 `actor_rollout_ref.model.mtp.enable=True` 一起使用，使 MTP loss 纳入训练过程。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：MTP 训练当前主要依赖 mbridge/Megatron 组合；开启后会引入 MTP 相关前向与辅助 loss 计算，并增加参数/激活显存压力。
- **精度影响**：文档说明：MTP 文档指出当 MTP loss 作用于全部模型参数且 `mtp_loss_scaling_factor` 为 0.1 一类非零值时，训练结果才会有明显变化。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:80` actor_rollout_ref.model.mtp.enable_train=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:67` actor_rollout_ref.model.mtp.enable_train=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:80` actor_rollout_ref.model.mtp.enable_train=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

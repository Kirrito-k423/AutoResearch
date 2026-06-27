# actor_rollout_ref.model.mtp.mtp_loss_scaling_factor

- **参数名**：`actor_rollout_ref.model.mtp.mtp_loss_scaling_factor`
- **分类**：算法
- **中文解释**：MTP 训练时辅助 MTP loss 的缩放系数，用来控制多 token 预测辅助目标相对主训练目标的权重。
- **常见值**：0.1、0.2
- **来源环境变量**：MTP_LOSS_SCALING_FACTOR
- **性能影响**：机制推断：系数大小本身不改变 MTP 计算图规模；真正的额外显存/算力主要来自开启 MTP 训练与 MTP 参数，非零系数会让该辅助 loss 参与优化。
- **精度影响**：文档说明：MTP 文档指出 MTP loss 作用于全部模型参数且系数为 0.1 一类非零值时会明显影响训练结果；系数越大，辅助预测目标约束越强。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:81` actor_rollout_ref.model.mtp.mtp_loss_scaling_factor=${mtp_loss_scaling_factor} \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:68` actor_rollout_ref.model.mtp.mtp_loss_scaling_factor=${mtp_loss_scaling_factor}
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:82` actor_rollout_ref.model.mtp.mtp_loss_scaling_factor=${mtp_loss_scaling_factor}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# actor_rollout_ref.model.mtp.detach_encoder

- **参数名**：`actor_rollout_ref.model.mtp.detach_encoder`
- **分类**：效率
- **中文解释**：文档说明：MTP 训练配置，`detach_encoder=True` 表示冻结/断开 Encoder 主干，只更新 MTP 模块参数，MTP loss 只作用在 MTP 参数上。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：只训练 MTP 模块可减少需要反传和更新的参数，降低优化器状态与梯度开销；仍需主干前向，因此吞吐收益取决于实现和模型结构。
- **精度影响**：文档说明：MTP 文档推荐采用 `detach_encoder=True` 的训练方式；它保护主干模型不被 MTP loss 改写，但也限制 MTP loss 对主干表征的适配能力。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:82` actor_rollout_ref.model.mtp.detach_encoder=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:69` actor_rollout_ref.model.mtp.detach_encoder=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:81` actor_rollout_ref.model.mtp.detach_encoder=True

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

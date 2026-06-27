# actor_rollout_ref.model.mtp.enable_rollout

- **参数名**：`actor_rollout_ref.model.mtp.enable_rollout`
- **分类**：效率
- **中文解释**：文档说明：控制模型配置中的 MTP（Multi-Token Prediction，多 token 预测）是否在 rollout/推理阶段启用。Verl Ascend 参数表把 `mtp.enable_rollout` 解释为“是否在推理中启用 MTP”。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：启用后 rollout 可利用 MTP/speculative 相关路径一次提出多个 draft token，若后端支持且 draft 命中率高，可降低逐 token 解码开销；也会增加 MTP 头、校验和兼容性成本。
- **精度影响**：机制推断：若采用带校验的 speculative decoding，理论上应保持目标分布；若 MTP draft 质量差、配置不匹配或训练/推理 MTP 状态不一致，可能改变生成长度、采样稳定性或 rollout 奖励分布。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:83` actor_rollout_ref.model.mtp.enable_rollout=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:128` ROLLOUT+=(actor_rollout_ref.model.mtp.enable_rollout=True)

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# actor_rollout_ref.model.mtp.enable

- **参数名**：`actor_rollout_ref.model.mtp.enable`
- **分类**：效率
- **中文解释**：开启模型侧 MTP（Multi-Token Prediction）配置，使训练流程加载、保存并携带 MTP 参数；单独开启时不等于训练或 rollout 使用 MTP，需要配合 `enable_train` 或 `enable_rollout`。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：仅加载 MTP 参数会增加显存占用和权重同步/导出体积；若进一步用于 rollout，MTP 文档提到可提升接受率，但在 H20 上整体吞吐不一定提升。
- **精度影响**：文档说明：MTP 文档指出“仅携带 MTP 参数但不训练”通常对训练结果无明显影响；需要结合 `enable_train` 和非零 MTP loss 才可能改变优化目标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:79` actor_rollout_ref.model.mtp.enable=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:66` actor_rollout_ref.model.mtp.enable=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:79` actor_rollout_ref.model.mtp.enable=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

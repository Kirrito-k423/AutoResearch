# async_training.partial_rollout

- **参数名**：`async_training.partial_rollout`
- **分类**：效率
- **中文解释**：文档说明：fully_async_policy 中允许参数同步前中断未完成 rollout，并在同步后从保存状态继续；官方文档把它用于 async partial tool agent loop。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：fully async 文档报告 streaming、staleness 与 `partial_rollout=True` 组合可显著降低 rollout 尾部等待，128 卡实验中整体收益可到约 2.35x。
- **精度影响**：文档说明：官方实验称 fully async/stale samples 未显著影响结果，但 partial rollout 会引入中断/恢复和更异步的样本路径；配置不当可能增加轨迹陈旧或工具调用状态一致性风险。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:138` async_training.partial_rollout=True \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

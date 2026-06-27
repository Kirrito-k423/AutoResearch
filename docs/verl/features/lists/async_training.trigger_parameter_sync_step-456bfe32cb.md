# async_training.trigger_parameter_sync_step

- **参数名**：`async_training.trigger_parameter_sync_step`
- **分类**：效率
- **中文解释**：文档说明：fully_async_policy 中触发参数同步的本地 step 间隔；源码用它推进 parameter version，并要求该值大于等于 1。
- **常见值**：4
- **来源环境变量**：TRIGGER_PARAMETER_SYNC_STEP
- **性能影响**：机制推断：值越大，trainer 与 rollouter 同步越不频繁，可减少同步阻塞、提高流水线利用率；但会增加样本陈旧度和一次同步前的排队规模。
- **精度影响**：机制推断：同步间隔变大意味着 rollout 使用旧参数的时间更长，可能提高 off-policy 偏差；较小值更贴近同步训练但吞吐收益较弱。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:136` async_training.trigger_parameter_sync_step=${trigger_parameter_sync_step} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

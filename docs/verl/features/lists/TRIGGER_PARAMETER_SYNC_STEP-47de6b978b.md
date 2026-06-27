# TRIGGER_PARAMETER_SYNC_STEP

- **参数名**：`TRIGGER_PARAMETER_SYNC_STEP`
- **分类**：效率
- **中文解释**：控制 fully async 中 Trainer 本地更新多少轮后触发一次与 Rollouter 的参数同步，映射到 `async_training.trigger_parameter_sync_step`；示例默认 4。
- **常见值**：4
- **来源环境变量**：TRIGGER_PARAMETER_SYNC_STEP
- **性能影响**：文档说明：官方 fully async 文档说明该值越大，同步越不频繁、计算效率越高；越小越接近 on-policy，但频繁同步会降低资源利用率。
- **精度影响**：文档说明：官方文档明确指出该值越大 off-policy 影响越强，可能影响精度；越小则更接近 on-policy、稳定性更好但吞吐较低。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:42` trigger_parameter_sync_step=${TRIGGER_PARAMETER_SYNC_STEP:-4}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

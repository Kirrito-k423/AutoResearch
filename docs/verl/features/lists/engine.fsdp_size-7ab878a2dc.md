# engine.fsdp_size

- **参数名**：`engine.fsdp_size`
- **分类**：效率
- **中文解释**：文档说明：SFT engine 的 FSDP 分片组大小；`-1` 表示使用全部可用设备组成全局 FSDP shard group，正数表示每个 FSDP 组包含的设备数。
- **常见值**：-1
- **来源环境变量**：FSDP_SIZE
- **性能影响**：文档说明：更大的 FSDP 组通常降低单卡参数/优化器显存，但增加 all-gather、reduce-scatter 等通信范围；更小分组可能减少通信但复制更多状态。
- **精度影响**：机制推断：正确分片下不改变训练目标；不同通信/归约顺序可能带来细小浮点差异，主要风险是组大小与设备拓扑不匹配导致启动或恢复失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:45` engine.fsdp_size=${FSDP_SIZE}"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

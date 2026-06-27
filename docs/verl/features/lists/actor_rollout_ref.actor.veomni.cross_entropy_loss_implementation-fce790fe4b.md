# actor_rollout_ref.actor.veomni.cross_entropy_loss_implementation

- **参数名**：`actor_rollout_ref.actor.veomni.cross_entropy_loss_implementation`
- **分类**：算法
- **中文解释**：选择 VeOmni actor 训练中 cross entropy loss 的内核实现；示例使用 `liger_kernel`，配置注释还列出 `eager`、`npu` 等后端。
- **常见值**：liger_kernel"
- **来源环境变量**：无
- **性能影响**：文档说明：该值会进入 VeOmni 的 `OpsImplementationConfig` 选择 CE kernel；`liger_kernel`/`npu` 等融合或设备专用实现通常用于降低显存和提升 loss 计算吞吐，兼容性取决于模型与设备。
- **精度影响**：机制推断：目标仍是交叉熵，不改变 RL 奖励或优势估计；不同 kernel 的 dtype、规约顺序或数值实现可能带来小幅数值差异，需在切换后看 loss 对齐。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:80` actor_rollout_ref.actor.veomni.cross_entropy_loss_implementation=liger_kernel"

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

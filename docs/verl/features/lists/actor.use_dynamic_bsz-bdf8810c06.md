# actor.use_dynamic_bsz

- **参数名**：`actor.use_dynamic_bsz`
- **分类**：效率
- **中文解释**：文档说明：Actor 更新时是否启用动态 batch size；开启后按 token 数而不是固定样本数组织前后向，让每次 forward 处理相近 token 量。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：`use_dynamic_bsz=True` 可显著提升训练效率并降低显存，且无需手工调大量 `*micro_batch_size_per_gpu`；某些 bshd/非 packed 模式脚本会要求关闭。
- **精度影响**：机制推断：主要改变批内 token 调度，不直接改变损失定义；但 batch 重组、梯度累积边界和 OOM/截断风险会间接影响训练稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:32` #     - actor.use_dynamic_bsz=False              (required for bshd mode)
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:17` #     - actor.use_dynamic_bsz=False              (required for bshd mode)

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

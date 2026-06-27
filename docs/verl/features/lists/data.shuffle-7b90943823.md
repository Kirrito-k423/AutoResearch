# data.shuffle

- **参数名**：`data.shuffle`
- **分类**：效率
- **中文解释**：文档说明：控制 dataloader 是否打乱训练数据顺序；`True` 每轮随机化样本顺序，`False` 保持数据集原始/确定顺序，常用于对齐、复现实验或固定评测口径。
- **常见值**：False、True
- **来源环境变量**：无
- **性能影响**：机制推断：打乱本身只带来很小的数据加载/索引开销，但在远程数据或缓存命中敏感场景可能降低顺序读取效率；对 GPU/NPU 计算吞吐通常不是主导因素。
- **精度影响**：机制推断：会改变样本到达优化器的顺序和随机性；`True` 通常有利于 SGD/RL 训练混合样本，`False` 更利于精度对齐、可复现和排查数据顺序差异。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：6
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh`
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh`

## 证据片段

- `examples/on_policy_distillation_trainer/run_qwen3_8b_fsdp.sh:60` data.shuffle=False
- `examples/on_policy_distillation_trainer/run_qwen3_8b_mopd_fsdp.sh:66` data.shuffle=True
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:67` data.shuffle=False
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:146` data.shuffle=False
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:67` data.shuffle=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

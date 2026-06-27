# MODEL_DIR

- **参数名**：`MODEL_DIR`
- **分类**：配置
- **中文解释**：gpt-oss 示例中转换后本地模型的保存目录；脚本先把源模型转存为 bf16 到该目录，再将其作为 `actor_rollout_ref.model.path` 训练。
- **常见值**：$HOME/models/gpt-oss-20b-bf16
- **来源环境变量**：MODEL_DIR
- **性能影响**：机制推断：目录影响模型转换、保存和后续加载的 I/O；放在慢盘或空间不足会显著拖慢准备/启动，但训练算子性能由实际模型和并行配置决定。
- **精度影响**：机制推断：目录本身不改精度；但它保存的是转换后的 bf16 模型，若内容与源模型不一致或被覆盖，会改变训练初始权重。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh:5` MODEL_DIR=${MODEL_DIR:-$HOME/models/gpt-oss-20b-bf16}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

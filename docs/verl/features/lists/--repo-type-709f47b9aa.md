# --repo-type

- **参数名**：`--repo-type`
- **分类**：效率
- **中文解释**：机制推断：`hf download` 的仓库类型参数；示例用 `--repo-type dataset` 从 Hugging Face 下载 `tyzhu/geo3k` 数据集到本地目录。
- **常见值**：dataset
- **来源环境变量**：无
- **性能影响**：机制推断：只影响下载阶段选择数据集/模型等仓库类型，不影响训练时每步吞吐；填错会导致下载失败或拿到错误资产。
- **精度影响**：机制推断：参数本身不改变算法；若下载的数据集版本或类型不同，会通过训练/评测数据内容影响指标。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:35` hf download tyzhu/geo3k --repo-type dataset --local-dir $HOME/data/geo3k

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

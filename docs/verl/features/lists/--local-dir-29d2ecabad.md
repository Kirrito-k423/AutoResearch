# --local-dir

- **参数名**：`--local-dir`
- **分类**：配置
- **中文解释**：Hugging Face CLI 下载命令的本地保存目录参数；示例用它把 `tyzhu/geo3k` 数据集下载到 `$HOME/data/geo3k`，供后续训练脚本读取。
- **常见值**：$HOME/data/geo3k
- **来源环境变量**：无
- **性能影响**：机制推断：只影响数据下载/缓存位置；本地目录命中可减少重复下载时间，目录位于慢盘或网络盘时会拖慢准备阶段。
- **精度影响**：机制推断：不直接改变训练精度；若目录指向错误版本或不完整数据集，会通过数据内容间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:35` hf download tyzhu/geo3k --repo-type dataset --local-dir $HOME/data/geo3k

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

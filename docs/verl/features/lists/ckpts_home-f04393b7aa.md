# ckpts_home

- **参数名**：`ckpts_home`
- **分类**：配置
- **中文解释**：文档说明：checkpoint 本地保存根目录，示例脚本创建该目录后传给 `trainer.default_local_dir`，用于保存训练 checkpoint、恢复训练和后续模型导出。
- **常见值**：~/verl/checkpoints/${project_name、~/verl/test/gsm8k-sft-${backend
- **来源环境变量**：ckpts_home
- **性能影响**：文档说明：checkpoint 会写入 `default_local_dir`；目录所在存储的吞吐和容量会影响保存/恢复耗时，频繁保存时 I/O 开销更明显。
- **精度影响**：机制推断：保存目录不改变训练目标；但它影响能否恢复指定 checkpoint、保留中间模型和复现实验结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:38` ckpts_home=${ckpts_home:-~/verl/test/gsm8k-sft-${backend}}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:79` ckpts_home=${ckpts_home:-~/verl/checkpoints/${project_name}/${exp_name}}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

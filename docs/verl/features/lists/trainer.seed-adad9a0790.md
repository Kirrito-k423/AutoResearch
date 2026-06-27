# trainer.seed

- **参数名**：`trainer.seed`
- **分类**：效率
- **中文解释**：设置 trainer 层随机种子，用于控制数据打乱、初始化、采样等随机过程的可复现性；AutoModel/FSDP/Megatron 配置中也有默认 seed。
- **常见值**：1111
- **来源环境变量**：无
- **性能影响**：机制推断：seed 本身通常不改变计算量；若同时开启完全确定性调试选项才可能牺牲吞吐。
- **精度影响**：机制推断：seed 会改变随机初始化、数据顺序、dropout/采样轨迹，因此会影响单次实验指标和可复现性，但不是固定方向的精度增益开关。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh`
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen2_5_0_5b_automodel.sh:54` trainer.seed=1111 \
- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:73` trainer.seed=1111 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

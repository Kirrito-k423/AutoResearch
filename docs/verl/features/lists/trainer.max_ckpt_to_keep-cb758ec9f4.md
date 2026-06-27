# trainer.max_ckpt_to_keep

- **参数名**：`trainer.max_ckpt_to_keep`
- **分类**：配置
- **中文解释**：机制推断：限制本地最多保留多少个 checkpoint；示例中常与 `trainer.default_local_dir`、`checkpoint.save_contents` 一起使用，避免训练过程中 checkpoint 无限增长。
- **常见值**：10、5
- **来源环境变量**：无
- **性能影响**：机制推断：较小值可减少磁盘占用和旧 checkpoint 清理压力；较大值保留更多恢复点，但会增加存储容量需求。
- **精度影响**：机制推断：不直接改变训练计算；保留过少会减少回滚、挑选最佳中间模型和排查退化的空间。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`
- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh`

## 证据片段

- `examples/sft/vlm/run_qwen3_vl_2b_fsdp.sh:99` trainer.max_ckpt_to_keep=5 \
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:97` trainer.max_ckpt_to_keep=10 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

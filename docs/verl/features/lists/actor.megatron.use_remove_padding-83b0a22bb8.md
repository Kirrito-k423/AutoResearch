# actor.megatron.use_remove_padding

- **参数名**：`actor.megatron.use_remove_padding`
- **分类**：效率
- **中文解释**：文档说明：Megatron actor 侧是否移除 padding token；官方配置说明 `use_remove_padding=True` 会去掉输入和回复中的 padding，提高模型运行效率。Qwen3.5 GDN 示例因要求 bshd 格式而显式设为 `False`。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：文档说明：开启 remove padding 可减少 padding token 上的无效计算，通常明显提升吞吐并降低显存；关闭可换取不支持 THD/packed sequence 模型的兼容性。
- **精度影响**：机制推断：正确实现下不改变有效 token 的训练目标；若模型或后端不支持 packed/THD 格式，强行开启可能导致失败或不可靠结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_35b_megatron.sh:31` #     - actor.megatron.use_remove_padding=False  (forces bshd compute format)
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:16` #     - actor.megatron.use_remove_padding=False  (forces bshd compute format)

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

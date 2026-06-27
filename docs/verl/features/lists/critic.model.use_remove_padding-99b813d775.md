# critic.model.use_remove_padding

- **参数名**：`critic.model.use_remove_padding`
- **分类**：效率
- **中文解释**：文档说明：控制 critic/value model 前向时是否移除 padding token 后再计算。Ascend 参数表列出 `critic.model.use_remove_padding`，官方 config 文档也说明 remove padding 可提升模型运行效率。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：文档说明：启用后 critic 只在有效 token 上做 value/logit 相关计算，可减少 padding 带来的无效显存和算力；关闭更保守但吞吐通常较低。
- **精度影响**：机制推断：mask 正确时不改变 value loss 的数学含义；若 remove-padding 与 response mask、position ids 或 packed batch 对齐错误，会影响 value 估计和 advantage 计算。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:107` critic.model.use_remove_padding=True
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:95` critic.model.use_remove_padding=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

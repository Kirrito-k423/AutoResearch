# critic.use_dynamic_bsz

- **参数名**：`critic.use_dynamic_bsz`
- **分类**：效率
- **中文解释**：文档说明：控制 critic 更新是否使用动态 batch size/按 token 数自动切分 batch。Verl critic 配置中该项默认继承 actor 的 `use_dynamic_bsz`，并配合 `ppo_max_token_len_per_gpu` 约束每 GPU token 预算。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：动态 batch 可按序列长度平衡 micro-batch 计算量，降低长短样本混排造成的 OOM 或空转；token 预算过小会增加 micro-batch 数和调度开销。
- **精度影响**：机制推断：理论上只改变 micro-batch 切分，不改变 value loss；但不同切分会改变浮点累加顺序，且若 token 预算导致样本拆分/跳过异常，会影响 critic 稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:110` critic.use_dynamic_bsz=True
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:97` critic.use_dynamic_bsz=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

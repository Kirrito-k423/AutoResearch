# actor_rollout_ref.ref.fsdp_config.model_dtype

- **参数名**：`actor_rollout_ref.ref.fsdp_config.model_dtype`
- **分类**：效率
- **中文解释**：机制推断：Reference policy 的 FSDP engine `model_dtype`，控制 ref 模型加载/计算时使用的模型精度；示例在 LoRA merge FSDP2 reference 中设为 `bf16`。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：`bf16` 相比 `fp32` 可降低 ref logprob 计算显存和带宽压力，通常更快；过低精度或不支持的 dtype 可能造成 kernel/硬件兼容问题。
- **精度影响**：机制推断：reference logprob/KL 使用低精度会带来轻微数值差异；通常 bf16 可接受，但若 KL 很敏感或 actor/ref dtype 不一致，需要监控 KL 与 reward 稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh:89` actor_rollout_ref.ref.fsdp_config.model_dtype=bf16

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

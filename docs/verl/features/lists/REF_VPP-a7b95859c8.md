# REF_VPP

- **参数名**：`REF_VPP`
- **分类**：效率
- **中文解释**：文档说明：reference policy 的 virtual pipeline parallel size，示例在 `ref_pp > 1` 时写入 `actor_rollout_ref.ref.megatron.virtual_pipeline_model_parallel_size`，否则置为 `null`。
- **常见值**：2
- **来源环境变量**：REF_VPP
- **性能影响**：机制推断：VPP 可把每个物理 pipeline stage 再虚拟切分，降低流水线气泡并改善负载均衡；也会增加调度复杂度并要求与 PP/层数匹配。
- **精度影响**：机制推断：正确配置应不改变 reference logprob；若与层数、PP 或 mbridge 支持不匹配，可能导致运行失败或非预期数值差异。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:47` ref_vpp=${REF_VPP:-2}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

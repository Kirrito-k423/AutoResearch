# actor_rollout_ref.model.mtp.speculative_algorithm

- **参数名**：`actor_rollout_ref.model.mtp.speculative_algorithm`
- **分类**：效率
- **中文解释**：文档说明：SGLang MTP rollout 使用的 speculative decoding 算法名；官方 MTP 文档给出的 SGLang 配置示例为 `speculative_algorithm=\"EAGLE\"`。
- **常见值**：EAGLE
- **来源环境变量**：SPEC_ALGORITHM
- **性能影响**：文档说明：该参数决定 SGLang speculative 后端路径；MTP 文档说明加速效果显著受模型大小与硬件影响，H20 上启用后吞吐可能下降约 50%。
- **精度影响**：机制推断：算法选择不改变训练损失；若 speculative verification 严格，最终 token 仍由目标模型接受/拒绝，但 draft 算法与权重不匹配会降低接受率并影响 rollout 稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:136` actor_rollout_ref.model.mtp.speculative_algorithm=${spec_algorithm}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

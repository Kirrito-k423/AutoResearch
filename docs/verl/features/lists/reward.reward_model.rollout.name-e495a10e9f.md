# reward.reward_model.rollout.name

- **参数名**：`reward.reward_model.rollout.name`
- **分类**：配置
- **中文解释**：选择 rollout 推理后端，例如 vLLM、SGLang 或 TensorRT-LLM，决定生成吞吐、兼容性和 NPU 迁移风险。
- **常见值**：vllm
- **来源环境变量**：无
- **性能影响**：机制推断：不同推理后端会改变生成吞吐、显存管理、启动开销和 NPU 兼容性。
- **精度影响**：机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:73` reward.reward_model.rollout.name=vllm

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

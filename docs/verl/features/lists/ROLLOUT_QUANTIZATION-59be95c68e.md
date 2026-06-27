# ROLLOUT_QUANTIZATION

- **参数名**：`ROLLOUT_QUANTIZATION`
- **分类**：效率
- **中文解释**：控制 TRT-LLM rollout 的量化模式；在该示例中仅允许 `INFER_BACKEND=trtllm` 时设置，`fp8` 会追加 `actor_rollout_ref.rollout.quantization=fp8`。
- **常见值**：未提取
- **来源环境变量**：ROLLOUT_QUANTIZATION
- **性能影响**：机制推断：FP8 rollout 可降低推理权重/激活相关显存与带宽压力，并可能提升 TRT-LLM 吞吐；但有后端兼容限制，且量化转换、权重同步和特定硬件支持会影响收益。
- **精度影响**：机制推断：量化 rollout 可能让生成 logits/logprob 与 bf16/fp16 训练路径产生数值差异，增加训练-推理 mismatch 或 KL 波动；若不设置则保持默认精度路径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:16` ROLLOUT_QUANTIZATION=${ROLLOUT_QUANTIZATION:-}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

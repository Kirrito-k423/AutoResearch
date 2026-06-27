# actor_rollout_ref.rollout.quantization

- **参数名**：`actor_rollout_ref.rollout.quantization`
- **分类**：效率
- **中文解释**：文档说明：指定 rollout 推理引擎的量化方式。Verl rollout 配置注释写明当前支持 `fp8` 和 `torchao`，Ascend 特性表也把 `actor_rollout_ref.rollout.quantization` 标为量化加载与推理能力。
- **常见值**："fp8"、fp8
- **来源环境变量**：无
- **性能影响**：文档说明：量化通常降低 rollout 权重/KV 或算子内存带宽压力，可提升大模型推理吞吐并减少显存；但会增加量化配置、权重转换和特定硬件 kernel 依赖。
- **精度影响**：机制推断：低精度量化会引入数值误差，可能改变 token logprob、采样结果和 reward 分布；FP8/torchao 需要与训练侧精度和权重同步流程保持一致。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:91` # +actor_rollout_ref.rollout.quantization="fp8"
- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:244` EXTRA+=(+actor_rollout_ref.rollout.quantization=fp8)

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

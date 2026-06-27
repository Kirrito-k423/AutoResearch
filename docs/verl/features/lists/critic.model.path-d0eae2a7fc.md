# critic.model.path

- **参数名**：`critic.model.path`
- **分类**：配置
- **中文解释**：指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。
- **常见值**："$CRITIC_MODEL_PATH"、Qwen/Qwen2.5-0.5B-Instruct
- **来源环境变量**：无
- **性能影响**：通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。
- **精度影响**：通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/ppo_trainer/run_qwen3_8b_fsdp.sh:106` critic.model.path="$CRITIC_MODEL_PATH"
- `examples/ppo_trainer/run_qwen3_8b_megatron.sh:94` critic.model.path="$CRITIC_MODEL_PATH"
- `examples/tutorial/skypilot/verl-ppo.yaml:86` critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# ADV_ESTIMATOR

- **参数名**：`ADV_ESTIMATOR`
- **分类**：算法
- **中文解释**：文档说明：`ADV_ESTIMATOR` 是 examples 暴露的优势估计方法，最终写入 `algorithm.adv_estimator`；Verl examples README 将 PPO/GRPO/RLOO/ReMax/REINFORCE++/OTB 等 trainer 与对应 estimator 对齐。
- **常见值**：grpo、optimal_token_baseline、reinforce_plus_plus
- **来源环境变量**：ADV_ESTIMATOR
- **性能影响**：机制推断：通常不是主要吞吐旋钮，但不同 estimator 可能改变是否需要 critic、分组统计或额外 baseline 计算，从而影响训练开销。
- **精度影响**：文档说明：优势估计直接决定策略梯度中的优势信号；选错 estimator 会改变 PPO/GRPO/RLOO/REINFORCE++ 等算法语义，显著影响稳定性和最终策略。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：4
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh`
- `examples/otb_trainer/run_qwen3_8b_fsdp.sh`
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh`

## 证据片段

- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:12` adv_estimator=${ADV_ESTIMATOR:-reinforce_plus_plus}
- `examples/otb_trainer/run_qwen3_8b_fsdp.sh:11` adv_estimator=${ADV_ESTIMATOR:-optimal_token_baseline}
- `examples/grpo_trainer/run_qwen3_next_80b_a3b_fsdp.sh:19` adv_estimator=${ADV_ESTIMATOR:-grpo}
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh:26` ADV_ESTIMATOR=${ADV_ESTIMATOR:-grpo}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

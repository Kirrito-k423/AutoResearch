# algorithm.adv_estimator

- **参数名**：`algorithm.adv_estimator`
- **分类**：算法
- **中文解释**：选择优势估计器，用来把 reward/价值信号转换为策略梯度中的 advantage；常见值包括 `gae`、`grpo`、`rloo`、`reinforce_plus_plus` 等。
- **常见值**：$adv_estimator、gae、gdpo、gpg、grpo、optimal_token_baseline、reinforce_plus_plus、remax、rloo
- **来源环境变量**：ADV_ESTIMATOR、adv_estimator
- **性能影响**：机制推断：估计器通常不主导单步算力，但会改变是否需要 value/baseline、分组统计或额外归一化，从而影响训练吞吐和显存占用。
- **精度影响**：文档说明：PPO README 列出多个支持的 estimator，best practices 指出 DAPO/GRPO 使用 `grpo`；不同 estimator 改变 bias/variance 与优化目标，直接影响稳定性和最终指标。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：78
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_235b_256k_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_30b_a3b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_fsdp.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`
- `examples/ascend_extras/grpo_trainer/run_qwen3_next_80b_fsdp.sh`
- `examples/cispo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh`
- `examples/gdpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_fsdp.sh`
- `examples/gpg_trainer/run_qwen3_8b_megatron.sh`
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/grpo_trainer/run_glm4_1v_9b_fsdp.sh`
- `examples/grpo_trainer/run_gpt_oss_20b_fsdp.sh`
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_mistral_nemo_12b_skyworkrm_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/grpo_trainer/run_qwen2-7b_math_megatron_fsdp.sh`

## 证据片段

- `examples/dppo_trainer/run_qwen3_30b_a3b_megatron.sh:57` algorithm.adv_estimator=grpo
- `examples/reinforce_plus_plus_trainer/run_qwen3_8b_fsdp.sh:45` algorithm.adv_estimator=${adv_estimator}
- `examples/gmpo_trainer/run_qwen3_8b_fsdp.sh:46` algorithm.adv_estimator=grpo
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:83` algorithm.adv_estimator=grpo
- `examples/gspo_trainer/run_qwen3_30b_a3b_megatron.sh:49` algorithm.adv_estimator=grpo

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# ROLLOUT_LOG_PROB_MAX_TOKEN_LEN_PER_GPU

- **参数名**：`ROLLOUT_LOG_PROB_MAX_TOKEN_LEN_PER_GPU`
- **分类**：效率
- **中文解释**：控制 `actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu`，在 rollout 侧计算 old log probability 时限制每张 GPU 一次动态 batch 前向最多处理的 token 数。
- **常见值**：40960
- **来源环境变量**：ROLLOUT_LOG_PROB_MAX_TOKEN_LEN_PER_GPU
- **性能影响**：文档说明：Verl perf tuning 将该类 `log_prob_max_token_len_per_gpu` 定义为动态 batch 下 `compute_log_prob` 前向的 token 上限；调大可减少切分并提升吞吐，但显存占用和 OOM 风险同步上升。
- **精度影响**：机制推断：该值不改变 logprob 公式；设得过小通常表现为更多 micro batch 或吞吐下降，若小到无法容纳长样本则可能触发失败或间接改变可训练样本。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:66` rollout_log_prob_max_token_len_per_gpu=${ROLLOUT_LOG_PROB_MAX_TOKEN_LEN_PER_GPU:-40960}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

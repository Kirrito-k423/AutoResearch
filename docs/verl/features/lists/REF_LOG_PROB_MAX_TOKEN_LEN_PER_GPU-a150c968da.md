# REF_LOG_PROB_MAX_TOKEN_LEN_PER_GPU

- **参数名**：`REF_LOG_PROB_MAX_TOKEN_LEN_PER_GPU`
- **分类**：效率
- **中文解释**：文档说明：reference policy 计算参考 logprob 时，动态 batch 模式下单 GPU 允许处理的最大 token 数，写入 `actor_rollout_ref.ref.log_prob_max_token_len_per_gpu`。
- **常见值**：40960
- **来源环境变量**：REF_LOG_PROB_MAX_TOKEN_LEN_PER_GPU
- **性能影响**：文档说明：该上限越大，reference logprob 前向分批越少、吞吐可能更好，但显存峰值更高；过大有 OOM 风险，过小会增加切分开销。
- **精度影响**：机制推断：不改变 reference logprob 的数学定义；若设置过低导致长序列处理受限或频繁切分，只会通过效率和稳定性间接影响结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_30b_a3b_megatron.sh:64` ref_log_prob_max_token_len_per_gpu=${REF_LOG_PROB_MAX_TOKEN_LEN_PER_GPU:-40960}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

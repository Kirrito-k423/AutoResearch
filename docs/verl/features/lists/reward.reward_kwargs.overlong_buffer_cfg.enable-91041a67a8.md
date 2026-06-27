# reward.reward_kwargs.overlong_buffer_cfg.enable

- **参数名**：`reward.reward_kwargs.overlong_buffer_cfg.enable`
- **分类**：算法
- **中文解释**：文档说明：启用 DAPO 奖励管理器的 overlong buffer 惩罚；当回复长度进入 `max_resp_len - len` 到 `max_resp_len` 的缓冲区间时，对过长回复施加线性负奖励。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：开启后每条样本多一次长度比较和惩罚计算，计算开销很小；若训练后模型学会更短回复，可能间接减少后续 rollout token 开销。
- **精度影响**：文档说明：会改变奖励目标并惩罚接近最大响应长度的输出，有助于抑制超长答案；若任务需要长推理，惩罚过强可能压低有效长答案奖励。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:115` +reward.reward_kwargs.overlong_buffer_cfg.enable=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:158` +reward.reward_kwargs.overlong_buffer_cfg.enable=True
- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:160` +reward.reward_kwargs.overlong_buffer_cfg.enable=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

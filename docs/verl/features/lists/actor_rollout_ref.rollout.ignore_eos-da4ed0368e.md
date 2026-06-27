# actor_rollout_ref.rollout.ignore_eos

- **参数名**：`actor_rollout_ref.rollout.ignore_eos`
- **分类**：效率
- **中文解释**：文档说明：控制 rollout 生成时是否忽略 EOS token。设为 `True` 时即使模型生成 EOS 也继续生成直到长度或停止条件耗尽；默认/常见 `False` 表示遇到 EOS 后结束该响应。
- **常见值**：False
- **来源环境变量**：无
- **性能影响**：机制推断：忽略 EOS 通常会生成更多 token，增加 rollout 解码时间、KV cache 占用和后续 logprob/reward 计算量；不忽略 EOS 则可提前结束短响应、节省吞吐。
- **精度影响**：机制推断：会改变响应长度分布和终止行为，可能影响奖励函数、长度惩罚和训练样本 mask；对需要严格终止格式的任务尤其敏感。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:110` actor_rollout_ref.rollout.ignore_eos=False
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh:110` actor_rollout_ref.rollout.ignore_eos=False

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

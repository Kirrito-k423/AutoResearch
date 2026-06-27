# actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_grad_reduce

- **参数名**：`actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_grad_reduce`
- **分类**：效率
- **中文解释**：机制推断：MindSpeed/Megatron Core 的梯度通信重叠开关，用于让梯度 reduce-scatter/all-reduce 尽量与反向计算并行执行。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：开启后可隐藏一部分梯度同步通信延迟，提高多卡训练吞吐；代价是更复杂的通信调度和额外缓冲，网络或后端实现不匹配时收益可能有限。
- **精度影响**：机制推断：通信重叠本身不改变梯度数学值；只有在异步通信顺序、bucket 切分或后端兼容性出错时，才会影响训练正确性和稳定性。
- **NPU/Ascend 证据**：部分
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh`

## 证据片段

- `examples/ascend_extras/grpo_trainer/run_qwen3_32b_mindspeed.sh:136` +actor_rollout_ref.actor.mindspeed.mcore_kwargs.overlap_grad_reduce=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

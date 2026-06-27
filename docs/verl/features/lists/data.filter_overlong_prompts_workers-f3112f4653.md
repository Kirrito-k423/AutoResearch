# data.filter_overlong_prompts_workers

- **参数名**：`data.filter_overlong_prompts_workers`
- **分类**：效率
- **中文解释**：控制启用 `data.filter_overlong_prompts` 时用于过滤超长 prompt 的工作进程/worker 数量；示例把大规模数据集场景调到 64。
- **常见值**：64
- **来源环境变量**：无
- **性能影响**：文档说明：Verl 配置文档说明大规模数据集中过滤超长 prompt 可能耗时，可增大 worker 数提升数据预处理速度；同时会占用更多 CPU 和 I/O 资源。
- **精度影响**：机制推断：worker 数量本身不改变过滤规则或样本长度阈值；正常实现下不直接影响精度，只可能通过预处理失败/超时影响训练数据供给。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh`
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh`

## 证据片段

- `examples/grpo_trainer/run_qwen3_5-122b-a10b_veomni.sh:141` data.filter_overlong_prompts_workers=64
- `examples/grpo_trainer/run_qwen3_5_35b_a3b_veomni.sh:136` data.filter_overlong_prompts_workers=64
- `examples/grpo_trainer/run_qwen3_5_122b_a10b_megatron.sh:162` data.filter_overlong_prompts_workers=64

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

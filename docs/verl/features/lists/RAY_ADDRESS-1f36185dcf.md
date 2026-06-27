# RAY_ADDRESS

- **参数名**：`RAY_ADDRESS`
- **分类**：效率
- **中文解释**：文档说明：Ray 集群地址，示例用于连接 `localhost:8265` 的 Ray dashboard/job server 并提交训练任务。
- **常见值**："http://localhost:8265"
- **来源环境变量**：RAY_ADDRESS
- **性能影响**：机制推断：本身不改变计算吞吐，但决定任务提交到哪个 Ray 集群；地址错误会导致提交失败、排队异常或连接超时。
- **精度影响**：机制推断：不直接影响模型精度；只有连接到错误集群、错误环境或旧 checkpoint 时，才会间接改变运行结果。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:52` RAY_ADDRESS=${RAY_ADDRESS:-"http://localhost:8265"}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

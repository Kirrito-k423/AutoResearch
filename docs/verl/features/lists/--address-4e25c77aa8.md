# --address

- **参数名**：`--address`
- **分类**：效率
- **中文解释**：文档说明：Ray worker 启动参数，指定要加入的 Ray head/GCS 地址，例如 `$HEAD_IP:6379`，用于多节点训练集群连接。
- **常见值**：$HEAD_IP:6379
- **来源环境变量**：无
- **性能影响**：机制推断：地址正确时 worker 才能加入 Ray 集群并贡献 GPU/CPU 资源；地址错误会导致节点无法加入、资源不足或任务卡住。
- **精度影响**：机制推断：连接地址本身不改变训练数学；但实际加入的节点数变化会影响可用并行资源，若同时改变全局 batch/调度配置则可能间接影响训练轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-grpo.yaml:95` ps aux | grep ray | grep $HEAD_IP:6379 &> /dev/null || ray start --address $HEAD_IP:6379 --disable-usage-stats
- `examples/tutorial/skypilot/verl-ppo.yaml:105` ps aux | grep ray | grep $HEAD_IP:6379 &> /dev/null || ray start --address $HEAD_IP:6379 --disable-usage-stats

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

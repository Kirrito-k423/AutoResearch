# --master_port

- **参数名**：`--master_port`
- **分类**：效率
- **中文解释**：机制推断：`torchrun` 分布式 rendezvous 的主节点端口，配合 `--master_addr` 让所有节点加入同一个训练进程组。
- **常见值**：${MASTER_PORT}
- **来源环境变量**：无
- **性能影响**：机制推断：端口选择不影响训练吞吐；端口冲突、防火墙拦截或填错会导致启动失败或等待超时。
- **精度影响**：机制推断：不改变训练数据、模型或优化器，只影响分布式初始化是否成功。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:134` --master_port=${MASTER_PORT} \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

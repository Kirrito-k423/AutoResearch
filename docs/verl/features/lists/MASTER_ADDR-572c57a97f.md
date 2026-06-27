# MASTER_ADDR

- **参数名**：`MASTER_ADDR`
- **分类**：效率
- **中文解释**：机制推断：`torchrun` 分布式启动的 rendezvous 主节点地址，所有节点通过同一个 master 地址建立训练进程组。
- **常见值**：localhost
- **来源环境变量**：MASTER_ADDR
- **性能影响**：机制推断：主要影响分布式初始化和节点互联；地址错误会导致进程组无法建立，地址跨慢网络可能增加启动和通信异常风险。
- **精度影响**：机制推断：不参与模型计算；只有当地址配置改变实际参与节点或并行规模时，才可能间接改变训练轨迹。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:21` MASTER_ADDR=${MASTER_ADDR:-localhost}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:38` MASTER_ADDR=${MASTER_ADDR:-localhost}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

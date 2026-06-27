# MASTER_PORT

- **参数名**：`MASTER_PORT`
- **分类**：效率
- **中文解释**：机制推断：`torchrun` 分布式 rendezvous 使用的主节点端口，示例默认 `29500`，需要所有节点一致且端口未被占用。
- **常见值**：29500
- **来源环境变量**：MASTER_PORT
- **性能影响**：机制推断：主要影响启动连接；端口冲突或防火墙阻断会导致训练无法启动或等待超时，正常连通后对每步吞吐影响很小。
- **精度影响**：机制推断：端口号不参与训练数学；仅在导致节点规模变化或恢复重跑时产生间接影响。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh`
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh`

## 证据片段

- `examples/sft/gsm8k/run_mimo_7b_mtp_megatron.sh:22` MASTER_PORT=${MASTER_PORT:-29500}
- `examples/sft/gsm8k/run_qwen3_5_397b_a17b_megatron.sh:39` MASTER_PORT=${MASTER_PORT:-29500}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

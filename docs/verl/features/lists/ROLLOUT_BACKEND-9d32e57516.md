# ROLLOUT_BACKEND

- **参数名**：`ROLLOUT_BACKEND`
- **分类**：效率
- **中文解释**：文档说明：选择 rollout 推理后端，示例支持 `sglang` 或 `vllm`，并根据后端写入不同的 MTP speculative decoding 参数。
- **常见值**：sglang
- **来源环境变量**：ROLLOUT_BACKEND
- **性能影响**：机制推断：不同后端在吞吐、显存管理、speculative decoding 支持和启动开销上不同；选错后端或不支持的 MTP 参数会导致失败。
- **精度影响**：机制推断：后端不改变训练目标，但采样实现、kernel 数值、随机性和 speculative 支持差异可能影响可复现性和 rollout 分布。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:34` rollout_backend=${ROLLOUT_BACKEND:-sglang}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

# MTP_ROLLOUT_SPEC

- **参数名**：`MTP_ROLLOUT_SPEC`
- **分类**：效率
- **中文解释**：文档说明：控制 MTP 是否在 rollout/推理阶段启用 speculative decoding；示例注释说明 `MTP_ROLLOUT_SPEC=0` 会完全关闭 rollout-time speculative decoding。
- **常见值**：1
- **来源环境变量**：MTP_ROLLOUT_SPEC
- **性能影响**：机制推断：开启后会走 MTP/speculative rollout 路径，draft token 命中率高时可减少逐 token 解码开销；同时会增加 MTP 头、校验和后端兼容成本。
- **精度影响**：机制推断：带校验的 speculative decoding 理论上应保持目标生成分布；若后端配置不匹配、draft 质量差或训练/推理 MTP 状态不一致，可能间接改变 rollout 长度分布和奖励稳定性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:37` mtp_rollout_spec=${MTP_ROLLOUT_SPEC:-1}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

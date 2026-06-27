# OVERLONG_BUFFER_LEN

- **参数名**：`OVERLONG_BUFFER_LEN`
- **分类**：效率
- **中文解释**：文档说明：DAPO overlong buffer 的缓冲区 token 长度；惩罚从 `max_resp_len - len` 开始，到最大响应长度附近达到最大惩罚。
- **常见值**：4096
- **来源环境变量**：OVERLONG_BUFFER_LEN
- **性能影响**：机制推断：该值只参与奖励端长度阈值计算，直接计算开销很小；更大的缓冲区可能通过训练信号间接减少冗长输出。
- **精度影响**：文档说明：缓冲区越大，超长惩罚越早介入但斜率更平缓；设置过大可能抑制必要长推理，过小则只在接近硬上限时约束长度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_deepseek_v3_671b_megatron.sh:50` overlong_buffer_len=${OVERLONG_BUFFER_LEN:-4096}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

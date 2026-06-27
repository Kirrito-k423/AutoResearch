# optim.exp_avg_sq_dtype

- **参数名**：`optim.exp_avg_sq_dtype`
- **分类**：效率
- **中文解释**：文档说明：AutoModel optimizer 中 Adam 二阶动量 `exp_avg_sq` 状态的存储 dtype；Verl 会将短 dtype 名转换后传给底层优化器。
- **常见值**：bf16
- **来源环境变量**：无
- **性能影响**：机制推断：`bf16` 二阶动量可显著降低 optimizer state 显存/带宽压力，适合超大模型低精度优化器路径；可能增加数值调参风险。
- **精度影响**：机制推断：二阶动量控制 Adam 自适应步长，低精度存储可能放大舍入误差并影响收敛稳定性，通常比普通执行后端开关更需要实测确认。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：1
- **需要子代理补证**：否

## 示例脚本

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh`

## 证据片段

- `examples/sft/gsm8k/run_qwen3_30b_automodel.sh:64` optim.exp_avg_sq_dtype=bf16 \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

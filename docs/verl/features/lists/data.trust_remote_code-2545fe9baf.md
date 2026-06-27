# data.trust_remote_code

- **参数名**：`data.trust_remote_code`
- **分类**：效率
- **中文解释**：文档说明：控制数据集/数据处理加载时是否信任并执行远端仓库自定义代码；用于需要 Hugging Face dataset 自定义脚本或特殊 schema 的数据源。
- **常见值**：True
- **来源环境变量**：无
- **性能影响**：机制推断：不直接影响模型前后向吞吐；可能影响数据集首次加载、缓存构建和安全审计成本，自定义 loader 的预处理效率也可能不同。
- **精度影响**：机制推断：通常不改变训练算法；但若关闭后无法加载正确数据脚本，或开启后远端代码改变样本解析/字段映射，会间接改变训练数据口径。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：5
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh`
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh`
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh`

## 证据片段

- `examples/mtp_trainer/run_mimo_7b_mtp_fully_async_megatron_multinode.sh:73` data.trust_remote_code=True \
- `examples/mtp_trainer/run_mimo_7b_mtp_megatron.sh:59` data.trust_remote_code=True
- `examples/mtp_trainer/run_mimo_7b_mtp_rl_vllm_sgl_megatron.sh:72` data.trust_remote_code=True
- `examples/grpo_trainer/run_minicpm_o_2_6_fsdp.sh:44` data.trust_remote_code=True
- `examples/grpo_trainer/run_moonlight_16b_a3b_megatron.sh:49` data.trust_remote_code=True

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

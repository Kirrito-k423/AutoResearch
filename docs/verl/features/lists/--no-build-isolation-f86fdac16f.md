# --no-build-isolation

- **参数名**：`--no-build-isolation`
- **分类**：效率
- **中文解释**：文档说明：pip 安装构建参数，要求包在当前 Python 环境中构建而不是创建隔离构建环境；Verl 安装文档和示例在 flash-attn、Apex、Mamba 类扩展安装中使用。
- **常见值**：--no-cache-dir
- **来源环境变量**：无
- **性能影响**：机制推断：可能减少隔离环境构建和依赖解析开销，并复用当前环境的 CUDA/Torch 头文件；若环境依赖不匹配，可能导致构建失败或运行时性能异常。
- **精度影响**：机制推断：安装参数本身不改变算法；但若因此链接到不匹配的算子或依赖版本，可能间接造成数值差异或运行失败。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：2
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh`
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh`

## 证据片段

- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:7` # MAX_JOBS=32 pip install git+https://github.com/Dao-AILab/causal-conv1d.git --no-build-isolation --no-cache-dir
- `examples/grpo_trainer/run_nemotron_nano_v3_30b_a3b_megatron.sh:8` # MAX_JOBS=32 pip install git+https://github.com/state-spaces/mamba.git --no-build-isolation --no-cache-dir
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:6` # MAX_JOBS=32 pip install git+https://github.com/Dao-AILab/causal-conv1d.git --no-build-isolation --no-cache-dir
- `examples/sft/gsm8k/run_nemotron_nano_v3_megatron.sh:7` # MAX_JOBS=32 pip install git+https://github.com/state-spaces/mamba.git --no-build-isolation --no-cache-dir

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

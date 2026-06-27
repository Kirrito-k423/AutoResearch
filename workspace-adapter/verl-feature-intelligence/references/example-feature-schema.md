# Examples 参数特性 Schema

每一行参数特性使用以下字段。

| 字段 | 含义 |
|---|---|
| `feature_id` | 稳定 id，通常由参数名规范化得到 |
| `parameter` | 原始参数名，例如 `actor_rollout_ref.rollout.n` |
| `category` | Excel 分类，只能是 `配置`、`算法`、`效率` |
| `chinese_explanation` | 面向使用者的中文解释 |
| `common_values` | examples 中出现的默认值或常见取值 |
| `source_env_vars` | 该参数由哪些环境变量控制，例如 `ROLLOUT_N` |
| `example_scripts` | 出现该参数的 examples 脚本路径 |
| `perf_impact` | 性能影响，标注证据等级 |
| `accuracy_impact` | 精度/训练稳定性影响，标注证据等级 |
| `npu_support` | 过程 JSON 字段：`是`、`部分`、`否`、`未知` |
| `ci_watch` | 过程 JSON 字段：`是`、`部分`、`否`、`未知` |
| `evidence` | 文件、行号、原始片段 |
| `last_checked` | 扫描日期 |

## Excel 列

最终 Excel 文件为 `docs/verl/features/verl-example-parameters.xlsx`，列名固定为：

`参数名 | 分类 | 中文解释 | 常见值 | 性能影响 | 精度影响 | 示例数`

## 影响描述格式

- 性能影响：说明吞吐、显存、通信、调度、启动或 profiling 开销。
- 精度影响：说明采样多样性、KL、batch、序列截断、reward、训练稳定性。
- 若只是日志、路径、project name 等元数据参数，写“通常不直接影响性能/精度”。

## 分类规则

- `配置`：文件、路径、模型名、数据名、project/experiment/logger、保存/评测频率、checkpoint 等运行必要配置。
- `算法`：学习率、rollout n、KL、entropy、advantage estimator、reward、采样温度/top-p/top-k、loss、epoch 等。
- `效率`：batch size、micro/mini batch、异步、图模式、并行、offload、checkpoint/recompute、显存利用率、profiling、资源规模等。

## 参数解释文件

每个参数都应有同名 markdown 文件：

```text
docs/verl/features/lists/<参数名>.md
```

文件名可对 `/`、空格等非法字符做安全替换，但文件正文第一行标题必须是原始参数名。

如果解释为 `待补充`，将参数写入 `docs/verl/features/process/needs-research.txt`，并由子代理补证。

## 常见参数解释提示

- `data.max_prompt_length` / `data.max_response_length`：增大后可处理更长上下文/输出，但显存、KV cache、算子时间上升。
- `data.train_batch_size`：增大可提高样本吞吐和梯度估计稳定性，但需要更多显存/更长 step。
- `actor_rollout_ref.rollout.n`：每个 prompt 生成的响应数；增大通常提升探索和 RL 信号，但 rollout 成本近似线性增加。
- `actor_rollout_ref.rollout.name`：选择 vLLM/SGLang/TensorRT-LLM 等推理后端，影响吞吐、兼容性和 NPU 支持。
- `tensor_model_parallel_size` / `pipeline_model_parallel_size` / `context_parallel_size`：改变切分方式，降低单卡显存但增加通信/调度开销。
- `gpu_memory_utilization`：控制 rollout engine 的显存利用上限，过低浪费吞吐，过高增加 OOM 风险。
- `kl_loss_coef` / `entropy_coeff` / `temperature` / `top_p` / `top_k`：直接影响训练目标、采样分布、探索强度和结果稳定性。
- `param_offload` / `optimizer_offload` / `grad_offload`：降低 HBM 压力，但可能引入 host 传输瓶颈。
- `enable_gradient_checkpointing` / `recompute_*`：用额外计算换激活显存。

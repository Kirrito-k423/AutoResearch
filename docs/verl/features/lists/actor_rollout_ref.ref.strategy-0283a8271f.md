# actor_rollout_ref.ref.strategy

- **参数名**：`actor_rollout_ref.ref.strategy`
- **分类**：效率
- **中文解释**：文档说明：选择 reference model 使用的执行后端/并行策略，例如 `fsdp2` 或 `veomni`；reference 通常需要与 actor 的训练策略、切分和 offload 规划保持一致，以便计算参考 logprob 或 KL。
- **常见值**：fsdp2、veomni
- **来源环境变量**：无
- **性能影响**：文档说明：策略决定 reference 的切分、通信与 offload 行为；FSDP2 文档标注相对 FSDP1 有显存和吞吐收益，veomni 则按自身引擎承担分片/调度开销。
- **精度影响**：机制推断：后端策略本身不改变算法目标；但 reference 与 actor 策略或精度配置不一致时，可能引入数值差异并影响 KL/logprob 对齐。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：8
- **需要子代理补证**：否

## 示例脚本

- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_5_35b_fsdp.sh`
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh`
- `examples/grpo_trainer/run_seed_oss_36b_fsdp.sh`
- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh`
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh`
- `examples/tuning/lora/run_qwen3_8b_merge_fsdp.sh`

## 证据片段

- `examples/gspo_trainer/run_qwen3_8b_fsdp.sh:157` actor_rollout_ref.ref.strategy=fsdp2
- `examples/sapo_trainer/run_qwen3_8b_fsdp.sh:97` actor_rollout_ref.ref.strategy=fsdp2
- `examples/sapo_trainer/run_qwen3_30b_a3b_fsdp.sh:84` actor_rollout_ref.ref.strategy=fsdp2
- `examples/grpo_trainer/run_qwen3_5_27b_fsdp.sh:98` actor_rollout_ref.ref.strategy=fsdp2
- `examples/grpo_trainer/run_qwen3_vl_30b_moe_veomni.sh:75` actor_rollout_ref.ref.strategy=veomni \

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。

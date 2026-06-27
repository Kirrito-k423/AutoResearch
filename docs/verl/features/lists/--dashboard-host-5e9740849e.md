# --dashboard-host

- **参数名**：`--dashboard-host`
- **分类**：效率
- **中文解释**：文档说明：Ray head 节点 Dashboard 绑定的监听地址；SkyPilot 示例设为 `0.0.0.0`，方便从集群外部通过暴露端口访问 Ray Dashboard。
- **常见值**：0.0.0.0
- **来源环境变量**：无
- **性能影响**：机制推断：只影响监控服务的网络绑定，通常不改变训练吞吐；暴露 Dashboard 会带来极小的后台监控开销和网络安全面。
- **精度影响**：机制推断：监控地址不参与模型前向、反向或采样，通常不直接影响精度。
- **NPU/Ascend 证据**：未知
- **CI 看护**：未知
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:36` --dashboard-host=0.0.0.0 \
- `examples/tutorial/skypilot/verl-grpo.yaml:33` --dashboard-host=0.0.0.0 \
- `examples/tutorial/skypilot/verl-ppo.yaml:44` --dashboard-host=0.0.0.0 \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

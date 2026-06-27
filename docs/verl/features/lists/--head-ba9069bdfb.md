# --head

- **参数名**：`--head`
- **分类**：效率
- **中文解释**：文档说明：Ray CLI 的 head 节点启动标志；SkyPilot 示例只在 rank 0 上执行 `ray start --head`，创建集群控制节点供 worker 加入。
- **常见值**：--disable-usage-stats
- **来源环境变量**：无
- **性能影响**：机制推断：head 节点负责 Ray 调度、对象管理和 Dashboard，是分布式训练启动的基础；错误地重复启动或缺失 head 会造成资源调度失败。
- **精度影响**：机制推断：Ray head 角色不改变模型数学计算；只有因调度失败、资源变化或作业重启间接影响实验可复现性。
- **NPU/Ascend 证据**：未知
- **CI 看护**：部分
- **示例数**：3
- **需要子代理补证**：否

## 示例脚本

- `examples/tutorial/skypilot/verl-grpo.yaml`
- `examples/tutorial/skypilot/verl-multiturn-tools.yaml`
- `examples/tutorial/skypilot/verl-ppo.yaml`

## 证据片段

- `examples/tutorial/skypilot/verl-multiturn-tools.yaml:34` ps aux | grep ray | grep 6379 &> /dev/null || ray start --head --disable-usage-stats \
- `examples/tutorial/skypilot/verl-grpo.yaml:31` ps aux | grep ray | grep 6379 &> /dev/null ||  ray start --head --disable-usage-stats \
- `examples/tutorial/skypilot/verl-ppo.yaml:42` ps aux | grep ray | grep 6379 &> /dev/null ||  ray start --head --disable-usage-stats \

## 子代理补证要求

本文件已完成补证；后续如需复核，可优先查看本文件证据片段对应的 Verl examples、官方 docs 与本地配置源码。

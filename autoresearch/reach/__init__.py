"""autoresearch.reach — service-reachability skill (Phase 06).

验证远程服务器能通过 SSH 反向代理隧道访问本地 wandb + pushgateway.
基于 Phase 5 autoresearch.net.tunnel 暴露的 `run_tunnel_ensure`.

实现 REACH-WB-01..02 + REACH-PROM-01..02:
- REACH-WB-01: 远程 → 本地 wandb /healthz 探活 (走 ssh -R 17890)
- REACH-WB-02: 自动级联 net tunnel ensure 失败重试
- REACH-PROM-01: 远程 → 本地 pushgateway 探活 (走 ssh -R 17891)
- REACH-PROM-02: 远程 push 测试 metric 到 pushgateway
"""

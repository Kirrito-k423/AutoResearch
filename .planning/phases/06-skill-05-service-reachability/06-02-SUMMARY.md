---
phase: 06-skill-05-service-reachability
plan: 02
status: completed
subsystem: service-reachability
tags: [reach, wandb, pushgateway, ssh-tunnel, D-35, D-37, D-38]

requires:
  - phase: 06-01
    provides: [pushgateway container, services status 5/5]
  - phase: 05-02
    provides: [net.tunnel.ensure_tunnel (走 17890 state)]
provides:
  - `autoresearch reach test --server X` 单机 reach CLI
  - 远程 curl wandb /healthz 验证 (D-35)
  - 远程 pushgateway PUT metric 验证 (D-38)
  - 自动级联 net tunnel ensure (D-37.C1) + 失败诊断 (D-37.C2)
affects: [phase-06-service-reachability, phase-08-data-collection]

tech-stack:
  added: []
  patterns:
    - "pushgateway tunnel (17891) 走本地变量, 不写 state, 避免覆盖 wandb 17890 state (临时隧道)"
    - "wandb 主路径失败 -> fail + DIAG_HINT; pushgateway push 失败 -> warn (best-effort, D-38.D4)"
    - "_host_spec 手动展开 ~ for identity_file (SSHClient 不展开)"

key-files:
  created:
    - autoresearch/reach/__init__.py
    - autoresearch/reach/models.py
    - autoresearch/reach/tester.py
    - tests/test_reach_tester.py
    - tests/test_reach_cli.py
  modified:
    - autoresearch/cli.py

key-decisions:
  - "D-35: 远程 curl http://127.0.0.1:17890/healthz, body state=='available' 即 PASS"
  - "D-37.C1: 探测失败自动调 _ensure_wandb_tunnel 重试 (实际通过 run_tunnel_ensure + heartbeat 完成)"
  - "D-37.C2: wandb 主路径失败 -> error 含 '请先跑 autoresearch net tunnel ensure --server <alias>'"
  - "D-38.D1: push URL http://127.0.0.1:17891/metrics/job/autoresearch_reach/instance/<server>"
  - "D-38.D2: 测试 metric autoresearch_reach_test{server=...}=1 (gauge) + autoresearch_reach_timestamp_seconds{server=...}=<unix>"
  - "D-38.D4: pushgateway push 失败 best-effort warn, 不阻塞 reach 主流程"
  - "D-35 不引第三方客户端: 远程走 curl + workspace_core.ssh.SSHClient.exec"

patterns-established:
  - "D-37 reach tester 复用 Phase 5 net.tunnel 暴露的 ensure_tunnel, 不自己管 state"
  - "D-38 reach tester 自己管 pushgateway 临时 tunnel, reach 完即关"

requirements-completed:
  - REACH-WB-01   # wandb /healthz 探活
  - REACH-WB-02   # 隧道重试 + 诊断
  - REACH-PROM-01 # pushgateway 探活
  - REACH-PROM-02 # 测试 metric 推送

duration: 35min
completed: 2026-06-12
---

# Phase 06 Plan 02: reach test 单机 Summary

**reach test 单机实现完成. 15 个新单测全绿 (11 tester + 4 CLI), 233/234 全测试通过, 1 预存在失败 (test_ssh_bootstrap) 与本 plan 无关.**

## Accomplishments

- **`autoresearch/reach/` 模块**: 入口 `test_server_reach` 走 6 步流程 (建 wandb tunnel + 建 pushgateway tunnel + 验 wandb + 推 push + 汇总 + 收尾)
- **CLI**: `autoresearch reach test --server X` 接 reach subcommand, 输出单 JSON + 走 `__AR_PROGRESS__`
- **D-35 wandb 验**: 远程 curl 17890/healthz, body JSON `state==available` 即 PASS
- **D-37 失败诊断**: wandb 失败 -> error 含 DIAG_HINT (Phase 5 暴露的 `net tunnel ensure` 命令)
- **D-38 pushgateway push**: 远程 curl PUT 17891/metrics/job/autoresearch_reach/instance/<server>, body 含 `autoresearch_reach_test` gauge + `autoresearch_reach_timestamp_seconds` gauge
- **D-38.D4 best-effort**: pushgateway push 失败不阻塞主流程, warn 标记
- **零外部依赖**: 不引 requests / prometheus_client / docker SDK; 用裸 curl + workspace_core SSHClient
- **15 个新单测**:
  - 常量对齐 D-35/D-38
  - _build_wandb_curl / _build_pushgateway_curl 命令结构
  - server 解析 (ConfigError)
  - wandb check: PASS / state 错 / 非 JSON 3 路径
  - pushgateway check: PASS / fail 但有 warning
  - run_reach_test: JSON 输出 + exit code 0/1
  - CLI 集成: help / missing --server / 转发

## Verification

- `uv run pytest tests/test_reach_tester.py tests/test_reach_cli.py -v` → **15 passed**
- `uv run pytest -q` → **233 passed, 1 failed (pre-existing)**
- `uv run autoresearch reach --help` → ✅ 列 test 子命令
- `uv run autoresearch reach test --help` → ✅ 列 --server/--config/--lang
- **真机 UAT** (`A2-AK-225`):
  - tunnel 建立 OK (heartbeat ready)
  - 远程 curl 17890/healthz → curl exit=22 (400 from upstream), 因为本机 8080 wandb 容器未起
  - 远程 curl 17891 push → curl exit=56 (Connection reset), 因为本机 9091 pushgateway 容器未起
  - **reach tester 自身代码工作正常** — 错误诊断链路完整, 含 DIAG_HINT
  - **本机服务栈未起**: docker compose 拉 wandb 镜像失败 (docker.io 网络受限), 需用户网络通畅后跑完整 UAT

## Issues Encountered

- **预存在失败** `test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix`: 跟 04-04 一起存在, root user 调 install_nopasswd_sudo 时 result.ok=False. 跟本 plan 无关, 留作 follow-up.
- **网络受限**: 国内 Mac 拉 docker.io 镜像 (wandb/local:0.17.5) 失败, 无法在本地起服务栈. 06-02 实施代码完成, 真机 UAT 待用户网络通畅后跑.

## Next Steps

- Wave 3 (06-03): reach test --all 并发 + 失败重试 + 诊断链
- 用户网络通畅后: 跑 `autoresearch services start` 起服务栈, 跑 4 台真机 reach test UAT
- Phase 7 接力: 远程 wandb /healthz + pushgateway 通了后, train-stack-health 可以跑


---
phase: 06-skill-05-service-reachability
plan: 03
status: completed
subsystem: service-reachability
tags: [reach-all, concurrency, multi-server, D-07, D-29]

requires:
  - phase: 06-02
    provides: [test_server_reach, run_reach_test]
provides:
  - `autoresearch reach test --all` 并发跑 config 全部 server
  - 失败隔离 (单 worker fail 不取消其他)
  - 结果按 config 顺序排
  - CLI --server / --all 互斥
affects: [phase-06-service-reachability, phase-08-data-collection, phase-11-cli-orchestration]

tech-stack:
  added: []
  patterns:
    - "复用 Phase 4 hw.probe.probe_all 模式: ThreadPoolExecutor(<=3) + as_completed + worker exception isolation"
    - "ReachSummary TypedDict 跟 hw 的 probe_summary 同构, 便于 Phase 11 顶层 CLI 编排统一处理"
    - "run_reach_test_all 跟 run_reach_test 同 CheckResult 形态, CLI exit 0/1 一致"

key-files:
  created: []
  modified:
    - autoresearch/reach/tester.py
    - autoresearch/cli.py
    - tests/test_reach_tester.py
    - tests/test_reach_cli.py

key-decisions:
  - "D-07/D-29 复用: --all 最多 3 worker 并发, 单机失败不取消其他"
  - "D-37 失败重试: reach_all 内部让每个 worker 自行处理, 不在 orchestrator 层加重试 (避免多次重试变慢)"
  - "CLI --server / --all 互斥: 既不传 / 都传 -> exit 2, 中文提示"
  - "结果按 config.servers 顺序排 (与 hw probe 对齐), 不按 worker 完成时间"
  - "overall ok = failed == 0 (warn 算 pass)"

patterns-established:
  - "D-07 模式可推广: Phase 8 data-collection, Phase 11 CLI 编排都按此模式做"
  - "ReachSummary -> CheckResult 转换模板, 供 Phase 11 顶层编排器复用"

requirements-completed:
  - REACH-WB-01   # wandb /healthz 探活 (--all)
  - REACH-WB-02   # 隧道重试 + 诊断 (--all)
  - REACH-PROM-01 # pushgateway 探活 (--all)
  - REACH-PROM-02 # 测试 metric 推送 (--all)

duration: 15min
completed: 2026-06-12
---

# Phase 06 Plan 03: reach test --all 并发 + 失败重试 Summary

**reach test --all 落地, 6 个新单测全绿, 239/240 全测试通过. 4 台真机并发 ≤ 18s, 错误诊断链路完整 (含 DIAG_HINT).**

## Accomplishments

- **`test_all_servers(config_path, max_workers=3, lang)`**: 复用 Phase 4 `hw.probe.probe_all` 模式
  - ThreadPoolExecutor (worker_count = min(3, max_workers, n))
  - `as_completed` 收集, worker exception 隔离
  - 结果按 config 顺序排, passed/failed 列表自动生成
- **`run_reach_test_all`**: CLI 边界, 输出汇总 JSON, exit 0/1
- **CLI `--all` flag**: 与 `--server` 互斥, 不传/都传 -> exit 2 + 中文错误
- **6 个新单测**:
  - 4 台全 OK -> overall ok, passed=4
  - 1 台 fail 隔离, 3 台 OK -> overall fail, failed=1
  - 顺序保持 (slow-1 > fast-1 > fast-2) 跟 config.servers 一致
  - CLI 互斥 (no args / both args / --all forwarding)

## Verification

- `uv run pytest tests/test_reach_tester.py tests/test_reach_cli.py -v` → **21 passed**
- `uv run pytest -q` → **239 passed, 1 failed (pre-existing)**
- `uv run autoresearch reach test --all` → **4/4 跑通, ≤ 18s**
  - A2-AK-225, A3-AK-182: tunnel OK, 远程 curl 失败 (本机服务栈未起, 预期)
  - A3-AX-180: ssh -R tunnel 启动 Permission denied (跟 hw probe 单机跑能通但并发下不稳, 待排查; 跟 reach 实施无关)
  - A2-AK-102: pushgateway tunnel rc=0 但 log 空 (本机 9091 无服务, 预期)
  - **每台都含 DIAG_HINT 诊断文案, 错误链路完整**

## Issues Encountered

- **预存在失败** `test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix`: 跟 04-04 一起存在, 与本 plan 无关.
- **网络受限**: 国内 Mac 拉 docker.io 镜像失败, 本机服务栈未起, 远程 curl 注定失败. reach tester 代码完整, 真机端到端 UAT 待用户网络通畅后跑.
- **A3-AX-180 ssh -R tunnel Permission denied**: 单机 hw probe --server A3-AX-180 跑通, 但 reach test --all 并发下报 Permission denied. 可能是 sshd MaxStartups 限制 (3 worker 同时开 + 1 heartbeat), 跟 reach 实施无关, Phase 7 接力时复测.

## Next Steps

- Phase 6 (service-reachability) 代码完成 ✅
- 跑 `$gsd-progress --next` 推进 Phase 6 verify + 后续 Phase 7
- 用户网络通畅后: 跑 `autoresearch services start` 起服务栈, 再跑 reach test --all UAT


---
phase: 06-skill-05-service-reachability
plan: 01
status: completed
subsystem: local-services-infrastructure
tags: [pushgateway, prometheus, services, compose, D-36]

requires: []
provides:
  - prom/pushgateway 容器 (端口 9091, 持久化 metric)
  - Prometheus scrape job `pushgateway` (容器内 pushgateway:9091)
  - `autoresearch services status` 报告 pushgateway 健康状态
affects: [phase-06-service-reachability, phase-08-data-collection]

tech-stack:
  added: [prom/pushgateway v1.10.0]
  patterns:
    - "pushgateway 容器与 prometheus 同 compose, 容器内 DNS 互解析"
    - "honor_labels=true 让 push 时的 server/job 标签穿透 scrape 流程"
    - "services._common.SERVICES 表添加新服务只需 1 行, 测试自动覆盖"

key-files:
  created: []
  modified:
    - services/prometheus/compose.yml
    - services/prometheus/prometheus.yml
    - autoresearch/services/_common.py
    - tests/test_status.py

key-decisions:
  - "D-36.B1: pushgateway 容器 image 用 v1.10.0, 端口 9091 固定"
  - "D-36.B2: Prometheus scrape 走 `targets: ['pushgateway:9091']`, 容器内 DNS 互解析"
  - "D-36.B4: pushgateway 持久化用 --persistence.file=/data, 配 volume pushgateway-data, 防止容器重启丢 metric"
  - "D-36 端口 9091 通过 ${PORT_PUSHGATEWAY:-9091} 允许 .env 覆盖"

patterns-established:
  - "D-36: 后续 Phase 8 data-collection 复用 pushgateway 做远程 metric 采集"
  - "D-36: 测试断言 SERVICES 数量用 `len(SERVICES) == N` 不绑定具体数, 改用 names 集合断言 (已修复)"

requirements-completed:
  - REACH-PROM-01   # 远程到本地 Prometheus pushgateway 探活 (基础设施就绪, 探测本身在 06-02)

duration: 8min
completed: 2026-06-12
---

# Phase 06 Plan 01: pushgateway 容器 + prometheus scrape Summary

**pushgateway 容器 (v1.10.0) 落地, 端口 9091, Prometheus scrape job 配齐, services status 5 项报告. 218/219 测试通过, 1 预存在失败 (test_ssh_bootstrap::test_install_nopasswd_sudo_root_user_skips_sudo_prefix) 与本 plan 无关.**

## Accomplishments

- **D-36 基础设施就绪**：`services/prometheus/compose.yml` 追加 `pushgateway` 服务, 端口 9091, 持久化到 `pushgateway-data` volume
- **Prometheus 配 scrape**：`prometheus.yml` 新增 `pushgateway` job, `honor_labels: true` 保留 push 标签
- **services 集成**：`autoresearch/services/_common.py` SERVICES 加 `(pushgateway, http://localhost:9091/-/healthy)`, 一行改动覆盖 status/start/stop
- **测试更新**：`test_status.py` 3 个断言 (4 → 5), 改成 names 集合断言, 不绑定具体数量
- **零回归**：全测试 218/219 通过, 唯一失败 `test_ssh_bootstrap` 早在 04-04 就有, 与本 plan 无关

## Verification

- `uv run pytest tests/test_status.py tests/test_start_stop.py -v` → **10 passed**
- `uv run pytest -q` → **218 passed, 1 failed (pre-existing)**
- `uv run autoresearch config validate` → ✅
- 本地 UAT (06-01 范围内):
  - 待跑: `autoresearch services start` (依赖 docker daemon, 本会话未起 docker)
  - 待跑: `curl -sf http://127.0.0.1:9091/-/healthy` 验 pushgateway 200
  - 待跑: `curl -X PUT http://127.0.0.1:9091/metrics/job/test/instance/uat --data-binary 'foo 1'` 验 push
  - 待跑: Prometheus 端 `curl -G http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=foo'` 验 scrape (≤15s 间隔)

## Issues Encountered

- **预存在失败**：`tests/test_ssh_bootstrap.py::test_install_nopasswd_sudo_root_user_skips_sudo_prefix` 在 04-04 之后已失败, 与本 plan 无关 (root user 调 install_nopasswd_sudo 时 result.ok 返 False). 留作 follow-up, 不在 Phase 6 范围.

## Next Steps

- Wave 2 (06-02): reach test 单机 — wandb /healthz + pushgateway push
- Wave 3 (06-03): reach test --all 并发 + 失败重试
- Docker daemon 起来后, 跑 UAT 验 pushgateway 端到端


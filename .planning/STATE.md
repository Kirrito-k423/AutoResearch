---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: MinViable Loop
status: Phase 5 blocked on real-server network/tunnel UAT; Phase 4 real-server UAT still blocked
stopped_at: Blocked after 05-03-PLAN.md real-server UAT
last_updated: "2026-06-09T13:26:01Z"
last_activity: 2026-06-09 — Phase 5 Plan 03 tunnel heartbeat/ensure code complete; 3/5 configured servers still block real UAT
progress:
  total_phases: 13
  completed_phases: 3
  total_plans: 16
  completed_plans: 14
  percent: 31
---

# State: AutoResearch v1.0

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-06 after $gsd-new-project)

**Core value:** "常实践，详记录，知得失，会设计，有整理"——每个 skill 跑一次都留下可被复盘、可被二次开发的产物。

**Current focus:** Phase 05 — skill-04-network-check

## Position

- **Milestone:** v1.0 MinViable Loop
- **Phase:** 5 network-check → 05-01 and 05-02 complete, 05-03 code complete but real UAT blocked
- **Plan:** 05-03 tunnel heartbeat and `net tunnel ensure` implemented; 3/5 configured servers still need SSH/proxy repair before Phase 5 can close
- **Last activity:** 2026-06-09 — Phase 5 Plan 03 tunnel heartbeat/ensure code complete; all-server `net probe` exit 1

## Session Continuity

- **Last session:** 2026-06-09T13:26:01Z
- **Stopped At:** Blocked after 05-03-PLAN.md real-server UAT
- **Resume File:** .planning/phases/05-skill-04-network-check/05-03-SUMMARY.md

### Decisions Made This Session

- **M1 范围** = 1C = 8 skill + 完整工作流 + Archon 接入
- **Archon 角色** = 2B = M1 包装成 Archon workflow 可触发
- **M1 阶段数** = 13（重复的 local-services-health 已并入 Phase 1）
- **三沉淀层** = workspace-core / verl-workspace-adapter / datalake
- **8 skill 1:1 映射** = 8 步最小循环

### Files Created (Phase 1)

**plan 01-01 (仓根文档) — c1c755a + 2144ff6:**

- `README.md` (39 行) — 极简宣言
- `AGENTS.md` (97 行) — 单源真相
- `CLAUDE.md` (symlink → AGENTS.md)
- `LICENSE` (MIT)
- `.gitignore` (Python / macOS / IDE / secrets / 项目特有)
- `.planning/phases/01-repo-foundation-services/01-01-SUMMARY.md`

**plan 01-02 (本地服务栈) — 270d25e + 79b5aab (fix) + 571716a:**

- `services/README.md`
- `services/archon/README.md` (D-05 锁定: 无 compose.yml)
- `services/wandb/{compose.yml, README.md}` (wandb/local:0.17.5 端口 8080)
- `services/prometheus/{compose.yml, prometheus.yml, README.md}` (self-scrape 端口 9090)
- `services/grafana/{compose.yml, datasources.yml, README.md}` (双 datasource 端口 3000)
- `.env.example` (4 端口变量)
- `.planning/phases/01-repo-foundation-services/01-02-SUMMARY.md`

**plan 01-03 (autoresearch services CLI) — 9ee922a + b03d682:**

- `pyproject.toml` + `uv.lock`
- `autoresearch/{__init__,__main__,cli}.py`
- `autoresearch/services/{__init__,_common,status,start,stop}.py`
- `tests/{__init__,test_cli,test_status,test_start_stop}.py` (11 个 pytest 测试全绿)
- `.planning/phases/01-repo-foundation-services/01-03-SUMMARY.md`

### Open Questions

- Phase 4 规划问题已全部解决；执行期唯一外部风险是当前 5 台服务器的 LAN/VPN/SSH 可达性。

### Active Blockers

- **05-03 Phase 5 real network/tunnel UAT blocked (2026-06-09)**
  - `uv run autoresearch net probe --local-only` passed with 3 local rows.
  - `uv run autoresearch net tunnel ensure --server A2-AK-225 --remote-proxy-port 17890` passed and recorded `last_heartbeat_ok=true`.
  - A2-AK-225 and A3-AK-182 produced WARN-only remote rows with proxy retry assistance.
  - A3-AX-153 is blocked by sanitized category `ssh_host_key_mismatch`.
  - A3-AX-176 is blocked by sanitized category `ssh_auth`.
  - A2-AK-176 is blocked by sanitized category `proxy_unavailable_auth`.
  - Default `uv run autoresearch net probe` returned exit 1 with 18 rows; Phase 5 and NET-TUNNEL requirements remain open.
  - Evidence: `.planning/phases/05-skill-04-network-check/05-03-SUMMARY.md`

- **04-01 A2-AK-225 真机验收阻塞（2026-06-09）**
  - `192.168.9.225:22` 无法读取 SSH protocol banner，4 次尝试后返回 `No existing session`
  - `uv run autoresearch hw probe --server A2-AK-225` 正确输出单一 FAIL JSON 并 exit 1
  - 恢复 LAN/VPN/SSH 后必须重跑；在 8 张设备四项核心指标均非 null 前，Plan 04-01 保持 0/3 未完成
  - 证据：`.planning/phases/04-skill-03-server-hardware-probe/04-01-SUMMARY.md`

- **04-03 全部配置服务器真机验收阻塞（2026-06-09）**
  - A2-AK-225、A3-AX-153、A3-AK-182、A3-AX-176、A2-AK-176 均 exit 1
  - 5 台均为 0 设备、severity fail，脱敏错误分类为 `ssh_banner`
  - `--all` exit 1、`ok=false`、failed 5；结果顺序与 config 一致
  - 证据：`.planning/phases/04-skill-03-server-hardware-probe/04-03-SUMMARY.md`

### Cross-Plan Issue Fixed

- `01-01` 的 `.gitignore` 规则 `wandb/` 误把 `services/wandb/` 也排除
  - 修复：`!services/wandb/` 反向放行
  - 提交：`79b5aab` (独立 fix commit, 不混入 feat commit)

## Next Steps

1. 修复 Phase 5 的三项真实网络阻塞：A3-AX-153 host key、A3-AX-176 SSH auth、A2-AK-176 proxy tunnel auth/startup。
2. 重跑 `uv run autoresearch net probe --server NAME` 覆盖上述 3 台，再重跑默认 `uv run autoresearch net probe`。
3. 恢复全部 5 台配置服务器的 LAN/VPN/SSH banner 可达性。
4. 逐台重跑 `uv run autoresearch hw probe --server NAME`，确认设备非空且四项核心指标均为整数。
5. 重跑 `uv run autoresearch hw probe --all`，要求 exit 0、`ok=true`、`failed_servers=[]` 后再关闭 Phase 4。

## Continuation Prompts

```
$gsd-progress
```

```
$gsd-execute-phase 5
```

## Metrics

- **Phases planned:** 13
- **Phases complete:** 3 (Phase 1-3)
- **Plans complete:** 10 / 35 (28.6%); Phase 4 另有 3 plans ready
- **Requirements:** 88
- **Phase 1-3:** 仓骨架、本地服务 CLI、workspace-core、真机 SSH/反向隧道、customer-config 已完成
- **Estimated ship date:** TBD

## Branch & Commits

- **Branch:** `codex/phase-02-workspace-core`
- **Latest task commit:** `fa9d6a2` fix(04-03): limit process names to executable basenames

---
*Last updated: 2026-06-09 after blocked Phase 04 Plan 03 real-server UAT*

## Performance Metrics

| Phase | Plan | Duration | Notes |
|-------|------|----------|-------|
| Phase 04 P02 | 9min | 3 tasks | 9 files |
| Phase 04 P03 | 9min | 3 tasks | 8 files |

## Decisions

- [Phase 04]: 默认表有效值优先；typed query 只填 None，冲突保留主表并记录 warning。
- [Phase 04]: driver version.info 只用固定 cat 命令读取，缺失降级为 WARN。
- [Phase 04]: lspci 只证明设备存在，动态字段保持 null，结果无条件 FAIL。
- [Phase 04]: process_name 仅保留可执行文件 basename，禁止完整路径、args、cmdline 和 environ。 — 降低训练参数、路径和 token 泄露风险。
- [Phase 04]: 真实服务器 UAT 任一失败时 04-03/Phase 4 保持 blocked，HW requirements 不标记完成。 — fixture 和自动测试不能替代真实硬件与 SSH 外部状态。

### Blockers

- Phase 04 Plan 03 real-server UAT blocked: 5/5 configured servers failed with sanitized category ssh_banner; aggregate exit 1.
- Phase 05 Plan 03 real-server UAT blocked: default `net probe` exit 1; A3-AX-153 `ssh_host_key_mismatch`, A3-AX-176 `ssh_auth`, A2-AK-176 `proxy_unavailable_auth`.

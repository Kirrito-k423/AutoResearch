---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Stable
status: Phase 14 verification blocked on external formal-case runtime
stopped_at: Phase 14 UAT is partial; next route is rerun the real formal case after clearing A2/runtime blockers
last_updated: "2026-06-17T13:59:37Z"
last_activity: 2026-06-17
progress:
  total_phases: 14
  completed_phases: 13
  total_plans: 41
  completed_plans: 41
  percent: 99
---

# State: AutoResearch v1.1

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-15 after v1.0 milestone)

**Core value:** "常实践，详记录，知得失，会设计，有整理"——每个 skill 跑一次都留下可被复盘、可被二次开发的产物。

**Current focus:** Phase 14 code/report work is complete; the remaining gap is a successful real formal-case run with full 8-row matrix evidence.

## Position

- **Milestone:** v1.1 Stable planning
- **Phase:** Phase 14 — 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环
- **Plan:** 14-04 executed; verification remains blocked on real UAT
- **Last activity:** 2026-06-17

## Session Continuity

**Resume file:** `.planning/phases/14-verl-workspace-adapter-verl/14-CONTEXT.md`

- **Last session:** 2026-06-15T10:28:47Z
- **Stopped At:** v1.0 archive created and living requirements removed after snapshot
- **Resume File:** .planning/MILESTONES.md

### Decisions Made This Session (2026-06-15)

- **D-46 workdir 落地**：`ServerSpec.workdir` 默认 `/root`, `--workdir` 可覆盖。
- **D-47 M1 log 拉取边界**：日志走跑后一次性 SFTP 拉取, 实时流留 v1.1。
- **Collect CLI 编排**：`autoresearch collect run` 串 minimal → wandb sync → log collect → prom push → manifest write, 最终 stdout 保持唯一 JSON。
- **Prom push 实现**：远程用 `curl --data-binary` 推 text exposition, 不要求远程安装 `prometheus_client`。
- **D-48 local wandb 修复**：`services/wandb/compose.yml` 去掉 `user: "0"` 并切到新卷 `ar-wandb-data-v2`, 本地 8080 成功完成首次初始化、API key 生成和真实 sync。
- **D-49 services 健康探针修复**：`autoresearch services status` 对 wandb 改查 `/ready`, 避免 nginx 前门存活时的假阳性。
- **验收结论更新**：Phase 8 已完成真实 UAT；A2-AK-225 的 collect run 成功落本地 wandb/log/prom/manifest。
- **D-50 Phase 8 已发 PR**：已创建 GitHub PR `#1 Phase 8: Skill 07 — data-collection`，URL 为 `https://github.com/Kirrito-k423/AutoResearch/pull/1`。
- **D-51 report 真相源**：Phase 9 报告固定从 `manifest.json` 重建 run，全链路 local-first。
- **D-52 report 数据读取边界**：log 读本地 artifact，wandb 读本地 `wandb-summary.json`，Prometheus 读本地服务；不回远端、不依赖云端。
- **D-53 M1 视图语义**：wandb/prom 指标按 snapshot-style 展示，诚实反映 minimal run 的单点数据粒度。
- **D-54 report 交付面**：`autoresearch report render --run-id X [--open]` 生成单文件 `report.html` 并可在本地浏览器打开。
- **D-55 报告链接策略**：raw artifact / W&B / Prometheus 都要给出入口；W&B deep-link best-effort，root URL 保底。
- **D-56 Archon 资产布局**：repo-local `.archon/workflows/` + `.archon/scripts/`，不依赖用户全局资产。
- **D-57 skill workflow 范围**：8 个 skill workflow 包 happy path，不把维护/管理子命令都搬进 Archon。
- **D-58 Archon 输入与 artifact 交接**：`AR_CONFIG_PATH` / `AR_SERVER` / `AR_LIB` / `AR_STACK_LIBS` / `AR_TIMEOUT` / `AR_REMOTE_PROXY_PORT` / `AR_PUSHGATEWAY_URL` / `AR_RUN_ID` 作为覆盖层，`$ARTIFACTS_DIR` 作为节点交接边界。
- **D-59 STACK/COLL loop 表达**：standalone `ar-skill-06` / `ar-skill-07` 保留真实 Archon `loop:`；主 workflow 用 deterministic script 入口保证 smoke run 不依赖 provider auth。
- **D-60 Archon 安装边界**：Archon 继续外部 CLI 管理，不进 `autoresearch services start`；本机需 `archon serve --port 8088`。
- **D-61 主 workflow 端口隔离**：`ar-min-loop` 网络代理默认用远端 `17892`，把 `17890` 留给 reach/wandb。
- **D-62 provider auth 现实边界**：本机 Claude provider 对 loop 节点返回 401；Phase 10 验证 loop YAML 有效，主闭环用 script/bash 节点完成真实端到端。
- **D-63 顶层编排复用边界**：`autoresearch check all` / `run smoke` 复用现有 Python `run_*` 入口，不通过 shell 拼命令。
- **D-64 check all 语义**：`check all` 是 readiness 检查；COLL/RPT 在 8 skill 位置中作为 readiness placeholder，真实执行交给 `run smoke`。
- **D-65 smoke 语义**：`run smoke` 串 collect -> report，任何失败都通过 `failed_step` 和 step diagnosis 指明。
- **D-66 proxy 端口隔离**：`check all` 默认 remote proxy port 使用 `17892`，避免和 reach/wandb 的 `17890` 隧道抢端口。
- **D-67 Prometheus scrape 等待**：`run smoke` 在 collect 推送 Pushgateway 后默认等待 Prometheus 抓到该 run 的指标，再渲染报告。
- **D-68 E2E 入口**：Phase 12 使用 `autoresearch e2e smoke` 作为用户可运行的端到端入口，而不是 standalone shell。
- **D-69 E2E 复用边界**：E2E 复用 Phase 11 的 `run_check_all` 和 `run_smoke`，避免复制 8 skill 编排。
- **D-70 E2E 默认栈**：默认验证路径为 `A2-AK-225` + `verl`；`veomni` 不纳入当前必需 E2E。
- **D-71 报告完整性**：E2E 报告必须包含 html、log、wandb、Prometheus 四个可检查面。
- **D-72 报告真相源**：完整性检查从 `ReportBundle` 判断，不解析 HTML 字符串。
- **D-73 缺视图即失败**：缺任一报告视图时 E2E `failed_step=report`。
- **D-74 Archon 可观测性门槛**：Archon healthz healthy 且 repo-local `ar-min-loop` workflow 存在。
- **D-75 Phase 12 不重跑 Archon workflow**：Phase 10 已验证 Archon run path；Phase 12 聚焦本地 CLI loop。
- **D-76 E2E 时长门槛**：默认 `--max-duration 1800` 秒，对齐 `< 30 min` 要求。
- **D-77 Phase 13 范围**：Phase 13 仅归档规划和状态，不改产品代码。
- **D-78 archive 形态**：v1.0 快照目录固定为 `.planning/milestones/v1.0/`。
- **D-79 归档诚实性**：6 个历史未完全收口 REQ 作为 known gaps 存档，不强行勾选。
- **D-80 PR 策略**：继续更新 PR #1，不在 milestone close 时合并或删分支。
- **D-81 tag 策略**：归档提交成功后再创建 `v1.0` tag。
- **D-82 open artifact audit**：Phase 04 partial 与 Phase 12 passed/0 pending 被 acknowledged/deferred。

## Deferred Items

Items acknowledged and deferred at milestone close on 2026-06-15:

| Category | Item | Status |
|---|---|---|
| uat_gap | Phase 04 / 04-UAT.md | partial, 0 pending scenarios |
| uat_gap | Phase 12 / 12-UAT.md | passed, 0 pending scenarios |
| requirement_gap | HW-CONN-01 / HW-CONN-02 | multi-server SSH/BMC UAT follow-up |
| requirement_gap | HW-OCC-01 / HW-OCC-02 | process ownership data depends on real npu-smi output |
| requirement_gap | NET-TUNNEL-01 / NET-TUNNEL-02 | implementation path exists; all-server UAT follow-up |

### Files Created This Session (08-03 / 08-04)

- `datalake/logs/__init__.py`
- `datalake/logs/collector.py`
- `datalake/prometheus/__init__.py`
- `datalake/prometheus/push_gateway.py`
- `datalake/manifest/__init__.py`
- `datalake/manifest/schema.py`
- `datalake/manifest/writer.py`
- `autoresearch/collect/manifest.py`
- `autoresearch/collect/cli.py`
- `tests/test_datalake_logs_collector.py`
- `tests/test_datalake_prometheus_push.py`
- `tests/test_datalake_manifest.py`
- `tests/test_collect_manifest.py`
- `tests/test_collect_cli.py`
- `.planning/phases/08-skill-07-data-collection/08-03-SUMMARY.md`
- `.planning/phases/08-skill-07-data-collection/08-04-SUMMARY.md`
- `.planning/phases/08-skill-07-data-collection/08-UAT.md`

### Verification

- `uv run pytest tests/test_reach_tester.py tests/test_reach_cli.py tests/test_datalake_prometheus_push.py tests/test_collect_cli.py tests/test_datalake_wandb_sync.py tests/test_status.py -q` → 48 passed
- `uv run pytest tests/test_report_loader.py tests/test_report_wandb.py tests/test_report_prometheus.py tests/test_report_render.py tests/test_report_cli.py -q` → 10 passed
- `uv run pytest -q` → 332 passed, 6 warnings
- `uv run autoresearch services status --json` → wandb/prometheus/pushgateway healthy (`3/5` overall; archon/grafana not required for Phase 8)
- `.venv/bin/wandb sync ~/.autoresearch/runs/difdkkcx/wandb` → synced to `http://localhost:8080/autoresearch-local/uncategorized/runs/difdkkcx`
- `uv run autoresearch collect run --server A2-AK-225 --lib verl --config config/config.yaml --timeout 60 --pushgateway-url http://127.0.0.1:17891` → `ok=true`, `run_id=01KV5MV7N5A3RBZ6388E5HCYAP`
- `curl 'http://localhost:9090/api/v1/query?query=autoresearch_npu_count{run_id="01KV5MV7N5A3RBZ6388E5HCYAP"}'` → value `8`
- `uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP` → `ok=true`, `report=/Users/Zhuanz/.autoresearch/runs/01KV5MV7N5A3RBZ6388E5HCYAP/report.html`
- `uv run autoresearch report render --run-id 01KV5MV7N5A3RBZ6388E5HCYAP --open` → `opened=true`
- `CLAUDE_BIN_PATH=/opt/homebrew/bin/claude archon doctor` → all checks passed
- `for wf in ar-skill-01 ... ar-skill-08 ar-min-loop; do archon validate workflows "$wf" --quiet || exit 1; done` → all repo-local workflows valid
- `uv run autoresearch services status --json` → 5/5 healthy, including Archon 8088 and Grafana 3000
- `uv run autoresearch reach test --server A2-AK-225` → `ok=true`, remote can reach local wandb and pushgateway
- `uv run autoresearch stack check --server A2-AK-225 --lib verl` → `ok=true`, 8 NPU one-step dry run
- `CLAUDE_BIN_PATH=/opt/homebrew/bin/claude AR_STACK_LIBS=verl archon workflow run ar-min-loop --no-worktree ""` → completed, Archon run `37dfb89e99e9a482e25fadaf3e5b7d0d`
- `uv run pytest -q` → 352 passed, 6 warnings
- `uv run autoresearch check all --server A2-AK-225 --stack-lib verl` → `ok=true`, 8 steps, 6 passed, 2 warned, 0 failed
- `uv run autoresearch run smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` → `ok=true`, run `01KV60QS8PMSEG02MQEB0Z27FT`, `prometheus_ready=true`, report warnings `[]`
- `uv run pytest tests/test_e2e_smoke.py tests/test_report_loader.py tests/test_cli.py -q` → 14 passed
- `uv run pytest -q` → 361 passed, 6 warnings
- `uv run autoresearch e2e smoke --server A2-AK-225 --lib verl --timeout 60 --pushgateway-url http://127.0.0.1:17891` → `ok=true`, run `01KV62JVH0N3ZRVRMH4PYWF1VB`, elapsed `146.673s`, report completeness passed

### Decisions Made This Session (2026-06-12)

- **D-32 BMC 密码明文**：用户决定"内网机器密码不加密"，schema 不强制 keyring；`BMCSpec.password` 直接读取
- **D-32 电源 dry-run 双保险**：默认仅返 `would_send`；`--apply` 真打时 `config.bmc.power_operations_allowed` 必须 True
- **D-32 BMC identify 优先级**：UUID > SerialNumber > SKU，第一个非空为 bmc_identifier
- **D-33 sudo_command 显式声明**：默认空字符串（不 sudo），非空则拼到 npu-smi/lspci/driver 命令前
- **A3-AX-176 → A3-AX-180** (ip 192.168.13.180)：同步 config + example
- **A3-AX-153 暂下线**：动态 IP + 宕机中，修好再加
- **A2-AK-102 需 sudo**：user=admin123 + sudo_command="sudo -n"（先 bootstrap NOPASSWD）
- **不引第三方 redfish 库**：用裸 requests + 标准 Redfish REST；iBMC 私有 `/api/` 待协议确认

### Files Created This Session (04-04)

**feat(04-04) commit:**

- `autoresearch/bmc/__init__.py` (27 行) — bmc 模块入口
- `autoresearch/bmc/client.py` (193 行) — Redfish 客户端 (Basic Auth + requests)
- `autoresearch/bmc/identify.py` (131 行) — 双源唯一编码查询
- `autoresearch/bmc/power.py` (161 行) — 电源 dry-run/apply 操作
- `autoresearch/cli.py` (+133 行) — bmc CLI group (identify + power sub-group)
- `autoresearch/hw/models.py` (+3 行) — HardwareData TypedDict 加 3 字段
- `autoresearch/hw/probe.py` (+66/-20 行) — sudo 前缀 + bmc identify 集成
- `config/config.example.yaml` (+74 行) — 4 台 servers 完整配置 + 安全声明
- `tests/test_bmc.py` (205 行) — 12 个 bmc 单元测试
- `tests/test_hw_probe.py` (+286 行) — 3 个 hw 集成测试
- `workspace-core/config/__init__.py` (+2 行) — 导出 BMCSpec
- `workspace-core/config/schema.py` (+35 行) — BMCSpec + sudo_command 字段
- `.planning/phases/04-skill-03-server-hardware-probe/04-04-SUMMARY.md`

### Real-Server UAT 现状

| Server | SSH | hw probe | BMC identify | 阻塞 |
|---|:-:|:-:|:-:|---|
| A2-AK-225 | ✅ | ✅ 8 设备 | ❌ BMC 192.168.12.225 不可达 | 待补 BMC IP |
| A3-AK-182 | ✅ | ✅ 16 设备 | ❌ BMC 192.168.12.182 不可达 | 待 BMC IP/路由修复 |
| A3-AX-180 | ❌ | ❌ ssh_auth | ❌ BMC 192.168.12.180 非 Redfish | 需 key 部署 + BMC 协议 |
| A2-AK-102 | ✅ | ❌ npu_smi_dcmi | ❌ BMC 192.168.12.102 非 Redfish | 需驱动修复 + BMC 协议 |
| A3-AX-153 | — | — | — | 暂下线 (动态 IP) |

## Open Questions

- **iBMC 是否真用 Redfish 还是私有 `/api/`**？决定 `client.py` 是否要写新端点
- **5 台 BMC IP/凭据何时齐**？等齐后跑 04-05 plan (BMC 真机验收)
- **A2-AK-102 NOPASSWD sudo 已配**？未配则 `sudo -n` 会失败，提示用户配

## Active Blockers

- **A3-AX-180 SSH 认证失败**（2026-06-12）— 用户运维事项，需重部署 SSH key
- **A2-AK-102 npu-smi dcmi 故障**（2026-06-12）— 驱动级，需远端调试
- **5 台 BMC iBMC 协议未确认**（2026-06-12）— 待用户确认走 Redfish 还是 `/api/`
- **A3-AX-153 暂宕机**（2026-06-12）— 用户说明动态 IP 修好再加

## Accumulated Context

### Roadmap Evolution

- Phase 14 added: 跑通 Verl 正式案例并沉淀 workspace-adapter/verl 实验闭环

## Next Steps

1. Finish the local `Qwen/Qwen3.5-2B` cache or provide a faster authenticated HF path
2. Capture fresh `torch_npu` minimum-repro and guard/watchdog evidence on `A2-AK-225`
3. Re-run the real formal case and close the remaining 8-row matrix / artifact-bundle UAT gaps

## Continuation Prompts

```
$gsd-verify-work 14
```

## Metrics

- **Phases planned:** 14
- **Phases complete:** 13 complete
- **Plans complete:** 41/41 summaries; Phase 14 is blocked in verification, not execution
- **Requirements:** 88 archived, 82 checked, 6 known gaps
- **Tests:** 408 / 408 passing
- **Phase 11 UAT:** pass; smoke run `01KV60QS8PMSEG02MQEB0Z27FT`
- **Phase 12 UAT:** pass; E2E run `01KV62JVH0N3ZRVRMH4PYWF1VB`
- **Phase 13 archive:** `.planning/milestones/v1.0/`
- **Latest PR:** `#1 Phase 12: E2E smoke validation`
- **Tag:** `v1.0`

## Branch & Commits

- **Branch:** `codex/verl-case-01KVAM6VFTQQK60PCTWREW88K5-phase-02-workspace-core`
- **Latest commit:** `docs: record shipped formal case provenance`
- **Open PR:** `https://github.com/Kirrito-k423/AutoResearch/pull/1`

---
*Last updated: 2026-06-17 after Phase 14 verification/UAT structuring*

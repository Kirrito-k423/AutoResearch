---
phase: 08-skill-07-data-collection
plan: 04
status: completed
subsystem: data-collection
tags: [prometheus, manifest, collect-cli, D-47]

requires:
  - phase: 08-01
  - phase: 08-02
  - phase: 08-03
provides:
  - "datalake/prometheus/push_gateway.py: 远程 curl text exposition 到 Pushgateway"
  - "datalake/manifest/schema.py: RunManifest Pydantic 模型"
  - "datalake/manifest/writer.py: 写 ~/.autoresearch/runs/<run-id>/manifest.json"
  - "autoresearch/collect/manifest.py: 从 minimal/wandb/log/prom 结果构造 manifest"
  - "autoresearch/collect/cli.py: `autoresearch collect run --server X --lib verl` 端到端编排"
  - "CLI 最终 stdout 唯一 JSON, 失败时仍写 manifest"
  - "10 个新增 08-04 单测覆盖 prom push、manifest、collect CLI"
affects: [phase-08-data-collection, phase-09-experiment-report]

tech-stack:
  added: []
  patterns:
    - "Pushgateway 不引远程 prometheus_client, 用 curl --data-binary 推 text/plain"
    - "Run id 使用 stdlib ULID-like 生成, 不新增依赖"
    - "端到端 collect: minimal → wandb sync → log collect → prom push → manifest write"
    - "下游非关键失败记录到 manifest.error, 不阻止 manifest 落盘"

key-files:
  created:
    - datalake/prometheus/__init__.py
    - datalake/prometheus/push_gateway.py
    - datalake/manifest/__init__.py
    - datalake/manifest/schema.py
    - datalake/manifest/writer.py
    - autoresearch/collect/manifest.py
    - autoresearch/collect/cli.py
    - tests/test_datalake_prometheus_push.py
    - tests/test_datalake_manifest.py
    - tests/test_collect_manifest.py
    - tests/test_collect_cli.py
  modified:
    - autoresearch/cli.py
    - tests/test_ssh_bootstrap.py

requirements-completed:
  - COLL-RUN-01
  - COLL-MANIFEST-01

requirements-blocked:
  - COLL-WB-01
  - COLL-WB-02
  - COLL-PROM-01
  - COLL-PROM-02

duration: 35min
completed: 2026-06-15
---

# Phase 08 Plan 04: datalake/prometheus/push_gateway.py + manifest 写入 Summary

**Phase 8 的本地沉淀编排已实现: `autoresearch collect run` 会生成 run_id, 跑 minimal 1-step, 拉 wandb/log, push Prometheus 指标, 最后写 manifest。即使 wandb sync 或 prom push 失败, CLI 也会把错误写进 manifest 并输出唯一 JSON。**

## Accomplishments

### 1. Prometheus Pushgateway 推送

`datalake/prometheus/push_gateway.py` 新增:

```python
def push_metrics(server, run_id, npu_count, pushgateway_url="http://localhost:9091", timeout=10.0) -> bool
```

远程命令使用 text exposition + `curl --data-binary @-`, 不要求远程 conda env 安装 `prometheus_client`.

### 2. RunManifest

`datalake/manifest/schema.py` 记录一轮最小实验的三路数据:

- run/server/env/lib/workdir
- one_step: sum, npu_count, elapsed_ms, lib
- wandb_run_id, wandb_path
- log_files
- prom_pushed, prom_metrics_file
- exit_code, error

`datalake/manifest/writer.py` 写入 `<runs-root>/<run-id>/manifest.json`.

### 3. `autoresearch collect run`

新增 CLI:

```bash
autoresearch collect run --server A2-AK-225 --lib verl \
  --config config/config.yaml \
  --pushgateway-url http://localhost:9091
```

流程:

1. 生成 run_id
2. `collect_minimal(..., run_id=run_id)`
3. `sync_run(wandb_run_id, ...)`
4. `collect_log(run_id, ...)`
5. `push_metrics(..., npu_count, ...)`
6. `build_manifest()` + `write_manifest()`
7. stdout 输出唯一 JSON, exit code 反映端到端成功/失败

## Verification

Targeted:

```bash
uv run pytest tests/test_minimal_runner.py tests/test_collect_minimal.py tests/workspace-core/test_config.py tests/test_datalake_logs_collector.py tests/test_datalake_prometheus_push.py tests/test_datalake_manifest.py tests/test_collect_manifest.py tests/test_collect_cli.py -q
```

结果: `53 passed`.

周边回归:

```bash
uv run pytest tests/test_datalake_wandb_sync.py tests/test_config_validate.py tests/test_cli.py tests/test_start_stop.py tests/test_status.py -q
```

结果: `32 passed`.

全量:

```bash
uv run pytest -q
```

结果: `320 passed, 6 warnings`.

## UAT Notes

当前本机运行时阻塞:

- `uv run autoresearch services status --json`: 5/5 unhealthy (archon, wandb, prometheus, grafana, pushgateway)
- `curl --unix-socket ~/.docker/run/docker.sock --max-time 3 http://localhost/_ping`: timeout
- 8080/9090/9091/3000 端口无监听进程

因此完整 UAT 不能声称通过:

- wandb offline run → local wandb UI 可见: blocked by local wandb service
- prom push → local Prometheus 可见: blocked by Docker/pushgateway

代码层已实现并单测覆盖; 运行时验收见 `08-UAT.md`.

## Issues Encountered

- hatch editable 的 `force-include` 目录不会把连字符目录直接作为可编辑包导入。修改 `workspace-core/` / `verl-workspace-adapter/` 后需要执行 `uv pip install -e .` 同步到 `.venv/site-packages`.
- 既有 `tests/test_ssh_bootstrap.py::test_install_nopasswd_sudo_root_user_skips_sudo_prefix` 的 mock 未处理 root 用户 `whoami` 验证, 全量测试暴露后补齐 fixture。

## Next Steps

1. 修复 Docker Desktop 后端或重启 Docker Desktop/Mac, 让 Docker socket `_ping` 返回 OK。
2. `autoresearch services start` 启动 wandb/prometheus/grafana/pushgateway。
3. 重跑 `autoresearch collect run --server A2-AK-225 --lib verl` 真机 UAT。
4. 若 08-UAT 全部通过, 进入 Phase 9 experiment-report。

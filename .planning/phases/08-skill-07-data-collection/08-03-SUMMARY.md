---
phase: 08-skill-07-data-collection
plan: 03
status: completed
subsystem: data-collection
tags: [logs, workdir, SFTP, D-46, D-47]

requires:
  - phase: 08-01
    provides: [collect_minimal, minimal_runner]
provides:
  - "ServerSpec.workdir schema 字段, 默认 /root"
  - "minimal runner 支持 run_id, 远程 tee stdout/stderr 到 <workdir>/runs/<run_id>.log"
  - "datalake/logs/collector.py: SFTP 拉远程 run log 到本地 ~/.autoresearch/runs/<run_id>/log.txt"
  - "tail_remote_log(server, remote_log_path) 兼容 API"
  - "10 个相关单测覆盖 workdir、tee remote log、SFTP OK/not-found/permission"
affects: [phase-08-data-collection, phase-09-experiment-report]

tech-stack:
  added: []
  patterns:
    - "D-46 workdir: ServerSpec.workdir = '/root' 默认, CLI --workdir 可覆盖"
    - "D-47 log collect: M1 一次性 SFTP 拉取, 实时流留 v1.1"
    - "run_in_env 命令顺序: cd '<workdir>' && conda run -n <env> <command>"

key-files:
  created:
    - datalake/logs/__init__.py
    - datalake/logs/collector.py
    - tests/test_datalake_logs_collector.py
  modified:
    - workspace-core/config/schema.py
    - config/config.example.yaml
    - autoresearch/collect/minimal.py
    - verl-workspace-adapter/common/conda_utils.py
    - verl-workspace-adapter/verl/minimal_runner.py
    - verl-workspace-adapter/veomni/minimal_runner.py
    - tests/workspace-core/test_config.py
    - tests/test_collect_minimal.py
    - tests/test_minimal_runner.py

requirements-completed:
  - COLL-RUN-02
  - COLL-LOG-01
  - COLL-LOG-02

duration: 20min
completed: 2026-06-15
---

# Phase 08 Plan 03: datalake/logs/collector.py 实时拉 Summary

**D-46 workdir 字段和 D-47 日志拉取闭环已落地。最小实验 runner 现在可按 run_id 在远程 `<workdir>/runs/<run_id>.log` 生成日志, 本地 `collect_log()` 通过 SFTP 拉到 `~/.autoresearch/runs/<run_id>/log.txt`. M1 锁定为跑后一次性拉取, 不做 inotify/流式 tail。**

## Accomplishments

### 1. `ServerSpec.workdir` 正式进入 schema

`workspace-core/config/schema.py` 新增:

```python
workdir: str = Field(default="/root", min_length=1, ...)
```

`autoresearch.collect.minimal._resolve_workdir()` 优先使用 CLI override, 其次使用 `spec.workdir`, 最后兜底 `/root`.

### 2. runner 写远程 run log

`verl` 和 `veomni` minimal runner 新增 `run_id` 参数。传入 run_id 时远程命令会:

1. 创建 `<workdir>/wandb` 和 `<workdir>/runs`
2. 清空 `<workdir>/runs/<run_id>.log`
3. 执行 one-step 脚本
4. 用 `tee -a` 把 stdout/stderr 写入远程日志
5. 在 `MinimalResult` 返回 `remote_log_path`

同时修正 `run_in_env()` 的命令顺序为:

```bash
cd '<workdir>' && conda run -n <env> <command>
```

避免 `conda run -n <env> cd ...` 这种把 `cd` 当二进制执行的错误。

### 3. `datalake/logs/collector.py`

新增:

```python
def collect_log(run_id, server, workdir_override=None, local_runs_root=None, remote_log_path=None) -> Path
def tail_remote_log(server, remote_log_path, run_id=None, local_runs_root=None) -> Path
```

错误分类为用户可读的 `LogFetchError`: 远程日志不存在、无权限、SSH/SFTP 失败。

## Verification

```bash
uv run pytest tests/test_minimal_runner.py tests/test_collect_minimal.py tests/workspace-core/test_config.py tests/test_datalake_logs_collector.py -q
```

结果: 相关测试全部通过。

全量验证:

```bash
uv run pytest -q
```

结果: `320 passed, 6 warnings`.

## UAT Notes

- 代码路径已覆盖远程 tee 和本地 SFTP 拉取。
- 真实 `autoresearch collect run` 的完整 UAT 仍依赖本地 wandb/pushgateway 服务；当前 Docker Desktop 后端 socket `_ping` 超时, 5 个本地服务均未健康, 因此 Phase 8 UAT 记录为 partial。

## Next Steps

- 08-04: 串接 prom push、manifest 和 `autoresearch collect run` 端到端 CLI。

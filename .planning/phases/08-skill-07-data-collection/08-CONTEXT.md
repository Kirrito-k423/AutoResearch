---
phase: 08-skill-07-data-collection
type: context
status: locked
locked_at: 2026-06-15
locks:
  - D-44
  - D-45
  - D-46
  - D-47
---

# Phase 08 CONTEXT — data-collection (Skill 07)

> 8-skill 最小循环第 7 步: 在远程跑一次最小实验, 3 路数据 (wandb / log / prom) 都落到本地 `~/.autoresearch/`.

## D-44 最小实验 = 复用 Phase 7 1-step 脚本 (locked, recommended)

**Decision:** `minimal-runner` 复用 Phase 7 1-step 干跑模板 (D-41)
- 远程 `conda run -n <env> python -c "import torch, torch_npu, <lib>; x=torch.randn(2,3).npu(); y=(x+1).sum(); print('SUM=', y.item()); print('NPU_COUNT=', torch_npu.npu.device_count())"`
- **不引** `verl.trainer.main(...)` (CUDA 风格不适用, Phase 7 已废)
- lib 选 `verl` 默认 (A2-AK-225 conda_env=verl-qwen3.5 已知 OK, D-43 单字段约束)
- 用户后续可加 `--lib veomni` 切 env 跑

**Rationale:** Phase 7 1-step 已经在 A2-AK-225 真机验证 (SUM=5.29, NPU=8, 22s 完成). 复用避免重新设计 / 重新验证.

**Affected files:**
- `workspace-adapter/verl/runner.py` — `MinimalRunner.run(server, lib='verl')` 包成 1-step
- `workspace-adapter/veomni/runner.py` — 同上 lib='veomni'
- `autoresearch/collect/minimal.py` — orchestrator, 调 runner + 落 3 路数据

## D-45 wandb 路径 = 离线模式 + 本地 sync (locked, recommended)

**Decision:** 远程 `WANDB_MODE=offline`, 写 `wandb/<run-id>/` 目录; 跑完 SCP 拉回本地, 走 `wandb sync wandb/<run-id>` 导入本地 wandb 服务 (Phase 1 起的容器).

**Why not direct push:** Phase 6 reach test 暴露远程 docker pull 受限, wandb 容器在远程启不来. 离线模式只走本地文件系统, 不依赖网络.

**Implementation:**
- 远程 export `WANDB_MODE=offline WANDB_DIR=<workdir>/wandb` 然后跑 1-step
- SCP `wandb/<run-id>` 到 `~/.autoresearch/runs/<run-id>/wandb/`
- 本地 `wandb sync <path>` 导入本地 wandb 服务 (假设 wandb 服务已起)
- datalake 抽象 `sync_run(run_id, server)` 不直接 import wandb SDK, 调 CLI

**Affected files:**
- `datalake/wandb/sync.py` — `sync_run(run_id) -> Path` 调 wandb CLI
- `datalake/wandb/api_client.py` — `query_metrics(run_id) -> DataFrame` (Phase 9 用)

## D-46 远程工作目录 = config.servers[].workdir (locked, recommended)

**Decision:** `ServerSpec` 加 `workdir: str = "/root"` 字段; A2-AK-102 等老用户机器配 `/home/t00906153`. 缺省 `/root` 兼容 root 直连.

**Why new field:** 现在 4 台机器 root 直连, 实际工作目录全是 `/root`. 但 PROJECT.md 写用户账号是 `root@192.168.13.154`, 工作目录 `/home/t00906153`. 现状是 4 台机器共享 config 字段差异大, schema 必扩.

**Affected files:**
- `workspace-core/config/schema.py` — `ServerSpec.workdir: str = "/root"`, `BMCSpec.workdir` 不需要
- `config/config.yaml` — 4 台机器根据实际工作目录填 (A2-AK-225 / 102 / 180 / 182 大概率全 `/root`)
- 所有 ssh_exec_capture 拼 `cd <workdir> && <cmd>` (或 `bash -c "cd <workdir> && <cmd>"`)

## D-47 manifest 粒度 = 含 1-step 元数据 (locked, recommended)

**Decision:** `RunManifest` 字段:
```python
class RunManifest(BaseModel):
    run_id: str                     # ULID/UUID
    started_at: datetime            # ISO 8601
    finished_at: datetime | None
    server: str                     # A2-AK-225
    conda_env: str                  # verl-qwen3.5
    lib: str                        # verl | veomni
    workdir_remote: str             # /root/ar/runs/<id>
    workdir_local: Path             # ~/.autoresearch/runs/<id>
    one_step: dict | None           # {sum: 5.29, npu_count: 8, elapsed_ms: 22085}
    exit_code: int | None
    error: str | None
    wandb_run_id: str | None        # wandb/<run-id> 同步前不知道
    log_files: list[Path]           # 本地 log 路径
    prom_metrics_file: Path | None  # 本地 prom metrics json
```

**Rationale:** 对齐 PROJECT.md core value "常实践，详记录，知得失". 1-step 元数据是这次 run 唯一可重放的"实证", manifest 不含就丢信息.

**Affected files:**
- `datalake/manifest/schema.py` — `RunManifest` Pydantic model
- `datalake/manifest/writer.py` — `RunManifestWriter.write(m)` 落 `~/.autoresearch/runs/<id>/manifest.json`
- `autoresearch/collect/manifest.py` — orchestrator 收集各路 → 写 manifest

## 子模块拆分 (4 plans)

| Plan | 内容 | 关键文件 |
|---|---|---|
| 08-01 | minimal-runner 抽象 + verl/veomni 实例 | `workspace-adapter/verl/runner.py`, `workspace-adapter/veomni/runner.py`, `autoresearch/collect/minimal.py` |
| 08-02 | datalake/wandb/sync.py 离线→本地 | `datalake/wandb/sync.py` |
| 08-03 | datalake/logs/collector.py 实时拉 | `datalake/logs/collector.py` (rsync 增量) |
| 08-04 | datalake/prometheus/push_gateway.py + manifest 写入 | `datalake/prometheus/push_gateway.py`, `datalake/manifest/{schema,writer}.py`, `autoresearch/collect/manifest.py` |

## 边界 & 不做

- **不做** 真实训练 (Phase 8 仍走 1-step 干跑, 真实 verl train 留 v1.1)
- **不做** 多服务器并发 (Phase 8 一次只跑一台, --all 留 v1.1)
- **不做** wandb 实时推 (D-45 锁定离线, 实时推留 v2.0)
- **不做** log 流式推到 Prom tail (Phase 8 rsync 增量足够)

## 关键依赖

- **Phase 6** reachability: 远程能 curl 本地 wandb /health (D-45 sync 时验证)
- **Phase 7** train-stack: 1-step 脚本 + conda_env 已知 (D-44 复用)
- **Phase 2** workspace-core: SSH 客户端 + 配置 + secrets (D-46 workdir 字段)
- **Phase 1** services: 本地 wandb 服务 (D-45 sync 目标)

## 真机 UAT 目标

| Server | 预期 |
|---|---|
| **A2-AK-225** | full pass: 1-step 跑通 + wandb 离线写入 + scp 拉回 + 本地 sync + log rsync + prom push + manifest 写完 |
| A3-AK-102 / 180 / 182 | 1-step 跳过 (无 conda / env broken), 但走通"配置 conda_env 缺失 → 失败但 manifest 含 error" 路径 |

## 风险 & 缓解

- **R1**: 远程 wandb 离线模式依赖 wandb Python 包. A2-AK-225 的 `verl-qwen3.5` env 已装 wandb (verl 依赖). 验证: `conda run -n verl-qwen3.5 python -c "import wandb; print(wandb.__version__)"`
- **R2**: 本地 wandb 同步依赖 `wandb` CLI 装在 Mac. 验证: `which wandb` (Mac pip 装)
- **R3**: SCP 大文件慢. wandb 离线 run 通常 < 10MB, 1-step 干跑产物小, 可接受
- **R4**: D-46 workdir 字段改动 schema 影响 Phase 2-7 所有用 spec 的代码. 验证: 跑完全测试 + 4 台 stack check --all

# workspace-adapter — 沉淀 2：训练栈适配

> 把 verl / veomni 的"环境探测 + 最小用例"封装成统一接口。
> **不依赖** workspace-core / datalake（独立可测）。

## 职责

| 子模块 | 职责 | 关键接口 |
|---|---|---|
| `verl/env_probe.py` | 探测 conda env 是否有 verl、版本、关键依赖 | `probe_verl(env_name) -> VerlEnvInfo` |
| `verl/minimal_runner.py` | 1-step 烟雾用例 (LLaMA-Factory 风格最小脚本) | `run_minimal(config) -> RunResult` |
| `verl/config_validator.py` | 校验 verl YAML 配置合法性 | `validate_verl_config(path) -> list[Issue]` |
| `veomni/...` | 同上，但针对 veomni | `probe_veomni(env_name)` |
| `common/conda_utils.py` | 共享 conda / pip 工具 | `conda_env_exists(name)`, `pip_list(env_name)` |
| `common/npu_utils.py` | 共享 npu-smi / CANN 工具 | `npu_smi_info() -> list[NPUSpec]` |

## 设计原则

- **verl / veomni 对称**：两个训练栈的 API 形态对齐
- **环境探测 vs 跑用例 分离**：probe 不副作用；minimal_runner 跑一次出 manifest

## 状态

⏳ **Phase 11 待开发** — 当前目录为占位。

---
*详见 `.planning/ROADMAP.md` Phase 11*

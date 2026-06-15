"""autoresearch.stack — train-stack-health skill (Phase 07).

验证远程服务器 verl + veomni 各自的 conda env 健康, 能跑 1-step 干跑 (NPU 算子).
基于 Phase 6 autoresearch.reach 暴露的 _ssh_exec_capture 模式 + workspace_core SSHClient.

实现 STACK-VERL-01..03 + STACK-VEOMNI-01..03:
- STACK-VERL-01 / V-01: 库检测 `python -c "import <lib>; print(<lib>.__version__)"`
- STACK-VERL-02 / V-02: conda env 探测 `conda env list | grep <env>`
- STACK-VERL-03 / V-03: 1-step 干跑 (NPU 适配 — torch_npu, D-41)
"""

"""workspace-core.result — 统一 check 返回结构 (D-21).

8 skill 全部用 CheckResult; 不是 REQ 衍生但下游都依赖.
"""
from .check import CheckResult, CheckSeverity, ok, fail, merge

__all__ = ["CheckResult", "CheckSeverity", "ok", "fail", "merge"]

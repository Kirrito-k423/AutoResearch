"""End-to-end smoke orchestration for AutoResearch."""

from .report_check import check_report_completeness
from .smoke import run_e2e_smoke

__all__ = ["check_report_completeness", "run_e2e_smoke"]

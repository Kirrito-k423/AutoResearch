"""workspace-core.log — 统一日志 (D-16).

8 skill 全部走 get_logger + configure_root, 不自己配 handler.
"""
from .logger import get_logger, configure_root

__all__ = ["get_logger", "configure_root"]

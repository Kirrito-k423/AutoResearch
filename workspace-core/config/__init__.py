"""workspace-core.config — Pydantic v2 配置加载 (D-10..13)."""
from .schema import (
    Config,
    ServerSpec,
    BMCSpec,
    NetworkProbes,
    LogConfig,
    WandbConfig,
)
from .loader import from_yaml, from_path, ConfigError

__all__ = [
    "Config",
    "ServerSpec",
    "BMCSpec",
    "NetworkProbes",
    "LogConfig",
    "WandbConfig",
    "from_yaml",
    "from_path",
    "ConfigError",
]

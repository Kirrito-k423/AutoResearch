"""config skill 共享: 路径解析 + 模板路径常量."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# config.example.yaml 在仓根随仓走 (用户改会进 git)
TEMPLATE_PATH: Final[Path] = (
    Path(__file__).resolve().parents[2] / "config" / "config.example.yaml"
)

# 默认配置路径 (跟 workspace_core.config.from_path 默认对齐)
DEFAULT_CONFIG_PATH: Final[Path] = Path("./config/config.yaml")


def resolve_config_path(path: Path | str | None) -> Path:
    """优先级: 参数 > env AUTORESEARCH_CONFIG > ./config/config.yaml.

    `~` 走 expanduser 展开.
    """
    if path is not None:
        return Path(path).expanduser()
    env_p = os.environ.get("AUTORESEARCH_CONFIG")
    if env_p:
        return Path(env_p).expanduser()
    return DEFAULT_CONFIG_PATH

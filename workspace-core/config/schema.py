"""config/config.yaml 的 Pydantic v2 schema (D-10..12)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ServerSpec(BaseModel):
    """单台远端服务器规格."""

    name: str = Field(min_length=1, description="服务器别名 (e.g. 'nvidia-01')")
    host: str = Field(min_length=1, description="hostname 或 IP")
    port: int = Field(default=22, ge=1, le=65535, description="SSH 端口")
    user: str = Field(min_length=1, description="登录用户名")
    identity_file: str | None = Field(default=None, description="可选: 私钥路径")
    bootstrap_password_secret: str | None = Field(
        default=None,
        description="<keyring:NAME> 或 <env:VAR>; 仅首次 bootstrap 用",
    )


class NetworkProbes(BaseModel):
    """外网探针配置."""

    enabled: bool = Field(default=True)
    targets: list[str] = Field(
        default_factory=lambda: [
            "https://baidu.com",
            "https://huggingface.co",
            "https://github.com",
        ],
    )


class LogConfig(BaseModel):
    """日志配置."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    json_format: bool = Field(default=False, description="JSON 格式 (vs 人类可读)")
    dir: str = Field(default="~/.autoresearch/logs")


class WandbConfig(BaseModel):
    """本地 wandb 配置."""

    enabled: bool = Field(default=True)
    entity: str | None = None
    project: str = "autoresearch"


class Config(BaseModel):
    """整份配置 schema."""

    version: int = Field(default=1, ge=1)
    servers: list[ServerSpec] = Field(default_factory=list)
    network: NetworkProbes = Field(default_factory=NetworkProbes)
    log: LogConfig = Field(default_factory=LogConfig)
    wandb: WandbConfig = Field(default_factory=WandbConfig)

    @field_validator("servers")
    @classmethod
    def _server_names_unique(cls, v: list[ServerSpec]) -> list[ServerSpec]:
        names = [s.name for s in v]
        if len(names) != len(set(names)):
            dupes = sorted({n for n in names if names.count(n) > 1})
            raise ValueError(f"servers.name 重复: {dupes}")
        return v

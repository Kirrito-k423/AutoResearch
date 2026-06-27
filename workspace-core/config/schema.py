"""config/config.yaml 的 Pydantic v2 schema (D-10..12)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class BMCSpec(BaseModel):
    """带外管理 (BMC) 凭据 (内网明文, 走 Redfish).

    安全声明: 密码字段明文存储, 仅适用内网环境 (D-32).
    内网机器密码泄露不影响外部安全, 配置可读即可.
    """

    host: str = Field(min_length=1, description="BMC IP / 主机名")
    port: int = Field(default=443, ge=1, le=65535, description="BMC HTTPS 端口")
    user: str = Field(min_length=1, description="BMC 登录用户")
    password: str = Field(min_length=1, description="BMC 登录密码 (内网明文)")
    protocol: Literal["redfish"] = Field(
        default="redfish",
        description="BMC 协议 (当前仅 redfish)",
    )
    power_operations_allowed: bool = Field(
        default=False,
        description="True 才允许 --apply 真正下电/上电 (默认 dry-run)",
    )


class ServerSpec(BaseModel):
    """单台远端服务器规格."""

    name: str = Field(min_length=1, description="服务器别名 (e.g. 'nvidia-01')")
    host: str = Field(min_length=1, description="hostname 或 IP (手动管理, 不自动发现)")
    port: int = Field(default=22, ge=1, le=65535, description="SSH 端口")
    user: str = Field(min_length=1, description="登录用户名")
    identity_file: str | None = Field(default=None, description="可选: 私钥路径")
    bootstrap_password_secret: str | None = Field(
        default=None,
        description="<keyring:NAME> 或 <env:VAR>; 仅首次 bootstrap 用",
    )
    sudo_command: str = Field(
        default="",
        description=(
            "非 root 用户的 sudo 前缀 (e.g. 'sudo -n');"
            " 留空 = 不加 sudo, 假设 user 已 root."
            " 推荐先 bootstrap NOPASSWD sudo, 再填 'sudo -n'."
        ),
    )
    conda_env: str = Field(
        default="",
        description=(
            "Phase 7 (D-40): conda env 名称, 跑 stack check 时走 `conda run -n <env>`."
            " 留空 = 走系统 python (没 conda env)."
        ),
    )
    workdir: str = Field(
        default="/root",
        min_length=1,
        description="Phase 8 (D-46): 远程实验工作目录, 用于 runs/wandb/log/prom 数据落点.",
    )
    bmc: BMCSpec | None = Field(
        default=None,
        description="带外管理 (BMC) 凭据; 不填则无 BMC 能力",
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


class VerlCaseConfig(BaseModel):
    """Phase 14 formal Verl case defaults.

    These are non-secret reproducibility defaults only. Tokens and credentials
    must stay in environment variables or local ignored config.
    """

    cache_root: str = Field(
        default="/Users/Zhuanz/autoResearchData",
        min_length=1,
        description="Local cache root for <=5GB model, data, and image metadata.",
    )
    artifact_root: str = Field(
        default="/Users/Zhuanz/autoResearchData/runs",
        min_length=1,
        description="Local data-repository root for formal run artifacts.",
    )
    docker_image: str = Field(
        default="quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5",
        min_length=1,
    )
    docker_images_by_server: dict[str, str] = Field(
        default_factory=dict,
        description="Optional per-server Docker image overrides for heterogeneous Ascend pools.",
    )
    model_id: str = Field(default="Qwen/Qwen3.5-2B", min_length=1)
    dataset_id: str = Field(default="hiyouga/geometry3k", min_length=1)
    local_asset_limit_gb: int = Field(default=5, ge=1)
    input_tokens: int = Field(default=1024, ge=1)
    output_tokens: list[int] = Field(
        default_factory=lambda: [2048, 4096, 8192, 16384]
    )
    ignore_eos: bool = False
    inference_modes: list[Literal["sync", "async"]] = Field(
        default_factory=lambda: ["sync", "async"]
    )
    wandb_project: str = Field(
        default="verl",
        min_length=1,
        description="W&B project for formal Verl case rows; use code-stack names such as 'verl'.",
    )
    github_owner: str = Field(default="Kirrito-k423", min_length=1)
    remote_workdir: str = Field(default="/home/t00906153", min_length=1)
    dependency_repo_paths: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Optional local or remote checkout paths for dependency provenance, "
            "for example verl/vllm/transformers/mindspeed."
        ),
    )
    dependency_source_mounts: list[str] = Field(
        default_factory=lambda: ["verl", "transformers", "mindspeed", "veomni"],
        description=(
            "Dependency source repos mounted into the runtime container. Keep vllm "
            "out by default so the image's vLLM and vLLM-Ascend versions stay compatible."
        ),
    )
    case_mode: Literal["validation", "training"] = Field(
        default="training",
        description="Formal case mode; training is the Phase 15 default.",
    )
    trainer_val_only: bool = Field(
        default=False,
        description="False enters the real GRPO training loop; true keeps the Phase 14 validation-only path.",
    )
    training_steps: int = Field(default=3, ge=1)
    single_card_start_batch_size: int = Field(default=1, ge=1)
    single_card_devices: list[int] = Field(default_factory=lambda: [0])
    single_node_devices: list[int] = Field(default_factory=lambda: list(range(8)))
    tuning_train_batch_sizes: list[int] = Field(default_factory=lambda: [1, 2, 4, 8])
    tuning_ppo_mini_batch_sizes: list[int] = Field(default_factory=lambda: [1])
    tuning_ppo_micro_batch_sizes_per_gpu: list[int] = Field(default_factory=lambda: [1])
    tuning_output_tokens: list[int] | None = Field(
        default=None,
        description=(
            "Optional training-tuning sequence lengths. None keeps the conservative "
            "single shortest output length; set explicitly to search sequence length."
        ),
    )
    tuning_inference_modes: list[Literal["sync", "async"]] | None = Field(
        default=None,
        description=(
            "Optional training-tuning inference modes. None keeps the first "
            "configured inference mode; set explicitly to search sync/async."
        ),
    )
    train_batch_size: int = Field(default=8, ge=1)
    val_batch_size: int = Field(default=1, ge=1)
    train_max_samples: int = Field(default=8, ge=1)
    val_max_samples: int = Field(default=2, ge=1)
    rollout_n: int = Field(default=1, ge=1)
    n_gpus_per_node: int = Field(default=8, ge=1)
    tensor_model_parallel_size: int = Field(default=2, ge=1)
    rollout_gpu_memory_utilization: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="vLLM rollout gpu_memory_utilization; raise when KV cache cannot allocate.",
    )
    rollout_max_model_len_floor: int = Field(
        default=24576,
        ge=0,
        description=(
            "Lower bound for rollout.max_model_len/max_num_batched_tokens. Set 0 "
            "to use the actual prompt+response length during short-context sweeps."
        ),
    )
    ppo_max_token_len_per_gpu_floor: int = Field(
        default=24576,
        ge=0,
        description=(
            "Lower bound for actor/ref/rollout log-prob max_token_len_per_gpu. "
            "Lower this for short-context sweeps when update_actor OOMs."
        ),
    )
    rollout_update_weights_bucket_megabytes: int = Field(
        default=2048,
        ge=1,
        description=(
            "Verl/vLLM rollout update_weights bucket size in MiB. Lower this when "
            "FSDP-to-rollout weight sync OOMs on the bucket allocation."
        ),
    )
    rollout_max_num_seqs: int | None = Field(
        default=None,
        ge=1,
        description=(
            "Optional vLLM rollout.max_num_seqs override. None keeps the adapter "
            "default of max(1, val_batch_size, train_batch_size)."
        ),
    )
    rollout_free_cache_engine: bool | None = Field(
        default=None,
        description=(
            "Optional vLLM rollout.free_cache_engine override. None keeps the "
            "adapter default true; set false to test avoiding repeated sleep/wake."
        ),
    )
    cleanup_stale_verl_processes: bool = Field(
        default=True,
        description=(
            "Before each formal matrix run, terminate stale Verl/Ray/vLLM worker "
            "processes from earlier failed runs so the selected single-node host "
            "starts with exclusive NPU access."
        ),
    )
    row_timeout_seconds: int = Field(
        default=7200,
        ge=1,
        description="Per formal matrix row timeout inside the container.",
    )
    execution_profile: Literal["auto", "fsdp", "fsdp2", "veomni"] = Field(
        default="fsdp",
        description=(
            "Formal Verl backend profile. fsdp is the portable default; fsdp2 "
            "and veomni must be selected explicitly after backend validation."
        ),
    )
    fsdp2_offload_policy: bool | None = Field(
        default=None,
        description=(
            "Optional FSDP2 fsdp_config.offload_policy override. Set true to "
            "activate FSDP2 CPUOffloadPolicy for param/grad/optimizer training."
        ),
    )
    use_remove_padding: bool | None = Field(
        default=None,
        description=(
            "Optional Verl model.use_remove_padding override. None lets the adapter "
            "choose a backend/model-compatible default."
        ),
    )
    use_dynamic_bsz: bool | None = Field(
        default=None,
        description=(
            "Optional Verl dynamic batch-size override for actor/ref/logprob paths. "
            "None lets the adapter choose a backend/model-compatible default."
        ),
    )

    @field_validator("output_tokens")
    @classmethod
    def _output_tokens_nonempty(cls, v: list[int]) -> list[int]:
        if not v:
            raise ValueError("output_tokens 不能为空")
        if any(item <= 0 for item in v):
            raise ValueError("output_tokens 必须全部为正整数")
        return v

    @field_validator("inference_modes")
    @classmethod
    def _inference_modes_nonempty(
        cls, v: list[Literal["sync", "async"]]
    ) -> list[Literal["sync", "async"]]:
        if not v:
            raise ValueError("inference_modes 不能为空")
        if len(set(v)) != len(v):
            raise ValueError("inference_modes 不能重复")
        return v

    @field_validator("tuning_output_tokens")
    @classmethod
    def _tuning_output_tokens_positive(cls, v: list[int] | None) -> list[int] | None:
        if v is not None and any(item <= 0 for item in v):
            raise ValueError("tuning_output_tokens 必须全部为正整数")
        return v

    @field_validator("tuning_inference_modes")
    @classmethod
    def _tuning_inference_modes_unique(
        cls, v: list[Literal["sync", "async"]] | None
    ) -> list[Literal["sync", "async"]] | None:
        if v is not None and len(set(v)) != len(v):
            raise ValueError("tuning_inference_modes 不能重复")
        return v


class Config(BaseModel):
    """整份配置 schema."""

    version: int = Field(default=1, ge=1)
    servers: list[ServerSpec] = Field(default_factory=list)
    network: NetworkProbes = Field(default_factory=NetworkProbes)
    log: LogConfig = Field(default_factory=LogConfig)
    wandb: WandbConfig = Field(default_factory=WandbConfig)
    verl_case: VerlCaseConfig = Field(default_factory=VerlCaseConfig)

    @field_validator("servers")
    @classmethod
    def _server_names_unique(cls, v: list[ServerSpec]) -> list[ServerSpec]:
        names = [s.name for s in v]
        if len(names) != len(set(names)):
            dupes = sorted({n for n in names if names.count(n) > 1})
            raise ValueError(f"servers.name 重复: {dupes}")
        return v

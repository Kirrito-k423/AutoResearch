"""Typed config and result helpers for the formal Verl case."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


InferenceMode = Literal["sync", "async"]


class VerlCaseConfig(BaseModel):
    """Serializable formal-case defaults used by the Verl adapter."""

    cache_root: str = "/Users/Zhuanz/autoResearchData"
    artifact_root: str = "/Users/Zhuanz/autoResearchData/runs"
    docker_image: str = "quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5"
    model_id: str = "Qwen/Qwen3.5-2B"
    dataset_id: str = "hiyouga/geometry3k"
    local_asset_limit_gb: int = 5
    input_tokens: int = 1024
    output_tokens: list[int] = Field(default_factory=lambda: [2048, 4096, 8192, 16384])
    ignore_eos: bool = False
    inference_modes: list[InferenceMode] = Field(default_factory=lambda: ["sync", "async"])
    wandb_project: str = "verl"
    github_owner: str = "Kirrito-k423"
    remote_workdir: str = "/home/t00906153"
    dependency_repo_paths: dict[str, str] = Field(default_factory=dict)
    trainer_val_only: bool = True
    train_batch_size: int = 8
    val_batch_size: int = 1
    train_max_samples: int = 8
    val_max_samples: int = 2
    rollout_n: int = 1
    n_gpus_per_node: int = 8
    tensor_model_parallel_size: int = 2
    row_timeout_seconds: int = 1800


class VerlCaseMatrixRow(BaseModel):
    """One strict experiment matrix row."""

    input_tokens: int
    output_tokens: int
    inference_mode: InferenceMode
    ignore_eos: bool = False

    @property
    def key(self) -> str:
        return f"{self.inference_mode}-{self.input_tokens}-{self.output_tokens}"


class RepoProvenance(BaseModel):
    """Git provenance for one repository participating in an experiment."""

    repo: str
    path: str | None = None
    upstream_url: str | None = None
    fork_url: str | None = None
    branch_url: str | None = None
    branch: str | None = None
    commit_sha: str | None = None
    dirty: bool = False
    pushed_url: str | None = None
    commit_push_attempted: bool = False


class VerlCaseRunConfig(BaseModel):
    """Immutable run config written before remote execution starts."""

    run_id: str
    created_at: datetime
    server: str
    config: VerlCaseConfig
    matrix: list[VerlCaseMatrixRow]
    provenance: list[RepoProvenance] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class VerlCaseResultRow(BaseModel):
    """One observed result row from remote Verl execution."""

    run_id: str
    input_tokens: int
    output_tokens: int
    inference_mode: InferenceMode
    ignore_eos: bool
    status: Literal["passed", "failed", "skipped"]
    elapsed_seconds: float | None = None
    tokens_per_second: float | None = None
    latency_ms: float | None = None
    sample_count: int = 0
    accuracy: float | None = None
    consistency: float | None = None
    error: str | None = None
    log_path: str | None = None


def build_length_matrix(config: VerlCaseConfig) -> list[VerlCaseMatrixRow]:
    """Build the strict length x mode matrix."""
    return [
        VerlCaseMatrixRow(
            input_tokens=config.input_tokens,
            output_tokens=output_tokens,
            inference_mode=mode,
            ignore_eos=config.ignore_eos,
        )
        for output_tokens in config.output_tokens
        for mode in config.inference_modes
    ]


def now_utc() -> datetime:
    """Return timezone-aware UTC now; split out for tests."""
    return datetime.now(timezone.utc)


def snapshot_timestamp(value: datetime | None = None) -> str:
    """Format a second-level timestamp for immutable config filenames."""
    value = value or now_utc()
    return value.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S")


def build_readable_run_id(config: VerlCaseConfig, created_at: datetime | None = None) -> str:
    """Build a human-readable artifact id for formal Verl experiment data."""
    created_at = created_at or now_utc()
    model = _model_slug(config.model_id)
    algorithm = "GRPO"
    sequence = f"{_token_slug(config.input_tokens)}to{_token_slug(max(config.output_tokens))}"
    timestamp = created_at.astimezone().strftime("%y%m%dd-%H%M%Ss")
    mode = "modes-" + "-".join(config.inference_modes)
    val_mode = "valonly" if config.trainer_val_only else "train"
    eos = "ignoreeos" if config.ignore_eos else "noignoreeos"
    return _safe_slug(f"{model}-{algorithm}-{sequence}-{timestamp}-{val_mode}-{mode}-{eos}")


def build_wandb_run_name(
    config: VerlCaseConfig,
    row: VerlCaseMatrixRow,
    created_at: datetime | None = None,
) -> str:
    """Build the per-matrix-row W&B run name shown in the web UI."""
    created_at = created_at or now_utc()
    model = _model_slug(config.model_id)
    algorithm = "GRPO"
    sequence = f"{_token_slug(row.input_tokens)}to{_token_slug(row.output_tokens)}"
    timestamp = created_at.astimezone().strftime("%y%m%dd-%H%M%Ss")
    val_mode = "valonly" if config.trainer_val_only else "train"
    eos = "ignoreeos" if row.ignore_eos else "noignoreeos"
    return _safe_slug(
        f"{model}-{algorithm}-{sequence}-{timestamp}-{val_mode}-{row.inference_mode}-{eos}"
    )


def _model_slug(model_id: str) -> str:
    name = model_id.rsplit("/", 1)[-1]
    name = name.replace("Qwen3.5", "Qwen35")
    name = re.sub(r"[^A-Za-z0-9]+", "-", name)
    return name.strip("-") or "model"


def _token_slug(tokens: int) -> str:
    if tokens % 1024 == 0:
        return f"{tokens // 1024}K"
    return str(tokens)


def _safe_slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def write_immutable_config(run_config: VerlCaseRunConfig, run_dir: Path) -> Path:
    """Write the full immutable run config before remote execution."""
    run_dir = Path(run_dir).expanduser()
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / f"config-{snapshot_timestamp(run_config.created_at)}.json"
    payload = run_config.model_dump(mode="json")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path

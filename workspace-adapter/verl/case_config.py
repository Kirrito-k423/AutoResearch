"""Typed config and result helpers for the formal Verl case."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


InferenceMode = Literal["sync", "async"]
CaseMode = Literal["validation", "training"]
ExecutionProfile = Literal["auto", "fsdp", "fsdp2", "veomni"]


class VerlCaseConfig(BaseModel):
    """Serializable formal-case defaults used by the Verl adapter."""

    cache_root: str = "/Users/Zhuanz/autoResearchData"
    artifact_root: str = "/Users/Zhuanz/autoResearchData/runs"
    docker_image: str = "quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5"
    docker_images_by_server: dict[str, str] = Field(default_factory=dict)
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
    dependency_source_mounts: list[str] = Field(
        default_factory=lambda: ["verl", "transformers", "mindspeed", "veomni"]
    )
    case_mode: CaseMode = "training"
    trainer_val_only: bool = False
    training_steps: int = 3
    single_card_start_batch_size: int = 1
    single_card_devices: list[int] = Field(default_factory=lambda: [0])
    single_node_devices: list[int] = Field(default_factory=lambda: list(range(8)))
    tuning_train_batch_sizes: list[int] = Field(default_factory=lambda: [1, 2, 4, 8])
    tuning_ppo_mini_batch_sizes: list[int] = Field(default_factory=lambda: [1])
    tuning_ppo_micro_batch_sizes_per_gpu: list[int] = Field(default_factory=lambda: [1])
    tuning_output_tokens: list[int] | None = None
    tuning_inference_modes: list[InferenceMode] | None = None
    train_batch_size: int = 8
    val_batch_size: int = 1
    train_max_samples: int = 8
    val_max_samples: int = 2
    rollout_n: int = 1
    n_gpus_per_node: int = 8
    tensor_model_parallel_size: int = 2
    rollout_gpu_memory_utilization: float = Field(default=0.5, ge=0.0, le=1.0)
    rollout_max_model_len_floor: int = Field(default=24576, ge=0)
    ppo_max_token_len_per_gpu_floor: int = Field(default=24576, ge=0)
    rollout_update_weights_bucket_megabytes: int = Field(default=2048, ge=1)
    cleanup_stale_verl_processes: bool = True
    row_timeout_seconds: int = 1800
    execution_profile: ExecutionProfile = "fsdp"
    use_remove_padding: bool | None = None
    use_dynamic_bsz: bool | None = None


class VerlCaseMatrixRow(BaseModel):
    """One strict experiment matrix row."""

    input_tokens: int
    output_tokens: int
    inference_mode: InferenceMode
    ignore_eos: bool = False

    @property
    def key(self) -> str:
        return f"{self.inference_mode}-{self.input_tokens}-{self.output_tokens}"


class VerlTrainingTuningRow(BaseModel):
    """One GRPO training tuning attempt."""

    case_id: str
    input_tokens: int
    output_tokens: int
    inference_mode: InferenceMode = "sync"
    ignore_eos: bool = False
    device_count: int
    visible_devices: list[int]
    train_batch_size: int
    ppo_mini_batch_size: int = 1
    ppo_micro_batch_size_per_gpu: int = 1
    rollout_n: int = 1

    @property
    def key(self) -> str:
        return self.case_id


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
    matrix: list[VerlCaseMatrixRow | VerlTrainingTuningRow]
    provenance: list[RepoProvenance] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class VerlCaseResultRow(BaseModel):
    """One observed result row from remote Verl execution."""

    run_id: str
    case_id: str | None = None
    input_tokens: int
    output_tokens: int
    inference_mode: InferenceMode
    ignore_eos: bool
    status: Literal["passed", "failed", "skipped"]
    started_at: str | None = None
    finished_at: str | None = None
    started_at_unix: float | None = None
    finished_at_unix: float | None = None
    elapsed_seconds: float | None = None
    tokens_per_second: float | None = None
    latency_ms: float | None = None
    sample_count: int = 0
    completed_training_steps: int | None = None
    target_training_steps: int | None = None
    steady_state_step_start: int | None = None
    steady_state_step_end: int | None = None
    steady_state_step_count: int | None = None
    steady_state_total_tokens: float | None = None
    steady_state_total_seconds: float | None = None
    steady_state_tokens_per_second: float | None = None
    steady_state_tokens_per_second_per_npu: float | None = None
    steady_state_token_source: str | None = None
    steady_state_time_keys: list[str] | None = None
    device_count: int | None = None
    visible_devices: list[int] | None = None
    train_batch_size: int | None = None
    ppo_mini_batch_size: int | None = None
    ppo_micro_batch_size_per_gpu: int | None = None
    failure_class: str | None = None
    accuracy: float | None = None
    consistency: float | None = None
    error: str | None = None
    log_path: str | None = None
    telemetry_raw_path: str | None = None
    telemetry_jsonl_path: str | None = None
    telemetry_summary: dict[str, Any] | None = None


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


def build_training_tuning_matrix(config: VerlCaseConfig) -> list[VerlTrainingTuningRow]:
    """Build the first-stage training tuning candidates.

    Promotion to 8-card single-node candidates is handled by orchestration after
    a stable smaller-device boundary is observed. If ``single_card_devices`` is
    configured with all local devices, this matrix directly starts full-node.
    """
    rows: list[VerlTrainingTuningRow] = []
    visible_devices = list(config.single_card_devices)
    device_count = len(visible_devices)
    train_batch_sizes = _unique_positive(
        [config.single_card_start_batch_size, *config.tuning_train_batch_sizes]
    )
    output_candidates = _unique_positive(
        list(config.tuning_output_tokens or [min(config.output_tokens)])
    )
    mode_candidates = list(config.tuning_inference_modes or [config.inference_modes[0]])
    for output_tokens in output_candidates:
        for mode in mode_candidates:
            for train_batch_size in train_batch_sizes:
                for mini_batch_size in _valid_ppo_mini_batch_sizes(
                    config.tuning_ppo_mini_batch_sizes,
                    device_count=device_count,
                    train_batch_size=train_batch_size,
                ):
                    for micro_batch_size in _unique_positive(config.tuning_ppo_micro_batch_sizes_per_gpu):
                        rows.append(
                            VerlTrainingTuningRow(
                                case_id=(
                                    f"train-{device_count}npu-{mode}-bs{train_batch_size}"
                                    f"-mini{mini_batch_size}-micro{micro_batch_size}"
                                    f"-{config.input_tokens}-{output_tokens}"
                                ),
                                input_tokens=config.input_tokens,
                                output_tokens=output_tokens,
                                inference_mode=mode,
                                ignore_eos=config.ignore_eos,
                                device_count=device_count,
                                visible_devices=visible_devices,
                                train_batch_size=train_batch_size,
                                ppo_mini_batch_size=mini_batch_size,
                                ppo_micro_batch_size_per_gpu=micro_batch_size,
                                rollout_n=config.rollout_n,
                            )
                        )
    return rows


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


def _unique_positive(values: list[int]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []
    for value in values:
        if value <= 0 or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _valid_ppo_mini_batch_sizes(
    values: list[int], *, device_count: int, train_batch_size: int
) -> list[int]:
    """Return PPO mini batches compatible with Verl's DP sharding rule."""
    candidates = [
        value
        for value in _unique_positive(values)
        if value <= train_batch_size
        and train_batch_size % value == 0
        and (value % device_count == 0 or value == train_batch_size)
    ]
    if candidates:
        return candidates
    if train_batch_size % device_count == 0:
        return [train_batch_size]
    return []


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

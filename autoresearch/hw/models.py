"""Serializable hardware-domain result contracts."""
from __future__ import annotations

from typing import Any, TypedDict


class NPUDevice(TypedDict):
    """One Ascend NPU and its core runtime metrics."""

    id: int | None
    chip_id: int | None
    name: str | None
    health: str | None
    bus_id: str | None
    memory_total_mib: int | None
    memory_used_mib: int | None
    temperature_c: int | None
    utilization_pct: int | None


class NPUProcess(TypedDict):
    """Process occupancy record, enriched in a later plan."""

    npu_id: int | None
    chip_id: int | None
    pid: int
    user: str | None
    process_name: str | None
    memory_used_mib: int | None


class DriverVersions(TypedDict):
    """Driver version sources collected from the remote server."""

    npu_smi: str | None
    driver: str | None
    package: str | None


class FieldError(TypedDict):
    """A field-level parsing failure that preserves partial device data."""

    device_id: int | None
    field: str
    reason: str


class HardwareData(TypedDict):
    """Stable payload carried in a hardware CheckResult."""

    server: dict[str, Any]
    devices: list[NPUDevice]
    processes: list[NPUProcess]
    driver_versions: DriverVersions
    warnings: list[str]
    field_errors: list[FieldError]
    fallback: str | None
    raw_log_path: str | None


class HardwareParseResult(TypedDict):
    """Pure parser output before server metadata is attached."""

    devices: list[NPUDevice]
    processes: list[NPUProcess]
    driver_versions: DriverVersions
    warnings: list[str]
    field_errors: list[FieldError]
    error: str | None

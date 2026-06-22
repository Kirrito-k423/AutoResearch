"""Runtime NPU telemetry helpers for formal Verl cases."""
from __future__ import annotations

import re
import shlex
from typing import Iterable

from pydantic import BaseModel, Field


SOURCE_NPU_SMI_WATCH = "npu-smi-watch"


class NpuTelemetrySample(BaseModel):
    """One normalized row from ``npu-smi info watch`` output."""

    run_id: str
    case_id: str
    server: str
    device_id: int
    sample_index: int
    source: str = SOURCE_NPU_SMI_WATCH
    observed_at: str | None = None
    hbm_used_mib: float | None = None
    hbm_total_mib: float | None = None
    ai_core_utilization_percent: float | None = None
    npu_utilization_percent: float | None = None
    raw_line: str = ""


class NpuTelemetrySummary(BaseModel):
    """Small aggregate used by rows, reports, and Prometheus evidence."""

    sample_count: int = 0
    device_count: int = 0
    sample_interval_seconds: int = 1
    source: str = SOURCE_NPU_SMI_WATCH
    max_hbm_used_mib: float | None = None
    hbm_total_mib: float | None = None
    max_ai_core_utilization_percent: float | None = None
    max_npu_utilization_percent: float | None = None


def build_npu_smi_watch_command(
    sample_interval_seconds: int | float = 1,
    metric_selector: str = "amn",
) -> str:
    """Build the native Ascend watch command used during Verl cases."""
    if isinstance(sample_interval_seconds, bool):
        raise ValueError("npu-smi watch interval must be an integer second in [1, 100]")
    if int(sample_interval_seconds) != sample_interval_seconds:
        raise ValueError(
            "npu-smi info watch only supports integer seconds in [1, 100]; "
            f"got {sample_interval_seconds!r}"
        )
    interval = int(sample_interval_seconds)
    if interval < 1 or interval > 100:
        raise ValueError("npu-smi watch interval must be in [1, 100] seconds")
    selector = metric_selector.strip()
    if not selector or not re.fullmatch(r"[A-Za-z]+", selector):
        raise ValueError("npu-smi watch metric selector must contain only letters")
    _ = shlex.quote(selector)
    return (
        "NPU_SMI_BIN=$(command -v npu-smi"
        " || { test -x /usr/local/sbin/npu-smi && echo /usr/local/sbin/npu-smi; }"
        " || { test -x /usr/local/Ascend/driver/tools/npu-smi"
        " && echo /usr/local/Ascend/driver/tools/npu-smi; }"
        " || { test -x /usr/local/Ascend/ascend-toolkit/latest/tools/npu-smi"
        " && echo /usr/local/Ascend/ascend-toolkit/latest/tools/npu-smi; }); "
        'test -n "$NPU_SMI_BIN" || exit 127; '
        f'while true; do date "+%Y-%m-%d %H:%M:%S"; "$NPU_SMI_BIN" info; sleep {interval}; done'
    )


def parse_npu_smi_watch_output(
    text: str,
    *,
    run_id: str,
    case_id: str,
    server: str,
) -> list[NpuTelemetrySample]:
    """Parse known ``npu-smi info watch`` table shapes without raising."""
    samples: list[NpuTelemetrySample] = []
    columns: dict[str, int] = {}
    sample_index = 0
    observed_at: str | None = None
    pending_info_device_id: int | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        timestamp = _timestamp_from_line(stripped)
        if timestamp is not None:
            observed_at = timestamp
        cells = _cells(stripped)
        if not cells:
            continue
        info_device_id = _info_device_id(cells)
        if info_device_id is not None:
            pending_info_device_id = info_device_id
            continue
        if pending_info_device_id is not None:
            info_sample = _sample_from_info_detail(
                cells,
                run_id=run_id,
                case_id=case_id,
                server=server,
                device_id=pending_info_device_id,
                sample_index=sample_index,
                observed_at=observed_at,
                raw_line=stripped,
            )
            pending_info_device_id = None
            if info_sample is not None:
                samples.append(info_sample)
                sample_index += 1
                continue
        maybe_columns = _column_map(cells)
        if maybe_columns:
            columns = maybe_columns
            continue
        sample = _sample_from_cells(
            cells,
            columns,
            run_id=run_id,
            case_id=case_id,
            server=server,
            sample_index=sample_index,
            observed_at=observed_at,
            raw_line=stripped,
        )
        if sample is not None:
            samples.append(sample)
            sample_index += 1
    return samples


def summarize_telemetry(
    samples: Iterable[NpuTelemetrySample],
    *,
    sample_interval_seconds: int = 1,
) -> NpuTelemetrySummary:
    """Summarize normalized telemetry rows for result metadata."""
    rows = list(samples)
    devices = {row.device_id for row in rows}
    return NpuTelemetrySummary(
        sample_count=len(rows),
        device_count=len(devices),
        sample_interval_seconds=sample_interval_seconds,
        max_hbm_used_mib=_max(row.hbm_used_mib for row in rows),
        hbm_total_mib=_max(row.hbm_total_mib for row in rows),
        max_ai_core_utilization_percent=_max(
            row.ai_core_utilization_percent for row in rows
        ),
        max_npu_utilization_percent=_max(
            row.npu_utilization_percent for row in rows
        ),
    )


def _cells(line: str) -> list[str]:
    if "|" not in line:
        return []
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if not cells or all(_is_separator(cell) for cell in cells):
        return []
    return cells


def _is_separator(value: str) -> bool:
    return bool(value) and set(value) <= {"-", "+", " "}


def _header_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _canonical_header(value: str) -> str | None:
    key = _header_key(value)
    if key in {"npuid", "deviceid", "id"} or key == "npu":
        return "device_id"
    if "aicore" in key:
        return "ai_core"
    if "npu" in key and ("util" in key or "usage" in key):
        return "npu_utilization"
    if "hbm" in key or "memory" in key:
        if "used" in key:
            return "hbm_used"
        if "total" in key or "capacity" in key:
            return "hbm_total"
        return "memory"
    return None


def _column_map(cells: list[str]) -> dict[str, int]:
    columns: dict[str, int] = {}
    for index, cell in enumerate(cells):
        canonical = _canonical_header(cell)
        if canonical is not None:
            columns[canonical] = index
    if "device_id" not in columns:
        return {}
    return columns


def _info_device_id(cells: list[str]) -> int | None:
    if len(cells) < 3:
        return None
    if not re.fullmatch(r"\d+\s+\S+", cells[0]):
        return None
    if not re.search(r"\bOK\b|FAIL|WARN", cells[1], flags=re.IGNORECASE):
        return None
    match = re.match(r"(\d+)", cells[0])
    return int(match.group(1)) if match else None


def _sample_from_info_detail(
    cells: list[str],
    *,
    run_id: str,
    case_id: str,
    server: str,
    device_id: int,
    sample_index: int,
    observed_at: str | None,
    raw_line: str,
) -> NpuTelemetrySample | None:
    if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
        return None
    values = [float(item) for item in re.findall(r"\d+(?:\.\d+)?", cells[2])]
    if len(values) < 5:
        return None
    return NpuTelemetrySample(
        run_id=run_id,
        case_id=case_id,
        server=server,
        device_id=device_id,
        sample_index=sample_index,
        observed_at=observed_at,
        hbm_used_mib=values[-2],
        hbm_total_mib=values[-1],
        ai_core_utilization_percent=values[0],
        raw_line=raw_line,
    )


def _sample_from_cells(
    cells: list[str],
    columns: dict[str, int],
    *,
    run_id: str,
    case_id: str,
    server: str,
    sample_index: int,
    observed_at: str | None,
    raw_line: str,
) -> NpuTelemetrySample | None:
    if not columns:
        return None
    device_id = _int_at(cells, columns.get("device_id"))
    if device_id is None:
        return None
    memory_used, memory_total = _memory_at(cells, columns)
    return NpuTelemetrySample(
        run_id=run_id,
        case_id=case_id,
        server=server,
        device_id=device_id,
        sample_index=sample_index,
        observed_at=observed_at,
        hbm_used_mib=memory_used,
        hbm_total_mib=memory_total,
        ai_core_utilization_percent=_number_at(cells, columns.get("ai_core")),
        npu_utilization_percent=_number_at(
            cells, columns.get("npu_utilization")
        ),
        raw_line=raw_line,
    )


def _memory_at(
    cells: list[str],
    columns: dict[str, int],
) -> tuple[float | None, float | None]:
    used = _number_at(cells, columns.get("hbm_used"))
    total = _number_at(cells, columns.get("hbm_total"))
    memory_index = columns.get("memory")
    if memory_index is not None and memory_index < len(cells):
        parsed_used, parsed_total = _parse_memory(cells[memory_index])
        used = used if used is not None else parsed_used
        total = total if total is not None else parsed_total
    return used, total


def _parse_memory(value: str) -> tuple[float | None, float | None]:
    parts = re.split(r"\s*/\s*", value)
    if len(parts) == 2:
        return _first_number(parts[0]), _first_number(parts[1])
    return _first_number(value), None


def _int_at(cells: list[str], index: int | None) -> int | None:
    value = _number_at(cells, index)
    return int(value) if value is not None else None


def _number_at(cells: list[str], index: int | None) -> float | None:
    if index is None or index >= len(cells):
        return None
    return _first_number(cells[index])


def _first_number(value: str) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if match is None:
        return None
    number = float(match.group(0))
    return int(number) if number.is_integer() else number


def _timestamp_from_line(value: str) -> str | None:
    match = re.search(
        r"(\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}:\d{2})",
        value,
    )
    return match.group(1) if match else None


def _max(values: Iterable[float | None]) -> float | None:
    numeric = [value for value in values if value is not None]
    return max(numeric) if numeric else None

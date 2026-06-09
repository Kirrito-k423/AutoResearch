"""Pure parsers for Ascend ``npu-smi info`` output."""
from __future__ import annotations

import re

from .models import (
    DriverVersions,
    FieldError,
    HardwareParseResult,
    NPUDevice,
)


CORE_FIELDS = (
    "memory_total_mib",
    "memory_used_mib",
    "temperature_c",
    "utilization_pct",
)


def _cells(line: str) -> list[str]:
    if "|" not in line:
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _header_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _is_header(cells: list[str], expected: set[str]) -> bool:
    return bool(expected.intersection({_header_key(cell) for cell in cells}))


def _column_map(cells: list[str]) -> dict[str, int]:
    return {_header_key(cell): index for index, cell in enumerate(cells)}


def _column(
    cells: list[str],
    columns: dict[str, int],
    *aliases: str,
) -> str | None:
    for alias in aliases:
        index = columns.get(alias)
        if index is not None and index < len(cells):
            return cells[index]
    return None


def _parse_int(
    value: str | None,
    *,
    device_id: int | None,
    field: str,
    field_errors: list[FieldError],
) -> int | None:
    if value is None or value.strip() in {"", "-", "N/A", "NA"}:
        field_errors.append(
            FieldError(
                device_id=device_id,
                field=field,
                reason="missing value",
            )
        )
        return None
    match = re.fullmatch(r"\s*(\d+)\s*(?:%|C|MB|MiB)?\s*", value)
    if match is None:
        field_errors.append(
            FieldError(
                device_id=device_id,
                field=field,
                reason=f"invalid integer: {value!r}",
            )
        )
        return None
    return int(match.group(1))


def _parse_memory(
    value: str | None,
    *,
    device_id: int | None,
    field_errors: list[FieldError],
) -> tuple[int | None, int | None]:
    if value is None:
        for field in ("memory_used_mib", "memory_total_mib"):
            _parse_int(
                None,
                device_id=device_id,
                field=field,
                field_errors=field_errors,
            )
        return None, None

    parts = re.split(r"\s*/\s*", value.strip())
    if len(parts) != 2:
        reason = f"expected used / total, got {value!r}"
        field_errors.extend(
            [
                FieldError(
                    device_id=device_id,
                    field="memory_used_mib",
                    reason=reason,
                ),
                FieldError(
                    device_id=device_id,
                    field="memory_total_mib",
                    reason=reason,
                ),
            ]
        )
        return None, None

    used = _parse_int(
        parts[0],
        device_id=device_id,
        field="memory_used_mib",
        field_errors=field_errors,
    )
    total = _parse_int(
        parts[1],
        device_id=device_id,
        field="memory_total_mib",
        field_errors=field_errors,
    )
    return used, total


def _new_device(device_id: int | None, name: str | None) -> NPUDevice:
    return NPUDevice(
        id=device_id,
        chip_id=None,
        name=name,
        health=None,
        bus_id=None,
        memory_total_mib=None,
        memory_used_mib=None,
        temperature_c=None,
        utilization_pct=None,
    )


def _append_missing_core_errors(
    devices: list[NPUDevice],
    field_errors: list[FieldError],
) -> None:
    existing = {
        (error["device_id"], error["field"])
        for error in field_errors
    }
    for device in devices:
        for field in CORE_FIELDS:
            if device[field] is None and (device["id"], field) not in existing:
                field_errors.append(
                    FieldError(
                        device_id=device["id"],
                        field=field,
                        reason="field not present in device record",
                    )
                )


def parse_npu_smi_info(text: str) -> HardwareParseResult:
    """Parse table-oriented ``npu-smi info`` output without side effects."""
    devices: list[NPUDevice] = []
    field_errors: list[FieldError] = []
    warnings: list[str] = []
    primary_columns: dict[str, int] | None = None
    detail_columns: dict[str, int] | None = None
    current: NPUDevice | None = None

    primary_headers = {"npuname", "health", "tempc", "temperaturec"}
    detail_headers = {
        "chipdevice",
        "busid",
        "aicore",
        "aicoreusage",
        "aicoreusagepct",
        "hbmusage",
        "hbmusagemb",
        "hbmusagemib",
    }

    for line in text.splitlines():
        cells = _cells(line)
        if not cells:
            continue
        if _is_header(cells, primary_headers):
            primary_columns = _column_map(cells)
            continue
        if _is_header(cells, detail_headers):
            detail_columns = _column_map(cells)
            continue
        if "No running processes found" in line:
            continue

        if primary_columns is not None:
            identity = _column(cells, primary_columns, "npuname", "npu")
            match = re.fullmatch(r"\s*(\d+)\s+(.+?)\s*", identity or "")
            if match is not None and not match.group(2).isdigit():
                if current is not None:
                    devices.append(current)
                device_id = int(match.group(1))
                current = _new_device(device_id, match.group(2))
                current["health"] = _column(
                    cells, primary_columns, "health", "status"
                )
                current["temperature_c"] = _parse_int(
                    _column(
                        cells,
                        primary_columns,
                        "tempc",
                        "temperaturec",
                        "temp",
                    ),
                    device_id=device_id,
                    field="temperature_c",
                    field_errors=field_errors,
                )
                continue

        if current is not None and detail_columns is not None:
            chip_device = _column(
                cells, detail_columns, "chipdevice", "chipid", "device"
            )
            chip_match = re.fullmatch(r"\s*(\d+)(?:\s+(\d+))?\s*", chip_device or "")
            if chip_match is None:
                continue
            current["chip_id"] = int(chip_match.group(2) or chip_match.group(1))
            current["bus_id"] = _column(cells, detail_columns, "busid", "pcibusid")
            current["utilization_pct"] = _parse_int(
                _column(
                    cells,
                    detail_columns,
                    "aicore",
                    "aicoreusage",
                    "aicoreusagepct",
                    "aicorepercent",
                ),
                device_id=current["id"],
                field="utilization_pct",
                field_errors=field_errors,
            )
            memory_used, memory_total = _parse_memory(
                _column(
                    cells,
                    detail_columns,
                    "hbmusage",
                    "hbmusagemb",
                    "hbmusagemib",
                    "hbm",
                ),
                device_id=current["id"],
                field_errors=field_errors,
            )
            current["memory_used_mib"] = memory_used
            current["memory_total_mib"] = memory_total

    if current is not None:
        devices.append(current)

    _append_missing_core_errors(devices, field_errors)
    error = None
    if not devices:
        error = "npu-smi output contained no recognizable device records"

    return HardwareParseResult(
        devices=devices,
        processes=[],
        driver_versions=DriverVersions(npu_smi=None, driver=None, package=None),
        warnings=warnings,
        field_errors=field_errors,
        error=error,
    )

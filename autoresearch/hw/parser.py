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

COLUMN_ALIASES = {
    "identity": {
        "npuname",
        "npu",
        "npuidname",
        "npuidproductname",
        "deviceproductname",
    },
    "health": {"health", "status"},
    "temperature": {"tempc", "temperaturec", "temp", "temperature"},
    "chip_device": {"chipdevice", "chipid", "device", "chipdeviceid"},
    "bus_id": {"busid", "pcibusid", "pcibus"},
    "utilization": {
        "aicore",
        "aicoreusage",
        "aicoreusagepct",
        "aicorepercent",
        "aicoreutilization",
        "aicoreutilizationpct",
    },
    "memory": {
        "hbmusage",
        "hbmusagemb",
        "hbmusagemib",
        "hbm",
        "memoryusage",
        "memoryusagemb",
        "memoryusagemib",
    },
    "device_id": {"npuid", "deviceid", "id"},
}

PRIMARY_HEADER_FIELDS = {"identity", "health", "temperature"}
DETAIL_HEADER_FIELDS = {"chip_device", "bus_id", "utilization", "memory"}


def _cells(line: str) -> list[str]:
    if "|" not in line:
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _header_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _canonical_header(value: str) -> str | None:
    key = _header_key(value)
    for canonical, aliases in COLUMN_ALIASES.items():
        if key in aliases:
            return canonical
    return None


def _column_map(cells: list[str]) -> dict[str, int]:
    columns: dict[str, int] = {}
    for index, cell in enumerate(cells):
        canonical = _canonical_header(cell)
        if canonical is not None:
            columns[canonical] = index
    return columns


def _column(
    cells: list[str],
    columns: dict[str, int],
    canonical: str,
) -> str | None:
    index = columns.get(canonical)
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


def core_field_errors(devices: list[NPUDevice]) -> list[FieldError]:
    """Return current missing-core errors after any supplemental merge."""
    errors: list[FieldError] = []
    _append_missing_core_errors(devices, errors)
    return errors


def parse_typed_metric_output(
    text: str,
    metric_type: str,
    device_id: int,
) -> dict[str, int]:
    """Parse one fixed typed-query response for an integer device id."""
    if metric_type not in {"memory", "temp", "usages"}:
        raise ValueError(f"unsupported typed metric: {metric_type}")
    if (
        not isinstance(device_id, int)
        or isinstance(device_id, bool)
        or device_id < 0
    ):
        raise ValueError("device_id must be a non-negative integer")

    header_columns: dict[str, int] | None = None
    for line in text.splitlines():
        cells = _cells(line)
        if not cells:
            continue
        columns = _column_map(cells)
        if "device_id" in columns and (
            "memory" in columns
            or "temperature" in columns
            or "utilization" in columns
        ):
            header_columns = columns
            continue
        if header_columns is None:
            continue

        row_id = _parse_plain_int(_column(cells, header_columns, "device_id"))
        if row_id != device_id:
            continue

        if metric_type == "memory":
            value = _column(cells, header_columns, "memory")
            parts = re.split(r"\s*/\s*", value or "")
            if len(parts) != 2:
                return {}
            used = _parse_plain_int(parts[0])
            total = _parse_plain_int(parts[1])
            if used is None or total is None:
                return {}
            return {
                "memory_used_mib": used,
                "memory_total_mib": total,
            }
        if metric_type == "temp":
            value = _parse_plain_int(
                _column(cells, header_columns, "temperature")
            )
            return {"temperature_c": value} if value is not None else {}

        value = _parse_plain_int(
            _column(cells, header_columns, "utilization")
        )
        return {"utilization_pct": value} if value is not None else {}

    return {}


def _parse_plain_int(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.fullmatch(
        r"\s*(\d+)\s*(?:%|C|MB|MiB)?\s*",
        value,
        flags=re.IGNORECASE,
    )
    return int(match.group(1)) if match is not None else None


def parse_npu_smi_info(text: str) -> HardwareParseResult:
    """Parse table-oriented ``npu-smi info`` output without side effects."""
    devices: list[NPUDevice] = []
    field_errors: list[FieldError] = []
    warnings: list[str] = []
    primary_columns: dict[str, int] | None = None
    detail_columns: dict[str, int] | None = None
    current: NPUDevice | None = None

    for line in text.splitlines():
        cells = _cells(line)
        if not cells:
            continue
        columns = _column_map(cells)
        if PRIMARY_HEADER_FIELDS.intersection(columns):
            primary_columns = columns
            continue
        if DETAIL_HEADER_FIELDS.intersection(columns):
            detail_columns = columns
            continue
        if "No running processes found" in line:
            continue

        if primary_columns is not None:
            identity = _column(cells, primary_columns, "identity")
            match = re.fullmatch(r"\s*(\d+)\s+(.+?)\s*", identity or "")
            if match is not None and not match.group(2).isdigit():
                if current is not None:
                    devices.append(current)
                device_id = int(match.group(1))
                current = _new_device(device_id, match.group(2))
                current["health"] = _column(
                    cells, primary_columns, "health"
                )
                current["temperature_c"] = _parse_int(
                    _column(cells, primary_columns, "temperature"),
                    device_id=device_id,
                    field="temperature_c",
                    field_errors=field_errors,
                )
                continue

        if current is not None and detail_columns is not None:
            chip_device = _column(
                cells, detail_columns, "chip_device"
            )
            chip_match = re.fullmatch(r"\s*(\d+)(?:\s+(\d+))?\s*", chip_device or "")
            if chip_match is None:
                continue
            current["chip_id"] = int(chip_match.group(2) or chip_match.group(1))
            current["bus_id"] = _column(cells, detail_columns, "bus_id")
            current["utilization_pct"] = _parse_int(
                _column(cells, detail_columns, "utilization"),
                device_id=current["id"],
                field="utilization_pct",
                field_errors=field_errors,
            )
            memory_used, memory_total = _parse_memory(
                _column(cells, detail_columns, "memory"),
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

"""Pure parsers for Ascend ``npu-smi info`` output."""
from __future__ import annotations

import re

from .models import (
    DriverVersions,
    FieldError,
    HardwareParseResult,
    NPUDevice,
    NPUProcess,
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
PROCESS_COLUMN_ALIASES = {
    "npu_id": {"npu", "npuid"},
    "chip_id": {"chip", "chipid"},
    "npu_chip": {"npuchip", "chipdevice", "npuchipid"},
    "pid": {"pid", "processid"},
    "memory": {
        "processmemory",
        "processmemorymb",
        "processmemorymib",
        "memorymb",
        "memorymib",
    },
}


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
        description=None,
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


def _process_column_map(cells: list[str]) -> dict[str, int]:
    columns: dict[str, int] = {}
    for index, cell in enumerate(cells):
        key = _header_key(cell)
        for canonical, aliases in PROCESS_COLUMN_ALIASES.items():
            if key in aliases:
                columns[canonical] = index
                break
    return columns


def _process_column(
    cells: list[str],
    columns: dict[str, int],
    canonical: str,
) -> str | None:
    index = columns.get(canonical)
    if index is None or index >= len(cells):
        return None
    return cells[index]


def parse_processes(
    text: str,
    warnings: list[str] | None = None,
) -> list[NPUProcess]:
    """Parse process occupancy rows without retaining untrusted PID text."""
    process_warnings = warnings if warnings is not None else []
    processes: list[NPUProcess] = []
    columns: dict[str, int] | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        cells = _cells(line)
        if not cells:
            continue
        candidate_columns = _process_column_map(cells)
        if (
            "pid" in candidate_columns
            and "memory" in candidate_columns
            and (
                "npu_chip" in candidate_columns
                or {
                    "npu_id",
                    "chip_id",
                }.issubset(candidate_columns)
            )
        ):
            columns = candidate_columns
            continue
        if columns is None:
            continue

        pid = _parse_plain_int(_process_column(cells, columns, "pid"))
        memory = _parse_plain_int(
            _process_column(cells, columns, "memory")
        )
        if "npu_chip" in columns:
            identity = _process_column(cells, columns, "npu_chip")
            identity_match = re.fullmatch(
                r"\s*(\d+)\s+(\d+)\s*",
                identity or "",
            )
            npu_id = (
                int(identity_match.group(1))
                if identity_match is not None
                else None
            )
            chip_id = (
                int(identity_match.group(2))
                if identity_match is not None
                else None
            )
        else:
            npu_id = _parse_plain_int(
                _process_column(cells, columns, "npu_id")
            )
            chip_id = _parse_plain_int(
                _process_column(cells, columns, "chip_id")
            )

        if None in (npu_id, chip_id, pid, memory):
            process_warnings.append(
                f"ignored invalid process record at line {line_number}"
            )
            continue
        processes.append(
            NPUProcess(
                npu_id=npu_id,
                chip_id=chip_id,
                pid=pid,
                user=None,
                process_name=None,
                memory_used_mib=memory,
            )
        )

    return processes


def parse_ps_output(text: str) -> dict[int, tuple[str, str]]:
    """Parse ``ps`` pid/user/comm rows, ignoring malformed PID values."""
    details: dict[int, tuple[str, str]] = {}
    for line in text.splitlines():
        parts = line.strip().split(maxsplit=2)
        if len(parts) != 3:
            continue
        pid = _parse_plain_int(parts[0])
        if pid is None:
            continue
        user = parts[1]
        process_name = parts[2].rsplit("/", 1)[-1]
        if user and process_name:
            details[pid] = (user, process_name)
    return details


def parse_driver_version_info(text: str) -> DriverVersions:
    """Parse supported keys from Ascend driver ``version.info``."""
    values = DriverVersions(npu_smi=None, driver=None, package=None)
    for line in text.splitlines():
        match = re.fullmatch(r"\s*([^=#]+?)\s*=\s*(.*?)\s*", line)
        if match is None:
            continue
        key = match.group(1).strip().lower()
        value = match.group(2).strip()
        if not value:
            continue
        if key == "version":
            values["driver"] = value
        elif key == "package_version":
            values["package"] = value
    return values


def parse_lspci_devices(text: str) -> list[NPUDevice]:
    """Parse presence-only Ascend accelerators from ``lspci -Dnn``."""
    devices: list[NPUDevice] = []
    excluded = ("bridge", "ethernet", "network", "management", "controller")
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(
            r"^(?P<address>[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:"
            r"[0-9a-fA-F]{2}\.[0-7])\s+(?P<description>.+)$",
            stripped,
        )
        if match is None:
            continue
        description = match.group("description")
        lowered = description.lower()
        if "processing accelerators" not in lowered or "huawei" not in lowered:
            continue
        if any(term in lowered for term in excluded):
            continue
        if "ascend" not in lowered and "d802" not in lowered:
            continue
        devices.append(
            NPUDevice(
                id=len(devices),
                chip_id=None,
                name="Huawei Ascend accelerator",
                health=None,
                bus_id=match.group("address"),
                description=stripped,
                memory_total_mib=None,
                memory_used_mib=None,
                temperature_c=None,
                utilization_pct=None,
            )
        )
    return devices


def parse_npu_smi_info(text: str) -> HardwareParseResult:
    """Parse table-oriented ``npu-smi info`` output without side effects."""
    devices: list[NPUDevice] = []
    field_errors: list[FieldError] = []
    warnings: list[str] = []
    primary_columns: dict[str, int] | None = None
    detail_columns: dict[str, int] | None = None
    current: NPUDevice | None = None
    in_process_table = False

    for line in text.splitlines():
        cells = _cells(line)
        if not cells:
            continue
        process_columns = _process_column_map(cells)
        if "pid" in process_columns and "memory" in process_columns:
            in_process_table = True
            continue
        if in_process_table:
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

    version_match = re.search(
        r"\bnpu-smi\s+([A-Za-z0-9][A-Za-z0-9._-]*)",
        text,
        flags=re.IGNORECASE,
    )
    processes = parse_processes(text, warnings)
    return HardwareParseResult(
        devices=devices,
        processes=processes,
        driver_versions=DriverVersions(
            npu_smi=version_match.group(1) if version_match is not None else None,
            driver=None,
            package=None,
        ),
        warnings=warnings,
        field_errors=field_errors,
        error=error,
    )

"""Push minimal run metrics to a reachable Prometheus Pushgateway."""
from __future__ import annotations

import re
import shlex
import importlib
from pathlib import Path
from typing import Any, Iterable

from workspace_core.config import ServerSpec
from workspace_core.ssh import HostSpec
from workspace_core.ssh.tunnel import open_reverse_tunnel

run_in_env = importlib.import_module("workspace-adapter.common.conda_utils").run_in_env

PUSHGATEWAY_REMOTE_PORT = 17891
PUSHGATEWAY_LOCAL_PORT = 9091


class PushError(Exception):
    """Pushgateway write failed."""


RESOURCE_METRIC_NAMES = (
    "autoresearch_npu_hbm_used_mib",
    "autoresearch_npu_hbm_total_mib",
    "autoresearch_npu_aicore_utilization_percent",
    "autoresearch_npu_utilization_percent",
)

MACHINE_RESOURCE_METRIC_NAMES = (
    "autoresearch_machine_npu_hbm_used_mib",
    "autoresearch_machine_npu_hbm_total_mib",
    "autoresearch_machine_npu_aicore_utilization_percent",
    "autoresearch_machine_npu_utilization_percent",
    "autoresearch_machine_npu_sample_time_seconds",
)

EXPERIMENT_CASE_METRIC_NAMES = (
    "autoresearch_experiment_case_info",
    "autoresearch_experiment_case_latest_sample_index",
    "autoresearch_experiment_case_start_time_seconds",
    "autoresearch_experiment_case_end_time_seconds",
    "autoresearch_experiment_case_elapsed_seconds",
)


def _job_suffix(run_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", run_id).strip("_")
    return cleaned or "unknown"


def push_metrics(
    server: ServerSpec,
    run_id: str,
    npu_count: int,
    pushgateway_url: str = "http://localhost:9091",
    timeout: float = 10.0,
) -> bool:
    """Push one NPU-count metric from the remote server.

    Uses Pushgateway's text exposition endpoint through ``curl`` so the remote
    conda env does not need the prometheus_client package.
    """
    if not run_id:
        raise PushError("run_id 不能为空")
    if npu_count < 0:
        raise PushError("npu_count 不能为负数")

    endpoint = f"{pushgateway_url.rstrip('/')}/metrics/job/ar_{_job_suffix(run_id)}"
    metric = f'autoresearch_npu_count{{run_id="{_job_suffix(run_id)}"}} {int(npu_count)}\n'
    command = (
        f"printf %s {shlex.quote(metric)} "
        f"| curl --fail --silent --show-error --data-binary @- {shlex.quote(endpoint)}"
    )
    tunnel = _open_pushgateway_tunnel(server)
    try:
        ec, stdout, stderr = run_in_env(
            server,
            command,
            conda_env=getattr(server, "conda_env", "") or "",
            workdir=getattr(server, "workdir", "/root") or "/root",
            timeout=timeout,
        )
    finally:
        tunnel.stop(timeout_s=3.0)
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True


def build_telemetry_exposition(samples: Iterable[Any]) -> str:
    """Build Prometheus text exposition for normalized NPU telemetry rows."""
    return _build_telemetry_exposition(samples, include_sample_index=True)


def build_latest_telemetry_exposition(samples: Iterable[Any]) -> str:
    """Build latest-value telemetry exposition suitable for Pushgateway.

    Pushgateway stores one current value per metric label set. The full
    per-sample file intentionally keeps every row for offline reports, while
    this helper collapses samples to the latest row for each run/case/device.
    """
    latest: dict[str, Any] = {}
    for sample in samples:
        latest[_telemetry_labels(sample, include_sample_index=False)] = sample
    return _build_telemetry_exposition(latest.values(), include_sample_index=False)


def build_machine_latest_telemetry_exposition(samples: Iterable[Any]) -> str:
    """Build latest-value machine telemetry without experiment/case labels.

    These metrics are for long-running machine dashboards. Keeping run/case
    labels out avoids the "one experiment creates many duplicate device lines"
    problem in Grafana.
    """
    latest: dict[str, Any] = {}
    for sample in samples:
        latest[_machine_telemetry_labels(sample)] = sample
    return _build_machine_telemetry_exposition(latest.values())


def build_experiment_case_exposition(
    samples: Iterable[Any],
    *,
    wandb_run_names: dict[str, str] | None = None,
    wandb_project: str | None = None,
    case_metadata: dict[str, Any] | None = None,
) -> str:
    """Build low-cardinality experiment/case metadata metrics.

    The value is intentionally simple; the labels are what Grafana uses to map
    an experiment case to server, case id, and W&B display name.
    """
    latest: dict[tuple[str, str, str], Any] = {}
    for sample in samples:
        run_id = _sample_value(sample, "run_id")
        case_id = _sample_value(sample, "case_id")
        server = _sample_value(sample, "server")
        if run_id is None or case_id is None or server is None:
            continue
        latest[(str(run_id), str(case_id), str(server))] = sample
    if not latest:
        return ""

    lines = [
        "# TYPE autoresearch_experiment_case_info gauge",
        "# TYPE autoresearch_experiment_case_latest_sample_index gauge",
        "# TYPE autoresearch_experiment_case_start_time_seconds gauge",
        "# TYPE autoresearch_experiment_case_end_time_seconds gauge",
        "# TYPE autoresearch_experiment_case_elapsed_seconds gauge",
    ]
    for (run_id, case_id, server), sample in sorted(latest.items()):
        metadata = _case_metadata(case_metadata, case_id)
        labels = {
            "run_id": run_id,
            "case_id": case_id,
            "server": server,
            "wandb_project": wandb_project or "verl",
            "wandb_run_name": (wandb_run_names or {}).get(case_id, case_id),
        }
        started_at = _sample_value(sample, "started_at") or _sample_value(metadata, "started_at")
        finished_at = _sample_value(sample, "finished_at") or _sample_value(metadata, "finished_at")
        if started_at is not None:
            labels["case_started_at"] = started_at
        if finished_at is not None:
            labels["case_finished_at"] = finished_at
        label_text = _labels_from_dict(labels)
        lines.append(f"autoresearch_experiment_case_info{{{label_text}}} 1")
        sample_index = _sample_value(sample, "sample_index")
        if sample_index is not None:
            lines.append(
                "autoresearch_experiment_case_latest_sample_index"
                f"{{{label_text}}} {float(sample_index):g}"
            )
        time_values = {
            "autoresearch_experiment_case_start_time_seconds": _first_not_none(
                _sample_value(sample, "started_at_unix"),
                _sample_value(sample, "start_time_seconds"),
                _sample_value(metadata, "started_at_unix"),
                _sample_value(metadata, "start_time_seconds"),
            ),
            "autoresearch_experiment_case_end_time_seconds": _first_not_none(
                _sample_value(sample, "finished_at_unix"),
                _sample_value(sample, "end_time_seconds"),
                _sample_value(metadata, "finished_at_unix"),
                _sample_value(metadata, "end_time_seconds"),
            ),
            "autoresearch_experiment_case_elapsed_seconds": _first_not_none(
                _sample_value(sample, "elapsed_seconds"),
                _sample_value(metadata, "elapsed_seconds"),
            ),
        }
        for name, value in time_values.items():
            if value is None:
                continue
            lines.append(f"{name}{{{label_text}}} {_metric_number(value)}")
    return "\n".join(lines + [""])


def _build_telemetry_exposition(
    samples: Iterable[Any],
    *,
    include_sample_index: bool,
) -> str:
    lines = [
        "# TYPE autoresearch_npu_hbm_used_mib gauge",
        "# TYPE autoresearch_npu_hbm_total_mib gauge",
        "# TYPE autoresearch_npu_aicore_utilization_percent gauge",
        "# TYPE autoresearch_npu_utilization_percent gauge",
    ]
    emitted = 0
    for sample in samples:
        labels = _telemetry_labels(sample, include_sample_index=include_sample_index)
        values = {
            "autoresearch_npu_hbm_used_mib": _sample_value(sample, "hbm_used_mib"),
            "autoresearch_npu_hbm_total_mib": _sample_value(sample, "hbm_total_mib"),
            "autoresearch_npu_aicore_utilization_percent": _sample_value(
                sample,
                "ai_core_utilization_percent",
            ),
            "autoresearch_npu_utilization_percent": _sample_value(
                sample,
                "npu_utilization_percent",
            ),
        }
        for name, value in values.items():
            if value is None:
                continue
            lines.append(f"{name}{{{labels}}} {_metric_number(value)}")
            emitted += 1
    if emitted == 0:
        return ""
    return "\n".join(lines + [""])


def _build_machine_telemetry_exposition(samples: Iterable[Any]) -> str:
    lines = [
        "# TYPE autoresearch_machine_npu_hbm_used_mib gauge",
        "# TYPE autoresearch_machine_npu_hbm_total_mib gauge",
        "# TYPE autoresearch_machine_npu_aicore_utilization_percent gauge",
        "# TYPE autoresearch_machine_npu_utilization_percent gauge",
        "# TYPE autoresearch_machine_npu_sample_time_seconds gauge",
    ]
    emitted = 0
    for sample in samples:
        labels = _machine_telemetry_labels(sample)
        values = {
            "autoresearch_machine_npu_hbm_used_mib": _sample_value(sample, "hbm_used_mib"),
            "autoresearch_machine_npu_hbm_total_mib": _sample_value(sample, "hbm_total_mib"),
            "autoresearch_machine_npu_aicore_utilization_percent": _sample_value(
                sample,
                "ai_core_utilization_percent",
            ),
            "autoresearch_machine_npu_utilization_percent": _sample_value(
                sample,
                "npu_utilization_percent",
            ),
            "autoresearch_machine_npu_sample_time_seconds": _sample_value(
                sample,
                "sample_time_seconds",
            ),
        }
        for name, value in values.items():
            if value is None:
                continue
            lines.append(f"{name}{{{labels}}} {_metric_number(value)}")
            emitted += 1
    if emitted == 0:
        return ""
    return "\n".join(lines + [""])


def push_telemetry_metrics(
    server: ServerSpec,
    run_id: str,
    samples: Iterable[Any],
    *,
    pushgateway_url: str = "http://localhost:9091",
    timeout: float = 10.0,
    exposition: str | None = None,
) -> bool:
    """Push normalized NPU telemetry metrics through the remote host."""
    if not run_id:
        raise PushError("run_id 不能为空")
    metric = exposition if exposition is not None else build_latest_telemetry_exposition(samples)
    if not metric.strip():
        return False

    endpoint = f"{pushgateway_url.rstrip('/')}/metrics/job/ar_{_job_suffix(run_id)}"
    command = (
        f"printf %s {shlex.quote(metric)} "
        f"| curl --fail --silent --show-error --data-binary @- {shlex.quote(endpoint)}"
    )
    tunnel = _open_pushgateway_tunnel(server)
    try:
        ec, stdout, stderr = run_in_env(
            server,
            command,
            conda_env=getattr(server, "conda_env", "") or "",
            workdir=getattr(server, "workdir", "/root") or "/root",
            timeout=timeout,
        )
    finally:
        tunnel.stop(timeout_s=3.0)
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True


def push_machine_telemetry_metrics(
    server: ServerSpec,
    samples: Iterable[Any],
    *,
    pushgateway_url: str = "http://localhost:9091",
    timeout: float = 10.0,
    exposition: str | None = None,
) -> bool:
    """Push latest machine-level NPU telemetry through the remote host."""
    metric = exposition if exposition is not None else build_machine_latest_telemetry_exposition(samples)
    if not metric.strip():
        return False

    endpoint = f"{pushgateway_url.rstrip('/')}/metrics/job/autoresearch_machine/server/{_job_suffix(server.name)}"
    command = (
        f"printf %s {shlex.quote(metric)} "
        f"| curl --fail --silent --show-error -X PUT --data-binary @- {shlex.quote(endpoint)}"
    )
    tunnel = _open_pushgateway_tunnel(server)
    try:
        ec, stdout, stderr = run_in_env(
            server,
            command,
            conda_env=getattr(server, "conda_env", "") or "",
            workdir=getattr(server, "workdir", "/root") or "/root",
            timeout=timeout,
        )
    finally:
        tunnel.stop(timeout_s=3.0)
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"machine telemetry pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True


def push_experiment_case_metrics(
    server: ServerSpec,
    run_id: str,
    samples: Iterable[Any],
    *,
    pushgateway_url: str = "http://localhost:9091",
    timeout: float = 10.0,
    exposition: str | None = None,
    wandb_run_names: dict[str, str] | None = None,
    wandb_project: str | None = None,
    case_metadata: dict[str, Any] | None = None,
) -> bool:
    """Push experiment/case metadata for Grafana run slicing."""
    metric = exposition if exposition is not None else build_experiment_case_exposition(
        samples,
        wandb_run_names=wandb_run_names,
        wandb_project=wandb_project,
        case_metadata=case_metadata,
    )
    if not metric.strip():
        return False

    endpoint = f"{pushgateway_url.rstrip('/')}/metrics/job/ar_{_job_suffix(run_id)}"
    command = (
        f"printf %s {shlex.quote(metric)} "
        f"| curl --fail --silent --show-error --data-binary @- {shlex.quote(endpoint)}"
    )
    tunnel = _open_pushgateway_tunnel(server)
    try:
        ec, stdout, stderr = run_in_env(
            server,
            command,
            conda_env=getattr(server, "conda_env", "") or "",
            workdir=getattr(server, "workdir", "/root") or "/root",
            timeout=timeout,
        )
    finally:
        tunnel.stop(timeout_s=3.0)
    if ec != 0:
        detail = (stderr or stdout or "").strip()
        raise PushError(f"experiment case pushgateway 推送失败 exit={ec}: {detail[:200]}")
    return True


def _telemetry_labels(sample: Any, *, include_sample_index: bool) -> str:
    label_values = {
        "run_id": _sample_value(sample, "run_id"),
        "case_id": _sample_value(sample, "case_id"),
        "server": _sample_value(sample, "server"),
        "device_id": _sample_value(sample, "device_id"),
        "source": _sample_value(sample, "source") or "npu-smi-watch",
    }
    if include_sample_index:
        sample_index = _sample_value(sample, "sample_index")
        if sample_index is not None:
            label_values["sample_index"] = sample_index
    return ",".join(
        f'{name}="{_label_escape(str(value))}"'
        for name, value in label_values.items()
        if value is not None
    )


def _machine_telemetry_labels(sample: Any) -> str:
    return _labels_from_dict(
        {
            "server": _sample_value(sample, "server"),
            "device_id": _sample_value(sample, "device_id"),
            "chip_id": _sample_value(sample, "chip_id") or "0",
            "source": _sample_value(sample, "source") or "npu-smi-watch",
        }
    )


def _labels_from_dict(label_values: dict[str, Any]) -> str:
    return ",".join(
        f'{name}="{_label_escape(str(value))}"'
        for name, value in label_values.items()
        if value is not None
    )


def _case_metadata(case_metadata: dict[str, Any] | None, case_id: str) -> Any:
    if not case_metadata:
        return {}
    return case_metadata.get(case_id) or {}


def _first_not_none(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _sample_value(sample: Any, key: str) -> Any:
    if isinstance(sample, dict):
        return sample.get(key)
    return getattr(sample, key, None)


def _metric_number(value: Any) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    if abs(number) >= 1_000_000:
        return f"{number:.6f}".rstrip("0").rstrip(".")
    return f"{number:g}"


def _label_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _open_pushgateway_tunnel(server: ServerSpec):
    identity_file = getattr(server, "identity_file", None)
    host = HostSpec(
        alias=server.name,
        host=server.host,
        port=int(server.port),
        user=server.user,
        identity_file=identity_file,
    )
    return open_reverse_tunnel(
        host,
        remote_port=PUSHGATEWAY_REMOTE_PORT,
        local_port=PUSHGATEWAY_LOCAL_PORT,
        identity_file=Path(identity_file).expanduser() if identity_file else None,
    )

"""Pure curl command construction and output parsing."""
from __future__ import annotations

from urllib.parse import urlsplit

from .models import AttemptMode, CurlAttempt


CURL_WRITE_OUT = (
    "\n__AR_CURL_BEGIN__\n"
    "http_code=%{http_code}\n"
    "time_total=%{time_total}\n"
    "speed_download=%{speed_download}\n"
    "__AR_CURL_END__\n"
)
_BEGIN = "__AR_CURL_BEGIN__"
_END = "__AR_CURL_END__"


def validate_target_url(url: str) -> str:
    """Validate a configured target URL before it reaches local or remote shell."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError("network target URL 不能为空")
    if url != url.strip():
        raise ValueError(f"network target URL 含首尾空白: {url!r}")
    if any(ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError("network target URL 含控制字符")
    if any(char.isspace() for char in url) or ";" in url:
        raise ValueError("network target URL 含不允许的 shell 特殊字符")

    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"network target URL 仅支持 http/https: {url}")
    if not parsed.netloc:
        raise ValueError(f"network target URL 缺少 host: {url}")
    return url


def target_label(url: str) -> str:
    """Derive a stable human label from a validated URL."""
    host = urlsplit(validate_target_url(url)).hostname or "unknown"
    if "huggingface" in host:
        return "huggingface"
    if "github" in host:
        return "github"
    if "baidu" in host:
        return "baidu"
    return host


def build_curl_command(
    url: str,
    proxy_url: str | None = None,
    timeout_s: int = 10,
) -> list[str]:
    """Build a local subprocess argv for the network probe curl command."""
    clean_url = validate_target_url(url)
    command = [
        "curl",
        "--max-time",
        str(timeout_s),
        "-L",
        "-o",
        "/dev/null",
        "-s",
        "-w",
        CURL_WRITE_OUT,
    ]
    if proxy_url:
        command.extend(["--proxy", proxy_url])
    command.append(clean_url)
    return command


def parse_curl_result(
    exit_code: int,
    stdout: str,
    stderr: str,
    mode: AttemptMode,
    target_url: str,
    proxy_url: str | None = None,
) -> CurlAttempt:
    """Parse curl write-out into a bounded, serializable attempt record."""
    fields = _parse_write_out(stdout)
    http_code = _int_or_none(fields.get("http_code"))
    latency_ms = _seconds_to_ms(fields.get("time_total"))
    speed_download_bps = _int_float_or_none(fields.get("speed_download"))
    parse_error = None if fields else "curl write-out missing or malformed"
    http_ok = http_code is not None and 200 <= http_code < 400
    ok = exit_code == 0 and parse_error is None and http_ok

    error = None
    if not ok:
        pieces: list[str] = []
        if exit_code != 0:
            pieces.append(f"curl exit code {exit_code}")
        if parse_error is not None:
            pieces.append(parse_error)
        if http_code is not None and not http_ok:
            pieces.append(f"http_code={http_code}")
        detail = _summarize(stderr)
        if detail:
            pieces.append(detail)
        error = "; ".join(pieces) or "curl probe failed"

    return CurlAttempt(
        mode=mode,
        target_url=target_url,
        proxy_url=proxy_url,
        exit_code=exit_code,
        ok=ok,
        status="ok" if ok else "fail",
        http_code=http_code,
        latency_ms=latency_ms,
        speed_download_bps=speed_download_bps,
        error=error,
    )


def _parse_write_out(stdout: str) -> dict[str, str]:
    if _BEGIN not in stdout or _END not in stdout:
        return {}
    segment = stdout.rsplit(_BEGIN, 1)[-1].split(_END, 1)[0]
    fields: dict[str, str] = {}
    for raw_line in segment.splitlines():
        line = raw_line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        fields[key.strip()] = value.strip()
    required = {"http_code", "time_total", "speed_download"}
    if not required.issubset(fields):
        return {}
    return fields


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int_float_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _seconds_to_ms(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(round(float(value) * 1000))
    except (TypeError, ValueError):
        return None


def _summarize(value: str, limit: int = 300) -> str:
    return " ".join(value.split())[:limit]

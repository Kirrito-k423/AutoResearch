"""datalake.prometheus — pushgateway collection helpers."""

from .push_gateway import PushError, push_metrics

__all__ = ["PushError", "push_metrics"]

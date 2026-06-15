"""datalake.logs — remote run log collection."""

from .collector import LogFetchError, collect_log, tail_remote_log

__all__ = ["LogFetchError", "collect_log", "tail_remote_log"]

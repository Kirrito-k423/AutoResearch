"""Tests for services.status subcommand."""
import json
from unittest.mock import patch

from click.testing import CliRunner

from autoresearch.cli import main
from autoresearch.services._common import SERVICES, check_all


def test_services_constant_has_5_entries():
    assert len(SERVICES) == 5
    names = {s[0] for s in SERVICES}
    assert names == {"archon", "wandb", "prometheus", "grafana", "pushgateway"}


def test_check_all_handles_connection_error():
    """When all services are down, check_all should return 5 unhealthy results (not raise)."""
    # No mocks; localhost:8088/8080/9090/3000/9091 are almost certainly unbound in test env
    results = check_all(timeout=0.5)
    assert len(results) == 5
    # All results should be unhealthy (no service running)
    assert all(r["healthy"] is False for r in results)
    # Each result has all required fields
    for r in results:
        assert "name" in r
        assert "url" in r
        assert "healthy" in r
        assert "latency_ms" in r
        assert "error" in r


def test_status_json_output():
    runner = CliRunner()
    result = runner.invoke(main, ["services", "status", "--json"])
    # exit code is 1 if any unhealthy (expected in test env)
    assert result.exit_code in (0, 1)
    # stdout is a valid JSON object
    payload = json.loads(result.output)
    assert "services" in payload
    assert "summary" in payload
    assert len(payload["services"]) == 5
    assert payload["summary"]["total"] == 5


def test_status_human_output():
    runner = CliRunner()
    result = runner.invoke(main, ["services", "status"])
    assert result.exit_code in (0, 1)
    # stdout has table headers
    assert "NAME" in result.output
    assert "URL" in result.output
    assert "HEALTHY" in result.output

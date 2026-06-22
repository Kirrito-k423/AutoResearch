"""Tests for report HTML rendering."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from autoresearch.report.models import ArtifactLink, LogView, MetricPoint, PrometheusView, ReportBundle, SkillUsage, WandbView
from autoresearch.report.render import render_report


def _bundle(tmp_path: Path) -> ReportBundle:
    return ReportBundle(
        run_id="run123",
        manifest_path=tmp_path / "run123" / "manifest.json",
        started_at=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 6, 15, 12, 1, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-qwen3.5",
        lib="verl",
        workdir_remote="/root",
        workdir_local=tmp_path / "run123",
        exit_code=0,
        error=None,
        one_step={"sum": 5.29, "npu_count": 8, "elapsed_ms": 1200},
        artifact_links=[ArtifactLink(label="manifest.json", href="file:///tmp/manifest.json")],
        warnings=[],
        log=LogView(
            available=True,
            path=tmp_path / "run123" / "log.txt",
            key_lines=["SUM= 5.29", "NPU_COUNT= 8"],
            tail_lines=["SUM= 5.29", "NPU_COUNT= 8"],
        ),
        wandb=WandbView(
            available=True,
            run_id="abc123",
            local_path=tmp_path / "wandb",
            service_url="http://localhost:8080",
            summary={"sum": 5.29, "npu_count": 8},
            charts={"sum": [MetricPoint(x=0, y=5.29, label="step 0")]},
            links=[ArtifactLink(label="W&B Local", href="http://localhost:8080")],
        ),
        prometheus=PrometheusView(
            available=True,
            metric_name="autoresearch_npu_count",
            query='autoresearch_npu_count{run_id="run123"}',
            query_url="http://localhost:9090/graph",
            service_url="http://localhost:9090",
            current_value=8.0,
            series=[MetricPoint(x=1, y=8.0, label="instant")],
            notes=["当前 evidence 只证明 NPU 数量。"],
        ),
        skills_used=[
            SkillUsage(
                name="08 experiment-report",
                path=".agents/skills/08-experiment-report/SKILL.md",
                purpose="渲染报告。",
            )
        ],
    )


def test_render_report_writes_html(tmp_path):
    bundle = _bundle(tmp_path)
    output = render_report(bundle, tmp_path / "run123" / "report.html")

    assert output.exists()
    html = output.read_text(encoding="utf-8")
    assert "AutoResearch 实验报告" in html
    assert "run123" in html
    assert "日志视图" in html
    assert "W&B 视图" in html
    assert "Prometheus 视图" in html
    assert "本次使用的仓库 Skill" in html

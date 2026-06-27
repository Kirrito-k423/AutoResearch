"""Tests for formal Verl case report loading and rendering."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from datalake.manifest import RunManifest, write

from autoresearch.e2e.report_check import check_report_completeness
from autoresearch.report.loader import load_report_bundle
from autoresearch.report.render import render_report
from autoresearch.report.verl_case import load_verl_case_view


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def _prometheus_payload():
    return {"status": "success", "data": {"result": [{"value": [1718452800, "8"]}]}}


def _matrix_rows(*, missing_async_16k: bool = False) -> list[dict[str, object]]:
    rows = []
    for output_tokens in (2048, 4096, 8192, 16384):
        for mode in ("sync", "async"):
            if missing_async_16k and output_tokens == 16384 and mode == "async":
                continue
            rows.append(
                {
                    "run_id": "run123",
                    "input_tokens": 1024,
                    "output_tokens": output_tokens,
                    "inference_mode": mode,
                    "ignore_eos": False,
                    "status": "passed",
                    "elapsed_seconds": 2.0,
                    "tokens_per_second": 1000.0 / (output_tokens / 2048),
                    "steady_state_tokens_per_second": 12.0 if mode == "sync" else 13.0,
                    "steady_state_tokens_per_second_per_npu": 12.0 if mode == "sync" else 13.0,
                    "steady_state_step_count": 3,
                    "completed_training_steps": 5,
                    "target_training_steps": 5,
                    "device_count": 1,
                    "train_batch_size": 1,
                    "latency_ms": float(output_tokens / 2),
                    "sample_count": 3,
                    "accuracy": 0.75 if mode == "sync" else 0.74,
                    "consistency": 0.95,
                }
            )
    return rows


def _seed_formal_run(tmp_path: Path, *, missing_async_16k: bool = False) -> Path:
    run_root = tmp_path / "run123"
    run_root.mkdir(parents=True, exist_ok=True)
    matrix_path = run_root / "matrix-results.jsonl"
    matrix_path.write_text(
        "".join(json.dumps(row) + "\n" for row in _matrix_rows(missing_async_16k=missing_async_16k)),
        encoding="utf-8",
    )
    stage_timing_path = run_root / "stage-timings.jsonl"
    stage_timing_path.write_text(
        json.dumps(
            {
                "run_id": "run123",
                "case_id": "sync-1024-2048",
                "stage": "rollout",
                "original_key": "timing/rollout_generate_seconds",
                "elapsed_seconds": 1.25,
                "source": "log",
                "step": 1,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    config_path = run_root / "config-20260616T155609.json"
    config_path.write_text(
        json.dumps(
            {
                "run_id": "run123",
                "config": {
                    "input_tokens": 1024,
                    "output_tokens": [2048, 4096, 8192, 16384],
                    "inference_modes": ["sync", "async"],
                    "trainer_val_only": True,
                    "val_max_samples": 2,
                },
            }
        ),
        encoding="utf-8",
    )
    provenance_path = run_root / "provenance.json"
    provenance_path.write_text(json.dumps([{"repo": "AutoResearch", "commit_sha": "abc123"}]), encoding="utf-8")
    log_path = run_root / "verl-case.log"
    log_path.write_text("run_id=run123\nmatrix_rows=8\n", encoding="utf-8")
    wandb_dir = run_root / "wandb"
    (wandb_dir / "files").mkdir(parents=True)
    (wandb_dir / "files" / "wandb-summary.json").write_text(
        json.dumps({"accuracy": 0.75, "_step": 1}),
        encoding="utf-8",
    )
    prom_path = run_root / "prom" / "formal-case-prometheus.json"
    prom_path.parent.mkdir(parents=True)
    prom_path.write_text(json.dumps({"run_id": "run123"}), encoding="utf-8")
    manifest = RunManifest(
        run_id="run123",
        started_at=datetime(2026, 6, 16, 15, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 6, 16, 15, 30, tzinfo=timezone.utc),
        server="A2-AK-225",
        conda_env="verl-env",
        lib="verl",
        workdir_remote="/home/t00906153",
        workdir_local=run_root,
        formal_case={
            "kind": "verl-case",
            "matrix_results": str(matrix_path),
            "log_path": str(log_path),
            "stage_timings": str(stage_timing_path),
        },
        exit_code=0,
        config_snapshot=config_path,
        provenance=[{"repo": "AutoResearch", "commit_sha": "abc123"}],
        wandb_run_id="run123",
        wandb_path=wandb_dir,
        log_files=[log_path],
        prom_pushed=False,
        prom_metrics_file=prom_path,
    )
    return write(manifest, root=tmp_path)


def test_load_verl_case_view_reports_complete_matrix(tmp_path):
    manifest_path = _seed_formal_run(tmp_path)
    manifest = RunManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

    view = load_verl_case_view(manifest, manifest_path=manifest_path)

    assert view is not None
    assert view.complete_matrix is True
    assert len(view.rows) == 8
    assert {item["output_tokens"] for item in view.length_summary} == {2048, 4096, 8192, 16384}
    assert isinstance(view.accuracy_overall, float)
    assert isinstance(view.consistency_overall, float)
    assert view.rows[0].steady_state_tokens_per_second_per_npu is not None
    assert view.length_summary[0]["steady_state_tokens_per_second_per_npu"] is not None
    assert view.stage_timings[0].stage == "rollout"
    assert view.stage_timing_summary[0]["avg_seconds"] == 1.25
    assert view.trainer_val_only is True
    assert "验证矩阵" in view.training_mode
    assert any("val_max_samples=2" in item for item in view.score_diagnostics)


def test_load_verl_case_view_warns_when_async_16k_missing(tmp_path):
    manifest_path = _seed_formal_run(tmp_path, missing_async_16k=True)
    manifest = RunManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

    view = load_verl_case_view(manifest, manifest_path=manifest_path)

    assert view is not None
    assert view.complete_matrix is False
    assert any("async" in warning and "16384" in warning for warning in view.warnings)


def test_render_formal_case_sections(tmp_path, monkeypatch):
    _seed_formal_run(tmp_path)
    monkeypatch.setattr("autoresearch.report.prometheus.urlopen", lambda *args, **kwargs: _Response(_prometheus_payload()))
    bundle = load_report_bundle("run123", root=tmp_path)
    output = tmp_path / "run123" / "report.html"

    render_report(bundle, output)

    html = output.read_text(encoding="utf-8")
    assert "Verl 正式 Case 矩阵" in html
    assert "稳态单卡吞吐排行" in html
    assert "稳态 tokens/s/卡" in html
    assert "序列长度影响" in html
    assert "同步/异步影响" in html
    assert "准确率" in html
    assert "一致性与诊断" in html
    assert "Verl 阶段耗时" in html
    assert "rollout" in html
    assert "交付件完整性" in html
    assert "不可变配置" in html
    assert "矩阵结果" in html
    assert "本次使用的仓库 Skill" in html
    assert ".agents/skills/01-customer-config/SKILL.md" in html
    assert "workspace-adapter/verl/SKILL.md" in html


def test_formal_report_completeness_fails_when_matrix_row_missing(tmp_path, monkeypatch):
    _seed_formal_run(tmp_path, missing_async_16k=True)
    (tmp_path / "run123" / "report.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr("autoresearch.report.prometheus.urlopen", lambda *args, **kwargs: _Response(_prometheus_payload()))

    exit_code, payload = check_report_completeness(
        run_id="run123",
        runs_root=tmp_path,
        formal_case=True,
    )

    assert exit_code == 1
    assert payload["ok"] is False
    assert "formal_matrix" in payload["missing"]


def test_verl_case_docs_cover_command_and_sources():
    text = Path("docs/verl-case.md").read_text(encoding="utf-8")

    assert "autoresearch run verl-case" in text
    assert "/Users/Zhuanz/autoResearchData" in text
    assert "Qwen/Qwen3.5-2B" in text
    assert "hiyouga/geometry3k" in text
    assert "quay.io/ascend/verl:verl-8.5.2-910b-ubuntu22.04-py3.11-qwen3-5" in text
    assert "row_timeout_seconds" in text

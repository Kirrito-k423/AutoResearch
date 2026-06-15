"""Static contract tests for repo-local Archon workflows."""
from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".archon" / "workflows"


def _load(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def test_all_archon_workflows_exist_and_have_unique_names():
    files = sorted(WORKFLOWS.glob("ar-*.yaml"))
    names = [_load(path.name)["name"] for path in files]

    assert len(files) == 9
    assert len(names) == len(set(names))
    assert "ar-min-loop" in names
    for idx in range(1, 9):
        assert f"ar-skill-{idx:02d}" in names


def test_skill_06_and_07_use_real_loop_nodes():
    skill_06 = _load("ar-skill-06.yaml")
    skill_07 = _load("ar-skill-07.yaml")

    assert any("loop" in node for node in skill_06["nodes"])
    assert any("loop" in node for node in skill_07["nodes"])
    assert "until_bash" in next(node["loop"] for node in skill_06["nodes"] if "loop" in node)
    assert "until_bash" in next(node["loop"] for node in skill_07["nodes"] if "loop" in node)


def test_main_workflow_preserves_the_eight_skill_order():
    main = _load("ar-min-loop.yaml")
    nodes = {node["id"]: node for node in main["nodes"]}

    expected = [
        "config-validate",
        "services-start-and-status",
        "hw-probe",
        "net-probe",
        "reach-test",
        "stack-check",
        "collect-run",
        "report-render",
    ]
    assert list(nodes) == expected
    assert nodes["report-render"]["depends_on"] == ["collect-run"]
    assert nodes["collect-run"]["depends_on"] == ["stack-check"]
    assert nodes["stack-check"]["depends_on"] == ["reach-test"]
    assert nodes["net-probe"]["bash"].startswith(
        "AR_REMOTE_PROXY_PORT=${AR_REMOTE_PROXY_PORT:-17892}"
    )


def test_named_script_nodes_point_to_repo_scripts():
    scripts = ROOT / ".archon" / "scripts"
    for idx in range(1, 9):
        assert (scripts / f"ar-skill-{idx:02d}.py").exists()

    for path in WORKFLOWS.glob("ar-*.yaml"):
        workflow = _load(path.name)
        for node in workflow["nodes"]:
            script = node.get("script")
            if script and script.startswith("ar-skill-"):
                assert (scripts / f"{script}.py").exists()
                assert node["runtime"] == "uv"

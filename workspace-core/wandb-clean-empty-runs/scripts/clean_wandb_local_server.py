#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
SYSTEM_SUMMARY_PATHS = ["$._runtime", "$._timestamp", "$._step", "$._wandb"]


@dataclass
class ServerRun:
    project_id: int
    entity: str
    project: str
    run: str
    display_name: str
    state: str
    history_count: int
    event_count: int
    log_count: int
    useful_summary_keys: int
    summary_keys: str
    selected_for_delete: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or soft-delete local W&B server runs with no useful step metrics."
    )
    parser.add_argument("--container", default="ar-wandb", help="W&B local Docker container name.")
    parser.add_argument("--entity", default="autoresearch-local", help="W&B entity name.")
    parser.add_argument("--project", default="verl", help="W&B project name.")
    parser.add_argument("--run", action="append", help="Specific run id to target. Can be repeated.")
    parser.add_argument("--delete", action="store_true", help="Soft-delete selected runs in MySQL.")
    parser.add_argument("--remove-files", action="store_true", help="Remove matching MinIO object directories.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    return parser.parse_args()


def checked_name(value: str, label: str) -> str:
    if not SAFE_NAME.match(value):
        raise SystemExit(f"Refusing unsafe {label}: {value!r}")
    return value


def sql_quote(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def run_cmd(args: list[str], *, input_text: str | None = None) -> str:
    proc = subprocess.run(
        args,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(args)}\n{proc.stderr.strip()}"
        )
    return proc.stdout


def mysql(container: str, sql: str, *, batch: bool = True) -> str:
    cmd = ["docker", "exec", "-i", container, "mysql", "-uroot"]
    if batch:
        cmd.extend(["--batch", "--raw"])
    cmd.append("wandb_local")
    return run_cmd(cmd, input_text=sql)


def fetch_candidates(container: str, entity: str, project: str, runs: list[str] | None) -> list[ServerRun]:
    remove_expr = "JSON_REMOVE(COALESCE(r.summary_metrics, JSON_OBJECT()), " + ", ".join(
        sql_quote(path) for path in SYSTEM_SUMMARY_PATHS
    ) + ")"
    run_filter = ""
    if runs:
        run_filter = "AND r.name IN (" + ", ".join(sql_quote(run) for run in runs) + ")"

    sql = f"""
SELECT
  r.project_id,
  e.name AS entity,
  p.name AS project,
  r.name AS run,
  COALESCE(r.display_name, '') AS display_name,
  COALESCE(r.state, '') AS state,
  COALESCE(r.history_count, 0) AS history_count,
  COALESCE(r.event_count, 0) AS event_count,
  COALESCE(r.log_count, 0) AS log_count,
  JSON_LENGTH({remove_expr}) AS useful_summary_keys,
  COALESCE(JSON_KEYS(COALESCE(r.summary_metrics, JSON_OBJECT())), JSON_ARRAY()) AS summary_keys
FROM runs r
JOIN projects p ON p.id = r.project_id
JOIN entities e ON e.id = p.entity_id
WHERE e.name = {sql_quote(entity)}
  AND p.name = {sql_quote(project)}
  AND r.deleted_at IS NULL
  {run_filter}
ORDER BY r.created_at DESC;
"""
    output = mysql(container, sql)
    lines = [line for line in output.splitlines() if line]
    if not lines:
        return []
    rows: list[ServerRun] = []
    for line in lines[1:]:
        fields = line.split("\t")
        rows.append(
            ServerRun(
                project_id=int(fields[0]),
                entity=fields[1],
                project=fields[2],
                run=fields[3],
                display_name=fields[4],
                state=fields[5],
                history_count=int(fields[6]),
                event_count=int(fields[7]),
                log_count=int(fields[8]),
                useful_summary_keys=int(fields[9]),
                summary_keys=fields[10],
            )
        )
    return rows


def select_runs(rows: list[ServerRun], explicit_runs: bool) -> list[ServerRun]:
    selected: list[ServerRun] = []
    for row in rows:
        should_delete = explicit_runs or (row.history_count == 0 and row.useful_summary_keys == 0)
        row.selected_for_delete = should_delete
        if should_delete:
            selected.append(row)
    return selected


def soft_delete(container: str, selected: list[ServerRun]) -> None:
    by_project: dict[int, list[str]] = {}
    for row in selected:
        by_project.setdefault(row.project_id, []).append(row.run)
    statements: list[str] = ["SET @deleted_at = NOW();"]
    for project_id, names in by_project.items():
        names_sql = ", ".join(sql_quote(name) for name in names)
        statements.append(
            f"UPDATE files SET deleted_at = COALESCE(deleted_at, @deleted_at), updated_at = @deleted_at "
            f"WHERE project_id = {project_id} AND run_name IN ({names_sql});"
        )
        statements.append(
            f"UPDATE runs_flat SET deleted_at = COALESCE(deleted_at, @deleted_at), updated_at = @deleted_at "
            f"WHERE project_id = {project_id} AND name IN ({names_sql});"
        )
        statements.append(
            f"UPDATE runs SET deleted_at = COALESCE(deleted_at, @deleted_at), updated_at = @deleted_at "
            f"WHERE project_id = {project_id} AND name IN ({names_sql});"
        )
    mysql(container, "\n".join(statements), batch=False)


def remove_object_dirs(container: str, selected: list[ServerRun]) -> list[str]:
    removed: list[str] = []
    for row in selected:
        for label, value in (("entity", row.entity), ("project", row.project), ("run", row.run)):
            checked_name(value, label)
        path = PurePosixPath("/vol/minio/local-files") / row.entity / row.project / row.run
        shell = f"if [ -e {shlex.quote(str(path))} ]; then rm -rf {shlex.quote(str(path))}; echo {shlex.quote(str(path))}; fi"
        out = run_cmd(["docker", "exec", container, "sh", "-lc", shell])
        removed.extend(line for line in out.splitlines() if line)
    return removed


def print_text(rows: list[ServerRun], selected: list[ServerRun], removed: list[str], mode: str) -> None:
    print(f"{mode}: scanned={len(rows)} selected={len(selected)}")
    for row in selected:
        print(
            "DELETE "
            f"{row.entity}/{row.project}/{row.run} "
            f"history={row.history_count} useful_summary_keys={row.useful_summary_keys} "
            f"events={row.event_count} logs={row.log_count} "
            f"name={row.display_name}"
        )
    if removed:
        print("removed_object_dirs:")
        for path in removed:
            print(path)


def main() -> int:
    args = parse_args()
    checked_name(args.entity, "entity")
    checked_name(args.project, "project")
    runs = args.run or None
    if runs:
        for run in runs:
            checked_name(run, "run")

    rows = fetch_candidates(args.container, args.entity, args.project, runs)
    selected = select_runs(rows, explicit_runs=bool(runs))
    removed: list[str] = []

    if args.delete and selected:
        soft_delete(args.container, selected)
        if args.remove_files:
            removed = remove_object_dirs(args.container, selected)

    payload = {
        "mode": "delete" if args.delete else "dry-run",
        "container": args.container,
        "entity": args.entity,
        "project": args.project,
        "scanned": len(rows),
        "selected": [row.__dict__ for row in selected],
        "removed_object_dirs": removed,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_text(rows, selected, removed, mode=payload["mode"].upper())
    return 0


if __name__ == "__main__":
    sys.exit(main())

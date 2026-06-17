"""Git provenance capture for formal experiment runs."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable

from .case_config import RepoProvenance


CommandRunner = Callable[[list[str], Path], tuple[int, str, str]]


def _run(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _git(runner: CommandRunner, cwd: Path, *args: str) -> str | None:
    code, stdout, _stderr = runner(["git", *args], cwd)
    if code != 0:
        return None
    return stdout.strip() or None


def capture_repo_provenance(
    path: str | Path,
    *,
    upstream_url: str | None = None,
    fork_owner: str = "Kirrito-k423",
    allow_commit_push: bool = False,
    branch_prefix: str | None = None,
    runner: CommandRunner = _run,
) -> RepoProvenance:
    """Capture git provenance and optionally commit/push dirty experiment repos."""
    repo_path = Path(path).expanduser()
    root_text = _git(runner, repo_path, "rev-parse", "--show-toplevel")
    root = Path(root_text) if root_text else repo_path
    repo_name = root.name
    origin_url = _git(runner, root, "remote", "get-url", "origin")
    source_url = upstream_url or origin_url
    fork_url = _fork_url(source_url, fork_owner) if source_url and fork_owner else None
    branch = _git(runner, root, "rev-parse", "--abbrev-ref", "HEAD")
    if branch == "HEAD":
        short_sha = _git(runner, root, "rev-parse", "--short", "HEAD")
        branch = f"detached-{short_sha}" if short_sha else None
    dirty = bool(_git(runner, root, "status", "--porcelain"))

    commit_push_attempted = False
    pushed_url = None
    push_remote, push_url = _select_push_target(runner, root, origin_url=origin_url, fork_url=fork_url)
    if allow_commit_push:
        commit_push_attempted = True
        if branch_prefix and branch and not branch.startswith(branch_prefix):
            branch = f"{branch_prefix}{branch}"
            runner(["git", "switch", "-C", branch], root)
        if dirty:
            runner(["git", "add", "-A"], root)
            runner(["git", "commit", "-m", "chore: capture verl case experiment state"], root)
        if branch and push_remote and push_url:
            code, _stdout, _stderr = runner(["git", "push", "-u", push_remote, branch], root)
            if code == 0:
                pushed_url = _branch_url(push_url, branch)

    commit_sha = _git(runner, root, "rev-parse", "HEAD")
    branch_url = _branch_url(fork_url or origin_url, branch) if branch else None
    return RepoProvenance(
        repo=repo_name,
        path=str(root),
        upstream_url=upstream_url or origin_url,
        fork_url=fork_url,
        branch_url=branch_url,
        branch=branch,
        commit_sha=commit_sha,
        dirty=dirty,
        pushed_url=pushed_url,
        commit_push_attempted=commit_push_attempted,
    )


def _fork_url(url: str, owner: str) -> str:
    clean = url.removesuffix(".git")
    name = clean.rsplit("/", 1)[-1]
    return f"https://github.com/{owner}/{name}"


def _select_push_target(
    runner: CommandRunner,
    cwd: Path,
    *,
    origin_url: str | None,
    fork_url: str | None,
) -> tuple[str | None, str | None]:
    target_url = fork_url or origin_url
    if not target_url:
        return None, None
    matched_remote = _find_remote_for_url(runner, cwd, target_url)
    if matched_remote:
        return matched_remote, target_url
    if not fork_url and origin_url:
        return "origin", origin_url
    return None, target_url


def _find_remote_for_url(runner: CommandRunner, cwd: Path, target_url: str) -> str | None:
    code, stdout, _stderr = runner(["git", "remote", "-v"], cwd)
    if code != 0:
        return None
    normalized_target = _normalize_git_url(target_url)
    for line in stdout.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        remote, url = parts[0], parts[1]
        if _normalize_git_url(url) == normalized_target:
            return remote
    return None


def _normalize_git_url(url: str) -> str:
    clean = url.strip().removesuffix(".git")
    if clean.startswith("git@github.com:"):
        clean = "https://github.com/" + clean.removeprefix("git@github.com:")
    return clean


def _branch_url(url: str | None, branch: str | None) -> str | None:
    if not url or not branch:
        return None
    clean = _normalize_git_url(url)
    return f"{clean}/tree/{branch}"

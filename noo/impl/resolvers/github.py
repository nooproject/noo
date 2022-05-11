from __future__ import annotations

from pathlib import Path
from shutil import rmtree

from git.repo import Repo


def clone_github(repo: str, dest: Path) -> None:
    Repo.clone_from(repo, dest)  # type: ignore

    rmtree(dest / ".git")

from __future__ import annotations

from pathlib import Path
from shutil import copytree


def clone_local(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True)
    copytree(src, dest)

from pathlib import Path
from re import compile
from shutil import copytree


def clone_local(src: Path, dest: Path) -> None:
    copytree(src, dest)
